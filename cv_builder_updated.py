"""
Professional CV Builder for Animesh Choudhury
Updated to match original CV format with clickable publication links
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import json
import os
from datetime import datetime
from PIL import Image as PILImage

class CVData:
    """Class to hold CV data"""
    def __init__(self, json_file='animesh_cv_data.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.personal_info = data.get('personal_info', {})
        self.summary = data.get('summary', '')
        self.education = data.get('education', [])
        self.experience = data.get('experience', [])
        self.publications = data.get('publications', [])
        self.conference_papers = data.get('conference_papers', [])
        self.skills = data.get('skills', {})
        self.languages = data.get('languages', {})
        self.awards = data.get('awards', [])
        self.service = data.get('service', [])

class CVBuilder:
    """Build a professional CV matching original format"""
    
    def __init__(self, cv_data, filename='Animesh_Choudhury_CV_Updated.pdf', include_image=True):
        self.cv_data = cv_data
        self.filename = filename
        self.include_image = include_image
        
        # Page setup - tight margins for more content
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=0.6*inch,
            rightMargin=0.6*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
        )
        
        self.styles = self._setup_custom_styles()
        self.story = []
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        styles = getSampleStyleSheet()
        
        # Name style
        styles.add(ParagraphStyle(
            name='CVName',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=20
        ))
        
        # Title/position style
        styles.add(ParagraphStyle(
            name='CVTitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=12
        ))
        
        # Contact info style
        styles.add(ParagraphStyle(
            name='CVContact',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            spaceAfter=2,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=10
        ))
        
        # Section header style
        styles.add(ParagraphStyle(
            name='CVSectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=6,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            leading=13
        ))
        
        # Job title/position style
        styles.add(ParagraphStyle(
            name='CVJobTitle',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=2,
            leading=12
        ))
        
        # Date/period style
        styles.add(ParagraphStyle(
            name='CVDate',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666'),
            spaceAfter=4,
            leading=11,
            leftIndent=0
        ))
        
        # Body text style
        styles.add(ParagraphStyle(
            name='CVBody',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=2,
            alignment=TA_JUSTIFY,
            leading=11
        ))
        
        # Publication style - with link
        styles.add(ParagraphStyle(
            name='CVPublication',
            parent=styles['Normal'],
            fontSize=8.5,
            fontName='Helvetica',
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=4,
            alignment=TA_JUSTIFY,
            leading=10.5,
            leftIndent=0
        ))
        
        # Bullet point style
        styles.add(ParagraphStyle(
            name='CVBullet',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=2,
            leftIndent=10,
            bulletIndent=0,
            leading=11
        ))
        
        return styles
    
    def _process_profile_image(self, image_path, size=1.1):
        """Process profile image - crop to square and resize"""
        try:
            img = PILImage.open(image_path)
            
            # Crop to square
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = left + min_dim
            bottom = top + min_dim
            img_cropped = img.crop((left, top, right, bottom))
            
            # Save temporarily
            temp_path = 'temp_profile.jpg'
            img_cropped.save(temp_path, 'JPEG', quality=95)
            
            # Create ReportLab image
            return Image(temp_path, width=size*inch, height=size*inch)
        except Exception as e:
            print(f"Warning: Could not process profile image: {e}")
            return None
    
    def _add_header(self, story):
        """Add CV header with name, contact info, and optional profile image"""
        
        profile_image = None
        image_path = self.cv_data.personal_info.get('profile_image', '')
        
        if self.include_image and image_path and os.path.exists(image_path):
            profile_image = self._process_profile_image(image_path, size=1.1)
        
        if profile_image:
            # Two-column layout: image on left, info on right
            info_elements = []
            
            # Name
            name_para = Paragraph(self.cv_data.personal_info['name'], self.styles['CVName'])
            info_elements.append(name_para)
            
            # Contact information in original CV format
            contact_lines = []
            
            # Date of birth, Nationality, Gender
            contact_line1 = []
            if self.cv_data.personal_info.get('date_of_birth'):
                contact_line1.append(f"Date of birth: {self.cv_data.personal_info['date_of_birth']}")
            if self.cv_data.personal_info.get('nationality'):
                contact_line1.append(f"Nationality: {self.cv_data.personal_info['nationality']}")
            if self.cv_data.personal_info.get('gender'):
                contact_line1.append(f"Gender: {self.cv_data.personal_info['gender']}")
            if contact_line1:
                contact_lines.append(' | '.join(contact_line1))
            
            # Phone and Email
            contact_line2 = []
            if self.cv_data.personal_info.get('phone'):
                phone_clean = self.cv_data.personal_info['phone'].replace('+', '').replace(' ', '').replace('-', '')
                contact_line2.append(f'Phone: <link href="https://wa.me/{phone_clean}" color="blue">{self.cv_data.personal_info["phone"]}</link>')
            if self.cv_data.personal_info.get('email'):
                contact_line2.append(f'Email: <link href="mailto:{self.cv_data.personal_info[\"email\"]}" color="blue">{self.cv_data.personal_info["email"]}</link>')
            if contact_line2:
                contact_lines.append(' | '.join(contact_line2))
            
            # Social links
            social_links = []
            if self.cv_data.personal_info.get('linkedin'):
                social_links.append(f'<link href="{self.cv_data.personal_info[\"linkedin\"]}" color="blue">LinkedIn</link>')
            if self.cv_data.personal_info.get('github'):
                social_links.append(f'<link href="{self.cv_data.personal_info[\"github\"]}" color="blue">GitHub</link>')
            if self.cv_data.personal_info.get('scholar'):
                social_links.append(f'<link href="{self.cv_data.personal_info[\"scholar\"]}" color="blue">ResearchGate</link>')
            if social_links:
                contact_lines.append(' | '.join(social_links))
            
            # Address
            if self.cv_data.personal_info.get('address'):
                contact_lines.append(f"Address: {self.cv_data.personal_info['address']}")
            
            # Add all contact lines
            for line in contact_lines:
                info_elements.append(Paragraph(line, self.styles['CVContact']))
            
            # Create header table
            header_table = Table(
                [[profile_image, info_elements]], 
                colWidths=[1.2*inch, 6*inch]
            )
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(header_table)
        else:
            # Header without image
            name = Paragraph(self.cv_data.personal_info['name'], self.styles['CVName'])
            story.append(name)
            
            # Contact information - same format as above
            contact_lines = []
            
            # Date of birth, Nationality, Gender
            contact_line1 = []
            if self.cv_data.personal_info.get('date_of_birth'):
                contact_line1.append(f"Date of birth: {self.cv_data.personal_info['date_of_birth']}")
            if self.cv_data.personal_info.get('nationality'):
                contact_line1.append(f"Nationality: {self.cv_data.personal_info['nationality']}")
            if self.cv_data.personal_info.get('gender'):
                contact_line1.append(f"Gender: {self.cv_data.personal_info['gender']}")
            if contact_line1:
                contact_lines.append(' | '.join(contact_line1))
            
            # Phone and Email
            contact_line2 = []
            if self.cv_data.personal_info.get('phone'):
                phone_clean = self.cv_data.personal_info['phone'].replace('+', '').replace(' ', '').replace('-', '')
                contact_line2.append(f'Phone: <link href="https://wa.me/{phone_clean}" color="blue">{self.cv_data.personal_info["phone"]}</link>')
            if self.cv_data.personal_info.get('email'):
                contact_line2.append(f'Email: <link href="mailto:{self.cv_data.personal_info[\"email\"]}" color="blue">{self.cv_data.personal_info["email"]}</link>')
            if contact_line2:
                contact_lines.append(' | '.join(contact_line2))
            
            # Social links
            social_links = []
            if self.cv_data.personal_info.get('linkedin'):
                social_links.append(f'<link href="{self.cv_data.personal_info[\"linkedin\"]}" color="blue">LinkedIn</link>')
            if self.cv_data.personal_info.get('github'):
                social_links.append(f'<link href="{self.cv_data.personal_info[\"github\"]}" color="blue">GitHub</link>')
            if self.cv_data.personal_info.get('scholar'):
                social_links.append(f'<link href="{self.cv_data.personal_info[\"scholar\"]}" color="blue">ResearchGate</link>')
            if social_links:
                contact_lines.append(' | '.join(social_links))
            
            # Address
            if self.cv_data.personal_info.get('address'):
                contact_lines.append(f"Address: {self.cv_data.personal_info['address']}")
            
            # Add all contact lines
            for line in contact_lines:
                story.append(Paragraph(line, self.styles['CVContact']))
        
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
        header = Paragraph(title.upper(), self.styles['CVSectionHeader'])
        story.append(header)
        
        # Thin underline
        line_table = Table([['']], colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#1a5490')),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(line_table)
    
    def _add_work_experience(self, story):
        """Add work experience section"""
        if not self.cv_data.experience:
            return
        
        self._add_section_header(story, "WORK EXPERIENCE")
        
        for exp in self.cv_data.experience:
            # Period and location
            period_location = f"{exp.get('period', 'N/A')}  -  {exp.get('location', '').upper()}"
            story.append(Paragraph(period_location, self.styles['CVDate']))
            
            # Position and organization
            position_org = f"<b>{exp.get('position', '').upper()}</b> {exp.get('organization', '').upper()}"
            story.append(Paragraph(position_org, self.styles['CVJobTitle']))
            
            # Project title if available
            if exp.get('project'):
                project_text = f'Project Title: "{exp["project"]}"'
                story.append(Paragraph(project_text, self.styles['CVBody']))
            
            # Responsibilities
            if exp.get('responsibilities'):
                for resp in exp['responsibilities']:
                    story.append(Paragraph(resp, self.styles['CVBody']))
                    story.append(Spacer(1, 0.02*inch))
            
            story.append(Spacer(1, 0.06*inch))
    
    def _add_education(self, story):
        """Add education section"""
        if not self.cv_data.education:
            return
        
        self._add_section_header(story, "EDUCATION & TRAINING")
        
        for edu in self.cv_data.education:
            # Year and location
            year_location = f"{edu.get('year', 'N/A')}  -  {edu.get('location', '').upper()}"
            story.append(Paragraph(year_location, self.styles['CVDate']))
            
            # Degree and institution
            degree_inst = f"<b>{edu.get('degree', '').upper()}</b>- {edu.get('institution', '').upper()}"
            story.append(Paragraph(degree_inst, self.styles['CVJobTitle']))
            
            # Website if available
            if edu.get('website'):
                website_text = f'Website: <link href="{edu[\"website\"]}" color="blue">{edu["website"]}</link>'
                story.append(Paragraph(website_text, self.styles['CVBody']))
            
            story.append(Spacer(1, 0.06*inch))
    
    def _add_languages(self, story):
        """Add language skills section"""
        if not self.cv_data.languages:
            return
        
        self._add_section_header(story, "LANGUAGE SKILLS")
        
        # Mother tongue
        for lang, proficiency in self.cv_data.languages.items():
            if 'Native' in proficiency:
                story.append(Paragraph(f"Mother tongue(s): {lang.upper()}", self.styles['CVBody']))
                break
        
        story.append(Spacer(1, 0.04*inch))
        
        # Language table header
        header_text = "<b>UNDERSTANDING</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>SPEAKING</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>WRITING</b>"
        story.append(Paragraph(header_text, self.styles['CVBody']))
        subheader_text = "Listening&nbsp;&nbsp;&nbsp;Reading&nbsp;&nbsp;&nbsp;Spoken production&nbsp;&nbsp;&nbsp;Spoken interaction"
        story.append(Paragraph(subheader_text, self.styles['CVBody']))
        
        # Languages
        for lang, proficiency in self.cv_data.languages.items():
            if 'Native' not in proficiency:
                lang_text = f"<b>{lang.upper()}</b> {proficiency}"
                story.append(Paragraph(lang_text, self.styles['CVBody']))
        
        story.append(Spacer(1, 0.06*inch))
    
    def _add_skills(self, story):
        """Add skills section"""
        if not self.cv_data.skills:
            return
        
        self._add_section_header(story, "SKILLS")
        
        # Combine all skills into one paragraph
        all_skills = []
        for category, skills_list in self.cv_data.skills.items():
            if isinstance(skills_list, list):
                all_skills.extend(skills_list)
            else:
                all_skills.append(skills_list)
        
        skills_text = " | ".join(all_skills)
        story.append(Paragraph(skills_text, self.styles['CVBody']))
        story.append(Spacer(1, 0.06*inch))
    
    def _add_publications(self, story):
        """Add publications section with clickable links"""
        if not self.cv_data.publications:
            return
        
        self._add_section_header(story, "PUBLICATIONS")
        
        for pub in self.cv_data.publications:
            # Format: Authors. Title. Venue, Year.
            pub_text = f"{pub.get('authors', '')}. "
            
            # Add title with link if DOI available
            if pub.get('doi'):
                pub_text += f'<link href="{pub[\"doi\"]}" color="blue">{pub.get(\"title\", \"\")}</link>. '
            else:
                pub_text += f"{pub.get('title', '')}. "
            
            # Venue with volume/issue/pages
            pub_text += f"<i>{pub.get('venue', '')}</i>"
            if pub.get('year'):
                pub_text += f". {pub['year']}"
            if pub.get('volume'):
                pub_text += f"; {pub['volume']}"
            if pub.get('issue'):
                pub_text += f"({pub['issue']})"
            if pub.get('pages'):
                pub_text += f":{pub['pages']}"
            pub_text += "."
            
            story.append(Paragraph(pub_text, self.styles['CVPublication']))
            story.append(Spacer(1, 0.04*inch))
        
        story.append(Spacer(1, 0.04*inch))
    
    def _add_conference_papers(self, story):
        """Add conference papers with clickable links"""
        if not self.cv_data.conference_papers:
            return
        
        self._add_section_header(story, "CONFERENCE PAPERS")
        
        for paper in self.cv_data.conference_papers:
            # Format: TITLE (with link)
            if paper.get('url'):
                paper_text = f'<b><link href="{paper[\"url\"]}" color="blue">{paper.get(\"title\", \"\").upper()}</link></b>'
            else:
                paper_text = f"<b>{paper.get('title', '').upper()}</b>"
            
            story.append(Paragraph(paper_text, self.styles['CVPublication']))
            
            # Links
            if paper.get('url'):
                link_text = f'Links <link href="{paper[\"url\"]}" color="blue">{paper["url"]}</link>'
                story.append(Paragraph(link_text, self.styles['CVBody']))
            
            story.append(Spacer(1, 0.04*inch))
        
        story.append(Spacer(1, 0.04*inch))
    
    def _add_posters_training(self, story):
        """Add poster presentations, training, and webinars"""
        if not self.cv_data.service and not self.cv_data.awards:
            return
        
        self._add_section_header(story, "POSTER, ONLINE TRAINING, WEBINAR")
        
        # Add awards (poster presentations)
        for award in self.cv_data.awards:
            award_text = f'<b>{award.get("name", "")}</b>'
            if award.get('description'):
                award_text += f' on "{award["description"]}"'
            award_text += f' in the {award.get("organization", "")}'
            if award.get('location'):
                award_text += f' held at {award["location"]}'
            if award.get('date'):
                award_text += f' during {award["date"]}'
            
            story.append(Paragraph(award_text, self.styles['CVBody']))
            story.append(Spacer(1, 0.04*inch))
        
        # Add training and webinars from service
        for item in self.cv_data.service:
            if item.get('type') == 'webinar':
                text = f'Attended a webinar on "{item.get("name", "")}" organized by {item.get("organization", "")}'
                if item.get('date'):
                    text += f' on {item["date"]}'
            elif item.get('type') == 'training':
                # Check length to determine format
                name = item.get('name', '')
                if 'days' in item.get('period', '').lower() or 'week' in item.get('period', '').lower():
                    text = f'Attended {item.get("period", "")} training program on "{name}" organized by {item.get("organization", "")}'
                else:
                    text = f'Completed the "{name}" organised by {item.get("organization", "")} during {item.get("period", "")}'
            else:
                continue
            
            story.append(Paragraph(text, self.styles['CVBody']))
            story.append(Spacer(1, 0.04*inch))
        
        story.append(Spacer(1, 0.04*inch))
    
    def build(self):
        """Build the complete CV"""
        print("\n" + "="*70)
        print("Professional CV Builder - Original Format")
        print("="*70)
        
        # Check if we should include image
        image_path = self.cv_data.personal_info.get('profile_image', '')
        if self.include_image and image_path:
            if os.path.exists(image_path):
                print(f"\n✓ Profile image found: {image_path}")
                choice = input("Include profile image in CV? (y/n, default=y): ").lower().strip()
                if choice == 'n':
                    self.include_image = False
                print(f"Profile picture: {'Enabled' if self.include_image else 'Disabled'}")
            else:
                print(f"\nNote: Profile image path specified but file not found: {image_path}")
                print("Continuing without profile image.")
                self.include_image = False
        
        print("\nGenerating CV PDF matching original format...")
        
        # Build CV sections
        self._add_header(self.story)
        self._add_work_experience(self.story)
        self._add_education(self.story)
        self._add_languages(self.story)
        self._add_skills(self.story)
        self._add_publications(self.story)
        self._add_conference_papers(self.story)
        self._add_posters_training(self.story)
        
        # Build PDF
        self.doc.build(self.story)
        
        print(f"\n✓ CV successfully generated: {self.filename}")
        print("\n" + "="*70)
        print("✓ CV Generation Complete!")
        print("="*70)
        print(f"\nOutput file: {self.filename}")
        print("\nFeatures:")
        print("  ✓ Clickable publication links (no citations shown)")
        print("  ✓ Clickable conference paper links (no DOI shown)")
        print("  ✓ WhatsApp-enabled phone number")
        print("  ✓ Original CV format maintained")
        print("  ✓ Professional layout")

if __name__ == '__main__':
    # Load data and build CV
    cv_data = CVData('animesh_cv_data.json')
    
    # Build CV
    builder = CVBuilder(cv_data, include_image=True)
    builder.build()
