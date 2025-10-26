"""
Smart Workflow Router
Automatically assigns tasks to appropriate staff based on application status
"""

from typing import Dict, List
from datetime import datetime
import json


class WorkflowRouter:
    """
    Intelligent routing engine for enrollment workflow
    Assigns tasks to departments and staff members
    """
    
    def __init__(self):
        # Department and staff configuration
        self.departments = {
            'admissions': {
                'staff': ['Sarah Johnson', 'Michael Chen', 'Emily Rodriguez'],
                'responsibilities': ['application_review', 'document_verification', 'initial_assessment']
            },
            'registrar': {
                'staff': ['David Kim', 'Jessica Martinez'],
                'responsibilities': ['enrollment_finalization', 'transcript_evaluation', 'credit_transfer']
            },
            'financial_aid': {
                'staff': ['Amanda Thompson', 'Robert Lee'],
                'responsibilities': ['osap_processing', 'scholarship_review', 'payment_plans']
            },
            'international': {
                'staff': ['Linda Chang', 'Mohammed Ahmed'],
                'responsibilities': ['study_permit_verification', 'international_credentials', 'visa_support']
            },
            'student_services': {
                'staff': ['Karen Wilson', 'James Brown'],
                'responsibilities': ['orientation_scheduling', 'student_support', 'accommodation_requests']
            }
        }
        
        self.task_queue = []
        self.task_assignments = []
        
        # Priority levels
        self.priority_rules = {
            'urgent': ['expired_documents', 'missing_critical_info', 'deadline_approaching'],
            'high': ['incomplete_application', 'manual_review_required', 'international_student'],
            'normal': ['standard_review', 'document_verification'],
            'low': ['information_request', 'status_inquiry']
        }
    
    def route_application(self, application: Dict) -> Dict:
        """
        Route application to appropriate department/staff
        
        Args:
            application: Application data with validation results
            
        Returns:
            Routing decision with assigned tasks
        """
        routing_decision = {
            'application_id': application.get('application_id'),
            'student_name': application.get('student_name'),
            'status': application.get('validation_status'),
            'tasks': [],
            'primary_assignee': None,
            'department': None,
            'priority': 'normal',
            'estimated_time': 0,
            'routing_reason': ''
        }
        
        validation_status = application.get('validation_status', '').lower()
        
        # Determine routing based on status
        if validation_status == 'approved':
            routing_decision.update(self._route_approved_application(application))
        elif validation_status == 'incomplete':
            routing_decision.update(self._route_incomplete_application(application))
        elif validation_status == 'requires_review':
            routing_decision.update(self._route_review_required(application))
        else:
            routing_decision.update(self._route_default(application))
        
        # Check for special cases
        if self._is_international_student(application):
            routing_decision = self._add_international_tasks(routing_decision, application)
        
        if self._has_financial_aid(application):
            routing_decision = self._add_financial_aid_tasks(routing_decision, application)
        
        # Assign priority
        routing_decision['priority'] = self._calculate_priority(application)
        
        # Add to task queue
        self.task_queue.append(routing_decision)
        
        return routing_decision
    
    def _route_approved_application(self, application: Dict) -> Dict:
        """Route approved applications"""
        return {
            'department': 'registrar',
            'primary_assignee': self._get_next_available_staff('registrar'),
            'tasks': [
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-001",
                    'type': 'finalize_enrollment',
                    'description': 'Finalize student enrollment and generate acceptance letter',
                    'department': 'registrar',
                    'estimated_time': 15,
                    'status': 'pending'
                },
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-002",
                    'type': 'send_acceptance',
                    'description': 'Send acceptance letter and enrollment package',
                    'department': 'admissions',
                    'estimated_time': 5,
                    'status': 'pending'
                },
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-003",
                    'type': 'schedule_orientation',
                    'description': 'Schedule student orientation session',
                    'department': 'student_services',
                    'estimated_time': 10,
                    'status': 'pending'
                }
            ],
            'estimated_time': 30,
            'routing_reason': 'Application approved - ready for enrollment finalization'
        }
    
    def _route_incomplete_application(self, application: Dict) -> Dict:
        """Route incomplete applications"""
        missing_docs = application.get('missing_documents', [])
        
        return {
            'department': 'admissions',
            'primary_assignee': self._get_next_available_staff('admissions'),
            'tasks': [
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-001",
                    'type': 'follow_up_documents',
                    'description': f'Follow up with student for missing documents: {", ".join(missing_docs)}',
                    'department': 'admissions',
                    'estimated_time': 10,
                    'status': 'automated',  # Automated email already sent
                    'note': 'Automated follow-up email sent. Manual follow-up if no response in 3 days.'
                },
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-002",
                    'type': 'review_resubmission',
                    'description': 'Review application once documents are resubmitted',
                    'department': 'admissions',
                    'estimated_time': 15,
                    'status': 'pending'
                }
            ],
            'estimated_time': 25,
            'routing_reason': f'Incomplete application - missing: {", ".join(missing_docs)}'
        }
    
    def _route_review_required(self, application: Dict) -> Dict:
        """Route applications requiring manual review"""
        issues = application.get('issues', [])
        
        return {
            'department': 'admissions',
            'primary_assignee': self._get_next_available_staff('admissions'),
            'tasks': [
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-001",
                    'type': 'manual_review',
                    'description': 'Conduct manual review of application and documents',
                    'department': 'admissions',
                    'estimated_time': 30,
                    'status': 'pending',
                    'priority': 'high',
                    'issues': issues
                },
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-002",
                    'type': 'contact_student',
                    'description': 'Contact student for clarification if needed',
                    'department': 'admissions',
                    'estimated_time': 15,
                    'status': 'conditional'
                }
            ],
            'estimated_time': 45,
            'routing_reason': 'Manual review required due to validation issues'
        }
    
    def _route_default(self, application: Dict) -> Dict:
        """Default routing for applications"""
        return {
            'department': 'admissions',
            'primary_assignee': self._get_next_available_staff('admissions'),
            'tasks': [
                {
                    'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-001",
                    'type': 'initial_review',
                    'description': 'Initial review of application',
                    'department': 'admissions',
                    'estimated_time': 20,
                    'status': 'pending'
                }
            ],
            'estimated_time': 20,
            'routing_reason': 'Standard application processing'
        }
    
    def _is_international_student(self, application: Dict) -> bool:
        """Check if student is international"""
        documents = application.get('documents', [])
        for doc in documents:
            if doc.get('type') == 'study_permit':
                return True
        
        # Check if address is non-Canadian
        address = application.get('address', '').upper()
        if 'CANADA' not in address and any(indicator in address for indicator in ['ON', 'ONTARIO']):
            return False
        
        return False
    
    def _has_financial_aid(self, application: Dict) -> bool:
        """Check if student applied for financial aid"""
        documents = application.get('documents', [])
        for doc in documents:
            if 'osap' in doc.get('type', '').lower():
                return True
        
        return application.get('financial_aid', False)
    
    def _add_international_tasks(self, routing: Dict, application: Dict) -> Dict:
        """Add tasks specific to international students"""
        routing['tasks'].append({
            'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-INT",
            'type': 'verify_study_permit',
            'description': 'Verify study permit validity and enrollment eligibility',
            'department': 'international',
            'estimated_time': 20,
            'status': 'pending'
        })
        
        routing['estimated_time'] += 20
        routing['routing_reason'] += ' | International student - additional verification required'
        
        return routing
    
    def _add_financial_aid_tasks(self, routing: Dict, application: Dict) -> Dict:
        """Add tasks for financial aid processing"""
        routing['tasks'].append({
            'task_id': f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}-FA",
            'type': 'process_financial_aid',
            'description': 'Process OSAP/financial aid documentation',
            'department': 'financial_aid',
            'estimated_time': 25,
            'status': 'pending'
        })
        
        routing['estimated_time'] += 25
        routing['routing_reason'] += ' | Financial aid application included'
        
        return routing
    
    def _calculate_priority(self, application: Dict) -> str:
        """Calculate task priority based on application characteristics"""
        # Check for urgent conditions
        issues = application.get('issues', [])
        for issue in issues:
            if any(keyword in issue.lower() for keyword in ['expired', 'invalid', 'critical']):
                return 'urgent'
        
        # Check for high priority conditions
        if application.get('validation_status') == 'requires_review':
            return 'high'
        
        if self._is_international_student(application):
            return 'high'
        
        # Check submission date for deadline approaching
        submission_date = application.get('submission_date')
        if submission_date:
            # In production, would check against start date deadlines
            pass
        
        return 'normal'
    
    def _get_next_available_staff(self, department: str) -> str:
        """Get next available staff member using round-robin"""
        if department not in self.departments:
            return 'Unassigned'
        
        staff_list = self.departments[department]['staff']
        
        # Simple round-robin - in production would check actual availability
        # Count assignments per staff member
        assignments_count = {}
        for staff in staff_list:
            count = sum(1 for task in self.task_assignments 
                       if task.get('assignee') == staff)
            assignments_count[staff] = count
        
        # Return staff with fewest assignments
        return min(staff_list, key=lambda s: assignments_count.get(s, 0))
    
    def get_task_queue(self, department: str = None, priority: str = None) -> List[Dict]:
        """
        Get filtered task queue
        
        Args:
            department: Filter by department
            priority: Filter by priority level
            
        Returns:
            Filtered task list
        """
        filtered = self.task_queue
        
        if department:
            filtered = [t for t in filtered if t.get('department') == department]
        
        if priority:
            filtered = [t for t in filtered if t.get('priority') == priority]
        
        return filtered
    
    def generate_workload_report(self) -> Dict:
        """Generate workload distribution report"""
        report = {
            'total_tasks': len(self.task_queue),
            'by_department': {},
            'by_priority': {},
            'by_staff': {},
            'average_processing_time': 0
        }
        
        total_time = 0
        
        for task in self.task_queue:
            # Count by department
            dept = task.get('department', 'unknown')
            report['by_department'][dept] = report['by_department'].get(dept, 0) + 1
            
            # Count by priority
            priority = task.get('priority', 'normal')
            report['by_priority'][priority] = report['by_priority'].get(priority, 0) + 1
            
            # Count by staff
            assignee = task.get('primary_assignee', 'unassigned')
            report['by_staff'][assignee] = report['by_staff'].get(assignee, 0) + 1
            
            # Sum estimated time
            total_time += task.get('estimated_time', 0)
        
        if len(self.task_queue) > 0:
            report['average_processing_time'] = total_time / len(self.task_queue)
        
        return report
    
    def export_tasks_to_json(self, filepath: str):
        """Export task queue to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.task_queue, f, indent=2, default=str)


if __name__ == "__main__":
    # Example usage
    router = WorkflowRouter()
    
    # Test routing
    test_application = {
        'application_id': 'APP-2025-001234',
        'student_name': 'John Smith',
        'validation_status': 'approved',
        'documents': [
            {'type': 'government_id', 'valid': True},
            {'type': 'transcript', 'valid': True},
            {'type': 'proof_of_address', 'valid': True}
        ]
    }
    
    routing = router.route_application(test_application)
    print(f"Application routed to: {routing['department']}")
    print(f"Assigned to: {routing['primary_assignee']}")
    print(f"Tasks: {len(routing['tasks'])}")
    print(f"Estimated time: {routing['estimated_time']} minutes")

