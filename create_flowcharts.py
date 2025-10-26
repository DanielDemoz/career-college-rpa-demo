"""
Generate Process Flowcharts
Creates visual flowcharts showing before/after processes
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class FlowchartGenerator:
    """Generate process flowcharts for documentation"""
    
    def __init__(self, output_dir: str = 'visualizations'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Try to load fonts
        try:
            self.font_title = ImageFont.truetype("arial.ttf", 32)
            self.font_heading = ImageFont.truetype("arial.ttf", 24)
            self.font_normal = ImageFont.truetype("arialbd.ttf", 18)
            self.font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            self.font_title = ImageFont.load_default()
            self.font_heading = ImageFont.load_default()
            self.font_normal = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
        
        # Colors
        self.colors = {
            'manual_primary': '#FF7043',
            'manual_secondary': '#FFCCBC',
            'automated_primary': '#66BB6A',
            'automated_secondary': '#C8E6C9',
            'background': '#F5F5F5',
            'text': '#212121',
            'arrow': '#757575'
        }
    
    def draw_rounded_rectangle(self, draw, coords, radius, fill, outline=None, width=1):
        """Draw a rounded rectangle"""
        x1, y1, x2, y2 = coords
        
        # Draw main rectangle
        draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=outline, width=width)
        draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=outline, width=width)
        
        # Draw corners
        draw.pieslice([x1, y1, x1+2*radius, y1+2*radius], 180, 270, fill=fill, outline=outline)
        draw.pieslice([x2-2*radius, y1, x2, y1+2*radius], 270, 360, fill=fill, outline=outline)
        draw.pieslice([x1, y2-2*radius, x1+2*radius, y2], 90, 180, fill=fill, outline=outline)
        draw.pieslice([x2-2*radius, y2-2*radius, x2, y2], 0, 90, fill=fill, outline=outline)
    
    def draw_arrow(self, draw, start, end, color='#757575'):
        """Draw an arrow from start to end"""
        x1, y1 = start
        x2, y2 = end
        
        # Draw line
        draw.line([x1, y1, x2, y2], fill=color, width=3)
        
        # Draw arrowhead
        if y2 > y1:  # Pointing down
            draw.polygon([
                (x2, y2),
                (x2-10, y2-15),
                (x2+10, y2-15)
            ], fill=color)
    
    def draw_process_box(self, draw, x, y, width, height, text, color, time_text=None):
        """Draw a process box with text"""
        # Draw box
        self.draw_rounded_rectangle(draw, [x, y, x+width, y+height], 10, fill=color)
        
        # Draw text (wrap if needed)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=self.font_normal)
            if bbox[2] - bbox[0] > width - 20:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center text vertically
        text_height = len(lines) * 22
        y_offset = y + (height - text_height) // 2
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=self.font_normal)
            text_width = bbox[2] - bbox[0]
            text_x = x + (width - text_width) // 2
            draw.text((text_x, y_offset), line, fill=self.colors['text'], font=self.font_normal)
            y_offset += 22
        
        # Draw time indicator
        if time_text:
            time_bbox = draw.textbbox((0, 0), time_text, font=self.font_small)
            time_width = time_bbox[2] - time_bbox[0]
            time_x = x + (width - time_width) // 2
            draw.text((time_x, y + height - 25), time_text, fill='#666666', font=self.font_small)
    
    def generate_manual_process_flowchart(self):
        """Generate manual process flowchart"""
        print("   Generating manual process flowchart...")
        
        # Create image
        img = Image.new('RGB', (1000, 1400), color=self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Title
        title = "MANUAL ENROLLMENT PROCESS"
        bbox = draw.textbbox((0, 0), title, font=self.font_title)
        title_width = bbox[2] - bbox[0]
        draw.text((500 - title_width//2, 30), title, fill=self.colors['text'], font=self.font_title)
        
        # Subtitle
        subtitle = "Average Time: 45 minutes per application"
        bbox = draw.textbbox((0, 0), subtitle, font=self.font_heading)
        subtitle_width = bbox[2] - bbox[0]
        draw.text((500 - subtitle_width//2, 75), subtitle, fill='#D32F2F', font=self.font_heading)
        
        # Process steps
        steps = [
            ("Student Submits Documents", "Email with attachments", "~5 min"),
            ("Staff Receives & Downloads", "Manual file organization", "~5 min"),
            ("Document Review", "Visual inspection, verify types", "~10 min"),
            ("Manual Data Entry", "Type info into database", "~12 min"),
            ("Validation & Checking", "Cross-reference requirements", "~8 min"),
            ("Decision & Routing", "Determine next steps", "~5 min"),
            ("Send Notifications", "Draft and send emails", "~5 min")
        ]
        
        y_pos = 140
        box_width = 400
        box_height = 120
        x_center = 500 - box_width // 2
        
        for i, (title, subtitle, time) in enumerate(steps):
            # Draw step box
            color = self.colors['manual_primary'] if i % 2 == 0 else self.colors['manual_secondary']
            self.draw_process_box(draw, x_center, y_pos, box_width, box_height, 
                                 f"{title}\n{subtitle}", color, time)
            
            # Draw arrow to next step
            if i < len(steps) - 1:
                arrow_start = (500, y_pos + box_height)
                arrow_end = (500, y_pos + box_height + 40)
                self.draw_arrow(draw, arrow_start, arrow_end, self.colors['arrow'])
            
            y_pos += box_height + 40
        
        # Issues section
        y_pos += 20
        issues_text = [
            "❌ Slow and tedious",
            "❌ High error rate (12%)",
            "❌ Staff burnout",
            "❌ Inconsistent quality"
        ]
        
        for issue in issues_text:
            draw.text((100, y_pos), issue, fill='#D32F2F', font=self.font_normal)
            y_pos += 30
        
        # Save
        filepath = self.output_dir / 'manual_process_flowchart.png'
        img.save(filepath)
        print(f"      ✓ Saved: {filepath}")
    
    def generate_automated_process_flowchart(self):
        """Generate automated process flowchart"""
        print("   Generating automated process flowchart...")
        
        # Create image
        img = Image.new('RGB', (1000, 1500), color=self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Title
        title = "AUTOMATED RPA/AI PROCESS"
        bbox = draw.textbbox((0, 0), title, font=self.font_title)
        title_width = bbox[2] - bbox[0]
        draw.text((500 - title_width//2, 30), title, fill=self.colors['text'], font=self.font_title)
        
        # Subtitle
        subtitle = "Average Time: 16 minutes per application (65% reduction)"
        bbox = draw.textbbox((0, 0), subtitle, font=self.font_heading)
        subtitle_width = bbox[2] - bbox[0]
        draw.text((500 - subtitle_width//2, 75), subtitle, fill='#388E3C', font=self.font_heading)
        
        # Process steps
        steps = [
            ("Student Uploads Documents", "Web portal submission", "~1 min", True),
            ("OCR Text Extraction", "🤖 Automated image processing", "~3 min", True),
            ("AI Document Classification", "🤖 ML-based type detection", "~2 min", True),
            ("Automated Validation", "🤖 Rule-based checking", "~3 min", True),
            ("Smart Workflow Routing", "🤖 Algorithm assignment", "~1 min", True),
            ("Automated Notifications", "🤖 Email generation & sending", "~1 min", True),
            ("Staff Oversight Review", "👤 Human verification", "~6 min", False)
        ]
        
        y_pos = 140
        box_width = 450
        box_height = 110
        x_center = 500 - box_width // 2
        
        for i, (title, subtitle, time, is_automated) in enumerate(steps):
            # Draw step box
            if is_automated:
                color = self.colors['automated_primary'] if i % 2 == 0 else self.colors['automated_secondary']
            else:
                color = '#BBDEFB'  # Different color for human steps
            
            self.draw_process_box(draw, x_center, y_pos, box_width, box_height, 
                                 f"{title}\n{subtitle}", color, time)
            
            # Draw arrow to next step
            if i < len(steps) - 1:
                arrow_start = (500, y_pos + box_height)
                arrow_end = (500, y_pos + box_height + 35)
                self.draw_arrow(draw, arrow_start, arrow_end, self.colors['arrow'])
            
            y_pos += box_height + 35
        
        # Benefits section
        y_pos += 30
        draw.rectangle([50, y_pos, 950, y_pos + 200], fill='#E8F5E9', outline='#388E3C', width=3)
        
        y_pos += 15
        draw.text((500 - 80, y_pos), "✅ BENEFITS", fill='#1B5E20', font=self.font_heading)
        
        y_pos += 40
        benefits = [
            "✓ 65% faster processing",
            "✓ 78% fewer errors",
            "✓ 85% automation rate",
            "✓ Consistent quality"
        ]
        
        col1_x = 100
        col2_x = 550
        for i, benefit in enumerate(benefits):
            x = col1_x if i < 2 else col2_x
            y = y_pos if i % 2 == 0 else y_pos + 40
            draw.text((x, y), benefit, fill='#1B5E20', font=self.font_normal)
        
        # Save
        filepath = self.output_dir / 'automated_process_flowchart.png'
        img.save(filepath)
        print(f"      ✓ Saved: {filepath}")
    
    def generate_comparison_diagram(self):
        """Generate side-by-side comparison"""
        print("   Generating comparison diagram...")
        
        # Create image
        img = Image.new('RGB', (1400, 800), color=self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Title
        title = "BEFORE vs AFTER COMPARISON"
        bbox = draw.textbbox((0, 0), title, font=self.font_title)
        title_width = bbox[2] - bbox[0]
        draw.text((700 - title_width//2, 30), title, fill=self.colors['text'], font=self.font_title)
        
        # BEFORE side
        draw.text((200, 100), "BEFORE: Manual Process", fill='#D32F2F', font=self.font_heading)
        
        metrics_before = [
            ("⏱️ Time per application", "45 minutes"),
            ("👥 Staff required", "8 people"),
            ("❌ Error rate", "12%"),
            ("💰 Monthly cost", "$6,300"),
            ("📊 Processing capacity", "300 apps/month"),
            ("😞 Staff satisfaction", "3.2 / 5.0")
        ]
        
        y_pos = 160
        for label, value in metrics_before:
            # Label
            draw.text((80, y_pos), label, fill=self.colors['text'], font=self.font_small)
            y_pos += 25
            # Value box
            self.draw_rounded_rectangle(draw, [80, y_pos, 430, y_pos + 50], 8, 
                                       fill=self.colors['manual_secondary'], 
                                       outline=self.colors['manual_primary'], width=2)
            bbox = draw.textbbox((0, 0), value, font=self.font_heading)
            text_width = bbox[2] - bbox[0]
            draw.text((255 - text_width//2, y_pos + 10), value, fill=self.colors['text'], font=self.font_heading)
            y_pos += 70
        
        # AFTER side
        draw.text((1000, 100), "AFTER: RPA/AI Automation", fill='#388E3C', font=self.font_heading)
        
        metrics_after = [
            ("⏱️ Time per application", "16 minutes"),
            ("👥 Staff required", "3 people"),
            ("✅ Error rate", "2.6%"),
            ("💰 Monthly cost", "$2,240"),
            ("📊 Processing capacity", "800 apps/month"),
            ("😊 Staff satisfaction", "4.5 / 5.0")
        ]
        
        y_pos = 160
        for label, value in metrics_after:
            # Label
            draw.text((830, y_pos), label, fill=self.colors['text'], font=self.font_small)
            y_pos += 25
            # Value box
            self.draw_rounded_rectangle(draw, [830, y_pos, 1180, y_pos + 50], 8, 
                                       fill=self.colors['automated_secondary'], 
                                       outline=self.colors['automated_primary'], width=2)
            bbox = draw.textbbox((0, 0), value, font=self.font_heading)
            text_width = bbox[2] - bbox[0]
            draw.text((1005 - text_width//2, y_pos + 10), value, fill=self.colors['text'], font=self.font_heading)
            y_pos += 70
        
        # Arrow in middle
        self.draw_arrow(draw, (650, 400), (750, 400), '#FFB300')
        draw.text((670, 350), "TRANSFORM", fill='#FF8F00', font=self.font_heading)
        
        # Save
        filepath = self.output_dir / 'before_after_comparison.png'
        img.save(filepath)
        print(f"      ✓ Saved: {filepath}")
    
    def generate_all_flowcharts(self):
        """Generate all flowcharts"""
        print("\n🎨 Generating Process Flowcharts & Visualizations...")
        print("-" * 70)
        
        self.generate_manual_process_flowchart()
        self.generate_automated_process_flowchart()
        self.generate_comparison_diagram()
        
        print("\n✅ All visualizations generated successfully!")
        print(f"📁 Location: {self.output_dir.absolute()}\n")


def main():
    """Generate all flowcharts"""
    generator = FlowchartGenerator()
    generator.generate_all_flowcharts()


if __name__ == "__main__":
    main()

