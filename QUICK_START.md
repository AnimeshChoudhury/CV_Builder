# Animesh's CV Builder - Quick Start Guide

## 📦 What You Have

1. **Animesh_Choudhury_CV.pdf** - Your generated CV
2. **cv_builder_v2.py** - Updated CV builder with profile image support
3. **animesh_cv_data.json** - Your CV data (easily editable)
4. **scholar_fetcher.py** - Google Scholar integration script
5. **README.md** - Detailed documentation

## 🚀 Quick Start

### 1. View Your Current CV
Open `Animesh_Choudhury_CV.pdf` to see your professional CV!

### 2. Make Changes
Edit `animesh_cv_data.json` to update any information:
- Personal details
- Work experience
- Publications
- Skills
- etc.

### 3. Regenerate CV
```bash
python cv_builder_v2.py
```

## 📸 Adding Your Profile Photo

### Step 1: Prepare Your Photo
- Use a professional headshot
- Square format works best (e.g., 500x500 pixels)
- Supported formats: JPG, PNG, JPEG
- File size: Keep under 2MB

### Step 2: Add Photo to Your Directory
Place your photo file (e.g., `animesh_photo.jpg`) in the same folder as the CV builder.

### Step 3: Update JSON File
Open `animesh_cv_data.json` and find the `personal_info` section:

```json
"personal_info": {
  "name": "Animesh Choudhury",
  "profile_image": "animesh_photo.jpg",  ← Add this line with your filename
  ...
}
```

### Step 4: Regenerate CV
```bash
python cv_builder_v2.py
```

When prompted "Include profile image in CV? (y/n)", press `y` or just Enter.

## 📚 Google Scholar Integration

### Automatic Publication Fetching

1. **Find Your Scholar ID**
   - Go to your Google Scholar profile
   - URL looks like: `https://scholar.google.com/citations?user=YOUR_ID`
   - Copy YOUR_ID part

2. **Install Required Package** (on your local machine)
   ```bash
   pip install scholarly
   ```

3. **Run the Fetcher**
   ```bash
   python scholar_fetcher.py
   ```
   
4. **Enter Your Scholar ID** when prompted

5. **Regenerate CV**
   ```bash
   python cv_builder_v2.py
   ```

## 📝 Editing Your Data

### Quick Tips

**Personal Info:**
```json
"personal_info": {
  "name": "Your Name",
  "title": "Your Professional Title",
  "email": "your.email@example.com",
  "phone": "+91 1234567890",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourusername",
  "profile_image": "your_photo.jpg"
}
```

**Adding Publications:**
```json
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
```

**Adding Experience:**
```json
"experience": [
  {
    "position": "Your Position",
    "organization": "Organization Name",
    "location": "City, Country",
    "period": "Jan 2020 - Present",
    "responsibilities": [
      "Responsibility 1",
      "Responsibility 2",
      "Responsibility 3"
    ]
  }
]
```

## 🎨 Customizing the Style

To change colors, fonts, or layout:

1. Open `cv_builder_v2.py`
2. Find the `_setup_custom_styles()` method (around line 90)
3. Modify:
   - `fontSize` - Text size
   - `textColor` - Color (use hex codes like `#2c3e50`)
   - `spaceAfter` - Spacing after elements
   - `fontName` - Font family

Example:
```python
self.styles.add(ParagraphStyle(
    name='CVSectionHeading',
    fontSize=14,  # Make section headers larger
    textColor=colors.HexColor('#1a5490'),  # Blue color
    ...
))
```

## 🔧 Troubleshooting

### Problem: Profile image not showing
**Solution:** 
- Check the file path is correct in JSON
- Make sure image file is in the same directory
- Try using a different image format (JPG or PNG)

### Problem: PDF generation fails
**Solution:**
```bash
pip install reportlab pillow
```

### Problem: Google Scholar fetching fails
**Solution:**
- Google may rate-limit requests
- Wait a few minutes and try again
- Manually add publications to JSON as fallback

## 📊 Creating Multiple CV Versions

### Academic CV (Full Version)
```bash
# Keep all publications and details
python cv_builder_v2.py
mv Animesh_Choudhury_CV.pdf Animesh_CV_Academic.pdf
```

### Industry CV (Short Version)
1. Edit JSON to include only relevant experience
2. Limit publications to 5 most impactful
3. Regenerate:
```bash
python cv_builder_v2.py
mv Animesh_Choudhury_CV.pdf Animesh_CV_Industry.pdf
```

### One-Page CV
1. Reduce experience descriptions to 1-2 bullet points
2. Include only top 3 publications
3. Remove less critical sections

## 📞 Next Steps

1. ✅ Add your profile photo
2. ✅ Update publications from Google Scholar
3. ✅ Review and edit all sections in JSON
4. ✅ Generate final CV
5. ✅ Keep JSON file updated as your career progresses

## 💡 Pro Tips

1. **Keep it Updated**: Run the Scholar fetcher monthly to update citations
2. **Version Control**: Keep different JSON files for different CV versions
3. **Backup**: Save your JSON file - it contains all your data
4. **Consistency**: Use the same format for all entries (e.g., date formats)
5. **Professional Photo**: Use a clear, professional headshot with good lighting

## 🌟 Your Current CV Includes

- ✅ All your work experience from 2018-present
- ✅ Education (B.Sc, M.Sc, PGD in RS&GIS)
- ✅ 3 journal publications
- ✅ 3 conference papers
- ✅ Technical skills (RS, GIS, Python, R, ML)
- ✅ Professional development activities
- ✅ Language proficiencies

---

**Questions or Issues?**
Edit the JSON file for data changes, or modify the Python script for style changes.

Good luck with your research career! 🚀
