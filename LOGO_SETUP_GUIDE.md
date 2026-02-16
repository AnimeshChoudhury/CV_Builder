# Adding Logo Icons to Your CV - Complete Guide

## 📋 Quick Summary

The CV builder now supports **clickable logo icons** for your contact information. All logos should be in the **same folder** as `cv_builder_professional.py`.

## 🎯 What You Need

### Required Logo Files:
1. **email.png** - Email/envelope icon
2. **phone.png** - Phone icon
3. **linkedin.png** - LinkedIn logo
4. **github.png** - GitHub logo
5. **scholar.png** OR **researchgate.png** - Your research profile logo

## 📁 File Location

```
your-cv-folder/
├── cv_builder_professional.py
├── animesh_cv_data.json
├── email.png          ← Put your logos here
├── phone.png          ← Same folder as the script
├── linkedin.png       ← Not in a subfolder
├── github.png         ← Same directory level
└── scholar.png        ← Same location
```

**IMPORTANT**: The logo files MUST be in the **exact same folder** as `cv_builder_professional.py`!

## ⚙️ Logo Specifications

### Format:
- **File type**: PNG (preferred) or JPG
- **Transparency**: Transparent background works best
- **Colors**: Any color (will be displayed as-is)

### Size:
- **Recommended**: 32x32 to 64x64 pixels
- **Minimum**: 16x16 pixels
- **Maximum**: 128x128 pixels (larger files load slower)
- **File size**: Keep under 50KB each

### Quality:
- Clear, recognizable icons
- High contrast (icon vs background)
- Professional appearance

## 🔍 Checking Your Setup

### Step 1: Run the Diagnostic Script

```bash
python check_logos.py
```

This will tell you:
- ✓ Which logo files are found
- ✗ Which logo files are missing
- 📂 All PNG files in your folder

### Example Output:
```
Checking for logo files:
✓ email.png          - Found (2847 bytes)
✓ phone.png          - Found (3142 bytes)
✓ linkedin.png       - Found (4521 bytes)
✓ github.png         - Found (3876 bytes)
✓ scholar.png        - Found (4102 bytes)

SUMMARY: Good! Found 5 logo files
```

## 🎨 Option 1: Use Your Own Logos

### Where to Get Professional Logos:

1. **Icons8** (https://icons8.com)
   - Search for: email, phone, linkedin, github
   - Download as PNG, 64x64 pixels
   - Free for personal use

2. **Flaticon** (https://www.flaticon.com)
   - Search for social media icons
   - Download individual PNG files
   - Check license (most are free with attribution)

3. **Font Awesome** (https://fontawesome.com/icons)
   - Search for icons
   - Download as PNG
   - Free tier available

4. **Official Brand Logos**:
   - LinkedIn: https://brand.linkedin.com/downloads
   - GitHub: https://github.com/logos

### Download Steps:
1. Download each icon as PNG
2. Rename to match required names (email.png, phone.png, etc.)
3. Place in same folder as cv_builder_professional.py
4. Run: `python check_logos.py` to verify
5. Generate CV: `python cv_builder_professional.py`

## 🎨 Option 2: Generate Simple Placeholder Icons

If you want to quickly test or don't have logo files yet:

```bash
python generate_placeholder_icons.py
```

This creates simple colored squares with letters:
- **E** on red background (email.png)
- **P** on green background (phone.png)
- **L** on blue background (linkedin.png)
- **G** on gray background (github.png)
- **S** on blue background (scholar.png)

**Note**: These are basic placeholders. Replace with professional logos for best results.

## 🔗 How Clickable Logos Work

### In Your CV:
```
[Name]
[Title]
[📧] [📱] [💼] [⚡] [🎓]  ← Clickable logo icons
email@example.com | +91 1234567890
```

### When Clicked:
- **Email icon** → Opens email client with your address
- **Phone icon** → Display only (not clickable)
- **LinkedIn icon** → Opens your LinkedIn profile
- **GitHub icon** → Opens your GitHub profile
- **Scholar icon** → Opens your ResearchGate/Google Scholar

## 🛠️ Troubleshooting

### Problem: "Icon file not found" warnings

**Solution 1**: Check file location
```bash
# Make sure you're in the right directory
pwd

# List PNG files
ls -la *.png
```

**Solution 2**: Check file names (case-sensitive!)
```
✓ Correct: email.png
✗ Wrong:   Email.png
✗ Wrong:   EMAIL.png
✗ Wrong:   email.PNG
```

**Solution 3**: Verify files exist
```bash
python check_logos.py
```

### Problem: Icons are too large/small in PDF

**Solution**: Edit the icon size in `cv_builder_professional.py`

Find this line:
```python
def _create_clickable_icon(self, icon_file, link_url, icon_size=0.14):
```

Change `icon_size`:
- `0.10` = Smaller icons
- `0.14` = Default size (recommended)
- `0.20` = Larger icons

### Problem: Icons not clickable in PDF

**Check**:
1. Open PDF in a proper PDF reader (Adobe, Preview, Chrome)
2. Some basic viewers don't support clickable links
3. Make sure URLs are correct in animesh_cv_data.json

### Problem: Wrong logo appears

**Solution**: Check filename spelling
- For ResearchGate: Use `scholar.png` OR `researchgate.png`
- Script tries `scholar.png` first, then `researchgate.png`

## 📝 Complete Workflow

### First Time Setup:

```bash
# 1. Get logo files (choose one method):

# Method A: Download professional logos manually
# - Visit icons8.com or flaticon.com
# - Download email.png, phone.png, linkedin.png, github.png, scholar.png
# - Save in same folder as cv_builder_professional.py

# Method B: Generate simple placeholders
python generate_placeholder_icons.py

# 2. Verify logos are in place
python check_logos.py

# 3. Generate your CV
python cv_builder_professional.py

# 4. Check the PDF
# - Open Animesh_Choudhury_CV.pdf
# - Look for icons in header
# - Click each icon to test
```

### Updating Logos Later:

```bash
# 1. Replace PNG files with new ones
# 2. Keep same filenames
# 3. Regenerate CV
python cv_builder_professional.py
```

## 🎯 Best Practices

1. **Use official brand logos** for LinkedIn and GitHub
2. **Consistent style** - all icons should have similar style
3. **Transparent backgrounds** for professional look
4. **Small file sizes** for faster PDF generation
5. **Test clickability** after generating PDF

## 📊 Example: High-Quality Setup

```
✓ Professional Setup:
  - Official LinkedIn logo (blue, 64x64px)
  - Official GitHub logo (black, 64x64px)
  - Material Design icons for email/phone
  - Google Scholar icon or ResearchGate logo
  - All with transparent backgrounds
  - Consistent visual style

✗ Avoid:
  - Mixed styles (cartoon + realistic)
  - Low resolution (pixelated icons)
  - Different sizes (16px mixed with 128px)
  - Heavy file sizes (>100KB per icon)
```

## 🔄 Workflow Summary

```
1. Download logos → Save as PNG → Place in folder
         ↓
2. Run check_logos.py → Verify all files found
         ↓
3. Run cv_builder_professional.py → Generate CV
         ↓
4. Open PDF → Test clickable icons → Done!
```

## 💡 Pro Tips

1. **Backup your logos** - keep a copy in cloud storage
2. **Version control** - if using Git, commit logo files
3. **Alternative names** - Script checks for both scholar.png and researchgate.png
4. **Optimization** - Use tools like TinyPNG to reduce file sizes
5. **Testing** - Always test the clickable links in the final PDF

## 🆘 Still Having Issues?

Run the diagnostic script for detailed information:
```bash
python check_logos.py
```

If issues persist:
1. Check you're in the correct folder
2. Verify file permissions (files should be readable)
3. Make sure PNG files are valid (open them in image viewer)
4. Try the placeholder generator as a test
5. Check that file names match exactly (case-sensitive)

---

**Remember**: The logo files must be in the **same folder** as your Python script!
