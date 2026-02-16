"""
Logo Files Checker - Verify your logo files are in the right place
"""

import os

print("=" * 70)
print("CV Logo Files Diagnostic")
print("=" * 70)

# Get current directory
current_dir = os.getcwd()
print(f"\nCurrent directory: {current_dir}")

# Required logo files (in images folder)
required_logos = [
    'images/email.png',
    'images/phone.png',
    'images/linkedin.png',
    'images/github.png',
    'images/scholar.png',  # or researchgate.png
]

print("\n" + "-" * 70)
print("Checking for logo files:")
print("-" * 70)

found_count = 0
missing_files = []

for logo in required_logos:
    if os.path.exists(logo):
        file_size = os.path.getsize(logo)
        print(f"✓ {logo:<25} - Found ({file_size} bytes)")
        found_count += 1
    else:
        print(f"✗ {logo:<25} - NOT FOUND")
        missing_files.append(logo)

# Check for alternative names
print("\n" + "-" * 70)
print("Checking for alternative names:")
print("-" * 70)

alternatives = {
    'images/researchgate.png': 'Alternative to scholar.png',
    'images/google-scholar.png': 'Alternative to scholar.png',
    'images/mail.png': 'Alternative to email.png',
    'images/telephone.png': 'Alternative to phone.png',
}

for alt_file, description in alternatives.items():
    if os.path.exists(alt_file):
        file_size = os.path.getsize(alt_file)
        print(f"✓ {alt_file:<30} - Found ({description})")
        found_count += 1

# List all PNG files in images directory
print("\n" + "-" * 70)
print("All PNG files in images directory:")
print("-" * 70)

if os.path.exists('images'):
    png_files = [f for f in os.listdir('images') if f.lower().endswith('.png')]
    if png_files:
        for png_file in png_files:
            file_size = os.path.getsize(f'images/{png_file}')
            print(f"  - images/{png_file} ({file_size} bytes)")
    else:
        print("  No PNG files found in images directory")
else:
    print("  Images directory not found")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if found_count >= 4:
    print(f"✓ Good! Found {found_count} logo files")
    print("  You can now generate your CV with logo icons!")
else:
    print(f"⚠ Only found {found_count} logo files")
    print(f"  Missing: {', '.join(missing_files)}")
    print("\nWhat to do:")
    print("  1. Download or create logo PNG files (16x16 to 64x64 pixels)")
    print("  2. Save them in the images folder")
    print("  3. Make sure the filenames match exactly:")
    for logo in required_logos:
        print(f"     - {logo}")

print("\n" + "=" * 70)
print("LOGO FILE REQUIREMENTS")
print("=" * 70)
print("Format: PNG (transparent background recommended)")
print("Size: 16x16 to 64x64 pixels (small icons work best)")
print("Location: images/ folder")
print("\nFree icon sources:")
print("  - https://icons8.com (search for email, phone, linkedin, github)")
print("  - https://www.flaticon.com")
print("  - https://fontawesome.com/icons")
print("\nOr create simple colored squares with letters:")
print("  - E (for email)")
print("  - P (for phone)")
print("  - L (for LinkedIn)")
print("  - G (for GitHub)")
print("  - S (for Scholar)")

print("\n" + "=" * 70)
