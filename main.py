"""
Main Orchestrator for Career College Enrollment Automation
Brukd Consultancy - RPA/AI Workflow Demo
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from modules import (
    OCREngine,
    DocumentClassifier,
    EnrollmentValidator,
    NotificationSystem,
    WorkflowRouter
)


class EnrollmentAutomationSystem:
    """
    Main orchestrator for automated enrollment processing
    """
    
    def __init__(self, config: Dict = None):
        """Initialize all automation components"""
        print("🚀 Initializing Brukd Career College Automation System...")
        
        self.config = config or {}
        
        # Initialize modules
        self.ocr = OCREngine()
        self.classifier = DocumentClassifier()
        self.validator = EnrollmentValidator()
        self.notifier = NotificationSystem()
        self.router = WorkflowRouter()
        
        # Processing statistics
        self.stats = {
            'applications_processed': 0,
            'documents_processed': 0,
            'total_processing_time': 0,
            'auto_approved': 0,
            'requires_review': 0,
            'incomplete': 0
        }
        
        # Create output directories
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / 'reports').mkdir(exist_ok=True)
        (self.output_dir / 'logs').mkdir(exist_ok=True)
        
        print("✅ System initialized successfully!\n")
    
    def process_application(self, application_data: Dict) -> Dict:
        """
        Process a complete student application
        
        Args:
            application_data: Dictionary containing application info and document paths
            
        Returns:
            Processing result with routing and notifications
        """
        start_time = datetime.now()
        
        application_id = application_data.get('application_id', f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        print(f"\n{'='*70}")
        print(f"📋 Processing Application: {application_id}")
        print(f"   Student: {application_data.get('student_name', 'Unknown')}")
        print(f"   Program: {application_data.get('program', 'N/A')}")
        print(f"{'='*70}\n")
        
        result = {
            'application_id': application_id,
            'student_info': {
                'name': application_data.get('student_name'),
                'email': application_data.get('student_email'),
                'phone': application_data.get('student_phone'),
                'program': application_data.get('program')
            },
            'documents': [],
            'validation': None,
            'routing': None,
            'notifications': [],
            'processing_time': 0,
            'status': 'processing'
        }
        
        # STEP 1: OCR Processing
        print("🔍 STEP 1: OCR Document Extraction")
        print("-" * 70)
        
        document_files = application_data.get('documents', [])
        for doc_file in document_files:
            doc_result = self._process_document(doc_file)
            result['documents'].append(doc_result)
            self.stats['documents_processed'] += 1
        
        print(f"   ✓ Processed {len(result['documents'])} documents\n")
        
        # STEP 2: Classification
        print("🤖 STEP 2: AI Document Classification")
        print("-" * 70)
        
        for doc in result['documents']:
            if doc['ocr_status'] == 'success':
                classification = self.classifier.classify_document(doc['extracted_text'])
                doc['classification'] = classification
                doc['document_type'] = classification['document_type']
                
                print(f"   📄 {doc['filename']}")
                print(f"      Type: {classification['document_type']}")
                print(f"      Confidence: {classification['confidence']:.0%}")
        
        print()
        
        # STEP 3: Structured Data Extraction
        print("📊 STEP 3: Structured Data Extraction")
        print("-" * 70)
        
        for doc in result['documents']:
            if doc.get('document_type') and doc['document_type'] != 'unknown':
                structured = self.ocr.extract_structured_data(
                    doc['file_path'],
                    doc['document_type']
                )
                doc['structured_data'] = structured
                print(f"   ✓ {doc['filename']}: {len(structured)} fields extracted")
        
        print()
        
        # STEP 4: Validation
        print("✅ STEP 4: Document Validation")
        print("-" * 70)
        
        validated_docs = []
        for doc in result['documents']:
            if doc.get('structured_data'):
                validation = self.validator.validate_document(
                    doc['document_type'],
                    doc['structured_data']
                )
                doc['validation'] = validation
                validated_docs.append(doc)
                
                status_icon = "✓" if validation['is_valid'] else "✗"
                print(f"   {status_icon} {doc['filename']}: {'Valid' if validation['is_valid'] else 'Invalid'}")
                
                if validation['errors']:
                    for error in validation['errors']:
                        print(f"      ❌ {error}")
        
        # Overall application validation
        application_validation = self.validator.validate_application(validated_docs)
        result['validation'] = application_validation
        
        print(f"\n   📋 Application Status: {application_validation['application_status'].upper()}")
        print(f"   📄 Valid Documents: {application_validation['documents_valid']}/{application_validation['documents_processed']}")
        
        if application_validation['missing_documents']:
            print(f"   ⚠️  Missing: {', '.join(application_validation['missing_documents'])}")
        
        print()
        
        # STEP 5: Workflow Routing
        print("🎯 STEP 5: Intelligent Workflow Routing")
        print("-" * 70)
        
        routing_data = {
            'application_id': application_id,
            'student_name': application_data.get('student_name'),
            'validation_status': application_validation['application_status'],
            'documents': result['documents'],
            'missing_documents': application_validation.get('missing_documents', []),
            'issues': application_validation.get('errors', [])
        }
        
        routing = self.router.route_application(routing_data)
        result['routing'] = routing
        
        print(f"   🏢 Department: {routing['department']}")
        print(f"   👤 Assigned to: {routing['primary_assignee']}")
        print(f"   ⚡ Priority: {routing['priority'].upper()}")
        print(f"   ⏱️  Estimated Time: {routing['estimated_time']} minutes")
        print(f"   📝 Tasks: {len(routing['tasks'])}")
        for task in routing['tasks']:
            print(f"      • {task['description']}")
        
        print()
        
        # STEP 6: Automated Notifications
        print("📧 STEP 6: Automated Notifications")
        print("-" * 70)
        
        # Notify student
        student_notification = self._send_student_notification(
            application_validation['application_status'],
            application_data,
            result
        )
        result['notifications'].append(student_notification)
        
        # Notify staff
        staff_notification = self._send_staff_notification(
            routing,
            application_data,
            result
        )
        result['notifications'].append(staff_notification)
        
        print(f"   ✓ Sent {len(result['notifications'])} notifications")
        
        print()
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        result['processing_time'] = round(processing_time, 2)
        result['status'] = 'completed'
        
        # Update statistics
        self.stats['applications_processed'] += 1
        self.stats['total_processing_time'] += processing_time
        
        status = application_validation['application_status']
        if status == 'approved':
            self.stats['auto_approved'] += 1
        elif status == 'requires_review':
            self.stats['requires_review'] += 1
        elif status == 'incomplete':
            self.stats['incomplete'] += 1
        
        # Generate report
        self._generate_application_report(result)
        
        print(f"{'='*70}")
        print(f"✅ Application Processing Complete!")
        print(f"   Processing Time: {processing_time:.2f} seconds")
        print(f"   Status: {application_validation['application_status'].upper()}")
        print(f"{'='*70}\n")
        
        return result
    
    def _process_document(self, doc_file: Dict) -> Dict:
        """Process a single document with OCR"""
        file_path = doc_file.get('path')
        filename = os.path.basename(file_path)
        
        print(f"   📄 Processing: {filename}")
        
        try:
            # Extract text
            text = self.ocr.extract_text(file_path)
            
            # Get confidence score
            confidence = self.ocr.get_confidence_score(file_path)
            
            # Quality assessment
            quality = self.classifier.validate_document_quality(text, confidence)
            
            print(f"      OCR Confidence: {confidence:.1f}%")
            print(f"      Quality Score: {quality['quality_score']}/100")
            
            return {
                'filename': filename,
                'file_path': file_path,
                'extracted_text': text,
                'ocr_confidence': confidence,
                'quality': quality,
                'ocr_status': 'success'
            }
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")
            return {
                'filename': filename,
                'file_path': file_path,
                'extracted_text': '',
                'ocr_confidence': 0,
                'quality': {'quality_score': 0, 'is_acceptable': False},
                'ocr_status': 'error',
                'error': str(e)
            }
    
    def _send_student_notification(self, status: str, application_data: Dict, result: Dict) -> Dict:
        """Send notification to student"""
        student = {
            'name': application_data.get('student_name'),
            'email': application_data.get('student_email'),
            'role': 'student'
        }
        
        notification_type = {
            'approved': 'application_approved',
            'incomplete': 'documents_incomplete',
            'requires_review': 'manual_review_required',
        }.get(status, 'application_received')
        
        notification_data = {
            'application_id': result['application_id'],
            'program': application_data.get('program'),
            'submission_date': datetime.now().strftime('%Y-%m-%d'),
            'documents': [doc['filename'] for doc in result['documents']],
            'missing_documents': result['validation'].get('missing_documents', []),
            'issues': result['validation'].get('errors', []),
            'start_date': 'January 15, 2026',
            'payment_deadline': 'December 15, 2025',
            'orientation_date': 'January 10, 2026'
        }
        
        notif_result = self.notifier.send_notification(notification_type, student, notification_data)
        
        print(f"   📧 Student notification: {notification_type}")
        
        return notif_result
    
    def _send_staff_notification(self, routing: Dict, application_data: Dict, result: Dict) -> Dict:
        """Send notification to assigned staff"""
        staff = {
            'name': routing['primary_assignee'],
            'email': f"{routing['primary_assignee'].lower().replace(' ', '.')}@careercollege.ca",
            'role': 'staff',
            'department': routing['department']
        }
        
        notification_data = {
            'application_id': result['application_id'],
            'student_name': application_data.get('student_name'),
            'student_email': application_data.get('student_email'),
            'student_phone': application_data.get('student_phone'),
            'program': application_data.get('program'),
            'start_date': 'January 2026',
            'documents': result['documents'],
            'documents_valid': result['validation']['documents_valid'],
            'documents_total': result['validation']['documents_processed'],
            'validation_status': result['validation']['application_status'],
            'missing_documents': result['validation'].get('missing_documents', []),
            'issues': result['validation'].get('errors', [])
        }
        
        notification_type = 'staff_review_needed' if routing['priority'] in ['high', 'urgent'] else 'staff_new_application'
        
        notif_result = self.notifier.send_notification(notification_type, staff, notification_data)
        
        print(f"   📧 Staff notification: {staff['name']} ({routing['department']})")
        
        return notif_result
    
    def _generate_application_report(self, result: Dict):
        """Generate detailed application report"""
        report_path = self.output_dir / 'reports' / f"{result['application_id']}_report.json"
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        # Also generate text report
        text_report_path = self.output_dir / 'reports' / f"{result['application_id']}_report.txt"
        
        with open(text_report_path, 'w') as f:
            f.write(self.validator.generate_validation_report(result['validation']))
    
    def get_statistics(self) -> Dict:
        """Get processing statistics"""
        avg_time = (self.stats['total_processing_time'] / self.stats['applications_processed'] 
                   if self.stats['applications_processed'] > 0 else 0)
        
        return {
            **self.stats,
            'average_processing_time': round(avg_time, 2),
            'automation_rate': round(self.stats['auto_approved'] / max(self.stats['applications_processed'], 1) * 100, 1)
        }
    
    def generate_summary_report(self):
        """Generate summary report of all processing"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("📊 PROCESSING SUMMARY")
        print("="*70)
        print(f"Applications Processed: {stats['applications_processed']}")
        print(f"Documents Processed: {stats['documents_processed']}")
        print(f"Auto-Approved: {stats['auto_approved']}")
        print(f"Requires Review: {stats['requires_review']}")
        print(f"Incomplete: {stats['incomplete']}")
        print(f"Average Processing Time: {stats['average_processing_time']:.2f} seconds")
        print(f"Automation Rate: {stats['automation_rate']:.1f}%")
        print("="*70)
        
        # Save to file
        summary_path = self.output_dir / 'reports' / 'summary.json'
        with open(summary_path, 'w') as f:
            json.dump(stats, f, indent=2)


def main():
    """Main entry point for demo"""
    print("\n" + "="*70)
    print("🏫 BRUKD CAREER COLLEGE ENROLLMENT AUTOMATION")
    print("   Process Automation & Smart Workflow with RPA/AI")
    print("="*70 + "\n")
    
    # Initialize system
    system = EnrollmentAutomationSystem()
    
    # Demo applications
    demo_applications = [
        {
            'application_id': 'APP-2025-001234',
            'student_name': 'Sarah Johnson',
            'student_email': 'sarah.johnson@email.com',
            'student_phone': '416-555-0123',
            'program': 'Healthcare Assistant Diploma',
            'documents': [
                {'path': 'sample_documents/sarah_id.png', 'type': 'government_id'},
                {'path': 'sample_documents/sarah_transcript.png', 'type': 'transcript'},
                {'path': 'sample_documents/sarah_address.png', 'type': 'proof_of_address'}
            ]
        },
        {
            'application_id': 'APP-2025-001235',
            'student_name': 'Michael Chen',
            'student_email': 'michael.chen@email.com',
            'student_phone': '647-555-0456',
            'program': 'Business Administration',
            'documents': [
                {'path': 'sample_documents/michael_id.png', 'type': 'government_id'},
                {'path': 'sample_documents/michael_transcript.png', 'type': 'transcript'}
                # Missing proof of address - will trigger incomplete status
            ]
        }
    ]
    
    # Process applications
    results = []
    for app in demo_applications:
        try:
            result = system.process_application(app)
            results.append(result)
        except Exception as e:
            print(f"❌ Error processing application: {str(e)}\n")
    
    # Generate summary
    system.generate_summary_report()
    
    print("\n✅ Demo completed! Check the 'output/reports' directory for detailed reports.")
    print("📊 Run 'streamlit run dashboard.py' to view the interactive dashboard.\n")


if __name__ == "__main__":
    main()

