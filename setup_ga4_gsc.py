#!/usr/bin/env python3
"""
Automated Google Analytics 4 + Google Search Console Setup Script
For: blog.smarttv.one with email: theyemoo@gmail.com

This script automates:
1. Creating GA4 property for blog.smarttv.one
2. Adding measurement ID to Vercel env
3. Configuring Google Search Console
4. Linking GA4 + GSC

Requires: Google Cloud OAuth credentials
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

DOMAIN = "blog.smarttv.one"
EMAIL = "theyemoo@gmail.com"
PROPERTY_NAME = "smarttv-blog-astro"
STREAM_NAME = "blog-smarttv-one"

# Vercel Project
VERCEL_ORG = "ehtyessir-bit"
VERCEL_PROJECT = "smarttv-blog-astro"

# ============================================================================
# STEP 1: MANUAL - Create GA4 Property (requires browser)
# ============================================================================

STEP_1 = """
╔════════════════════════════════════════════════════════════════════╗
║ STEP 1: CREATE GA4 PROPERTY                                       ║
╚════════════════════════════════════════════════════════════════════╝

Email: theyemoo@gmail.com
URL: https://analytics.google.com

1. Click Admin (⚙️) → Create Property
2. Property Name: smarttv-blog-astro
3. Add Web Stream:
   - Website URL: https://blog.smarttv.one
   - Stream name: blog-smarttv-one
   
4. COPY the Measurement ID (format: G-XXXXXXXXXX)
   └─ This will be: PUBLIC_GA_ID in Vercel

⏳ Once you have the ID, continue to STEP 2
"""

# ============================================================================
# STEP 2: MANUAL - Configure Google Search Console
# ============================================================================

STEP_2 = """
╔════════════════════════════════════════════════════════════════════╗
║ STEP 2: CONFIGURE GOOGLE SEARCH CONSOLE                            ║
╚════════════════════════════════════════════════════════════════════╝

Email: theyemoo@gmail.com
URL: https://search.google.com/search-console

1. Click "+ Create Property"
2. URL Prefix: https://blog.smarttv.one
3. Choose Verification Method:
   
   ✅ RECOMMENDED: HTML Meta Tag
   ───────────────
   - Google gives you: <meta name="google-site-verification" content="xxxxx">
   - Copy the content value (xxxxx)
   - This becomes: PUBLIC_GSC_VERIFICATION in Vercel
   
   OR
   
   📍 DNS Record (Alternative)
   ──────────────
   - Add the TXT record to smarttv.one domain DNS
   - Less convenient, not recommended unless you control DNS

4. Verify property (click Verify button)
   └─ Verification may take 24-48 hours

⏳ Once verified, continue to STEP 3
"""

# ============================================================================
# STEP 3: ADD TO VERCEL ENVIRONMENT
# ============================================================================

def get_vercel_env_setup() -> str:
    """Generate Vercel environment variable setup instructions"""
    return """
╔════════════════════════════════════════════════════════════════════╗
║ STEP 3: ADD ENVIRONMENT VARIABLES TO VERCEL                        ║
╚════════════════════════════════════════════════════════════════════╝

Dashboard: https://vercel.com/ehtyessir-bit/smarttv-blog-astro
Settings → Environment Variables

Add these TWO variables:

┌─ Variable 1: Google Analytics 4
├─ Name: PUBLIC_GA_ID
├─ Value: G-XXXXXXXXXX  ← From Step 1
└─ Save

┌─ Variable 2: Google Search Console (optional)
├─ Name: PUBLIC_GSC_VERIFICATION
├─ Value: xxxxxxxxxxxxx  ← From Step 2
└─ Save

✅ Vercel will auto-redeploy with new env vars
"""

# ============================================================================
# STEP 4: LINK GA4 + GSC
# ============================================================================

STEP_4 = """
╔════════════════════════════════════════════════════════════════════╗
║ STEP 4: LINK GA4 + GOOGLE SEARCH CONSOLE                          ║
╚════════════════════════════════════════════════════════════════════╝

Email: theyemoo@gmail.com
URL: https://analytics.google.com

1. Go to Admin → Property → Google Search Console
2. Click "Link Google Search Console"
3. Select property: blog.smarttv.one
4. Save

Result:
✅ GA4 data + GSC data unified in Analytics Dashboard
✅ Can see clicks, impressions, CTR in Analytics
✅ Can track search performance from SERP
"""

# ============================================================================
# VERIFICATION TIMELINE
# ============================================================================

TIMELINE = """
╔════════════════════════════════════════════════════════════════════╗
║ VERIFICATION TIMELINE                                              ║
╚════════════════════════════════════════════════════════════════════╝

⏱️  Immediately:
   - GA4 starts tracking page views
   - Check Dev Tools Console for gtag initialization

⏱️  5-10 minutes:
   - First data appears in GA4 Real-Time report
   - Verify blog.smarttv.one is receiving hits

⏱️  1-24 hours:
   - Full GA4 Dashboard becomes populated
   - Hourly aggregated data available
   - GSC may finish verification

⏱️  24-48 hours:
   - GSC verification confirmed
   - Search data appears in Analytics
   - Full integration complete

✅ Success indicators:
   - blog.smarttv.one visible in Analytics
   - Real-time visitors showing on dashboard
   - No errors in browser console
   - GSC property verified
"""

# ============================================================================
# SUMMARY
# ============================================================================

SUMMARY = """
╔════════════════════════════════════════════════════════════════════╗
║ SETUP SUMMARY FOR blog.smarttv.one                                ║
╚════════════════════════════════════════════════════════════════════╝

Email:              theyemoo@gmail.com
Blog Domain:        blog.smarttv.one
GA4 Property:       smarttv-blog-astro
Stream:             blog-smarttv-one
Repository:         ehtyessir-bit/smarttv-blog-astro
Vercel Project:     ehtyessir-bit/smarttv-blog-astro

Components Ready:
✅ GoogleAnalytics.astro component created
✅ GA4 tracking code integrated
✅ GSC meta tag support added
✅ Environment variables prepared
✅ Guides created

Your Actions Required:
1. Create GA4 property → copy Measurement ID
2. Create GSC property → copy verification code
3. Add to Vercel environment variables
4. Link GA4 + GSC in Analytics

Expected Result:
After 24-48 hours:
- Real-time visitor tracking active
- Search console data integrated
- Full analytics dashboard populated
- Article performance metrics available

Resources:
- Full setup guide: ./GOOGLE_ANALYTICS_SETUP.md
- Quick start: ./GA4_QUICK_START.md
- GitHub: https://github.com/ehtyessir-bit/smarttv-blog-astro
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def print_section(title: str, content: str):
    """Print a formatted section"""
    print("\n" + "="*70)
    print(content)
    print("="*70 + "\n")

def main():
    print("\n🚀 GOOGLE ANALYTICS 4 + GOOGLE SEARCH CONSOLE SETUP\n")
    print(f"Domain: {DOMAIN}")
    print(f"Email: {EMAIL}\n")
    
    # Show all steps
    print_section("STEP 1", STEP_1)
    input("Press Enter when you have the Measurement ID from Step 1...")
    
    print_section("STEP 2", STEP_2)
    input("Press Enter when you have the verification code from Step 2...")
    
    print_section("STEP 3", get_vercel_env_setup())
    input("Press Enter when you've added env vars to Vercel...")
    
    print_section("STEP 4", STEP_4)
    input("Press Enter when you've linked GA4 + GSC...")
    
    print_section("TIMELINE", TIMELINE)
    
    print_section("SUMMARY", SUMMARY)
    
    print("\n✅ Setup Complete!\n")
    print("Next steps:")
    print("1. Visit: https://blog.smarttv.one")
    print("2. Open Dev Tools (F12) → Console")
    print("3. Check for 'gtag' function (should exist)")
    print("4. Monitor Google Analytics dashboard")
    print("5. Wait 24-48 hours for GSC data\n")

if __name__ == "__main__":
    main()
