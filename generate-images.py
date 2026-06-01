#!/usr/bin/env python3
"""
Generate context-aware images for all blog articles using Unsplash API
"""
import os
import re
from pathlib import Path
import subprocess

# Unsplash API - free tier (no key needed for basic requests)
UNSPLASH_API = "https://api.unsplash.com/search/photos"
UNSPLASH_ACCESS_KEY = "6cqVfSVCNzozXdL8oF6R7V0hjAL04uJHPNvIxQQ1aRs"  # Free dev key

# Article-to-image mapping
IMAGE_MAPPING = {
    "argentinien-wm-2026": "Argentina football stadium 2026 World Cup",
    "florian-wirtz": "Florian Wirtz football player Germany",
    "jamal-musiala": "Jamal Musiala football player",
    "deutschland-gegner": "Germany football national team 2026",
    "deutschland-wm": "World Cup 2026 football Germany",
    "wm-2026": "FIFA World Cup 2026 stadium",
    "berlin-iptv": "Berlin city skyline Germany",
    "wien-oesterreich": "Vienna Austria city",
    "zuerich-schweiz": "Zurich Switzerland city",
    "legal-deutschland": "German law legal document",
    "legal-oesterreich": "Austria law legal document",
    "legal-schweiz": "Switzerland law legal document",
    "smart-tv": "Smart TV IPTV streaming device",
    "firestick": "Amazon Fire TV Stick device",
    "android": "Android smartphone mobile device",
    "app": "Mobile app interface streaming",
    "preise": "Price comparison shopping",
    "vergleich": "Comparison test analysis",
    "anbieter": "IPTV service provider",
    "anleitung": "Tutorial guide instruction",
    "puffer": "Streaming buffer loading",
    "internet": "Internet speed connection",
    "iptv": "IPTV streaming television",
    "testbericht": "Product test review",
    "vs": "Versus comparison battle",
    "favoriten": "Favorite winner trophy",
    "spielplan": "Football match schedule",
    "spielorte": "Stadium arena venue",
    "teams": "Football team sport",
    "kader": "Football team squad players",
    "kostenlos": "Free streaming watch",
}

def get_image_url(article_slug: str) -> str:
    """Generate Unsplash image URL based on article slug"""
    # Find best matching query
    query = "streaming IPTV"
    for key, val in IMAGE_MAPPING.items():
        if key in article_slug:
            query = val
            break
    
    # Unsplash URL format: direct image search
    # Format: https://source.unsplash.com/1200x400/?query
    return f"https://source.unsplash.com/1200x400/?{query.replace(' ', ',')}"

def update_frontmatter_with_image(file_path: str, image_url: str) -> bool:
    """Add image URL to article frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if frontmatter already has image
        if 'image:' in content[:500]:  # Check first 500 chars (frontmatter area)
            print(f"  ✓ Already has image: {Path(file_path).name}")
            return False
        
        # Find frontmatter end (---)
        match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL | re.MULTILINE)
        if not match:
            print(f"  ✗ No frontmatter found: {Path(file_path).name}")
            return False
        
        frontmatter = match.group(1)
        frontmatter_end = match.end()
        
        # Add image to frontmatter (before closing ---)
        new_frontmatter = frontmatter.rstrip() + f'\nimage: "{image_url}"'
        new_content = content[:match.start()] + f'---\n{new_frontmatter}\n---\n' + content[frontmatter_end:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Image added: {Path(file_path).name}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {file_path} - {str(e)}")
        return False

def main():
    blog_dir = Path('/Users/yessir/Desktop/yemar/smarttv-blog-fixed/src/content/blog')
    articles = sorted(blog_dir.glob('*.md'))
    
    print(f"🎨 Adding context-aware images to {len(articles)} articles...\n")
    
    updated = 0
    for article_file in articles:
        slug = article_file.stem
        image_url = get_image_url(slug)
        
        if update_frontmatter_with_image(str(article_file), image_url):
            updated += 1
    
    print(f"\n✅ Images added to {updated}/{len(articles)} articles")
    
    # Rebuild
    print("\n🔨 Rebuilding site...")
    result = subprocess.run(['npm', 'run', 'build'], cwd='/Users/yessir/Desktop/yemar/smarttv-blog-fixed')
    return result.returncode == 0

if __name__ == '__main__':
    exit(0 if main() else 1)
