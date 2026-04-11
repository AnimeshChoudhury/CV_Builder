# Academic CV Builder

A Python-based PDF CV generator for academic researchers. It builds a clean, publication-ready Curriculum Vitae from a single JSON data file — complete with a profile image, clickable DOI/URL links embedded in publication entries, social profile icon links, and an auto-sorted work experience section. No LaTeX or manual formatting required.

---

## Features

- **PDF generation** using [ReportLab](https://www.reportlab.com/) with precise, tight layout control
- **Profile image** embedded in the CV header with automatic square-crop and aspect-ratio handling
- **Clickable icons** in the header (email, phone/WhatsApp, LinkedIn, GitHub, Google Scholar, ResearchGate) using custom `ClickableImage` flowables
- **Clickable publication titles** — DOI/URL hyperlinks embedded directly in the PDF text
- **Auto-sorted work experience** — positions sorted chronologically by end date (most recent first); "Current" entries always appear at the top
- **JSON-driven content** — all CV data lives in a single editable JSON file; no code changes needed for content updates
- **Google Scholar integration** — optional script to auto-fetch publication list and citation counts
- **Modular section rendering** — each CV section is an independent method, making it easy to add, remove, or reorder sections

---

## Repository Structure

```
CV_Builder/
│
├── cv_builder_final.py           ← Primary CV builder (use this)
├── animesh_cv_data.json          ← CV content data (edit to update your CV)
├── scholar_fetcher.py            ← Fetches publications from Google Scholar
│
├── images/                       ← Clickable icon images used in CV header
│   ├── email.png
│   ├── phone.png
│   ├── linkedin.png
│   ├── github.png
│   ├── google_scholar.png
│   └── researchgate.png
│
├── profileImage.png              ← Profile photo embedded in the CV
├── requirements.txt              ← Python dependencies
│
├── check_logos.py                ← Utility: verifies icon files exist before building
├── generate_placeholder_icons.py ← Utility: generates letter-based placeholder icons
│
└── *.pdf                         ← Generated CV outputs
```

### Scripts Not Required to Build the CV

The following scripts are **utility/helper tools** and are **not part of the CV build pipeline**:

| Script | Purpose | Required to Build CV? |
|---|---|---|
| `check_logos.py` | Diagnoses which icon PNG files are present in `images/` | ❌ No — run before building if icons are missing |
| `generate_placeholder_icons.py` | Creates simple letter-based placeholder icons if real logos aren't available | ❌ No — one-time setup only |
| `scholar_fetcher.py` | Fetches publication data from Google Scholar and updates JSON | ❌ No — optional; run to keep publications updated |
| `cv_builder_v2.py` | Earlier iteration of the CV builder (no clickable icons, no date sorting) | ❌ No — superseded by `cv_builder_final.py` |
| `cv_builder_updated.py` | Intermediate iteration | ❌ No — superseded |

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

### 4. Verify Icon Files (Recommended)

Before generating the CV, confirm all icon images are in place:

```bash
python check_logos.py
```

If any icons are missing, either download them or generate placeholder icons:

```bash
python generate_placeholder_icons.py
```

### 5. Generate the CV

```bash
python cv_builder_final.py
```

The script will:
1. Load content from `animesh_cv_data.json`
2. Detect the profile image and prompt whether to include it
3. Build and save `Animesh_Choudhury_CV.pdf`

---

## Editing Your CV Content

All CV data is stored in `animesh_cv_data.json`. Edit this file to update any section — no Python changes needed.

### Personal Information

```json
"personal_info": {
  "name": "Your Full Name",
  "title": "PhD Researcher in ...",
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
  "venue": "Journal of Example Research",
  "year": 2025,
  "citations": 12,
  "type": "journal",
  "doi": "https://doi.org/10.xxxx/xxxxx"
}
```

> Publication titles with a `doi` field are rendered as **clickable blue hyperlinks** in the PDF.

### Adding a Conference Paper

```json
{
  "title": "Conference Presentation Title",
  "venue": "IEEE Conference on Example",
  "year": 2024,
  "url": "https://ieeexplore.ieee.org/..."
}
```

> Conference paper titles with a `url` field are also rendered as **clickable hyperlinks**.

### Adding Work Experience

```json
{
  "position": "Junior Research Fellow",
  "organization": "University Name",
  "location": "City, Country",
  "period": "15/02/2022 - 30/06/2025",
  "responsibilities": [
    "Responsibility point one",
    "Responsibility point two"
  ]
}
```

> Experience entries are **automatically sorted by end date** (most recent first). Use `"Current"` in the period string to pin ongoing positions to the top.

---

## CV Sections

The generated PDF contains these sections, assembled in order:

1. **Header** — Profile photo, name, title, and clickable social/contact icons
2. **Professional Summary** — Research overview paragraph
3. **Education** — Degrees with institution, location, year, and optional thesis title
4. **Work Experience** — Positions sorted by recency, with bullet-point responsibilities
5. **Selected Publications** — Journal articles with clickable DOI hyperlinks, sorted by year
6. **Conference Papers & Proceedings** — Presentations with clickable URL hyperlinks
7. **Technical Skills** — Categorized skill groups (e.g., ML & AI, Remote Sensing, GIS)
8. **Poster, Online Training, Webinar** — Combined section covering poster presentations, training programs, and webinars
9. **Footer** — Auto-generated `Last updated: Month Year` timestamp

---

## Google Scholar Integration

Use `scholar_fetcher.py` to automatically pull your full publication list with citation counts from Google Scholar.

### Find Your Scholar ID

```
https://scholar.google.com/citations?user=YOUR_ID_HERE&hl=en
                                             ^^^^^^^^^^^
                                         Copy this part
```

### Run the Fetcher

```bash
python scholar_fetcher.py
```

Enter your Scholar ID or full profile URL when prompted. The script:
- Fetches all publications (title, venue, year, citations)
- Sorts them by year (most recent first)
- Updates `animesh_cv_data.json` automatically

Then regenerate your CV:

```bash
python cv_builder_final.py
```

> **Rate Limiting:** The fetcher adds a configurable delay (default: 2 seconds per publication) to avoid Google Scholar rate limits. If you encounter errors, wait 10–15 minutes before retrying.

---

## Customizing Styles

Open `cv_builder_final.py` and locate `_setup_custom_styles()` (around line 80) to adjust fonts, sizes, and colors.

The color scheme is defined at the top of that method:

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
| `CVContact` | Contact metadata lines |
| `CVSectionHeading` | Section labels (EDUCATION, SKILLS, etc.) |
| `CVBody` | General body text and summary |
| `CVPublication` | Journal and conference paper entries |
| `CVJobTitle` | Position title or degree name |
| `CVOrganization` | Institution/organization and location |
| `CVBullet` | Indented bullet points under experience entries |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: reportlab` | Run `pip install -r requirements.txt` |
| Icons not appearing in CV header | Run `python check_logos.py` to identify missing files |
| Profile image not shown | Verify the filename in `personal_info.profile_image` matches the actual file |
| `PIL` error during image processing | Run `pip install Pillow` |
| Scholar fetcher blocked by Google | Wait 10–15 minutes; increase request delay at the prompt |
| Experience entries not in expected order | Check date format in `"period"` — use `DD/MM/YYYY` or include `"Current"` for ongoing roles |
| PDF content cut off or overlapping | Reduce content in a section or check `leftMargin`/`rightMargin` in `build_cv()` |

---

## Tips

- **Commit `animesh_cv_data.json` to version control** — it is your single source of truth for all CV content.
- **Run `scholar_fetcher.py` periodically** to keep citation counts current without manual editing.
- **Use separate JSON files** (e.g., `cv_data_academic.json`, `cv_data_industry.json`) to maintain multiple CV variants for different application contexts.
- **Use high-resolution real logos** in `images/` — replace placeholder icons with actual brand logos from [icons8.com](https://icons8.com) or [flaticon.com](https://www.flaticon.com) for a more polished result.
- **Square-crop your profile photo** before using it — the builder crops to a square automatically, but a pre-cropped image ensures the subject is correctly centered.

---

*Built with [ReportLab](https://www.reportlab.com/) · Designed for researchers in Earth & Atmospheric Sciences and beyond.*
