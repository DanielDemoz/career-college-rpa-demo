"""
OCR Engine for Document Processing
Extracts text from student enrollment documents
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
from pathlib import Path
from typing import Dict, List, Tuple
import json


class OCREngine:
    """
    Intelligent OCR engine for processing enrollment documents
    Handles ID cards, transcripts, proof of address documents
    """
    
    def __init__(self, tesseract_path: str = None):
        """
        Initialize OCR engine
        
        Args:
            tesseract_path: Path to Tesseract executable (Windows: C:/Program Files/Tesseract-OCR/tesseract.exe)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf']
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Enhance image quality for better OCR accuracy
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image as numpy array
        """
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding for better contrast
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Deskew if needed
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        if abs(angle) > 0.5:  # Only deskew if needed
            (h, w) = thresh.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            thresh = cv2.warpAffine(thresh, M, (w, h), 
                                   flags=cv2.INTER_CUBIC, 
                                   borderMode=cv2.BORDER_REPLICATE)
        
        return thresh
    
    def extract_text(self, image_path: str, lang: str = 'eng') -> str:
        """
        Extract all text from document
        
        Args:
            image_path: Path to document image
            lang: Language code (default: 'eng')
            
        Returns:
            Extracted text as string
        """
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Convert back to PIL Image for pytesseract
            pil_img = Image.fromarray(processed_img)
            
            # Extract text with configuration
            custom_config = r'--oem 3 --psm 6'  # LSTM OCR Engine, assume uniform text block
            text = pytesseract.image_to_string(pil_img, lang=lang, config=custom_config)
            
            return text.strip()
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def extract_structured_data(self, image_path: str, document_type: str) -> Dict:
        """
        Extract structured data based on document type
        
        Args:
            image_path: Path to document
            document_type: Type of document (id, transcript, proof_of_address)
            
        Returns:
            Dictionary with extracted fields
        """
        text = self.extract_text(image_path)
        
        if document_type == 'id':
            return self._extract_id_data(text)
        elif document_type == 'transcript':
            return self._extract_transcript_data(text)
        elif document_type == 'proof_of_address':
            return self._extract_address_data(text)
        else:
            return {'raw_text': text}
    
    def _extract_id_data(self, text: str) -> Dict:
        """Extract data from government-issued ID"""
        data = {
            'document_type': 'government_id',
            'full_name': None,
            'date_of_birth': None,
            'id_number': None,
            'expiry_date': None,
            'address': None,
            'raw_text': text
        }
        
        # Extract name patterns (usually in caps)
        name_patterns = [
            r'(?:NAME|SURNAME|GIVEN NAMES?)[\s:]+([A-Z\s]+)',
            r'([A-Z]{2,}\s+[A-Z]{2,}(?:\s+[A-Z]+)?)'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match and not data['full_name']:
                data['full_name'] = match.group(1).strip()
        
        # Extract dates (DOB, expiry)
        date_pattern = r'\b(\d{2}[-/]\d{2}[-/]\d{4}|\d{4}[-/]\d{2}[-/]\d{2})\b'
        dates = re.findall(date_pattern, text)
        if len(dates) >= 1:
            data['date_of_birth'] = dates[0]
        if len(dates) >= 2:
            data['expiry_date'] = dates[1]
        
        # Extract ID number (various formats)
        id_patterns = [
            r'(?:ID|LICENSE|CARD)\s*(?:NO|#|NUMBER)?[\s:]*([A-Z0-9\-]{6,})',
            r'\b([A-Z]\d{4}-\d{5}-\d{5})\b'  # Ontario format
        ]
        for pattern in id_patterns:
            match = re.search(pattern, text)
            if match:
                data['id_number'] = match.group(1)
                break
        
        # Extract address
        address_pattern = r'(\d+\s+[\w\s]+(?:STREET|ST|AVENUE|AVE|ROAD|RD|DRIVE|DR)[\s,]+[\w\s]+,?\s*[A-Z]{2}\s+[A-Z0-9\s]+)'
        match = re.search(address_pattern, text, re.IGNORECASE)
        if match:
            data['address'] = match.group(1).strip()
        
        return data
    
    def _extract_transcript_data(self, text: str) -> Dict:
        """Extract data from educational transcript"""
        data = {
            'document_type': 'transcript',
            'student_name': None,
            'institution_name': None,
            'graduation_date': None,
            'program': None,
            'gpa': None,
            'courses': [],
            'raw_text': text
        }
        
        # Extract student name
        name_patterns = [
            r'(?:STUDENT NAME|NAME)[\s:]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z]{2,}\s+[A-Z]{2,})'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                data['student_name'] = match.group(1).strip()
                break
        
        # Extract institution
        institution_patterns = [
            r'([\w\s]+(?:HIGH SCHOOL|SECONDARY SCHOOL|COLLEGIATE))',
            r'(?:SCHOOL|INSTITUTION)[\s:]+(.+?)(?:\n|$)'
        ]
        for pattern in institution_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['institution_name'] = match.group(1).strip()
                break
        
        # Extract graduation date
        date_pattern = r'(?:GRADUATED?|COMPLETION)[\s:]+(\w+\s+\d{4}|\d{2}/\d{2}/\d{4})'
        match = re.search(date_pattern, text, re.IGNORECASE)
        if match:
            data['graduation_date'] = match.group(1)
        
        # Extract GPA
        gpa_pattern = r'(?:GPA|AVERAGE)[\s:]+(\d+\.?\d*)'
        match = re.search(gpa_pattern, text, re.IGNORECASE)
        if match:
            data['gpa'] = match.group(1)
        
        return data
    
    def _extract_address_data(self, text: str) -> Dict:
        """Extract data from proof of address document"""
        data = {
            'document_type': 'proof_of_address',
            'name': None,
            'address': None,
            'document_date': None,
            'issuer': None,
            'raw_text': text
        }
        
        # Extract name
        name_pattern = r'(?:NAME|TO|FOR)[\s:]+([A-Z][a-z]+\s+[A-Z][a-z]+)'
        match = re.search(name_pattern, text)
        if match:
            data['name'] = match.group(1).strip()
        
        # Extract full address
        address_pattern = r'(\d+\s+[\w\s]+(?:STREET|ST|AVENUE|AVE|ROAD|RD)[\s,]+[\w\s]+,?\s*ON\s+[A-Z0-9\s]+)'
        match = re.search(address_pattern, text, re.IGNORECASE)
        if match:
            data['address'] = match.group(1).strip()
        
        # Extract date
        date_pattern = r'(?:DATE|BILL DATE)[\s:]+(\w+\s+\d{1,2},?\s+\d{4}|\d{2}/\d{2}/\d{4})'
        match = re.search(date_pattern, text, re.IGNORECASE)
        if match:
            data['document_date'] = match.group(1)
        
        # Extract issuer (utility company, bank, etc.)
        issuer_patterns = [
            r'((?:HYDRO|ENBRIDGE|ROGERS|BELL)[\w\s]*)',
            r'^([\w\s]+(?:UTILITY|ELECTRIC|GAS|TELECOM))'
        ]
        for pattern in issuer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['issuer'] = match.group(1).strip()
                break
        
        return data
    
    def process_batch(self, file_paths: List[str]) -> List[Dict]:
        """
        Process multiple documents in batch
        
        Args:
            file_paths: List of document paths
            
        Returns:
            List of extracted data dictionaries
        """
        results = []
        for file_path in file_paths:
            try:
                text = self.extract_text(file_path)
                results.append({
                    'file': file_path,
                    'text': text,
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'file': file_path,
                    'text': '',
                    'status': 'error',
                    'error': str(e)
                })
        return results
    
    def get_confidence_score(self, image_path: str) -> float:
        """
        Get OCR confidence score for a document
        
        Args:
            image_path: Path to document
            
        Returns:
            Confidence score (0-100)
        """
        try:
            processed_img = self.preprocess_image(image_path)
            pil_img = Image.fromarray(processed_img)
            
            # Get detailed OCR data with confidence
            data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence (excluding -1 values)
            confidences = [int(conf) for conf in data['conf'] if int(conf) != -1]
            if confidences:
                return sum(confidences) / len(confidences)
            return 0.0
        except:
            return 0.0


if __name__ == "__main__":
    # Example usage
    ocr = OCREngine()
    
    print("OCR Engine initialized successfully!")
    print(f"Supported formats: {ocr.supported_formats}")

