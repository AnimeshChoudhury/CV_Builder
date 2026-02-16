# Professional CV Builder for Researchers

A Python-based CV generator that creates professional PDFs with automatic Google Scholar publication integration.

## Features

✅ Clean, professional CV layout  
✅ Google Scholar publication import  
✅ Easy customization via JSON file  
✅ Automatic citation counts  
✅ Professional formatting  
✅ Support for multiple sections (Education, Experience, Publications, Skills, Awards, Service)

## Installation

### Required Packages

```bash
pip install reportlab
```

### Optional (for Google Scholar integration)

```bash
pip install scholarly
```

## Quick Start

### 1. Generate Your First CV

```bash
python cv_builder.py
```

This will:
- Create a `cv_data.json` file with template data
- Generate a `professional_cv.pdf` with sample content

### 2. Customize Your Data

Edit `cv_data.json` with your personal information:

```json
{
  "personal_info": {
    "name": "Your Name",
    "title": "Your Title",
    "email": "your.email@example.com",
    ...
  },
  "education": [...],
  "experience": [...],
  "publications": [...],
  ...
}
```

### 3. Regenerate CV

After editing the JSON file:

```bash
python cv_builder.py
```

Your CV will be regenerated with your updated information.

## Google Scholar Integration

### Automatic Publication Fetching

1. Find your Google Scholar profile URL:
   - Example: `https://scholar.google.com/citations?user=ABC123`
   - Your Scholar ID is the part after `user=` (e.g., `ABC123`)

2. Run the Scholar fetcher:

```bash
python scholar_fetcher.py
```

3. Enter your Scholar ID when prompted

4. The script will:
   - Fetch all your publications
   - Get citation counts
   - Update `cv_data.json` automatically

5. Regenerate your CV:

```bash
python cv_builder.py
```

### Manual Scholar Integration

You can also manually update your Scholar URL in `cv_data.json`:

```json
{
  "personal_info": {
    "scholar": "scholar.google.com/citations?user=YOUR_ID"
  }
}
```

## File Structure

```
├── cv_builder.py          # Main CV generator script
├── scholar_fetcher.py     # Google Scholar integration
├── cv_data.json          # Your CV data (editable)
└── professional_cv.pdf   # Generated CV output
```

## Customization Guide

### Adding Sections

The CV includes these sections:
- **Professional Summary**: Brief overview
- **Education**: Degrees and institutions
- **Professional Experience**: Work history
- **Selected Publications**: Research papers
- **Technical Skills & Expertise**: Skills by category
- **Awards & Honors**: Recognition
- **Professional Service**: Committee work, reviewing, etc.

### Publication Format

Publications are automatically formatted as:

```
[1] Authors. "Title." Venue, Year. [Citations: X]
```

### Styling

To customize the appearance, edit the `_setup_custom_styles()` method in `cv_builder.py`:

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

```bash
# Academic CV
python cv_builder.py

# Industry CV (edit cv_data.json to focus on applied work)
python cv_builder.py

# Short CV
# Edit cv_data.json to include only recent highlights
python cv_builder.py
```

## Troubleshooting

### Google Scholar Issues

If `scholar_fetcher.py` fails:
- Google Scholar may rate-limit requests
- Try again after a few minutes
- Alternatively, manually add publications to `cv_data.json`

### PDF Generation Issues

If PDF generation fails:
- Ensure `reportlab` is installed: `pip install reportlab`
- Check file permissions in the output directory
- Verify JSON file is valid (use a JSON validator)

### Character Encoding

For non-ASCII characters (accents, special symbols):
- The scripts use UTF-8 encoding
- Ensure your JSON file is saved as UTF-8

## Advanced Usage

### Batch Processing

Create multiple CVs at once:

```python
from cv_builder import CVData, CVBuilder

# Load data
cv_data = CVData()
cv_data.load_from_json("cv_data.json")

# Generate different versions
builder = CVBuilder(cv_data)
builder.build_cv("cv_full.pdf")

# Modify for short version
cv_data.publications = cv_data.publications[:5]  # Top 5 papers
builder = CVBuilder(cv_data)
builder.build_cv("cv_short.pdf")
```

### Custom Formatting

You can extend the `CVBuilder` class to add custom sections:

```python
def _add_custom_section(self, story):
    self._add_section_header(story, "CUSTOM SECTION")
    # Add your content here
```

## Support

For issues or questions:
- Edit the JSON file for data changes
- Edit `cv_builder.py` for styling changes
- Run `scholar_fetcher.py` for publication updates

## License

Free to use and modify for personal and professional purposes.
