"""
Generate Sample Enrollment Documents
Creates realistic sample documents for demonstration
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
from datetime import datetime, timedelta


class SampleDocumentGenerator:
    """Generate sample enrollment documents for demo"""
    
    def __init__(self, output_dir: str = 'sample_documents'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Try to use a system font, fallback to default
        try:
            self.font_large = ImageFont.truetype("arial.ttf", 32)
            self.font_medium = ImageFont.truetype("arial.ttf", 24)
            self.font_small = ImageFont.truetype("arial.ttf", 18)
            self.font_tiny = ImageFont.truetype("arial.ttf", 14)
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()
    
    def generate_ontario_id(self, name: str, dob: str, address: str, filename: str):
        """Generate mock Ontario Photo Card"""
        # Create image
        img = Image.new('RGB', (800, 500), color='#E8F4F8')
        draw = ImageDraw.Draw(img)
        
        # Header
        draw.rectangle([0, 0, 800, 80], fill='#003DA5')
        draw.text((20, 15), "ONTARIO PHOTO CARD", fill='white', font=self.font_large)
        draw.text((20, 50), "CARTE-PHOTO DE L'ONTARIO", fill='white', font=self.font_tiny)
        
        # Photo placeholder
        draw.rectangle([30, 120, 230, 380], fill='#CCCCCC')
        draw.text((90, 230), "PHOTO", fill='white', font=self.font_medium)
        
        # Personal info
        y_pos = 120
        
        draw.text((260, y_pos), "SURNAME / NOM DE FAMILLE:", fill='black', font=self.font_small)
        y_pos += 30
        draw.text((280, y_pos), name.split()[1].upper(), fill='black', font=self.font_medium)
        y_pos += 50
        
        draw.text((260, y_pos), "GIVEN NAMES / PRÉNOMS:", fill='black', font=self.font_small)
        y_pos += 30
        draw.text((280, y_pos), name.split()[0].upper(), fill='black', font=self.font_medium)
        y_pos += 50
        
        draw.text((260, y_pos), "DATE OF BIRTH / DATE DE NAISSANCE:", fill='black', font=self.font_small)
        y_pos += 30
        draw.text((280, y_pos), dob, fill='black', font=self.font_medium)
        y_pos += 50
        
        draw.text((260, y_pos), "SEX / SEXE: M    HEIGHT / TAILLE: 175 cm", fill='black', font=self.font_small)
        
        # Bottom section
        y_pos = 420
        card_number = f"P{random.randint(1000, 9999)}-{random.randint(10000, 99999)}-{random.randint(10000, 99999)}"
        draw.text((30, y_pos), f"CARD NUMBER: {card_number}", fill='black', font=self.font_tiny)
        
        issue_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        expiry_date = (datetime.now() + timedelta(days=1095)).strftime('%Y-%m-%d')
        
        draw.text((30, y_pos+20), f"ISSUE DATE: {issue_date}", fill='black', font=self.font_tiny)
        draw.text((30, y_pos+40), f"EXPIRY DATE: {expiry_date}", fill='black', font=self.font_tiny)
        
        # Save
        img.save(self.output_dir / filename)
        print(f"   ✓ Generated: {filename}")
    
    def generate_transcript(self, student_name: str, school: str, filename: str):
        """Generate mock high school transcript"""
        img = Image.new('RGB', (850, 1100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Header
        draw.rectangle([0, 0, 850, 120], fill='#2E5C8A')
        draw.text((50, 20), school.upper(), fill='white', font=self.font_large)
        draw.text((50, 65), "OFFICIAL TRANSCRIPT", fill='white', font=self.font_medium)
        
        # Student info
        y_pos = 160
        draw.text((50, y_pos), f"STUDENT NAME: {student_name}", fill='black', font=self.font_medium)
        y_pos += 40
        
        draw.text((50, y_pos), f"STUDENT NUMBER: {random.randint(100000, 999999)}", fill='black', font=self.font_small)
        y_pos += 35
        
        draw.text((50, y_pos), f"GRADUATION DATE: June 2023", fill='black', font=self.font_small)
        y_pos += 35
        
        draw.text((50, y_pos), f"ONTARIO SECONDARY SCHOOL DIPLOMA (OSSD)", fill='black', font=self.font_small)
        y_pos += 60
        
        # Courses
        draw.text((50, y_pos), "GRADE 12 COURSES:", fill='black', font=self.font_medium)
        y_pos += 40
        
        courses = [
            ("English, Grade 12, U", "ENG4U", "85"),
            ("Advanced Functions, U", "MHF4U", "78"),
            ("Chemistry, Grade 12, U", "SCH4U", "82"),
            ("Biology, Grade 12, U", "SBI4U", "88"),
            ("World Issues, U", "CGW4U", "91"),
            ("Families in Canada, U", "HHS4U", "87")
        ]
        
        for course, code, grade in courses:
            draw.text((70, y_pos), f"{course}", fill='black', font=self.font_tiny)
            draw.text((550, y_pos), f"{code}", fill='black', font=self.font_tiny)
            draw.text((700, y_pos), f"{grade}%", fill='black', font=self.font_tiny)
            y_pos += 30
        
        y_pos += 40
        draw.text((50, y_pos), f"OVERALL AVERAGE: 85.2%", fill='black', font=self.font_medium)
        y_pos += 40
        draw.text((50, y_pos), f"CREDITS EARNED: 30 / 30 Required", fill='black', font=self.font_small)
        
        # Footer
        y_pos = 1000
        draw.rectangle([0, y_pos, 850, 1100], fill='#F0F0F0')
        draw.text((50, y_pos+20), "This is an official transcript.", fill='black', font=self.font_tiny)
        draw.text((50, y_pos+40), f"Issued: {datetime.now().strftime('%B %d, %Y')}", fill='black', font=self.font_tiny)
        draw.text((50, y_pos+60), "Ontario Ministry of Education", fill='black', font=self.font_tiny)
        
        # Save
        img.save(self.output_dir / filename)
        print(f"   ✓ Generated: {filename}")
    
    def generate_proof_of_address(self, name: str, address: str, filename: str):
        """Generate mock utility bill"""
        img = Image.new('RGB', (850, 1100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Header
        draw.rectangle([0, 0, 850, 100], fill='#006B3D')
        draw.text((50, 25), "TORONTO HYDRO", fill='white', font=self.font_large)
        draw.text((50, 65), "Electricity Bill", fill='white', font=self.font_small)
        
        # Bill date
        bill_date = (datetime.now() - timedelta(days=15)).strftime('%B %d, %Y')
        y_pos = 140
        
        draw.text((50, y_pos), f"BILL DATE: {bill_date}", fill='black', font=self.font_medium)
        y_pos += 40
        
        draw.text((50, y_pos), f"ACCOUNT NUMBER: {random.randint(1000000000, 9999999999)}", fill='black', font=self.font_small)
        y_pos += 60
        
        # Customer info
        draw.rectangle([40, y_pos, 810, y_pos+120], outline='black', width=2)
        y_pos += 15
        
        draw.text((60, y_pos), "CUSTOMER INFORMATION", fill='black', font=self.font_medium)
        y_pos += 35
        
        draw.text((60, y_pos), f"NAME: {name}", fill='black', font=self.font_small)
        y_pos += 30
        
        draw.text((60, y_pos), f"SERVICE ADDRESS:", fill='black', font=self.font_small)
        y_pos += 25
        
        # Split address into lines
        address_parts = address.split(',')
        for part in address_parts:
            draw.text((60, y_pos), part.strip(), fill='black', font=self.font_small)
            y_pos += 25
        
        y_pos += 40
        
        # Usage info
        draw.text((50, y_pos), "BILLING SUMMARY", fill='black', font=self.font_medium)
        y_pos += 40
        
        draw.text((70, y_pos), f"Previous Balance:", fill='black', font=self.font_small)
        draw.text((600, y_pos), "$0.00", fill='black', font=self.font_small)
        y_pos += 30
        
        draw.text((70, y_pos), f"Current Charges:", fill='black', font=self.font_small)
        draw.text((600, y_pos), f"${random.randint(80, 150)}.{random.randint(10, 99)}", fill='black', font=self.font_small)
        y_pos += 30
        
        draw.text((70, y_pos), f"Usage (kWh): {random.randint(300, 600)}", fill='black', font=self.font_tiny)
        y_pos += 50
        
        draw.rectangle([60, y_pos, 750, y_pos+45], fill='#F0F0F0')
        y_pos += 10
        draw.text((70, y_pos), f"TOTAL AMOUNT DUE:", fill='black', font=self.font_medium)
        total = random.randint(80, 150)
        draw.text((600, y_pos), f"${total}.{random.randint(10, 99)}", fill='black', font=self.font_medium)
        
        y_pos += 80
        due_date = (datetime.now() + timedelta(days=14)).strftime('%B %d, %Y')
        draw.text((70, y_pos), f"DUE DATE: {due_date}", fill='black', font=self.font_small)
        
        # Footer
        y_pos = 1000
        draw.text((50, y_pos), "Toronto Hydro-Electric System Limited", fill='#666666', font=self.font_tiny)
        draw.text((50, y_pos+20), "14 Carlton Street, Toronto, ON M5B 1K5", fill='#666666', font=self.font_tiny)
        draw.text((50, y_pos+40), "Customer Service: 416-542-8000", fill='#666666', font=self.font_tiny)
        
        # Save
        img.save(self.output_dir / filename)
        print(f"   ✓ Generated: {filename}")
    
    def generate_all_samples(self):
        """Generate complete set of sample documents"""
        print("\n📄 Generating Sample Enrollment Documents...")
        print("-" * 70)
        
        # Student 1: Sarah Johnson (complete application)
        print("\n👤 Student 1: Sarah Johnson")
        self.generate_ontario_id(
            name="Sarah Johnson",
            dob="1998-05-15",
            address="123 Main Street, Toronto, ON M5V 2T6",
            filename="sarah_id.png"
        )
        self.generate_transcript(
            student_name="Sarah Johnson",
            school="Toronto Central Secondary School",
            filename="sarah_transcript.png"
        )
        self.generate_proof_of_address(
            name="Sarah Johnson",
            address="123 Main Street, Toronto, ON M5V 2T6",
            filename="sarah_address.png"
        )
        
        # Student 2: Michael Chen (incomplete - missing proof of address)
        print("\n👤 Student 2: Michael Chen")
        self.generate_ontario_id(
            name="Michael Chen",
            dob="1999-11-22",
            address="456 Oak Avenue, Mississauga, ON L5B 3C8",
            filename="michael_id.png"
        )
        self.generate_transcript(
            student_name="Michael Chen",
            school="Mississauga High School",
            filename="michael_transcript.png"
        )
        
        # Student 3: Additional sample
        print("\n👤 Student 3: Emily Rodriguez")
        self.generate_ontario_id(
            name="Emily Rodriguez",
            dob="2000-03-08",
            address="789 Elm Street, Ottawa, ON K1P 5H9",
            filename="emily_id.png"
        )
        self.generate_transcript(
            student_name="Emily Rodriguez",
            school="Ottawa East High School",
            filename="emily_transcript.png"
        )
        self.generate_proof_of_address(
            name="Emily Rodriguez",
            address="789 Elm Street, Ottawa, ON K1P 5H9",
            filename="emily_address.png"
        )
        
        print("\n✅ Sample documents generated successfully!")
        print(f"📁 Location: {self.output_dir.absolute()}\n")


def main():
    """Generate all sample documents"""
    generator = SampleDocumentGenerator()
    generator.generate_all_samples()


if __name__ == "__main__":
    main()

