"""Certificate generator for Typing Speed Test application."""

import os
from datetime import datetime
from pathlib import Path
import random
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, 
    Table, TableStyle, BaseDocTemplate, Frame, PageTemplate
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from config import RESOURCES_DIR, USER_LEVELS

# Define certificate directory
CERTIFICATE_DIR = RESOURCES_DIR / "certificates"
CERTIFICATE_DIR.mkdir(exist_ok=True)

# Define certificate templates
CERTIFICATE_TEMPLATES = [
    {
        "name": "Modern",
        "border_color": colors.lightblue,
        "accent_color": colors.blue,
        "text_color": colors.darkblue,
        "font": "Helvetica"
    },
    {
        "name": "Professional",
        "border_color": colors.lightgrey,
        "accent_color": colors.dimgrey,
        "text_color": colors.black,
        "font": "Times-Roman"
    },
    {
        "name": "Vibrant",
        "border_color": colors.lightgreen,
        "accent_color": colors.green,
        "text_color": colors.darkgreen,
        "font": "Helvetica-Bold"
    }
]

class CertificateGenerator:
    """Generates certificates of achievement for typing speed tests."""
    
    def __init__(self):
        """Initialize the certificate generator."""
        # Create certificate directory if it doesn't exist
        CERTIFICATE_DIR.mkdir(exist_ok=True)
    
    def generate_certificate(self, certificate_data, template_idx=None):
        """Generate a certificate PDF and return the path."""
        # Select template (randomly if not specified)
        if template_idx is None:
            template_idx = random.randint(0, len(CERTIFICATE_TEMPLATES) - 1)
        template = CERTIFICATE_TEMPLATES[template_idx]
        
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = ''.join(c if c.isalnum() else '_' for c in certificate_data["full_name"])
        filename = f"typing_certificate_{sanitized_name}_{timestamp}.pdf"
        output_path = CERTIFICATE_DIR / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=landscape(letter),
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontName=template["font"],
            fontSize=36,
            textColor=template["text_color"],
            alignment=1,  # Center
            spaceAfter=20
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontName=template["font"],
            fontSize=24,
            textColor=template["text_color"],
            alignment=1,
            spaceAfter=30
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontName=template["font"],
            fontSize=12,
            textColor=template["text_color"],
            alignment=1,
            spaceAfter=12
        )
        
        detail_style = ParagraphStyle(
            'Detail',
            parent=styles['Normal'],
            fontName=template["font"],
            fontSize=16,
            textColor=template["accent_color"],
            alignment=1,
            spaceAfter=6
        )
        
        # Get skill level info
        level = certificate_data["level"]
        level_color = USER_LEVELS[level]["color"]
        
        # Build certificate content
        elements = []
        
        # Certificate title
        elements.append(Paragraph("CERTIFICATE OF ACHIEVEMENT", title_style))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Recipient name
        elements.append(Paragraph("This is to certify that", normal_style))
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph(f"<b>{certificate_data['full_name']}</b>", subtitle_style))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Achievement text
        elements.append(Paragraph(
            f"has achieved a typing speed of <b>{certificate_data['wpm']} WPM</b> "
            f"with <b>{certificate_data['accuracy']}</b> accuracy "
            f"on the text \"{certificate_data['text_title']}\" "
            f"in the {certificate_data['text_genre']} category.",
            detail_style
        ))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Skill level
        elements.append(Paragraph(f"Typing Skill Level: <b>{level}</b>", detail_style))
        elements.append(Spacer(1, 0.5 * inch))
        
        # Date
        elements.append(Paragraph(f"Issued on {certificate_data['date']}", normal_style))
        
        # Build the PDF
        self._draw_certificate_border(doc, template)
        doc.build(elements)
        
        return str(output_path)
    
    def _draw_certificate_border(self, doc, template):
        """Draw a decorative border around the certificate."""
        # Create a canvas for drawing
        width, height = landscape(letter)
        
        def draw_border(canvas, doc):
            # Draw fancy border
            canvas.saveState()
            
            # Outer border
            canvas.setStrokeColor(template["border_color"])
            canvas.setLineWidth(3)
            canvas.rect(
                inch,
                inch,
                width - 2 * inch,
                height - 2 * inch
            )
            
            # Inner border
            canvas.setStrokeColor(template["accent_color"])
            canvas.setLineWidth(1)
            canvas.rect(
                1.25 * inch,
                1.25 * inch,
                width - 2.5 * inch,
                height - 2.5 * inch
            )
            
            # Corner decorations
            canvas.setFillColor(template["accent_color"])
            corner_size = 0.25 * inch
            
            # Top-left
            canvas.rect(
                inch,
                height - inch - corner_size,
                corner_size,
                corner_size,
                stroke=0,
                fill=1
            )
            
            # Top-right
            canvas.rect(
                width - inch - corner_size,
                height - inch - corner_size,
                corner_size,
                corner_size,
                stroke=0,
                fill=1
            )
            
            # Bottom-left
            canvas.rect(
                inch,
                inch,
                corner_size,
                corner_size,
                stroke=0,
                fill=1
            )
            
            # Bottom-right
            canvas.rect(
                width - inch - corner_size,
                inch,
                corner_size,
                corner_size,
                stroke=0,
                fill=1
            )
            
            # Add "Typing Speed Test Pro" as a watermark/ribbon at the bottom
            canvas.setFillColor(template["accent_color"])
            canvas.setFont(template["font"], 10)
            canvas.drawCentredString(
                width / 2,
                0.75 * inch,
                "Typing Speed Test Pro - Certificate of Achievement"
            )
            
            # Add a seal/stamp effect
            canvas.saveState()
            canvas.translate(width - 2.5 * inch, 2.25 * inch)
            canvas.setStrokeColor(template["accent_color"])
            canvas.setFillColor(colors.white)
            canvas.setLineWidth(2)
            canvas.circle(0, 0, 0.5 * inch, stroke=1, fill=0)
            canvas.circle(0, 0, 0.4 * inch, stroke=1, fill=0)
            canvas.setFont(template["font"], 12)
            canvas.setFillColor(template["text_color"])
            canvas.drawCentredString(0, -4, "CERTIFIED")
            canvas.restoreState()
            
            canvas.restoreState()
        
        # Add the border drawing function
        doc.beforePage = draw_border
