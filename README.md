# 📄 Academic CV Builder

A **Python-based PDF CV generator** tailored for academic researchers. It programmatically builds a professional, publication-ready Curriculum Vitae from a single JSON data file, with support for profile images, Google Scholar integration, and customizable styling — all without manual formatting in Word or LaTeX.

---

## ✨ Features

- **PDF Generation** — Produces a clean, professional-grade PDF using [ReportLab](https://www.reportlab.com/)
- **Profile Image Support** — Embeds a headshot in the CV header with automatic aspect-ratio preservation
- **JSON-Driven Data** — All CV content (personal info, education, experience, publications, skills, awards) is managed via a single editable JSON file
- **Google Scholar Integration** — Optionally auto-fetches publications and citation counts via `scholar_fetcher.py`
- **Publication Sections** — Separate handling for journal articles and conference papers, sorted by recency
- **Custom Styling** — Configurable paragraph styles, fonts, colors, and layout without touching layout logic
- **Lightweight & Portable** — No LaTeX installation required; runs in any standard Python environment

---

## 🗂️ Repository Structure

```
CV_Builder/
├── cv_builder_v2.py          # ✅ Main CV builder (primary entry point)
├── animesh_cv_data.json      # CV content data (edit this to update your CV)
├── scholar_fetcher.py        # Google Scholar publication fetcher
├── check_logos.py            # Utility to verify image/logo assets
├── generate_placeholder_icons.py  # Generates placeholder icons for testing
├── requirements.txt          # Python dependencies
├── profileImage.png          # Profile photo used in the CV header
├── images/                   # Additional image assets
│
├── QUICK_START.md            # Step-by-step usage guide
├── CONTACT_INFO_GUIDE.md     # Guide for formatting contact details
├── GOOGLE_SCHOLAR_GUIDE.md   # Guide for Scholar ID setup and fetching
├── LOGO_SETUP_GUIDE.md       # Guide for institutional logo usage
│
└── *.pdf                     # Generated CV outputs
```

> **Note:** `cv_builder_final.py`, `cv_builder_professional.py`, and `cv_builder_updated.py` are earlier iterations. `cv_builder_v2.py` is the most current and recommended version.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AnimeshChoudhury/CV_Builder.git
cd CV_Builder
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**

| Package | Purpose |
|---|---|
| `reportlab >= 4.0.0` | PDF generation engine |
| `Pillow >= 10.0.0` | Profile image processing |
| `scholarly >= 1.7.0` | Google Scholar API (optional) |
| `requests >= 2.31.0` | HTTP requests for Scholar |
| `beautifulsoup4 >= 4.12.0` | Web scraping for Scholar |
| `python-dateutil >= 2.8.0` | Date parsing utilities |

### 4. Generate Your CV

```bash
python cv_builder_v2.py
```

The script will:
1. Load your CV content from `animesh_cv_data.json`
2. Detect and optionally embed your profile image
3. Generate `Animesh_Choudhury_CV.pdf` in the current directory

---

## 🔧 Customizing Your CV

### Edit CV Content

All CV data lives in `animesh_cv_data.json`. Open it and update any section:

**Personal Information:**
```json
"personal_info": {
  "name": "Your Full Name",
  "title": "Your Professional Title",
  "email": "your.email@example.com",
  "phone": "+91 XXXXXXXXXX",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourusername",
  "scholar": "https://www.researchgate.net/profile/your-profile",
  "google_scholar": "https://scholar.google.com/citations?user=YOUR_ID",
  "profile_image": "your_photo.png"
}
```

**Adding a Publication:**
```json
{
  "title": "Your Paper Title",
  "authors": "Author A, Author B, & Author C",
  "venue": "Journal of Example Research",
  "year": 2025,
  "citations": 12,
  "type": "journal",
  "doi": "https://doi.org/10.xxxx/xxxxx"
}
```

**Adding Work Experience:**
```json
{
  "position": "Research Fellow",
  "organization": "University Name",
  "location": "City, Country",
  "period": "Jan 2022 - Present",
  "responsibilities": [
    "Key responsibility 1",
    "Key responsibility 2"
  ]
}
```

### Customizing Visual Styles

Open `cv_builder_v2.py` and locate the `_setup_custom_styles()` method (~line 82). Modify paragraph style properties:

```python
self.styles.add(ParagraphStyle(
    name='CVSectionHeading',
    fontSize=13,                            # Adjust font size
    textColor=colors.HexColor('#1a5490'),   # Change accent color
    fontName='Helvetica-Bold',
    spaceAfter=8,
))
```

Key style names and their usage:

| Style Name | Used For |
|---|---|
| `CVName` | Researcher's name in the header |
| `CVTitle` | Professional title subtitle |
| `CVContact` | Contact info lines |
| `CVSectionHeading` | Section titles (EDUCATION, SKILLS, etc.) |
| `CVBody` | Body text, bullet points |
| `CVPublication` | Journal and conference paper entries |
| `CVJobTitle` | Position or degree title |
| `CVOrganization` | Organization name and location |

---

## 📸 Adding a Profile Photo

1. Place your photo (JPG or PNG) in the project directory
2. Update `animesh_cv_data.json`:
   ```json
   "profile_image": "your_photo.jpg"
   ```
3. Re-run the builder:
   ```bash
   python cv_builder_v2.py
   ```
4. When prompted, type `y` to include the image

> The builder automatically handles aspect-ratio correction and resizes the image to fit neatly in the CV header alongside your name and contact details.

---

## 📚 Google Scholar Integration

Use `scholar_fetcher.py` to automatically pull your publication list and citation counts directly from your Google Scholar profile.

### Find Your Scholar ID

Your Scholar ID is in the URL of your Google Scholar profile:
```
https://scholar.google.com/citations?user=YOUR_ID_HERE&hl=en
                                             ^^^^^^^^^^^
                                         Copy this part
```

### Run the Fetcher

```bash
python scholar_fetcher.py
```

Enter your Scholar ID or full profile URL when prompted. The script will:
- Fetch all publications with titles, venues, years, and citation counts
- Sort them by publication year (most recent first)
- Update `animesh_cv_data.json` automatically (with a backup of existing entries)

Then regenerate your CV:
```bash
python cv_builder_v2.py
```

> **Rate Limiting:** The fetcher includes configurable delays (default: 2 seconds per publication) to avoid being blocked by Google Scholar. If you encounter errors, wait 10–15 minutes and retry.

---

## 🏗️ Architecture Overview

```
cv_builder_v2.py
│
├── CVData                        # Data model class
│   ├── load_from_json()          # Loads animesh_cv_data.json
│   └── save_to_json()            # Persists data back to JSON
│
└── CVBuilder                     # PDF generation class
    ├── __init__()                # Initializes styles and data
    ├── _setup_custom_styles()    # Defines all ReportLab paragraph styles
    ├── _process_profile_image()  # Handles image resize & aspect ratio
    ├── _add_header()             # Builds name/contact/image header block
    ├── _add_section_header()     # Renders titled section dividers
    ├── _add_summary()            # Professional summary paragraph
    ├── _add_education()          # Education entries
    ├── _add_experience()         # Work experience with bullet points
    ├── _add_publications()       # Journal articles (sorted by year)
    ├── _add_conference_papers()  # Conference proceedings
    ├── _add_skills()             # Categorized technical skills
    ├── _add_languages()          # Language proficiencies
    ├── _add_awards()             # Awards and recognition
    ├── _add_service()            # Professional development & service
    └── build_cv()                # Assembles and renders the full PDF
```

---

## 📋 CV Sections

The generated PDF includes the following sections in order:

1. **Header** — Name, title, contact info (email, phone, LinkedIn, GitHub, Scholar), and profile image
2. **Professional Summary** — Concise research overview paragraph
3. **Education** — Degrees with institution, location, year, and thesis title
4. **Work Experience** — Positions with organization, period, and bullet-point responsibilities
5. **Selected Publications** — Peer-reviewed journal articles with DOI links, sorted by year
6. **Conference Papers & Proceedings** — Conference presentations and proceedings
7. **Technical Skills & Expertise** — Skill categories (e.g., ML & AI, Remote Sensing, GIS)
8. **Languages** — Language proficiencies and levels
9. **Awards & Recognition** — Prizes, symposia, and speaking roles
10. **Professional Development & Service** — Training programs, workshops, and webinars
11. **Footer** — Auto-generated "Last updated: Month Year" timestamp

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: reportlab` | Run `pip install -r requirements.txt` |
| Profile image not appearing | Verify `profile_image` path in JSON matches the actual filename |
| `PIL` image error | Run `pip install Pillow` |
| Scholar fetcher blocked | Wait 10–15 minutes; increase delay when prompted |
| PDF not updating | Ensure you saved `animesh_cv_data.json` before re-running |
| Unicode rendering issues | The builder uses UTF-8 encoding throughout; ensure your JSON editor saves in UTF-8 |

---

## 💡 Tips & Best Practices

- **Version control your JSON** — `animesh_cv_data.json` is your single source of truth. Commit it to Git.
- **Run Scholar fetcher monthly** — Keeps citation counts current without manual updates.
- **Multiple CV variants** — Maintain separate JSON files (e.g., `cv_data_academic.json`, `cv_data_industry.json`) for targeted applications.
- **Profile photo format** — Square-cropped, high-resolution JPG or PNG with neutral background works best.
- **Keep DOIs accurate** — The builder inserts DOI links verbatim into the PDF; broken DOIs are difficult to correct post-distribution.

---

## 📄 License

This project is open source. You are free to use, modify, and adapt it for your own academic CV generation needs.

---

*Built with [ReportLab](https://www.reportlab.com/) · Designed for researchers in Earth & Atmospheric Sciences and beyond.*
