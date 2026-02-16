# Google Scholar Integration - Step-by-Step Guide

## Prerequisites

Make sure you have installed the required packages:
```bash
pip install scholarly requests beautifulsoup4
```

## Step 1: Find Your Google Scholar ID

1. Go to your Google Scholar profile
2. Look at the URL in your browser
3. It will look like: `https://scholar.google.com/citations?user=YOUR_ID_HERE&hl=en`
4. Copy the `YOUR_ID_HERE` part (this is your Scholar ID)

**Example:**
- URL: `https://scholar.google.com/citations?user=abc123XYZ&hl=en`
- Scholar ID: `abc123XYZ`

## Step 2: Update Your CV Data JSON

Open `animesh_cv_data.json` and update the scholar field:

```json
{
  "personal_info": {
    "name": "Animesh Choudhury",
    "scholar": "YOUR_SCHOLAR_ID_HERE",
    ...
  }
}
```

**OR** if you prefer the full URL:
```json
"scholar": "https://scholar.google.com/citations?user=YOUR_ID"
```

## Step 3: Run the Scholar Fetcher

### Method A: Using the scholar_fetcher.py script

```bash
python scholar_fetcher.py
```

When prompted, enter your Scholar ID or full profile URL.

The script will:
- ✅ Fetch all your publications
- ✅ Get citation counts for each paper
- ✅ Automatically update `animesh_cv_data.json`
- ✅ Preserve all other CV data

### Method B: Using Python directly

Create a test script to fetch your data:

```python
from scholarly import scholarly

# Replace with your actual Scholar ID
scholar_id = "YOUR_SCHOLAR_ID_HERE"

# Fetch author profile
author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=['publications'])

print(f"Found: {author['name']}")
print(f"Total publications: {len(author['publications'])}")

# Display first publication as example
if author['publications']:
    first_pub = scholarly.fill(author['publications'][0])
    print(f"\nFirst publication:")
    print(f"  Title: {first_pub['bib']['title']}")
    print(f"  Year: {first_pub['bib'].get('pub_year', 'N/A')}")
    print(f"  Citations: {first_pub.get('num_citations', 0)}")
```

## Step 4: Regenerate Your CV

After the publications are fetched and saved:

```bash
python cv_builder_v2.py
```

Your CV will now include all publications with citation counts from Google Scholar!

## Common Issues and Solutions

### Issue 1: "scholarly" module not found

**Solution:**
```bash
pip install scholarly
```

### Issue 2: "Failed to fetch publications" or timeout errors

**Cause:** Google Scholar rate-limits requests to prevent scraping.

**Solutions:**
1. **Wait and retry**: Wait 5-10 minutes and try again
2. **Use a VPN**: Sometimes changing your IP helps
3. **Run during off-peak hours**: Less traffic means less rate limiting
4. **Be patient**: The scholarly package is slow by design to avoid detection

### Issue 3: Some publications are missing

**Cause:** The scholarly package might not fetch all publications or some data might be incomplete.

**Solutions:**
1. Check if all publications are visible on your Scholar profile
2. Manually add missing publications to the JSON file
3. Try fetching again later

### Issue 4: Citation counts are zero or incorrect

**Cause:** Citations might not be publicly visible or the data hasn't updated.

**Solutions:**
1. Check your Google Scholar profile settings (make sure it's public)
2. Wait a few hours - Scholar data updates periodically
3. Manually update citation counts in the JSON file

## Manual Alternative

If Google Scholar fetching doesn't work, you can manually add publications to your JSON:

```json
"publications": [
  {
    "title": "Your Paper Title",
    "authors": "Choudhury A, Author2, Author3",
    "venue": "Journal Name",
    "year": 2024,
    "citations": 150,
    "type": "journal",
    "doi": "https://doi.org/10.xxxx/xxxxx"
  }
]
```

## Advanced: Automatic Updates

Create a script to automatically update citations monthly:

```python
# auto_update_scholar.py
import json
from scholarly import scholarly
import time

def update_citations(scholar_id):
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=['publications'])
    
    # Load current CV data
    with open('animesh_cv_data.json', 'r') as f:
        cv_data = json.load(f)
    
    # Update citation counts
    for pub in cv_data['publications']:
        title = pub['title'].lower()
        for scholar_pub in author['publications']:
            scholar_title = scholar_pub['bib']['title'].lower()
            if title in scholar_title or scholar_title in title:
                filled = scholarly.fill(scholar_pub)
                pub['citations'] = filled.get('num_citations', 0)
                print(f"Updated: {pub['title']} - {pub['citations']} citations")
                time.sleep(2)  # Be nice to Google Scholar
                break
    
    # Save updated data
    with open('animesh_cv_data.json', 'w') as f:
        json.dump(cv_data, f, indent=2)
    
    print("\n✓ Citation counts updated!")

if __name__ == "__main__":
    scholar_id = "YOUR_SCHOLAR_ID_HERE"
    update_citations(scholar_id)
```

## Tips for Success

1. **Be Patient**: Scholar fetching can take 1-2 minutes per publication
2. **Don't Run Too Often**: Google will block you if you fetch too frequently
3. **Verify Data**: Always check the fetched data before regenerating CV
4. **Keep Backups**: Save a copy of your JSON before fetching new data
5. **Manual Backup**: Keep a manual list of your publications just in case

## Expected Output

When successful, you'll see:

```
Fetching publications for Scholar ID: abc123XYZ
This may take a minute...
  ✓ A Response of Snow Cover to the Climate in the Northwest Himalaya... (2021)
  ✓ Regional variation of drought parameters and long-term trends... (2021)
  ✓ Transport of a severe dust storm from Middle East to Indian region... (2022)

✓ Successfully fetched 3 publications
✓ CV data updated with 3 publications
✓ Saved to animesh_cv_data.json

You can now run cv_builder_v2.py to regenerate your CV with updated publications.
```

## Next Steps

After successful fetching:

1. ✅ Check `animesh_cv_data.json` to verify publications are correct
2. ✅ Run `python cv_builder_v2.py` to generate updated CV
3. ✅ Review the PDF to ensure everything looks good
4. ✅ Set a reminder to update citations monthly

---

**Need Help?**

If you encounter issues:
1. Check that your Google Scholar profile is public
2. Verify your Scholar ID is correct
3. Try the manual alternative if automatic fetching fails
4. Check the scholarly package documentation: https://scholarly.readthedocs.io/
