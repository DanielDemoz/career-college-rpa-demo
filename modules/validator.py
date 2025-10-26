"""
Rule-Based Validation Engine
Validates enrollment documents against Ontario career college requirements
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re


class EnrollmentValidator:
    """
    Validates student enrollment documents and data
    Ensures compliance with Ontario career college regulations
    """
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
        self.current_date = datetime.now()
        
    def _load_validation_rules(self) -> Dict:
        """Load validation rules for different document types"""
        return {
            'government_id': {
                'required_fields': ['full_name', 'date_of_birth', 'id_number'],
                'validators': [
                    ('expiry_date', self._validate_id_not_expired),
                    ('date_of_birth', self._validate_age_requirement),
                ]
            },
            'transcript': {
                'required_fields': ['student_name', 'institution_name'],
                'validators': [
                    ('graduation_date', self._validate_education_date),
                ]
            },
            'proof_of_address': {
                'required_fields': ['name', 'address', 'document_date'],
                'validators': [
                    ('address', self._validate_ontario_address),
                    ('document_date', self._validate_document_recency),
                ]
            }
        }
    
    def validate_document(self, document_type: str, extracted_data: Dict) -> Dict:
        """
        Validate a single document
        
        Args:
            document_type: Type of document
            extracted_data: Data extracted from document
            
        Returns:
            Validation result dictionary
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'field_validations': {}
        }
        
        if document_type not in self.validation_rules:
            results['warnings'].append(f"No validation rules found for: {document_type}")
            return results
        
        rules = self.validation_rules[document_type]
        
        # Check required fields
        for field in rules['required_fields']:
            if field not in extracted_data or not extracted_data[field]:
                results['errors'].append(f"Missing required field: {field}")
                results['is_valid'] = False
                results['field_validations'][field] = {
                    'valid': False,
                    'message': 'Field is missing or empty'
                }
            else:
                results['field_validations'][field] = {
                    'valid': True,
                    'message': 'Field present',
                    'value': extracted_data[field]
                }
        
        # Run specific validators
        for field, validator_func in rules['validators']:
            if field in extracted_data and extracted_data[field]:
                validation_result = validator_func(extracted_data[field], extracted_data)
                results['field_validations'][field] = validation_result
                
                if not validation_result['valid']:
                    if validation_result.get('severity') == 'error':
                        results['errors'].append(validation_result['message'])
                        results['is_valid'] = False
                    else:
                        results['warnings'].append(validation_result['message'])
        
        return results
    
    def _validate_id_not_expired(self, expiry_date: str, data: Dict) -> Dict:
        """Validate that ID has not expired"""
        try:
            # Parse different date formats
            date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', '%Y/%m/%d', '%d/%m/%Y']
            expiry = None
            
            for fmt in date_formats:
                try:
                    expiry = datetime.strptime(expiry_date, fmt)
                    break
                except ValueError:
                    continue
            
            if not expiry:
                return {
                    'valid': False,
                    'message': f"Invalid expiry date format: {expiry_date}",
                    'severity': 'error'
                }
            
            if expiry < self.current_date:
                return {
                    'valid': False,
                    'message': f"ID expired on {expiry_date}",
                    'severity': 'error'
                }
            
            # Warn if expiring soon (within 3 months)
            if expiry < self.current_date + timedelta(days=90):
                return {
                    'valid': True,
                    'message': f"ID expires soon: {expiry_date}",
                    'severity': 'warning'
                }
            
            return {
                'valid': True,
                'message': f"ID valid until {expiry_date}"
            }
        except Exception as e:
            return {
                'valid': False,
                'message': f"Error validating expiry date: {str(e)}",
                'severity': 'error'
            }
    
    def _validate_age_requirement(self, date_of_birth: str, data: Dict) -> Dict:
        """Validate student meets age requirement (typically 16+)"""
        try:
            date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', '%Y/%m/%d', '%d/%m/%Y']
            dob = None
            
            for fmt in date_formats:
                try:
                    dob = datetime.strptime(date_of_birth, fmt)
                    break
                except ValueError:
                    continue
            
            if not dob:
                return {
                    'valid': False,
                    'message': f"Invalid date of birth format: {date_of_birth}",
                    'severity': 'error'
                }
            
            age = (self.current_date - dob).days / 365.25
            
            if age < 16:
                return {
                    'valid': False,
                    'message': f"Student must be at least 16 years old (currently {int(age)})",
                    'severity': 'error'
                }
            
            if age < 18:
                return {
                    'valid': True,
                    'message': f"Student is {int(age)} years old - parental consent may be required",
                    'severity': 'warning'
                }
            
            return {
                'valid': True,
                'message': f"Age requirement met ({int(age)} years old)"
            }
        except Exception as e:
            return {
                'valid': False,
                'message': f"Error validating age: {str(e)}",
                'severity': 'error'
            }
    
    def _validate_education_date(self, graduation_date: str, data: Dict) -> Dict:
        """Validate graduation date is reasonable"""
        try:
            # Try to parse various date formats
            if re.search(r'\d{4}', graduation_date):  # Contains a year
                year = int(re.search(r'\d{4}', graduation_date).group())
                current_year = self.current_date.year
                
                if year > current_year:
                    return {
                        'valid': True,
                        'message': f"Expected graduation: {graduation_date}",
                        'severity': 'info'
                    }
                
                if year < current_year - 50:
                    return {
                        'valid': True,
                        'message': f"Graduation date is more than 50 years ago",
                        'severity': 'warning'
                    }
                
                return {
                    'valid': True,
                    'message': f"Graduation date: {graduation_date}"
                }
            
            return {
                'valid': True,
                'message': f"Graduation date noted: {graduation_date}"
            }
        except Exception as e:
            return {
                'valid': True,
                'message': f"Could not parse graduation date: {graduation_date}",
                'severity': 'warning'
            }
    
    def _validate_ontario_address(self, address: str, data: Dict) -> Dict:
        """Validate address is in Ontario"""
        ontario_indicators = [
            r'\bON\b', r'\bONT\b', r'\bONTARIO\b',
            r'\b[KLMNP]\d[A-Z]\s*\d[A-Z]\d\b'  # Ontario postal code pattern
        ]
        
        address_upper = address.upper()
        
        for pattern in ontario_indicators:
            if re.search(pattern, address_upper):
                return {
                    'valid': True,
                    'message': 'Ontario address verified'
                }
        
        return {
            'valid': False,
            'message': 'Address does not appear to be in Ontario',
            'severity': 'error'
        }
    
    def _validate_document_recency(self, document_date: str, data: Dict) -> Dict:
        """Validate document is recent (within 90 days for proof of address)"""
        try:
            date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', '%B %d, %Y', '%b %d, %Y']
            doc_date = None
            
            for fmt in date_formats:
                try:
                    doc_date = datetime.strptime(document_date.strip(), fmt)
                    break
                except ValueError:
                    continue
            
            # Try parsing "Month Year" format
            if not doc_date:
                try:
                    doc_date = datetime.strptime(document_date.strip(), '%B %Y')
                except ValueError:
                    pass
            
            if not doc_date:
                return {
                    'valid': False,
                    'message': f"Could not parse document date: {document_date}",
                    'severity': 'error'
                }
            
            days_old = (self.current_date - doc_date).days
            
            if days_old > 90:
                return {
                    'valid': False,
                    'message': f"Document is {days_old} days old (must be within 90 days)",
                    'severity': 'error'
                }
            
            if days_old < 0:
                return {
                    'valid': False,
                    'message': f"Document date is in the future: {document_date}",
                    'severity': 'error'
                }
            
            return {
                'valid': True,
                'message': f"Document is {days_old} days old (within 90-day requirement)"
            }
        except Exception as e:
            return {
                'valid': False,
                'message': f"Error validating document date: {str(e)}",
                'severity': 'error'
            }
    
    def validate_application(self, documents: List[Dict]) -> Dict:
        """
        Validate complete enrollment application
        
        Args:
            documents: List of document validation results
            
        Returns:
            Overall application validation result
        """
        result = {
            'application_status': 'pending',
            'overall_valid': True,
            'documents_processed': len(documents),
            'documents_valid': 0,
            'missing_documents': [],
            'errors': [],
            'warnings': [],
            'next_steps': []
        }
        
        # Required document types for standard enrollment
        required_types = ['government_id', 'transcript', 'proof_of_address']
        found_types = set()
        
        for doc in documents:
            doc_type = doc.get('document_type', 'unknown')
            found_types.add(doc_type)
            
            validation = doc.get('validation', {})
            if validation.get('is_valid'):
                result['documents_valid'] += 1
            else:
                result['overall_valid'] = False
                result['errors'].extend(validation.get('errors', []))
            
            result['warnings'].extend(validation.get('warnings', []))
        
        # Check for missing required documents
        for req_type in required_types:
            if req_type not in found_types:
                result['missing_documents'].append(req_type)
                result['overall_valid'] = False
        
        # Determine status and next steps
        if result['overall_valid'] and len(result['missing_documents']) == 0:
            result['application_status'] = 'approved'
            result['next_steps'] = [
                'Send acceptance letter to student',
                'Process tuition payment',
                'Schedule orientation session'
            ]
        elif len(result['missing_documents']) > 0:
            result['application_status'] = 'incomplete'
            result['next_steps'] = [
                f"Request missing documents: {', '.join(result['missing_documents'])}",
                'Send follow-up email to student'
            ]
        else:
            result['application_status'] = 'requires_review'
            result['next_steps'] = [
                'Manual review required by admissions staff',
                'Contact student to resolve issues'
            ]
        
        return result
    
    def generate_validation_report(self, application_result: Dict) -> str:
        """
        Generate human-readable validation report
        
        Args:
            application_result: Result from validate_application
            
        Returns:
            Formatted text report
        """
        report = []
        report.append("=" * 60)
        report.append("ENROLLMENT APPLICATION VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"Status: {application_result['application_status'].upper()}")
        report.append(f"Documents Processed: {application_result['documents_processed']}")
        report.append(f"Documents Valid: {application_result['documents_valid']}")
        report.append("")
        
        if application_result['missing_documents']:
            report.append("MISSING DOCUMENTS:")
            for doc in application_result['missing_documents']:
                report.append(f"  - {doc}")
            report.append("")
        
        if application_result['errors']:
            report.append("ERRORS:")
            for error in application_result['errors']:
                report.append(f"  ❌ {error}")
            report.append("")
        
        if application_result['warnings']:
            report.append("WARNINGS:")
            for warning in application_result['warnings']:
                report.append(f"  ⚠️  {warning}")
            report.append("")
        
        if application_result['next_steps']:
            report.append("NEXT STEPS:")
            for i, step in enumerate(application_result['next_steps'], 1):
                report.append(f"  {i}. {step}")
        
        report.append("=" * 60)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Example usage
    validator = EnrollmentValidator()
    
    # Test ID validation
    test_data = {
        'full_name': 'JOHN SMITH',
        'date_of_birth': '1998-05-15',
        'id_number': 'P1234-56789-01234',
        'expiry_date': '2028-01-10'
    }
    
    result = validator.validate_document('government_id', test_data)
    print("Validation Result:")
    print(f"  Valid: {result['is_valid']}")
    print(f"  Errors: {result['errors']}")
    print(f"  Warnings: {result['warnings']}")

