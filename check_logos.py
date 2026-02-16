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

# Required logo files
required_logos = [
    'email.png',
    'phone.png',
    'linkedin.png',
    'github.png',
    'scholar.png',  # or researchgate.png
]

print("\n" + "-" * 70)
print("Checking for logo files:")
print("-" * 70)

found_count = 0
missing_files = []

for logo in required_logos:
    if os.path.exists(logo):
        file_size = os.path.getsize(logo)
        print(f"✓ {logo:<20} - Found ({file_size} bytes)")
        found_count += 1
    else:
        print(f"✗ {logo:<20} - NOT FOUND")
        missing_files.append(logo)

# Check for alternative names
print("\n" + "-" * 70)
print("Checking for alternative names:")
print("-" * 70)

alternatives = {
    'researchgate.png': 'Alternative to scholar.png',
    'google-scholar.png': 'Alternative to scholar.png',
    'mail.png': 'Alternative to email.png',
    'telephone.png': 'Alternative to phone.png',
}

for alt_file, description in alternatives.items():
    if os.path.exists(alt_file):
        file_size = os.path.getsize(alt_file)
        print(f"✓ {alt_file:<25} - Found ({description})")
        found_count += 1

# List all PNG files in directory
print("\n" + "-" * 70)
print("All PNG files in current directory:")
print("-" * 70)

png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]
if png_files:
    for png_file in png_files:
        file_size = os.path.getsize(png_file)
        print(f"  - {png_file} ({file_size} bytes)")
else:
    print("  No PNG files found in current directory")

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
    print("  2. Save them in the same folder as cv_builder_professional.py")
    print("  3. Make sure the filenames match exactly:")
    for logo in required_logos:
        print(f"     - {logo}")

print("\n" + "=" * 70)
print("LOGO FILE REQUIREMENTS")
print("=" * 70)
print("Format: PNG (transparent background recommended)")
print("Size: 16x16 to 64x64 pixels (small icons work best)")
print("Location: Same folder as cv_builder_professional.py")
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
