"""
Automated Notification System
Sends emails and notifications to students and staff
"""

from datetime import datetime
from typing import Dict, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


class NotificationSystem:
    """
    Handles automated notifications for enrollment workflow
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize notification system
        
        Args:
            config: Configuration dict with email settings
        """
        self.config = config or {}
        self.notification_log = []
        
        # Email templates
        self.templates = {
            'application_received': self._template_application_received,
            'application_approved': self._template_application_approved,
            'documents_incomplete': self._template_documents_incomplete,
            'manual_review_required': self._template_manual_review,
            'staff_new_application': self._template_staff_notification,
            'staff_review_needed': self._template_staff_review_needed
        }
    
    def send_notification(self, notification_type: str, recipient: Dict, data: Dict) -> Dict:
        """
        Send a notification
        
        Args:
            notification_type: Type of notification template
            recipient: Recipient info (name, email, role)
            data: Data to populate template
            
        Returns:
            Notification result
        """
        if notification_type not in self.templates:
            return {
                'success': False,
                'error': f"Unknown notification type: {notification_type}"
            }
        
        # Generate notification content
        template_func = self.templates[notification_type]
        content = template_func(recipient, data)
        
        # In production, this would send actual email
        # For demo, we'll log the notification
        notification = {
            'timestamp': datetime.now().isoformat(),
            'type': notification_type,
            'recipient': recipient,
            'subject': content['subject'],
            'body': content['body'],
            'status': 'sent'
        }
        
        self.notification_log.append(notification)
        
        return {
            'success': True,
            'notification_id': len(self.notification_log),
            'message': f"Notification sent to {recipient['email']}"
        }
    
    def _template_application_received(self, recipient: Dict, data: Dict) -> Dict:
        """Template for application received confirmation"""
        subject = "Application Received - Welcome to Career College"
        
        body = f"""
Dear {recipient['name']},

Thank you for submitting your application to Career College Ontario!

Application Details:
- Application ID: {data.get('application_id', 'N/A')}
- Program: {data.get('program', 'N/A')}
- Submission Date: {data.get('submission_date', 'N/A')}

Your documents are currently being processed by our admissions team. You will receive 
an update within 2-3 business days.

Documents Received:
{self._format_document_list(data.get('documents', []))}

You can track your application status at: 
https://careercollege.ca/applications/{data.get('application_id', '')}

If you have any questions, please contact our admissions office:
📧 Email: admissions@careercollege.ca
📞 Phone: 1-800-555-0123

Best regards,
Admissions Team
Career College Ontario

---
This is an automated message. Please do not reply to this email.
"""
        
        return {'subject': subject, 'body': body}
    
    def _template_application_approved(self, recipient: Dict, data: Dict) -> Dict:
        """Template for approved application"""
        subject = "🎉 Congratulations! Your Application Has Been Approved"
        
        body = f"""
Dear {recipient['name']},

Congratulations! We are pleased to inform you that your application to Career College 
Ontario has been APPROVED!

Program: {data.get('program', 'N/A')}
Start Date: {data.get('start_date', 'N/A')}
Application ID: {data.get('application_id', 'N/A')}

NEXT STEPS:
1. Review and sign your enrollment agreement (link in separate email)
2. Complete tuition payment by {data.get('payment_deadline', 'TBD')}
3. Attend mandatory orientation on {data.get('orientation_date', 'TBD')}
4. Complete online student portal registration

Important Dates:
- Tuition Payment Due: {data.get('payment_deadline', 'TBD')}
- Orientation Session: {data.get('orientation_date', 'TBD')}
- First Day of Classes: {data.get('start_date', 'TBD')}

We're excited to welcome you to our student community!

For questions or assistance, contact:
📧 studentservices@careercollege.ca
📞 1-800-555-0123

Warm regards,
Admissions Team
Career College Ontario
"""
        
        return {'subject': subject, 'body': body}
    
    def _template_documents_incomplete(self, recipient: Dict, data: Dict) -> Dict:
        """Template for incomplete application"""
        subject = "Action Required: Complete Your Application"
        
        missing_docs = data.get('missing_documents', [])
        issues = data.get('issues', [])
        
        body = f"""
Dear {recipient['name']},

Thank you for your interest in Career College Ontario. We've reviewed your application 
and need some additional information to proceed.

Application ID: {data.get('application_id', 'N/A')}

MISSING DOCUMENTS:
{self._format_missing_documents(missing_docs)}

{self._format_issues(issues)}

Please submit the missing documents within 7 days to avoid application delays.

HOW TO SUBMIT:
1. Log in to your application portal: https://careercollege.ca/applications
2. Upload the required documents
3. You'll receive a confirmation email once submitted

Need help? Our admissions team is here to assist:
📧 admissions@careercollege.ca
📞 1-800-555-0123
⏰ Mon-Fri, 9am-5pm EST

We look forward to completing your application!

Best regards,
Admissions Team
Career College Ontario
"""
        
        return {'subject': subject, 'body': body}
    
    def _template_manual_review(self, recipient: Dict, data: Dict) -> Dict:
        """Template for manual review needed"""
        subject = "Application Under Review"
        
        body = f"""
Dear {recipient['name']},

Thank you for submitting your application to Career College Ontario.

Your application requires additional review by our admissions team. This is a standard 
process for certain applications and does not indicate any problem.

Application ID: {data.get('application_id', 'N/A')}
Program: {data.get('program', 'N/A')}

REASON FOR REVIEW:
{data.get('review_reason', 'Additional verification required')}

WHAT TO EXPECT:
- An admissions counselor will contact you within 2-3 business days
- You may be asked to provide additional information or clarification
- We will process your application as quickly as possible

If you have immediate questions, please contact:
📧 admissions@careercollege.ca
📞 1-800-555-0123

Thank you for your patience.

Best regards,
Admissions Team
Career College Ontario
"""
        
        return {'subject': subject, 'body': body}
    
    def _template_staff_notification(self, recipient: Dict, data: Dict) -> Dict:
        """Template for staff notification of new application"""
        subject = f"New Application: {data.get('student_name', 'Unknown')} - {data.get('program', 'N/A')}"
        
        body = f"""
New enrollment application received and processed by automation system.

STUDENT INFORMATION:
- Name: {data.get('student_name', 'N/A')}
- Email: {data.get('student_email', 'N/A')}
- Phone: {data.get('student_phone', 'N/A')}
- Application ID: {data.get('application_id', 'N/A')}

PROGRAM:
- {data.get('program', 'N/A')}
- Intended Start: {data.get('start_date', 'N/A')}

DOCUMENT STATUS:
{self._format_document_status(data.get('documents', []))}

VALIDATION RESULT:
- Status: {data.get('validation_status', 'N/A')}
- Documents Valid: {data.get('documents_valid', 0)}/{data.get('documents_total', 0)}

{self._format_action_required(data)}

View full application: https://admin.careercollege.ca/applications/{data.get('application_id', '')}

---
Automated by Brukd RPA System
"""
        
        return {'subject': subject, 'body': body}
    
    def _template_staff_review_needed(self, recipient: Dict, data: Dict) -> Dict:
        """Template for staff when manual review is needed"""
        subject = f"⚠️ REVIEW REQUIRED: Application {data.get('application_id', 'N/A')}"
        
        body = f"""
MANUAL REVIEW REQUIRED

Application ID: {data.get('application_id', 'N/A')}
Student: {data.get('student_name', 'N/A')}
Program: {data.get('program', 'N/A')}

ISSUES DETECTED:
{self._format_issues(data.get('issues', []))}

MISSING DOCUMENTS:
{self._format_missing_documents(data.get('missing_documents', []))}

RECOMMENDED ACTION:
{data.get('recommended_action', 'Contact student for clarification')}

Priority: {data.get('priority', 'Normal')}
Assigned To: {recipient['name']}

View application: https://admin.careercollege.ca/applications/{data.get('application_id', '')}

---
Please review and take action within 24 hours.
Automated by Brukd RPA System
"""
        
        return {'subject': subject, 'body': body}
    
    def _format_document_list(self, documents: List[str]) -> str:
        """Format list of documents"""
        if not documents:
            return "  - None"
        return "\n".join(f"  ✓ {doc}" for doc in documents)
    
    def _format_missing_documents(self, documents: List[str]) -> str:
        """Format list of missing documents"""
        if not documents:
            return "  None - all documents received!"
        return "\n".join(f"  ❌ {doc}" for doc in documents)
    
    def _format_issues(self, issues: List[str]) -> str:
        """Format list of issues"""
        if not issues:
            return ""
        return "\nISSUES FOUND:\n" + "\n".join(f"  ⚠️  {issue}" for issue in issues)
    
    def _format_document_status(self, documents: List[Dict]) -> str:
        """Format document validation status"""
        if not documents:
            return "  No documents processed"
        
        lines = []
        for doc in documents:
            status = "✓" if doc.get('valid', False) else "❌"
            lines.append(f"  {status} {doc.get('type', 'Unknown')}: {doc.get('status', 'Unknown')}")
        
        return "\n".join(lines)
    
    def _format_action_required(self, data: Dict) -> str:
        """Format action required section"""
        status = data.get('validation_status', '').lower()
        
        if status == 'approved':
            return "\nACTION: Send acceptance letter and enrollment package"
        elif status == 'incomplete':
            return "\nACTION: Automated follow-up email sent to student for missing documents"
        elif status == 'requires_review':
            return "\nACTION: Manual review required - please investigate flagged issues"
        else:
            return "\nACTION: Please review application"
    
    def get_notification_log(self, limit: int = None) -> List[Dict]:
        """
        Get notification history
        
        Args:
            limit: Maximum number of notifications to return
            
        Returns:
            List of notifications
        """
        if limit:
            return self.notification_log[-limit:]
        return self.notification_log
    
    def generate_notification_report(self) -> Dict:
        """Generate summary report of all notifications sent"""
        if not self.notification_log:
            return {
                'total_notifications': 0,
                'by_type': {},
                'by_recipient': {}
            }
        
        by_type = {}
        by_recipient = {}
        
        for notif in self.notification_log:
            # Count by type
            notif_type = notif['type']
            by_type[notif_type] = by_type.get(notif_type, 0) + 1
            
            # Count by recipient role
            recipient_role = notif['recipient'].get('role', 'unknown')
            by_recipient[recipient_role] = by_recipient.get(recipient_role, 0) + 1
        
        return {
            'total_notifications': len(self.notification_log),
            'by_type': by_type,
            'by_recipient': by_recipient,
            'first_notification': self.notification_log[0]['timestamp'] if self.notification_log else None,
            'last_notification': self.notification_log[-1]['timestamp'] if self.notification_log else None
        }


if __name__ == "__main__":
    # Example usage
    notifier = NotificationSystem()
    
    # Test notification
    recipient = {
        'name': 'John Smith',
        'email': 'john.smith@email.com',
        'role': 'student'
    }
    
    data = {
        'application_id': 'APP-2025-001234',
        'program': 'Healthcare Assistant Diploma',
        'submission_date': '2025-10-26',
        'documents': ['Government ID', 'Transcript', 'Proof of Address']
    }
    
    result = notifier.send_notification('application_received', recipient, data)
    print(f"Notification sent: {result['success']}")
    print(f"Message: {result['message']}")

