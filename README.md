# Academic CV Builder

A Python-based PDF CV generator for academic researchers. It builds a clean, publication-ready Curriculum Vitae from a single JSON data file — complete with a profile image, clickable social profile icons in the header, and clickable DOI/URL hyperlinks embedded directly in publication entries. No LaTeX or manual formatting required.

---

## Repository Structure

```
CV_Builder/
│
├── cv_builder_final.py       ← CV builder script (single entry point)
├── animesh_cv_data.json      ← All CV content (edit this to update your CV)
├── profileImage.png          ← Profile photo embedded in the CV header
├── requirements.txt          ← Python dependencies
│
├── images/                   ← Clickable icon images used in the CV header
│   ├── email.png
│   ├── phone.png
│   ├── linkedin.png
│   ├── github.png
│   ├── google_scholar.png
│   └── researchgate.png
│
└── Animesh_Choudhury_CV.pdf  ← Generated CV output
```

---

## Features

- **PDF generation** with precise, tight layout control via [ReportLab](https://www.reportlab.com/)
- **Profile image** embedded in the header — automatically square-cropped for a clean look
- **Clickable social icons** in the header (email, phone/WhatsApp, LinkedIn, GitHub, Google Scholar, ResearchGate) using custom `ClickableImage` flowables
- **Clickable publication titles** — DOI and URL hyperlinks embedded directly in the PDF text
- **Auto-sorted work experience** — entries sorted chronologically by end date (most recent first); roles marked `"Current"` always appear at the top
- **JSON-driven content** — all CV data managed in one editable file; no code changes needed for content updates
- **Modular section rendering** — each CV section is an independent method, making it straightforward to add, remove, or reorder sections

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AnimeshChoudhury/CV_Builder.git
cd CV_Builder
```

### 2. Set Up a Virtual Environment

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

| Package | Version | Purpose |
|---|---|---|
| `reportlab` | ≥ 4.0.0 | PDF generation engine |
| `Pillow` | ≥ 10.0.0 | Profile image processing |
| `scholarly` | ≥ 1.7.0 | Google Scholar API *(optional)* |
| `requests` | ≥ 2.31.0 | HTTP requests for Scholar |
| `beautifulsoup4` | ≥ 4.12.0 | Web scraping for Scholar |
| `python-dateutil` | ≥ 2.8.0 | Date parsing for experience sorting |

### 4. Generate the CV

```bash
python cv_builder_final.py
```

The script will:
1. Load all content from `animesh_cv_data.json`
2. Detect the profile photo and prompt whether to include it
3. Build and save `Animesh_Choudhury_CV.pdf`

---

## Editing CV Content

All CV data lives in `animesh_cv_data.json`. Edit this file to update any section — no Python changes required.

### Personal Information

```json
"personal_info": {
  "name": "Your Full Name",
  "title": "Your Professional Title",
  "email": "your.email@example.com",
  "phone": "+91 XXXXXXXXXX",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourusername",
  "google_scholar": "https://scholar.google.com/citations?user=YOUR_ID",
  "scholar": "https://www.researchgate.net/profile/your-profile",
  "profile_image": "profileImage.png"
}
```

### Adding a Publication

```json
{
  "title": "Your Paper Title",
  "authors": "Author A, Author B, & Author C",
  "venue": "Journal Name",
  "year": 2025,
  "citations": 12,
  "type": "journal",
  "doi": "https://doi.org/10.xxxx/xxxxx"
}
```

> Papers with a `doi` field are rendered as **clickable blue hyperlinks** in the PDF.

### Adding a Conference Paper

```json
{
  "title": "Conference Presentation Title",
  "venue": "IEEE Conference on Example",
  "year": 2024,
  "url": "https://ieeexplore.ieee.org/..."
}
```

> Conference papers with a `url` field are also rendered as **clickable hyperlinks**.

### Adding Work Experience

```json
{
  "position": "Junior Research Fellow",
  "organization": "University Name",
  "location": "City, Country",
  "period": "15/02/2022 - 30/06/2025",
  "responsibilities": [
    "Key responsibility one",
    "Key responsibility two"
  ]
}
```

> Experience entries are **automatically sorted by end date** (most recent first). Use `"Current"` in the period string to keep an ongoing role pinned at the top.

---

## CV Sections

The generated PDF contains these sections, assembled in this order:

| # | Section | Description |
|---|---|---|
| 1 | **Header** | Profile photo, name, title, and clickable social/contact icons |
| 2 | **Professional Summary** | Research background overview |
| 3 | **Education** | Degrees with institution, location, year, and optional thesis title |
| 4 | **Work Experience** | Positions sorted by recency, with bullet-point responsibilities |
| 5 | **Selected Publications** | Journal articles with clickable DOI hyperlinks, sorted by year |
| 6 | **Conference Papers & Proceedings** | Presentations with clickable URL hyperlinks |
| 7 | **Technical Skills** | Categorized skill groups (e.g., ML & AI, Remote Sensing, GIS) |
| 8 | **Poster, Online Training, Webinar** | Combined section: poster presentations, training programs, and webinars |
| 9 | **Footer** | Auto-generated *Last updated: Month Year* timestamp |

---

## Customizing the Style

Open `cv_builder_final.py` and locate `_setup_custom_styles()` (around line 80) to adjust fonts, sizes, and colors.

The color palette is defined at the top of that method:

```python
primary_color   = colors.HexColor('#1a5490')  # Section headings and dividers
secondary_color = colors.HexColor('#2c3e50')  # Name and job titles
text_color      = colors.HexColor('#333333')  # Body text
light_gray      = colors.HexColor('#666666')  # Subtitles and metadata
```

| Style Name | Used For |
|---|---|
| `CVName` | Researcher's name in the header |
| `CVTitle` | Professional title subtitle |
| `CVContact` | Contact metadata |
| `CVSectionHeading` | Section labels (EDUCATION, SKILLS, etc.) |
| `CVBody` | General body text |
| `CVPublication` | Journal and conference paper entries |
| `CVJobTitle` | Position title or degree name |
| `CVOrganization` | Institution/organization name and location |
| `CVBullet` | Indented bullet points under experience entries |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: reportlab` | Run `pip install -r requirements.txt` |
| Icons not appearing in CV header | Check that all PNG files exist in `images/` |
| Profile image not shown | Verify the filename in `personal_info.profile_image` matches the actual file |
| PIL error during image processing | Run `pip install Pillow` |
| Experience entries not in expected order | Check date format in `"period"` — use `DD/MM/YYYY` or include `"Current"` for ongoing roles |

---

## Tips

- **Commit `animesh_cv_data.json`** — it is the single source of truth for all CV content; keep it version-controlled.
- **Use real brand logos** in `images/` for the most polished result — download from [icons8.com](https://icons8.com) or [flaticon.com](https://www.flaticon.com).
- **Square-crop your profile photo** before use — the builder crops automatically, but a pre-cropped image ensures the subject is centered correctly.
- **Maintain separate JSON files** (e.g., `cv_data_academic.json`, `cv_data_industry.json`) if you need multiple CV variants for different application contexts.

---

*Built with [ReportLab](https://www.reportlab.com/) · Designed for researchers in Earth & Atmospheric Sciences and beyond.*
