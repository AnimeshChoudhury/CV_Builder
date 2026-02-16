"""
Professional CV Builder for Researchers with Profile Image Support
Generates a clean, professional PDF CV with research publications
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import json
import os
from PIL import Image as PILImage


class CVData:
    """Structure to hold CV data"""
    
    def __init__(self):
        self.personal_info = {}
        self.summary = ""
        self.education = []
        self.experience = []
        self.publications = []
        self.conference_papers = []
        self.skills = {}
        self.awards = []
        self.service = []
        self.languages = {}

    def save_to_json(self, filename="cv_data.json"):
        """Save CV data to JSON file for easy editing"""
        data = {
            "personal_info": self.personal_info,
            "summary": self.summary,
            "education": self.education,
            "experience": self.experience,
            "publications": self.publications,
            "conference_papers": getattr(self, 'conference_papers', []),
            "skills": self.skills,
            "awards": self.awards,
            "service": self.service,
            "languages": getattr(self, 'languages', {})
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"CV data saved to {filename}")
    
    def load_from_json(self, filename="cv_data.json"):
        """Load CV data from JSON file"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.personal_info = data.get("personal_info", {})
            self.summary = data.get("summary", "")
            self.education = data.get("education", [])
            self.experience = data.get("experience", [])
            self.publications = data.get("publications", [])
            self.conference_papers = data.get("conference_papers", [])
            self.skills = data.get("skills", {})
            self.awards = data.get("awards", [])
            self.service = data.get("service", [])
            self.languages = data.get("languages", {})
            print(f"CV data loaded from {filename}")
        else:
            print(f"File {filename} not found. Using default data.")


class CVBuilder:
    """Builds professional PDF CV with optional profile image"""
    
    def __init__(self, cv_data, include_image=True):
        self.cv_data = cv_data
        self.include_image = include_image
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Name style - large and bold
        self.styles.add(ParagraphStyle(
            name='CVName',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Title style - medium size
        self.styles.add(ParagraphStyle(
            name='CVTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#555555'),
            spaceAfter=8,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
        
        # Contact info style - compact
        self.styles.add(ParagraphStyle(
            name='CVContact',
            parent=self.styles['Normal'],
            fontSize=8.5,
            textColor=colors.HexColor('#666666'),
            spaceAfter=2,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=11
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='CVSectionHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold',
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CVBody',
            parent=self.styles['Normal'],
            fontSize=9.5,
            textColor=colors.HexColor('#333333'),
            spaceAfter=5,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=12
        ))
        
        # Publication style
        self.styles.add(ParagraphStyle(
            name='CVPublication',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            spaceAfter=7,
            leftIndent=0,
            fontName='Helvetica',
            leading=11
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='CVJobTitle',
            parent=self.styles['Normal'],
            fontSize=10.5,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))
        
        # Organization style
        self.styles.add(ParagraphStyle(
            name='CVOrganization',
            parent=self.styles['Normal'],
            fontSize=9.5,
            textColor=colors.HexColor('#666666'),
            spaceAfter=5,
            fontName='Helvetica-Oblique'
        ))
    
    def _process_profile_image(self, image_path, max_size=1.2):
        """Process and resize profile image"""
        if not image_path or not os.path.exists(image_path):
            return None
        
        try:
            # Open and process image
            img = PILImage.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate dimensions to maintain aspect ratio
            aspect = img.width / img.height
            if aspect > 1:
                width = max_size * inch
                height = width / aspect
            else:
                height = max_size * inch
                width = height * aspect
            
            return Image(image_path, width=width, height=height)
        except Exception as e:
            print(f"Warning: Could not load profile image: {e}")
            return None
    
    def _add_header(self, story):
        """Add CV header with name, contact info, and optional profile image"""
        
        profile_image = None
        image_path = self.cv_data.personal_info.get('profile_image', '')
        
        if self.include_image and image_path:
            profile_image = self._process_profile_image(image_path)
        
        if profile_image:
            # Create header table with image
            header_data = []
            
            # Name and title column
            name_title_text = f"<font size=22><b>{self.cv_data.personal_info['name']}</b></font><br/>"
            name_title_text += f"<font size=11 color='#555555'>{self.cv_data.personal_info.get('title', '')}</font>"
            name_title_para = Paragraph(name_title_text, self.styles['Normal'])
            
            # Contact info
            contact_lines = []
            if self.cv_data.personal_info.get('email'):
                contact_lines.append(f"✉ {self.cv_data.personal_info['email']}")
            if self.cv_data.personal_info.get('phone'):
                contact_lines.append(f"☎ {self.cv_data.personal_info['phone']}")
            if self.cv_data.personal_info.get('linkedin'):
                contact_lines.append(f"💼 {self.cv_data.personal_info['linkedin'].replace('https://', '')}")
            if self.cv_data.personal_info.get('github'):
                contact_lines.append(f"⚡ {self.cv_data.personal_info['github'].replace('https://', '')}")
            if self.cv_data.personal_info.get('scholar'):
                scholar_url = self.cv_data.personal_info['scholar'].replace('https://', '').replace('http://', '')
                contact_lines.append(f"📚 {scholar_url}")
            
            contact_text = "<br/>".join(contact_lines)
            contact_para = Paragraph(f"<font size=8.5 color='#666666'>{contact_text}</font>", self.styles['Normal'])
            
            # Build header table
            header_data = [[profile_image, [name_title_para, Spacer(1, 0.05*inch), contact_para]]]
            
            header_table = Table(header_data, colWidths=[1.4*inch, 5.6*inch])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('LEFTPADDING', (1, 0), (1, 0), 0),
            ]))
            story.append(header_table)
            
        else:
            # Header without image
            name = Paragraph(self.cv_data.personal_info['name'], self.styles['CVName'])
            story.append(name)
            
            title = Paragraph(self.cv_data.personal_info.get('title', ''), self.styles['CVTitle'])
            story.append(title)
            
            # Contact information - compact format
            contact_parts = []
            if self.cv_data.personal_info.get('email'):
                contact_parts.append(f"✉ {self.cv_data.personal_info['email']}")
            if self.cv_data.personal_info.get('phone'):
                contact_parts.append(f"☎ {self.cv_data.personal_info['phone']}")
            if self.cv_data.personal_info.get('linkedin'):
                contact_parts.append(f"💼 LinkedIn")
            if self.cv_data.personal_info.get('github'):
                contact_parts.append(f"⚡ GitHub")
            
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['CVContact'])
            story.append(contact)
        
        # Divider line
        story.append(Spacer(1, 0.08*inch))
        line_table = Table([['']], colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.5, colors.HexColor('#2c3e50')),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.1*inch))
    
    def _add_section_header(self, story, title):
        """Add a section header with a line underneath"""
        heading = Paragraph(f"<b>{title.upper()}</b>", self.styles['CVSectionHeading'])
        story.append(heading)
        
        # Add a horizontal line
        line_table = Table([['']], colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#2c3e50')),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.08*inch))
    
    def _add_summary(self, story):
        """Add professional summary"""
        if not self.cv_data.summary:
            return
        self._add_section_header(story, "Professional Summary")
        summary = Paragraph(self.cv_data.summary.strip(), self.styles['CVBody'])
        story.append(summary)
        story.append(Spacer(1, 0.12*inch))
    
    def _add_education(self, story):
        """Add education section"""
        if not self.cv_data.education:
            return
        self._add_section_header(story, "Education")
        
        for edu in self.cv_data.education:
            # Degree and year on same line
            degree_text = f"<b>{edu['degree']}</b>"
            if edu.get('year'):
                degree_text += f" <font color='#666666'>({edu['year']})</font>"
            degree = Paragraph(degree_text, self.styles['CVJobTitle'])
            story.append(degree)
            
            # Institution and location
            inst_text = edu['institution']
            if edu.get('location'):
                inst_text += f", {edu['location']}"
            institution = Paragraph(inst_text, self.styles['CVOrganization'])
            story.append(institution)
            
            # Thesis if available
            if edu.get('thesis') and edu['thesis']:
                thesis_text = f"<i>Thesis:</i> {edu['thesis']}"
                thesis = Paragraph(thesis_text, self.styles['CVBody'])
                story.append(thesis)
            
            story.append(Spacer(1, 0.1*inch))
    
    def _add_experience(self, story):
        """Add work experience section"""
        if not self.cv_data.experience:
            return
        self._add_section_header(story, "Work Experience")
        
        for exp in self.cv_data.experience:
            # Position title
            position = Paragraph(f"<b>{exp['position']}</b>", self.styles['CVJobTitle'])
            story.append(position)
            
            # Organization and period
            org_text = f"{exp['organization']}"
            if exp.get('location'):
                org_text += f", {exp['location']}"
            org_text += f" | <font color='#444444'>{exp['period']}</font>"
            organization = Paragraph(org_text, self.styles['CVOrganization'])
            story.append(organization)
            
            # Responsibilities
            if exp.get('responsibilities'):
                for resp in exp['responsibilities']:
                    bullet = Paragraph(f"• {resp}", self.styles['CVBody'])
                    story.append(bullet)
            
            story.append(Spacer(1, 0.1*inch))
    
    def _add_publications(self, story):
        """Add publications section"""
        if not self.cv_data.publications:
            return
        self._add_section_header(story, "Selected Publications")
        
        # Sort by year (most recent first)
        sorted_pubs = sorted(self.cv_data.publications, 
                           key=lambda x: x.get('year', 0), 
                           reverse=True)
        
        for i, pub in enumerate(sorted_pubs, 1):
            # Format: [1] Authors. "Title." Venue, Year. [Citations: X]
            pub_text = f"[{i}] {pub.get('authors', 'Unknown')}. <b>\"{pub.get('title', 'Untitled')}\"</b> "
            pub_text += f"<i>{pub.get('venue', 'Unknown Venue')}</i>, {pub.get('year', 'N/A')}."
            
            if pub.get('doi'):
                pub_text += f" DOI: {pub['doi']}"
            elif pub.get('citations', 0) > 0:
                pub_text += f" [Citations: {pub['citations']}]"
            
            publication = Paragraph(pub_text, self.styles['CVPublication'])
            story.append(publication)
        
        story.append(Spacer(1, 0.12*inch))
    
    def _add_conference_papers(self, story):
        """Add conference papers section"""
        if not self.cv_data.conference_papers:
            return
        self._add_section_header(story, "Conference Papers & Proceedings")
        
        for i, paper in enumerate(self.cv_data.conference_papers, 1):
            paper_text = f"[{i}] <b>\"{paper.get('title', 'Untitled')}\"</b> "
            paper_text += f"<i>{paper.get('venue', 'Unknown Venue')}</i>, {paper.get('year', 'N/A')}."
            
            if paper.get('url'):
                paper_text += f" URL: {paper['url']}"
            
            conf_paper = Paragraph(paper_text, self.styles['CVPublication'])
            story.append(conf_paper)
        
        story.append(Spacer(1, 0.12*inch))
    
    def _add_skills(self, story):
        """Add skills section"""
        if not self.cv_data.skills:
            return
        self._add_section_header(story, "Technical Skills & Expertise")
        
        for category, skills_list in self.cv_data.skills.items():
            if isinstance(skills_list, list):
                skills_text = f"<b>{category}:</b> {', '.join(skills_list)}"
            else:
                skills_text = f"<b>{category}:</b> {skills_list}"
            skills = Paragraph(skills_text, self.styles['CVBody'])
            story.append(skills)
        
        story.append(Spacer(1, 0.12*inch))
    
    def _add_languages(self, story):
        """Add languages section"""
        if not self.cv_data.languages:
            return
        self._add_section_header(story, "Languages")
        
        lang_text = ""
        for lang, level in self.cv_data.languages.items():
            lang_text += f"<b>{lang}:</b> {level} | "
        lang_text = lang_text.rstrip(" | ")
        
        languages = Paragraph(lang_text, self.styles['CVBody'])
        story.append(languages)
        story.append(Spacer(1, 0.12*inch))
    
    def _add_awards(self, story):
        """Add awards and honors section"""
        if not self.cv_data.awards:
            return
        self._add_section_header(story, "Awards & Recognition")
        
        for award in self.cv_data.awards:
            award_text = f"• <b>{award.get('name', 'Award')}</b>"
            if award.get('organization'):
                award_text += f", {award['organization']}"
            if award.get('year'):
                award_text += f", {award['year']}"
            award_para = Paragraph(award_text, self.styles['CVBody'])
            story.append(award_para)
        
        story.append(Spacer(1, 0.12*inch))
    
    def _add_service(self, story):
        """Add professional service section"""
        if not self.cv_data.service:
            return
        self._add_section_header(story, "Professional Development & Service")
        
        for service in self.cv_data.service:
            service_text = f"• {service}"
            service_para = Paragraph(service_text, self.styles['CVBody'])
            story.append(service_para)
    
    def build_cv(self, filename="professional_cv.pdf"):
        """Build the complete CV PDF"""
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=0.7*inch,
            rightMargin=0.7*inch,
            topMargin=0.7*inch,
            bottomMargin=0.7*inch
        )
        
        story = []
        
        # Add all sections
        self._add_header(story)
        self._add_summary(story)
        self._add_education(story)
        self._add_experience(story)
        self._add_publications(story)
        self._add_conference_papers(story)
        self._add_skills(story)
        self._add_languages(story)
        self._add_awards(story)
        self._add_service(story)
        
        # Add footer
        story.append(Spacer(1, 0.2*inch))
        footer_text = f"<i>Last updated: {datetime.now().strftime('%B %Y')}</i>"
        footer = Paragraph(footer_text, self.styles['CVContact'])
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        print(f"\n✓ CV successfully generated: {filename}")
        return filename


def main():
    """Main function to generate CV"""
    print("=" * 70)
    print("Professional CV Builder for Researchers (with Profile Image)")
    print("=" * 70)
    
    # Create CV data instance
    cv_data = CVData()
    
    # Check for custom JSON file first
    json_file = "animesh_cv_data.json"
    if not os.path.exists(json_file):
        json_file = "cv_data.json"
    
    # Load data
    if os.path.exists(json_file):
        print(f"\nLoading data from {json_file}...")
        cv_data.load_from_json(json_file)
    else:
        print("\nNo CV data file found. Please create one first.")
        return
    
    # Ask about profile image
    include_image = True
    profile_image_path = cv_data.personal_info.get('profile_image', '')
    
    if profile_image_path and os.path.exists(profile_image_path):
        print(f"\nProfile image found: {profile_image_path}")
        choice = input("Include profile image in CV? (y/n, default=y): ").lower()
        if choice == 'n':
            include_image = False
    else:
        include_image = False
        if profile_image_path:
            print(f"\nWarning: Profile image path specified but file not found: {profile_image_path}")
    
    # Build CV
    print("\nGenerating CV PDF...")
    builder = CVBuilder(cv_data, include_image=include_image)
    output_file = builder.build_cv("Animesh_Choudhury_CV.pdf")
    
    print("\n" + "=" * 70)
    print("✓ CV Generation Complete!")
    print("=" * 70)
    print(f"\nOutput file: {output_file}")
    print(f"Data file: {json_file}")
    print("\nTo add a profile image:")
    print("  1. Place your image file in the same directory")
    print("  2. Edit the JSON file and set: 'profile_image': 'your_photo.jpg'")
    print("  3. Run this script again")
    print("\nTip: For circular profile images, crop your photo to a square first.")
    

if __name__ == "__main__":
    main()
