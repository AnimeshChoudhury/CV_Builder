"""
Generate Simple Placeholder Logo Icons
Creates basic colored square icons with letters if you don't have logo files
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_icon(letter, color, filename, size=64):
    """Create a simple square icon with a letter"""
    # Create image with colored background
    img = Image.new('RGB', (size, size), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        # This will work on most systems
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(size * 0.6))
    except:
        try:
            font = ImageFont.truetype("arial.ttf", int(size * 0.6))
        except:
            font = ImageFont.load_default()
    
    # Draw white letter in center
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - bbox[1]
    
    draw.text((x, y), letter, fill='white', font=font)
    
    # Save
    img.save(filename)
    print(f"✓ Created {filename}")

def main():
    print("=" * 70)
    print("Simple Logo Icon Generator")
    print("=" * 70)
    print("\nThis script creates basic placeholder icons for your CV.")
    print("You can replace these with professional logos later.")
    
    print("\n" + "-" * 70)
    print("Creating icons...")
    print("-" * 70 + "\n")
    
    # Define icons with colors
    icons = [
        ('E', (220, 78, 65), 'email.png'),       # Red for email
        ('P', (76, 175, 80), 'phone.png'),       # Green for phone
        ('L', (0, 119, 181), 'linkedin.png'),    # LinkedIn blue
        ('G', (51, 51, 51), 'github.png'),       # Dark gray for GitHub
        ('S', (66, 133, 244), 'scholar.png'),    # Google blue for Scholar
    ]
    
    for letter, color, filename in icons:
        if os.path.exists(filename):
            choice = input(f"{filename} already exists. Overwrite? (y/n): ")
            if choice.lower() != 'y':
                print(f"  Skipped {filename}")
                continue
        
        create_simple_icon(letter, color, filename)
    
    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)
    print("\n✓ Logo icons created successfully!")
    print("\nYou can now run: python cv_builder_professional.py")
    print("\nThese are basic placeholder icons. For a more professional look:")
    print("  1. Download actual logo images from:")
    print("     - https://icons8.com")
    print("     - https://www.flaticon.com")
    print("  2. Replace the generated PNG files")
    print("  3. Regenerate your CV")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
        main()
    except ImportError:
        print("\n" + "=" * 70)
        print("ERROR: Pillow (PIL) not installed")
        print("=" * 70)
        print("\nPlease install Pillow:")
        print("  pip install Pillow")
        print("\nThen run this script again.")
        print("=" * 70)
