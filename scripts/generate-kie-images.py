#!/usr/bin/env python3
"""
Generate featured images for all blog articles using Kie.ai.
One unique image per article.

Usage:
    python3 scripts/generate-kie-images.py
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional
import requests
import frontmatter

# Add parent directory to path so we can import from yemar
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class KieImageGenerator:
    """Generate images via Kie.ai for blog articles."""

    def __init__(self):
        self.api_key = os.getenv("KIE_API_KEY", "")
        self.endpoint = os.getenv(
            "KIE_IMAGE_API_URL",
            "https://api.kie.ai/api/v1/images/generations"
        )
        self.model = os.getenv("KIE_IMAGE_MODEL", "flux-schnell")
        self.size = os.getenv("KIE_IMAGE_SIZE", "1024x576")
        self.quality = os.getenv("KIE_IMAGE_QUALITY", "economy")
        
        self.images_dir = Path("public/images/blog")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            print("⚠️  WARNING: KIE_API_KEY not set in environment")

    def generate_prompt(self, article_data: Dict[str, Any]) -> str:
        """Generate a detailed image prompt from article metadata."""
        
        title = article_data.get("title", "Article")
        keywords = article_data.get("keywords", "")
        slug = article_data.get("slug", "article")
        
        # Build a more specific prompt based on keywords
        if "iptv" in keywords.lower():
            prompt = f"Professional IPTV streaming service interface on smart TV, 4K ultra HD, modern living room with TV showing channels and guide, professional photography, clean modern design. Article: {title}"
        elif "wm" in keywords.lower() or "fußball" in keywords.lower():
            prompt = f"World Cup 2026 football stadium, fans watching match, sports broadcasting setup, professional sports photography. Article: {title}"
        elif "streaming" in keywords.lower():
            prompt = f"Multiple streaming apps and devices showing entertainment content, 4K resolution, professional product photography. Article: {title}"
        else:
            prompt = f"Professional tech product photo, {title}, modern design, 4K quality, clean background"
        
        return prompt

    def generate_image(self, prompt: str, filename: str) -> Optional[str]:
        """Generate image via Kie.ai and save locally."""
        
        if not self.api_key:
            print(f"❌ KIE_API_KEY missing, skipping image generation for {filename}")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "size": self.size,
                "quality": self.quality,
                "format": "jpeg",
                "n": 1,
            }
            
            print(f"   📸 Calling Kie.ai... ({self.model})")
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=180
            )
            response.raise_for_status()
            
            data = response.json() if response.content else {}
            
            # Extract image URL from various possible response shapes
            image_url = (
                data.get("image_url")
                or data.get("url")
                or data.get("data", {}).get("image_url")
                or data.get("data", {}).get("url")
                or (data.get("data", [{}])[0].get("url") if isinstance(data.get("data"), list) else None)
            )
            
            if not image_url:
                print(f"   ❌ No image URL in response: {data}")
                return None
            
            # Download image
            print(f"   ⬇️  Downloading image...")
            img_response = requests.get(image_url, timeout=120)
            img_response.raise_for_status()
            
            # Save locally
            file_path = self.images_dir / filename
            with open(file_path, "wb") as f:
                f.write(img_response.content)
            
            rel_path = f"/images/blog/{filename}"
            print(f"   ✅ Saved: {rel_path}")
            return rel_path
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    def process_articles(self, articles_dir: Path = Path("src/content/blog")) -> Dict[str, Any]:
        """Process all articles and generate images."""
        
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "articles": [],
        }
        
        md_files = sorted(articles_dir.glob("*.md"))
        
        if not md_files:
            print(f"❌ No articles found in {articles_dir}")
            return results
        
        print(f"\n{'='*70}")
        print(f"🎨 GENERATING IMAGES FOR {len(md_files)} ARTICLES (via Kie.ai)")
        print(f"{'='*70}\n")
        
        results["total"] = len(md_files)
        
        for i, md_file in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] {md_file.name}")
            
            try:
                # Parse frontmatter
                with open(md_file, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                
                article_data = post.metadata
                slug = article_data.get("slug", md_file.stem)
                title = article_data.get("title", "Article")
                
                # Generate prompt and image
                prompt = self.generate_prompt(article_data)
                image_filename = f"{slug}-featured.jpg"
                image_url = self.generate_image(prompt, image_filename)
                
                if image_url:
                    # Update article frontmatter
                    post.metadata["image"] = image_url
                    
                    # Write back
                    with open(md_file, "w", encoding="utf-8") as f:
                        f.write(frontmatter.dumps(post))
                    
                    results["success"] += 1
                    results["articles"].append({
                        "file": md_file.name,
                        "title": title,
                        "image": image_url,
                        "status": "success"
                    })
                else:
                    results["failed"] += 1
                    results["articles"].append({
                        "file": md_file.name,
                        "title": title,
                        "status": "failed"
                    })
                    
            except Exception as e:
                print(f"   ❌ Error processing {md_file.name}: {e}")
                results["failed"] += 1
                results["articles"].append({
                    "file": md_file.name,
                    "status": "error",
                    "error": str(e)
                })
        
        print(f"\n{'='*70}")
        print(f"✅ COMPLETE: {results['success']}/{results['total']} images generated")
        print(f"{'='*70}\n")
        
        return results


def main():
    """Run the image generation pipeline."""
    
    os.chdir(Path(__file__).parent.parent)  # Change to blog root
    
    generator = KieImageGenerator()
    results = generator.process_articles()
    
    # Save results
    with open("image-generation-results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Exit with proper code
    exit_code = 0 if results["failed"] == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
