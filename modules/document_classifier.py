"""
AI-Powered Document Classifier
Identifies document types and validates completeness
"""

import re
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import numpy as np


class DocumentClassifier:
    """
    Classifies enrollment documents using rule-based + ML approach
    """
    
    def __init__(self):
        self.document_types = [
            'government_id',
            'drivers_license', 
            'transcript',
            'diploma',
            'proof_of_address',
            'utility_bill',
            'bank_statement',
            'osap_document',
            'study_permit',
            'unknown'
        ]
        
        # Keywords for each document type
        self.keywords = {
            'government_id': [
                'ontario', 'photo card', 'identification', 'date of birth',
                'sex', 'height', 'issue date', 'expiry date', 'card number'
            ],
            'drivers_license': [
                'driver', 'license', 'licence', 'class', 'endorsements',
                'restrictions', 'ministry of transportation', 'operator'
            ],
            'transcript': [
                'transcript', 'grades', 'credits', 'course', 'semester',
                'gpa', 'grade point', 'academic', 'term', 'year'
            ],
            'diploma': [
                'diploma', 'certificate', 'graduated', 'conferred',
                'awarded', 'completion', 'honors', 'honours'
            ],
            'proof_of_address': [
                'bill', 'statement', 'account', 'service address',
                'billing address', 'customer'
            ],
            'utility_bill': [
                'hydro', 'water', 'gas', 'electric', 'electricity',
                'enbridge', 'toronto hydro', 'kwh', 'usage'
            ],
            'bank_statement': [
                'bank', 'account statement', 'balance', 'transaction',
                'deposit', 'withdrawal', 'branch', 'transit'
            ],
            'osap_document': [
                'osap', 'ontario student assistance', 'loan', 'grant',
                'financial aid', 'nslsc', 'ministry training'
            ],
            'study_permit': [
                'study permit', 'immigration', 'ircc', 'temporary resident',
                'international student', 'visa', 'authorized to study'
            ]
        }
        
        self.vectorizer = None
        self.model = None
        
    def classify_document(self, text: str, confidence_threshold: float = 0.6) -> Dict:
        """
        Classify document based on extracted text
        
        Args:
            text: Extracted text from OCR
            confidence_threshold: Minimum confidence for classification
            
        Returns:
            Dictionary with document_type, confidence, and matched_keywords
        """
        text_lower = text.lower()
        
        # Rule-based classification (fast and accurate for known patterns)
        scores = {}
        matched_keywords = {}
        
        for doc_type, keywords in self.keywords.items():
            matches = []
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(keyword)
                    # Weight longer keywords more heavily
                    score += len(keyword.split())
            
            scores[doc_type] = score
            matched_keywords[doc_type] = matches
        
        # Get best match
        if scores:
            best_type = max(scores, key=scores.get)
            max_score = scores[best_type]
            
            # Calculate confidence based on keyword matches
            total_possible_score = sum(len(kw.split()) for kw in self.keywords[best_type])
            confidence = min(max_score / total_possible_score, 1.0) if total_possible_score > 0 else 0
            
            if confidence >= confidence_threshold:
                return {
                    'document_type': best_type,
                    'confidence': round(confidence, 2),
                    'matched_keywords': matched_keywords[best_type],
                    'classification_method': 'rule_based'
                }
        
        return {
            'document_type': 'unknown',
            'confidence': 0.0,
            'matched_keywords': [],
            'classification_method': 'rule_based'
        }
    
    def validate_document_quality(self, text: str, ocr_confidence: float = None) -> Dict:
        """
        Assess document quality and readability
        
        Args:
            text: Extracted text
            ocr_confidence: OCR confidence score (0-100)
            
        Returns:
            Quality assessment dictionary
        """
        issues = []
        quality_score = 100
        
        # Check text length
        if len(text) < 50:
            issues.append("Document appears too short or incomplete")
            quality_score -= 30
        
        # Check for gibberish (high ratio of non-alphanumeric)
        alphanumeric_ratio = sum(c.isalnum() or c.isspace() for c in text) / len(text) if len(text) > 0 else 0
        if alphanumeric_ratio < 0.7:
            issues.append("Document contains too many unreadable characters")
            quality_score -= 25
        
        # Check OCR confidence
        if ocr_confidence is not None:
            if ocr_confidence < 60:
                issues.append(f"Low OCR confidence: {ocr_confidence:.1f}%")
                quality_score -= 20
            elif ocr_confidence < 75:
                issues.append(f"Moderate OCR confidence: {ocr_confidence:.1f}%")
                quality_score -= 10
        
        # Check for common OCR errors
        suspicious_patterns = [
            (r'[^a-zA-Z0-9\s\.,;:\-\'\"()\[\]{}!?@#$%&*+=/\\]+', "Contains unusual characters"),
            (r'(.)\1{5,}', "Contains suspicious repeated characters")
        ]
        
        for pattern, message in suspicious_patterns:
            if re.search(pattern, text):
                issues.append(message)
                quality_score -= 15
        
        quality_score = max(0, quality_score)
        
        return {
            'quality_score': quality_score,
            'is_acceptable': quality_score >= 60,
            'issues': issues,
            'text_length': len(text),
            'ocr_confidence': ocr_confidence
        }
    
    def check_completeness(self, document_type: str, extracted_data: Dict) -> Dict:
        """
        Check if all required fields are present for document type
        
        Args:
            document_type: Type of document
            extracted_data: Data extracted from document
            
        Returns:
            Completeness assessment
        """
        required_fields = {
            'government_id': ['full_name', 'date_of_birth', 'id_number'],
            'drivers_license': ['full_name', 'date_of_birth', 'id_number', 'expiry_date'],
            'transcript': ['student_name', 'institution_name'],
            'proof_of_address': ['name', 'address', 'document_date'],
            'utility_bill': ['name', 'address', 'document_date'],
            'bank_statement': ['name', 'address', 'document_date']
        }
        
        if document_type not in required_fields:
            return {
                'is_complete': False,
                'missing_fields': [],
                'message': f"Unknown document type: {document_type}"
            }
        
        required = required_fields[document_type]
        missing = []
        
        for field in required:
            if field not in extracted_data or not extracted_data[field]:
                missing.append(field)
        
        is_complete = len(missing) == 0
        
        return {
            'is_complete': is_complete,
            'missing_fields': missing,
            'found_fields': [f for f in required if f not in missing],
            'completeness_percentage': round((len(required) - len(missing)) / len(required) * 100, 1)
        }
    
    def classify_batch(self, documents: List[Dict]) -> List[Dict]:
        """
        Classify multiple documents
        
        Args:
            documents: List of dicts with 'text' and optionally 'file' keys
            
        Returns:
            List of classification results
        """
        results = []
        for doc in documents:
            classification = self.classify_document(doc.get('text', ''))
            result = {
                'file': doc.get('file', 'unknown'),
                **classification
            }
            results.append(result)
        return results
    
    def get_ontario_requirements(self, program_type: str = 'standard') -> Dict:
        """
        Get enrollment document requirements for Ontario career colleges
        
        Args:
            program_type: Type of program (standard, healthcare, international)
            
        Returns:
            Required documents list
        """
        base_requirements = {
            'required_documents': [
                {
                    'type': 'government_id',
                    'description': 'Valid government-issued photo ID',
                    'accepted_types': ['Ontario Photo Card', 'Driver\'s License', 'Passport']
                },
                {
                    'type': 'transcript',
                    'description': 'High school transcript or equivalency',
                    'accepted_types': ['OSSD Transcript', 'GED Certificate', 'International Equivalent']
                },
                {
                    'type': 'proof_of_address',
                    'description': 'Proof of Ontario residency (within 90 days)',
                    'accepted_types': ['Utility Bill', 'Bank Statement', 'Lease Agreement']
                }
            ],
            'optional_documents': [
                {
                    'type': 'osap_document',
                    'description': 'OSAP confirmation (if applying for financial aid)'
                }
            ]
        }
        
        if program_type == 'healthcare':
            base_requirements['required_documents'].append({
                'type': 'immunization_record',
                'description': 'Immunization records required for healthcare programs'
            })
            base_requirements['required_documents'].append({
                'type': 'criminal_record_check',
                'description': 'Vulnerable sector check'
            })
        
        if program_type == 'international':
            base_requirements['required_documents'].append({
                'type': 'study_permit',
                'description': 'Valid Canadian study permit'
            })
            base_requirements['required_documents'].append({
                'type': 'language_proficiency',
                'description': 'IELTS, TOEFL, or equivalent (if applicable)'
            })
        
        return base_requirements


if __name__ == "__main__":
    # Example usage
    classifier = DocumentClassifier()
    
    # Test classification
    sample_text = """
    ONTARIO PHOTO CARD
    CARTE-PHOTO DE L'ONTARIO
    
    SURNAME / NOM DE FAMILLE: SMITH
    GIVEN NAMES / PRÉNOMS: JOHN DAVID
    
    DATE OF BIRTH / DATE DE NAISSANCE: 1998-05-15
    SEX / SEXE: M
    HEIGHT / TAILLE: 175 cm
    
    CARD NUMBER / NUMÉRO DE CARTE: P1234-56789-01234
    ISSUE DATE / DATE DE DÉLIVRANCE: 2023-01-10
    EXPIRY DATE / DATE D'EXPIRATION: 2028-01-10
    """
    
    result = classifier.classify_document(sample_text)
    print("Classification Result:")
    print(f"  Type: {result['document_type']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Keywords matched: {result['matched_keywords']}")

