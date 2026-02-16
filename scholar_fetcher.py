"""
Google Scholar Integration for CV Builder
Fetches publications from Google Scholar profile

NOTE: This requires the 'scholarly' package to be installed:
      pip install scholarly

This script can be run separately to fetch your publications and save them
to the cv_data.json file.
"""

import json
import os
import time


def fetch_scholar_publications(scholar_id, delay=2):
    """
    Fetch publications from Google Scholar profile
    
    Args:
        scholar_id: Your Google Scholar user ID (from your profile URL)
                   Example: scholar.google.com/citations?user=YOUR_ID_HERE
        delay: Delay in seconds between requests (default: 2)
    
    Returns:
        List of publication dictionaries
    """
    try:
        from scholarly import scholarly
        
        print(f"\n{'='*70}")
        print(f"Fetching publications for Scholar ID: {scholar_id}")
        print(f"{'='*70}")
        print("\nThis may take 1-2 minutes depending on number of publications...")
        print("Please be patient - we add delays to avoid being blocked by Google.\n")
        
        # Search for the author
        try:
            author = scholarly.search_author_id(scholar_id)
        except Exception as e:
            print(f"\n❌ Error: Could not find author with ID '{scholar_id}'")
            print("Please check that:")
            print("  1. Your Scholar ID is correct")
            print("  2. Your Google Scholar profile is public")
            print("  3. You have internet connection")
            return []
        
        # Fill author information
        print(f"✓ Found author profile")
        author = scholarly.fill(author, sections=['publications'])
        
        print(f"✓ Author: {author.get('name', 'Unknown')}")
        print(f"✓ Affiliation: {author.get('affiliation', 'N/A')}")
        print(f"✓ Total publications found: {len(author.get('publications', []))}\n")
        
        publications = []
        total = len(author.get('publications', []))
        
        for idx, pub in enumerate(author['publications'], 1):
            # Fill in details for each publication
            try:
                print(f"[{idx}/{total}] Fetching details...", end=" ")
                filled_pub = scholarly.fill(pub)
                
                # Extract relevant information
                pub_data = {
                    "title": filled_pub['bib'].get('title', 'Untitled'),
                    "authors": filled_pub['bib'].get('author', 'Unknown'),
                    "venue": filled_pub['bib'].get('venue', filled_pub['bib'].get('journal', 'Unknown venue')),
                    "year": int(filled_pub['bib'].get('pub_year', 0)) if filled_pub['bib'].get('pub_year') else 0,
                    "citations": filled_pub.get('num_citations', 0),
                    "type": "journal" if 'journal' in filled_pub['bib'] else "conference"
                }
                
                publications.append(pub_data)
                print(f"✓ {pub_data['title'][:50]}... ({pub_data['year']}, {pub_data['citations']} citations)")
                
                # Add delay to avoid rate limiting
                if idx < total:
                    time.sleep(delay)
                
            except Exception as e:
                print(f"✗ Error: {e}")
                continue
        
        # Sort by year (most recent first)
        publications.sort(key=lambda x: x['year'], reverse=True)
        
        print(f"\n{'='*70}")
        print(f"✓ Successfully fetched {len(publications)} publications")
        print(f"{'='*70}\n")
        return publications
        
    except ImportError:
        print("\n❌ ERROR: 'scholarly' package not installed.")
        print("\nPlease install it using:")
        print("  pip install scholarly")
        print("\nOr install all requirements:")
        print("  pip install -r requirements.txt")
        return []
    except Exception as e:
        print(f"\n❌ ERROR: Failed to fetch publications from Google Scholar")
        print(f"Error details: {e}")
        print("\nPossible reasons:")
        print("  1. Google Scholar is rate-limiting requests (wait 10-15 minutes and try again)")
        print("  2. Internet connection issues")
        print("  3. Your Scholar profile is not public")
        print("\nYou can manually add publications to animesh_cv_data.json as an alternative.")
        return []


def update_cv_with_scholar_data(scholar_id, json_file="animesh_cv_data.json", delay=2):
    """
    Fetch publications from Google Scholar and update cv_data.json
    
    Args:
        scholar_id: Your Google Scholar user ID
        json_file: Path to cv_data.json file
        delay: Delay between requests in seconds
    """
    # Fetch publications
    publications = fetch_scholar_publications(scholar_id, delay)
    
    if not publications:
        print("\n❌ No publications fetched. CV data not updated.")
        print("\nTroubleshooting:")
        print("  1. Check your Scholar ID is correct")
        print("  2. Make sure your Google Scholar profile is public")
        print("  3. Wait 10-15 minutes if you've been rate-limited")
        print("  4. Try using a VPN if the problem persists")
        return False
    
    # Load existing CV data
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            cv_data = json.load(f)
    else:
        print(f"\n❌ ERROR: {json_file} not found.")
        print("Please make sure you're in the correct directory.")
        print("The file should be in the same folder as this script.")
        return False
    
    # Backup original publications
    original_pubs = cv_data.get('publications', [])
    
    # Update publications
    cv_data['publications'] = publications
    
    # Save updated data
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cv_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*70}")
        print(f"✓ SUCCESS!")
        print(f"{'='*70}")
        print(f"✓ CV data updated with {len(publications)} publications")
        print(f"✓ Saved to {json_file}")
        print(f"\nNext steps:")
        print(f"  1. Review the updated publications in {json_file}")
        print(f"  2. Run: python cv_builder_v2.py")
        print(f"  3. Check your generated CV PDF")
        print(f"\n💡 Tip: Run this script monthly to keep citation counts updated!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to save updated CV data: {e}")
        # Restore original publications
        cv_data['publications'] = original_pubs
        return False


def get_scholar_id_from_url(url):
    """
    Extract Scholar ID from Google Scholar profile URL
    
    Args:
        url: Full Google Scholar profile URL
        
    Returns:
        Scholar ID string
    """
    if "user=" in url:
        scholar_id = url.split("user=")[1].split("&")[0]
        return scholar_id
    return url


def main():
    """Main function for Google Scholar integration"""
    print("\n" + "="*70)
    print(" "*15 + "Google Scholar Publications Fetcher")
    print("="*70)
    
    print("\n📚 This script will:")
    print("  1. Connect to your Google Scholar profile")
    print("  2. Fetch all your publications")
    print("  3. Get citation counts for each paper")
    print("  4. Update your animesh_cv_data.json file")
    print("  5. Preserve all other CV data")
    
    print("\n" + "-"*70)
    print("HOW TO FIND YOUR SCHOLAR ID:")
    print("-"*70)
    print("1. Go to your Google Scholar profile in a web browser")
    print("2. Look at the URL in the address bar")
    print("3. The URL looks like:")
    print("   https://scholar.google.com/citations?user=YOUR_ID_HERE&hl=en")
    print("4. Copy the YOUR_ID_HERE part (after 'user=' and before '&')")
    print("\nExample:")
    print("  URL: https://scholar.google.com/citations?user=abc123XYZ&hl=en")
    print("  Scholar ID: abc123XYZ")
    
    print("\n" + "-"*70)
    scholar_input = input("\nEnter your Google Scholar ID or full profile URL: ").strip()
    
    if not scholar_input:
        print("\n❌ ERROR: No Scholar ID provided.")
        return
    
    # Extract ID from URL if full URL was provided
    scholar_id = get_scholar_id_from_url(scholar_input)
    
    print(f"\n✓ Using Scholar ID: {scholar_id}")
    confirm = input("Is this correct? (y/n, default=y): ").lower()
    
    if confirm == 'n':
        print("\n❌ Cancelled by user.")
        return
    
    # Ask about delay
    print("\n" + "-"*70)
    print("RATE LIMITING PROTECTION:")
    print("-"*70)
    print("To avoid being blocked by Google Scholar, we add delays between requests.")
    print("Recommended: 2-3 seconds per publication")
    
    delay_input = input("Enter delay in seconds (default=2): ").strip()
    try:
        delay = int(delay_input) if delay_input else 2
        if delay < 1:
            delay = 2
    except:
        delay = 2
    
    print(f"\n✓ Using {delay} second delay between requests")
    
    # Fetch and update
    success = update_cv_with_scholar_data(scholar_id, delay=delay)
    
    if not success:
        print("\n" + "="*70)
        print("ALTERNATIVE: Manual Entry")
        print("="*70)
        print("If automatic fetching doesn't work, you can manually add publications")
        print("to animesh_cv_data.json using this format:")
        print("""
{
  "publications": [
    {
      "title": "Your Paper Title",
      "authors": "Author1, Author2, Author3",
      "venue": "Journal or Conference Name",
      "year": 2024,
      "citations": 100,
      "type": "journal",
      "doi": "https://doi.org/10.xxxx/xxxxx"
    }
  ]
}
        """)


if __name__ == "__main__":
    main()
