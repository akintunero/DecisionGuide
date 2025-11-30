"""PDF export service for decision results."""
from typing import Optional
from datetime import datetime
from pathlib import Path
from models.decision_tree import DecisionResult
from utils.config import Config

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFService:
    """Service for generating PDF reports from decision results."""
    
    def __init__(self):
        """Initialize PDF service."""
        self.available = REPORTLAB_AVAILABLE and Config.ENABLE_PDF_EXPORT
        if not REPORTLAB_AVAILABLE:
            print("Warning: reportlab not installed. PDF export disabled.")
    
    def generate_pdf(
        self, 
        result: DecisionResult, 
        tree_name: str,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Generate PDF report from decision result.
        
        Args:
            result: DecisionResult object
            tree_name: Name of the decision tree used
            output_path: Optional output path (defaults to data directory)
            
        Returns:
            Path to generated PDF or None if generation failed
        """
        if not self.available:
            return None
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"decision_report_{timestamp}.pdf"
            output_path = Config.DATA_DIR / filename
        
        try:
            doc = SimpleDocTemplate(str(output_path), pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#1f77b4',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph("DecisionGuide Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata
            meta_style = ParagraphStyle(
                'Meta',
                parent=styles['Normal'],
                fontSize=10,
                textColor='#666666'
            )
            story.append(Paragraph(f"<b>Tree:</b> {tree_name}", meta_style))
            story.append(Paragraph(
                f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                meta_style
            ))
            story.append(Spacer(1, 0.3*inch))
            
            # Decision
            if result.decision:
                decision_style = ParagraphStyle(
                    'Decision',
                    parent=styles['Heading2'],
                    fontSize=16,
                    textColor='#2ca02c',
                    spaceAfter=12
                )
                story.append(Paragraph("<b>Decision:</b>", decision_style))
                story.append(Paragraph(result.decision, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Explanation
            if result.explanation:
                story.append(Paragraph("<b>Explanation:</b>", styles['Heading3']))
                story.append(Paragraph(result.explanation, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Path
            if result.path:
                story.append(Paragraph("<b>Decision Path:</b>", styles['Heading3']))
                for step in result.path:
                    story.append(Paragraph(f"• {step}", styles['Normal']))
            
            doc.build(story)
            return output_path
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None

