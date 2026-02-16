# Professional CV Builder for Researchers

A Python-based CV generator that creates professional PDFs with automatic Google Scholar publication integration.

## Features

✅ Clean, professional CV layout  
✅ Google Scholar publication import  
✅ Easy customization via JSON file  
✅ Automatic citation counts  
✅ Professional formatting  
✅ Support for multiple sections (Education, Experience, Publications, Skills, Awards, Service)
✅ Profile image support
✅ Clickable logo icons for contact information

## Installation

### Required Packages

```
bash
pip install reportlab pillow
```

### Optional (for Google Scholar integration)

```
bash
pip install scholarly requests beautifulsoup4 lxml python-dateutil
```

## Quick Start

### 1. Generate Your First CV

```
bash
python cv_builder_v2.py
```

This will generate a `Animesh_Choudhury_CV.pdf` with the data from `animesh_cv_data.json`.

### 2. Customize Your Data

Edit `animesh_cv_data.json` with your personal information:

```
json
{
  "personal_info": {
    "name": "Your Name",
    "title": "Your Title",
    "email": "your.email@example.com",
    "phone": "+91 1234567890",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "github": "https://github.com/yourusername",
    "profile_image": "profileImage.jpg"
  },
  "education": [...],
  "experience": [...],
  "publications": [...],
  ...
}
```

### 3. Regenerate CV

After editing the JSON file:

```
bash
python cv_builder_v2.py
```

Your CV will be regenerated with your updated information.

## File Structure

```
CV_Builder/
├── cv_builder_v2.py           # Main CV generator (with profile image support)
├── cv_builder_professional.py # Professional CV with logo icons
├── scholar_fetcher.py         # Google Scholar integration
├── animesh_cv_data.json       # Your CV data (editable)
├── Animesh_Choudhury_CV.pdf  # Generated CV output
├── check_logos.py             # Diagnostic script for logo files
├── generate_placeholder_icons.py # Generate placeholder logos
├── images/                    # Logo icons folder
│   ├── email.png
│   ├── phone.png
│   ├── linkedin.png
│   ├── github.png
│   └── scholar.png
└── profileImage.jpg           # Your profile photo
```

## Adding Your Profile Photo

### Step 1: Prepare Your Photo
- Use a professional headshot
- Square format works best (e.g., 500x500 pixels)
- Supported formats: JPG, PNG, JPEG
- File size: Keep under 2MB

### Step 2: Add Photo to Your Directory
Place your photo file (e.g., `profileImage.jpg`) in the same folder as the CV builder.

### Step 3: Update JSON File
Open `animesh_cv_data.json` and find the `personal_info` section:

```
json
"personal_info": {
  "name": "Your Name",
  "profile_image": "profileImage.jpg",  ← Add this line with your filename
  ...
}
```

### Step 4: Regenerate CV
```
bash
python cv_builder_v2.py
```

When prompted "Include profile image in CV? (y/n)", press `y` or just Enter.

## Logo Icons Setup

### What You Need

The CV builder supports clickable logo icons for your contact information. Logo files should be placed in the `images/` folder:

1. **images/email.png** - Email/envelope icon
2. **images/phone.png** - Phone icon
3. **images/linkedin.png** - LinkedIn logo
4. **images/github.png** - GitHub logo
5. **images/scholar.png** OR **images/researchgate.png** - Your research profile logo

### Logo Specifications

- **Format**: PNG (preferred) or JPG
- **Transparency**: Transparent background works best
- **Size**: 32x32 to 64x64 pixels recommended
- **File size**: Keep under 50KB each

### Getting Professional Logos

1. **Icons8** (https://icons8.com) - Search for email, phone, linkedin, github
2. **Flaticon** (https://www.flaticon.com) - Download social media icons
3. **Official Brand Logos**:
   - LinkedIn: https://brand.linkedin.com/downloads
   - GitHub: https://github.com/logos

### Generate Placeholder Icons

If you don't have logos, you can generate simple placeholders:

```
bash
python generate_placeholder_icons.py
```

This will create basic colored square icons with letters in the `images/` folder.

### Check Logo Setup

Run the diagnostic script to verify your logo files:

```
bash
python check_logos.py
```

## Google Scholar Integration

### Automatic Publication Fetching

1. **Find Your Scholar ID**
   - Go to your Google Scholar profile
   - URL looks like: `https://scholar.google.com/citations?user=YOUR_ID`
   - Copy YOUR_ID part

2. **Run the Fetcher**
   
```
bash
   python scholar_fetcher.py
   
```

3. **Enter Your Scholar ID** when prompted

4. **Regenerate CV**
   
```
bash
   python cv_builder_v2.py
   
```

The script will:
- ✅ Fetch all your publications
- ✅ Get citation counts for each paper
- ✅ Update `animesh_cv_data.json` automatically
- ✅ Preserve all other CV data

### Manual Scholar Integration

You can also manually update your Scholar URL in `cv_data.json`:

```
json
{
  "personal_info": {
    "scholar": "scholar.google.com/citations?user=YOUR_ID"
  }
}
```

### Troubleshooting Scholar Issues

- **Rate limiting**: Google may limit requests. Wait a few minutes and try again
- **Profile not public**: Make sure your Google Scholar profile is set to public
- **Missing publications**: Manually add publications to JSON as fallback

## Contact Information Layout

### New Design Features

1. **Fixed Icons** - Using proper Unicode symbols that display correctly
2. **Clickable Links** - All links are now clickable
3. **Multi-line Layout** - Organized into 3 separate lines for clarity
4. **Color-coded Links** - Different colors for different platforms

### Contact Info Structure

**Line 1: Email & Phone**
```
✉ your.email@example.com | ☎ +91 1234567890
```

**Line 2: LinkedIn**
```
🔗 LinkedIn Profile
```

**Line 3: GitHub & Research Profile**
```
⚙ GitHub Profile | 🎓 Research Profile
```

### How Links Work

- **Email** → Opens email client with address pre-filled
- **LinkedIn Profile** → Opens LinkedIn page in browser
- **GitHub Profile** → Opens GitHub page in browser
- **Research Profile** → Opens ResearchGate/Scholar page in browser

## Data Structure

### Personal Info
```
json
{
  "name": "Your Name",
  "title": "Your Professional Title",
  "email": "your.email@example.com",
  "phone": "+91 1234567890",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourusername",
  "scholar": "https://www.researchgate.net/profile/Your-Name",
  "profile_image": "profileImage.jpg"
}
```

### Publications
```
json
{
  "publications": [
    {
      "title": "Your Paper Title",
      "authors": "Author1, Author2, Author3",
      "venue": "Journal or Conference Name",
      "year": 2024,
      "citations": 50,
      "type": "journal",
      "doi": "https://doi.org/10.xxxx/xxxxx"
    }
  ]
}
```

### Skills
```
json
{
  "skills": {
    "Programming": ["Python", "R", "SQL"],
    "Tools": ["ArcGIS", "QGIS", "Google Earth Engine"],
    "Domain Expertise": ["Remote Sensing", "GIS", "Machine Learning"]
  }
}
```

## Customization Guide

### Adding Sections

The CV includes these sections:
- **Professional Summary**: Brief overview
- **Education**: Degrees and institutions
- **Professional Experience**: Work history
- **Selected Publications**: Research papers
- **Conference Papers**: Conference presentations
- **Technical Skills & Expertise**: Skills by category
- **Awards**: Recognition
- **Professional Service**: Committee work, reviewing, etc.
- **Languages**: Language proficiencies

### Publication Format

Publications are automatically formatted as:

```
[1] Authors. "Title." Venue, Year. [Citations: X]
```

### Styling

To customize the appearance, edit the `_setup_custom_styles()` method in `cv_builder_professional.py`:

- Font sizes
- Colors
- Spacing
- Alignment

## Tips for Researchers

### Publication Management

1. **Keep publications updated**: Run `scholar_fetcher.py` regularly to update citation counts
2. **Select your best work**: Edit the `publications` list in `cv_data.json` to highlight specific papers
3. **Categorize publications**: You can manually add a `category` field to group publications

### Maintaining Multiple Versions

Create different JSON files for different purposes:

```
bash
# Academic CV (full version)
python cv_builder_v2.py

# Industry CV (edit JSON to focus on applied work)
python cv_builder_v2.py

# Short CV (edit JSON to include only recent highlights)
python cv_builder_v2.py
```

## Troubleshooting

### PDF Generation Issues

If PDF generation fails:
- Ensure `reportlab` is installed: `pip install reportlab pillow`
- Check file permissions in the output directory
- Verify JSON file is valid (use a JSON validator)

### Profile Image Issues

**Problem: Profile image not showing**
- Check the file path is correct in JSON
- Make sure image file is in the same directory
- Try using a different image format (JPG or PNG)

### Logo Icon Issues

**Problem: Logo icons not showing**
- Run `python check_logos.py` to diagnose
- Ensure PNG files are in the `images/` folder
- Verify file names match exactly (case-sensitive)

### Character Encoding

For non-ASCII characters (accents, special symbols):
- The scripts use UTF-8 encoding
- Ensure your JSON file is saved as UTF-8

## Advanced Usage

### Batch Processing

Create multiple CVs at once:

```
python
from cv_builder_v2 import CVData, CVBuilder

# Load data
cv_data = CVData()
cv_data.load_from_json("animesh_cv_data.json")

# Generate different versions
builder = CVBuilder(cv_data)
builder.build_cv("CV_Full.pdf")

# Modify for short version
cv_data.publications = cv_data.publications[:5]  # Top 5 papers
builder = CVBuilder(cv_data)
builder.build_cv("CV_Short.pdf")
```

### Custom Formatting

You can extend the `CVBuilder` class to add custom sections:

```
python
def _add_custom_section(self, story):
    self._add_section_header(story, "CUSTOM SECTION")
    # Add your content here
```

## Requirements

```
reportlab>=4.0.0
Pillow>=10.0.0
scholarly>=1.7.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dateutil>=2.8.0
```

## Support

For issues or questions:
- Edit the JSON file for data changes
- Edit Python scripts for styling changes
- Run `scholar_fetcher.py` for publication updates

## License

Free to use and modify for personal and professional purposes.

---

**Author**: Animesh Choudhury  
**Last Updated**: 2024
