"""
Professional CV Builder for Researchers - Redesigned with Tight Layout
Generates a clean, professional PDF CV with research publications
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
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
    """Builds professional PDF CV with optional profile image - Tight Layout"""
    
    def __init__(self, cv_data, include_image=True):
        self.cv_data = cv_data
        self.include_image = include_image
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles with tight spacing"""
        
        # Define color scheme
        primary_color = colors.HexColor('#1a5490')  # Professional blue
        secondary_color = colors.HexColor('#2c3e50')  # Dark gray
        text_color = colors.HexColor('#333333')  # Main text
        light_gray = colors.HexColor('#666666')  # Light text
        
        # Name style - bold and prominent
        self.styles.add(ParagraphStyle(
            name='CVName',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=secondary_color,
            spaceAfter=2,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=22
        ))
        
        # Title style - professional subtitle
        self.styles.add(ParagraphStyle(
            name='CVTitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=light_gray,
            spaceAfter=6,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=12
        ))
        
        # Contact info style - compact
        self.styles.add(ParagraphStyle(
            name='CVContact',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=light_gray,
            spaceAfter=1,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=10
        ))
        
        # Section heading style - bold with line
        self.styles.add(ParagraphStyle(
            name='CVSectionHeading',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=primary_color,
            spaceAfter=4,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            leading=13
        ))
        
        # Body text style - compact
        self.styles.add(ParagraphStyle(
            name='CVBody',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=text_color,
            spaceAfter=3,
            spaceBefore=0,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=11
        ))
        
        # Publication style - tight
        self.styles.add(ParagraphStyle(
            name='CVPublication',
            parent=self.styles['Normal'],
            fontSize=8.5,
            textColor=text_color,
            spaceAfter=4,
            spaceBefore=0,
            leftIndent=0,
            fontName='Helvetica',
            leading=10.5,
            alignment=TA_JUSTIFY
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='CVJobTitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=secondary_color,
            spaceAfter=1,
            spaceBefore=0,
            fontName='Helvetica-Bold',
            leading=12
        ))
        
        # Organization style
        self.styles.add(ParagraphStyle(
            name='CVOrganization',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=light_gray,
            spaceAfter=3,
            spaceBefore=0,
            fontName='Helvetica-Oblique',
            leading=11
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='CVBullet',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=text_color,
            spaceAfter=2,
            spaceBefore=0,
            leftIndent=12,
            fontName='Helvetica',
            leading=11,
            bulletIndent=0
        ))
    
    def _process_profile_image(self, image_path, size=1.0):
        """Process and resize profile image to be circular"""
        if not image_path or not os.path.exists(image_path):
            return None
        
        try:
            # Open and process image
            img = PILImage.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Make it square by cropping
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            img = img.crop((left, top, right, bottom))
            
            # Calculate dimensions
            img_size = size * inch
            
            return Image(image_path, width=img_size, height=img_size)
        except Exception as e:
            print(f"Warning: Could not load profile image: {e}")
            return None
    
    def _create_clickable_icon(self, icon_file, link_url, icon_size=0.18):
        """Create a truly clickable icon using Image with link annotation"""
        try:
            if not os.path.exists(icon_file):
                print(f"Warning: Icon file not found: {icon_file}")
                return None
            
            # Create image
            from reportlab.platypus.flowables import Image as FlowImage
            
            class ClickableImage(FlowImage):
                """Custom Image class that supports hyperlinks"""
                def __init__(self, filename, width, height, hyperlink=None):
                    FlowImage.__init__(self, filename, width=width, height=height)
                    self.hyperlink = hyperlink
                
                def draw(self):
                    # Draw the image
                    FlowImage.draw(self)
                    # Add clickable link annotation if hyperlink is provided
                    if self.hyperlink:
                        # Add link annotation to the canvas
                        self.canv.linkURL(
                            self.hyperlink,
                            (0, 0, self.drawWidth, self.drawHeight),
                            relative=1
                        )
            
            if link_url:
                img = ClickableImage(icon_file, icon_size*inch, icon_size*inch, hyperlink=link_url)
            else:
                img = Image(icon_file, width=icon_size*inch, height=icon_size*inch)
            
            img.hAlign = 'LEFT'
            return img
            
        except Exception as e:
            print(f"Warning: Could not create clickable icon {icon_file}: {e}")
            return None
    
    def _add_header(self, story):
        """Add CV header with name, contact info, and clickable logo icons"""
        
        profile_image = None
        image_path = self.cv_data.personal_info.get('profile_image', '')
        
        if self.include_image and image_path:
            profile_image = self._process_profile_image(image_path, size=1.1)
        
        if profile_image:
            # Create two-column layout: image on left, info on right
            
            # Build info column
            info_elements = []
            
            # Name
            name_para = Paragraph(self.cv_data.personal_info['name'], self.styles['CVName'])
            info_elements.append(name_para)
            
            # Title
            if self.cv_data.personal_info.get('title'):
                title_para = Paragraph(self.cv_data.personal_info['title'], self.styles['CVTitle'])
                info_elements.append(title_para)
            
            # Contact icons in one line
            icon_row = []
            
            # Email icon
            if self.cv_data.personal_info.get('email'):
                email = self.cv_data.personal_info['email']
                email_icon = self._create_clickable_icon('images/email.png', f'mailto:{email}')
                if email_icon:
                    icon_row.append(email_icon)
            
            # Phone icon - link to WhatsApp
            if self.cv_data.personal_info.get('phone'):
                phone = self.cv_data.personal_info['phone']
                # Remove spaces and special characters for WhatsApp link
                phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                whatsapp_url = f'https://wa.me/{phone_clean}'
                phone_icon = self._create_clickable_icon('images/phone.png', whatsapp_url)
                if phone_icon:
                    icon_row.append(phone_icon)
            
            # LinkedIn icon
            if self.cv_data.personal_info.get('linkedin'):
                linkedin_url = self.cv_data.personal_info['linkedin']
                linkedin_icon = self._create_clickable_icon('images/linkedin.png', linkedin_url)
                if linkedin_icon:
                    icon_row.append(linkedin_icon)
            
            # GitHub icon
            if self.cv_data.personal_info.get('github'):
                github_url = self.cv_data.personal_info['github']
                github_icon = self._create_clickable_icon('images/github.png', github_url)
                if github_icon:
                    icon_row.append(github_icon)
            
            # Google Scholar icon
            if self.cv_data.personal_info.get('google_scholar'):
                scholar_url = self.cv_data.personal_info['google_scholar']
                scholar_icon = self._create_clickable_icon('images/google_scholar.png', scholar_url)
                if scholar_icon:
                    icon_row.append(scholar_icon)
            
            # Scholar/ResearchGate icon
            if self.cv_data.personal_info.get('scholar'):
                scholar_url = self.cv_data.personal_info['scholar']
                if not scholar_url.startswith('http'):
                    scholar_url = 'https://' + scholar_url
                # Try scholar.png first, then researchgate.png
                rg_icon = self._create_clickable_icon('images/scholar.png', scholar_url)
                if not rg_icon:
                    rg_icon = self._create_clickable_icon('images/researchgate.png', scholar_url)
                if rg_icon:
                    icon_row.append(rg_icon)
            
            # Create icon table if we have icons
            if icon_row:
                # Add small spacing between icons
                icon_table_data = []
                for i, icon in enumerate(icon_row):
                    icon_table_data.append(icon)
                    if i < len(icon_row) - 1:
                        icon_table_data.append(Spacer(0.18*inch, 0.18*inch))
                
                # Create horizontal layout for icons
                num_cols = len(icon_table_data)
                col_widths = []
                for i, item in enumerate(icon_table_data):
                    if isinstance(item, Spacer):
                        col_widths.append(0.18*inch)
                    else:
                        col_widths.append(0.18*inch)
                
                icon_table = Table([icon_table_data], colWidths=col_widths)
                icon_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ]))
                info_elements.append(icon_table)
            
            # Create header table
            header_table = Table(
                [[profile_image, info_elements]], 
                colWidths=[1.2*inch, 6*inch]
            )
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), 8),
                ('LEFTPADDING', (1, 0), (1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(header_table)
            
        else:
            # Header without profile image
            name = Paragraph(self.cv_data.personal_info['name'], self.styles['CVName'])
            story.append(name)
            
            if self.cv_data.personal_info.get('title'):
                title = Paragraph(self.cv_data.personal_info['title'], self.styles['CVTitle'])
                story.append(title)
            
            # Contact icons in one line
            icon_row = []
            
            # Email icon
            if self.cv_data.personal_info.get('email'):
                email = self.cv_data.personal_info['email']
                email_icon = self._create_clickable_icon('images/email.png', f'mailto:{email}')
                if email_icon:
                    icon_row.append(email_icon)
            
            # Phone icon - link to WhatsApp
            if self.cv_data.personal_info.get('phone'):
                phone = self.cv_data.personal_info['phone']
                # Remove spaces and special characters for WhatsApp link
                phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                whatsapp_url = f'https://wa.me/{phone_clean}'
                phone_icon = self._create_clickable_icon('images/phone.png', whatsapp_url)
                if phone_icon:
                    icon_row.append(phone_icon)
            
            # LinkedIn icon
            if self.cv_data.personal_info.get('linkedin'):
                linkedin_url = self.cv_data.personal_info['linkedin']
                linkedin_icon = self._create_clickable_icon('images/linkedin.png', linkedin_url)
                if linkedin_icon:
                    icon_row.append(linkedin_icon)
            
            # GitHub icon
            if self.cv_data.personal_info.get('github'):
                github_url = self.cv_data.personal_info['github']
                github_icon = self._create_clickable_icon('images/github.png', github_url)
                if github_icon:
                    icon_row.append(github_icon)
            
            # Google Scholar icon
            if self.cv_data.personal_info.get('google_scholar'):
                scholar_url = self.cv_data.personal_info['google_scholar']
                scholar_icon = self._create_clickable_icon('images/google_scholar.png', scholar_url)
                if scholar_icon:
                    icon_row.append(scholar_icon)
            
            # Scholar/ResearchGate icon
            if self.cv_data.personal_info.get('scholar'):
                scholar_url = self.cv_data.personal_info['scholar']
                if not scholar_url.startswith('http'):
                    scholar_url = 'https://' + scholar_url
                rg_icon = self._create_clickable_icon('images/scholar.png', scholar_url)
                if not rg_icon:
                    rg_icon = self._create_clickable_icon('images/researchgate.png', scholar_url)
                if rg_icon:
                    icon_row.append(rg_icon)
            
            # Create icon table
            if icon_row:
                icon_table_data = []
                for i, icon in enumerate(icon_row):
                    icon_table_data.append(icon)
                    if i < len(icon_row) - 1:
                        icon_table_data.append(Spacer(0.18*inch, 0.18*inch))
                
                num_cols = len(icon_table_data)
                col_widths = []
                for item in icon_table_data:
                    if isinstance(item, Spacer):
                        col_widths.append(0.18*inch)
                    else:
                        col_widths.append(0.18*inch)
                
                icon_table = Table([icon_table_data], colWidths=col_widths)
                icon_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                story.append(icon_table)
        
        # Divider line
        story.append(Spacer(1, 0.06*inch))
        line_table = Table([['']], colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.5, colors.HexColor('#1a5490')),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.08*inch))
    
    def _add_section_header(self, story, title):
        """Add a section header"""
        heading = Paragraph(f"<b>{title.upper()}</b>", self.styles['CVSectionHeading'])
        story.append(heading)
        
        # Thin line under section
        line_table = Table([['']], colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#1a5490')),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(line_table)
    
    def _add_summary(self, story):
        """Add professional summary"""
        if not self.cv_data.summary:
            return
        self._add_section_header(story, "Professional Summary")
        summary = Paragraph(self.cv_data.summary.strip(), self.styles['CVBody'])
        story.append(summary)
        story.append(Spacer(1, 0.06*inch))
    
    def _add_education(self, story):
        """Add education section"""
        if not self.cv_data.education:
            return
        self._add_section_header(story, "Education")
        
        for edu in self.cv_data.education:
            # Degree and year
            degree_text = f"<b>{edu['degree']}</b>"
            if edu.get('year'):
                degree_text += f" <font color='#666666'>| {edu['year']}</font>"
            degree = Paragraph(degree_text, self.styles['CVJobTitle'])
            story.append(degree)
            
            # Institution
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
            
            story.append(Spacer(1, 0.05*inch))
    
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
            org_text = f"<i>{exp['organization']}"
            if exp.get('location'):
                org_text += f", {exp['location']}"
            org_text += f"</i> | <font color='#666666'>{exp['period']}</font>"
            organization = Paragraph(org_text, self.styles['CVOrganization'])
            story.append(organization)
            
            # Responsibilities as bullets
            if exp.get('responsibilities'):
                for resp in exp['responsibilities']:
                    bullet = Paragraph(f"• {resp}", self.styles['CVBullet'])
                    story.append(bullet)
            
            story.append(Spacer(1, 0.05*inch))
    
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
                # Shorten DOI for display
                doi_display = pub['doi'].replace('https://doi.org/', 'doi:')
                pub_text += f" {doi_display}"
            if pub.get('citations', 0) > 0:
                pub_text += f" <font color='#666666'>[{pub['citations']} citations]</font>"
            
            publication = Paragraph(pub_text, self.styles['CVPublication'])
            story.append(publication)
        
        story.append(Spacer(1, 0.06*inch))
    
    def _add_conference_papers(self, story):
        """Add conference papers section"""
        if not self.cv_data.conference_papers:
            return
        self._add_section_header(story, "Conference Papers & Proceedings")
        
        for i, paper in enumerate(self.cv_data.conference_papers, 1):
            paper_text = f"[{i}] <b>\"{paper.get('title', 'Untitled')}\"</b> "
            paper_text += f"<i>{paper.get('venue', 'Unknown Venue')}</i>, {paper.get('year', 'N/A')}."
            
            conf_paper = Paragraph(paper_text, self.styles['CVPublication'])
            story.append(conf_paper)
        
        story.append(Spacer(1, 0.06*inch))
    
    def _add_skills(self, story):
        """Add skills section in compact format"""
        if not self.cv_data.skills:
            return
        self._add_section_header(story, "Technical Skills")
        
        for category, skills_list in self.cv_data.skills.items():
            if isinstance(skills_list, list):
                skills_text = f"<b>{category}:</b> {', '.join(skills_list)}"
            else:
                skills_text = f"<b>{category}:</b> {skills_list}"
            skills = Paragraph(skills_text, self.styles['CVBody'])
            story.append(skills)
        
        story.append(Spacer(1, 0.06*inch))
    
    def _add_languages(self, story):
        """Add languages section"""
        if not self.cv_data.languages:
            return
        self._add_section_header(story, "Languages")
        
        lang_parts = []
        for lang, level in self.cv_data.languages.items():
            lang_parts.append(f"<b>{lang}:</b> {level}")
        
        lang_text = " | ".join(lang_parts)
        languages = Paragraph(lang_text, self.styles['CVBody'])
        story.append(languages)
        story.append(Spacer(1, 0.06*inch))
    
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
                award_text += f" <font color='#666666'>({award['year']})</font>"
            award_para = Paragraph(award_text, self.styles['CVBullet'])
            story.append(award_para)
        
        story.append(Spacer(1, 0.06*inch))
    
    def _add_service(self, story):
        """Add professional service section"""
        if not self.cv_data.service:
            return
        self._add_section_header(story, "Professional Development")
        
        for service in self.cv_data.service:
            service_text = f"• {service}"
            service_para = Paragraph(service_text, self.styles['CVBullet'])
            story.append(service_para)
    
    def build_cv(self, filename="professional_cv.pdf"):
        """Build the complete CV PDF with tight layout"""
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=0.6*inch,
            rightMargin=0.6*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
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
        story.append(Spacer(1, 0.15*inch))
        footer_text = f"<font size=7 color='#999999'><i>Last updated: {datetime.now().strftime('%B %Y')}</i></font>"
        footer = Paragraph(footer_text, self.styles['Normal'])
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        print(f"\n✓ CV successfully generated: {filename}")
        return filename


def main():
    """Main function to generate CV"""
    print("=" * 70)
    print("Professional CV Builder - Redesigned Layout")
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
            print(f"\nNote: Profile image path specified but file not found: {profile_image_path}")
    
    # Build CV
    print("\nGenerating CV PDF with professional tight layout...")
    builder = CVBuilder(cv_data, include_image=include_image)
    output_file = builder.build_cv("Animesh_Choudhury_CV.pdf")
    
    print("\n" + "=" * 70)
    print("✓ CV Generation Complete!")
    print("=" * 70)
    print(f"\nOutput file: {output_file}")
    print(f"Data file: {json_file}")
    print("\nLayout improvements:")
    print("  ✓ Fixed name/title overlapping")
    print("  ✓ Tight, professional spacing")
    print("  ✓ Clean, modern design")
    print("  ✓ Better use of page space")
    

if __name__ == "__main__":
    main()
