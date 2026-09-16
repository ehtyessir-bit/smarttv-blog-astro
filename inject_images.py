#!/usr/bin/env python3
"""
Inject inline images with entity-optimised alt text into every article.
Alt text = focus keyword + descriptive context → Google Image + AI Search.
"""
import os, re

BLOG_DIR = "src/content/blog"

# Per-article: focusKeyword + list of (photo_id, alt_text) for inline images
ARTICLES = {
    "argentinien-wm-2026": {
        "focusKeyword": "Argentinien WM 2026",
        "images": [
            ("photo-1574629810360-7efbbe195018",
             "Argentinien WM 2026 Messi – Argentinische Nationalmannschaft trainiert für die Weltmeisterschaft 2026"),
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 Stadion – Weltmeisterschaft 2026 Spielort in Nordamerika live per IPTV schauen"),
        ]
    },
    "bester-iptv-anbieter-test": {
        "focusKeyword": "Bester IPTV Anbieter Test 2026",
        "images": [
            ("photo-1593784991095-a205069470b6",
             "Bester IPTV Anbieter Test 2026 – Smart TV mit IPTV-Stream in HD-Qualität für Deutschland"),
            ("photo-1461151304267-38231e0cb52d",
             "IPTV Anbieter Vergleich Deutschland 2026 – Fernseher zeigt IPTV-Sender in 4K Qualität"),
        ]
    },
    "bestes-iptv-oesterreich": {
        "focusKeyword": "Bestes IPTV Österreich 2026",
        "images": [
            ("photo-1516550135131-fe3dcb0bedc1",
             "Bestes IPTV Österreich 2026 – Wien Stadtpanorama, IPTV-Streaming in Österreich legal nutzen"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Österreich Smart TV einrichten – österreichische Sender in HD streamen ab €4,83/Monat"),
        ]
    },
    "bestes-iptv-wm-2026": {
        "focusKeyword": "Bestes IPTV WM 2026",
        "images": [
            ("photo-1551698618-1dfe5d97d256",
             "Bestes IPTV WM 2026 – Fußball-Weltmeisterschaft 2026 live im Stadion und per IPTV verfolgen"),
            ("photo-1508098682722-e99c43a406b2",
             "WM 2026 IPTV Stream HD – Deutschland-Spiele live ohne Abo in bester Qualität schauen"),
        ]
    },
    "deutschland-gegner-wm-2026-gruppe": {
        "focusKeyword": "Deutschland WM 2026 Gruppe Gegner",
        "images": [
            ("photo-1508098682722-e99c43a406b2",
             "Deutschland WM 2026 Gruppe Gegner – DFB-Nationalmannschaft Gruppenphase Spielplan Analyse"),
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 Spielplan Deutschland – alle Gruppenspiele live per IPTV in HD schauen"),
        ]
    },
    "deutschland-gegner-wm-2026": {
        "focusKeyword": "Deutschland Gegner WM 2026",
        "images": [
            ("photo-1508098682722-e99c43a406b2",
             "Deutschland Gegner WM 2026 – Analyse der deutschen Gruppe, Chancen auf das Halbfinale"),
            ("photo-1574629810360-7efbbe195018",
             "DFB WM 2026 Kader – Deutschlands stärkste Spieler für die Weltmeisterschaft in Nordamerika"),
        ]
    },
    "deutschland-wm-2026-kader-spielplan": {
        "focusKeyword": "Deutschland WM 2026 Kader Spielplan",
        "images": [
            ("photo-1574629810360-7efbbe195018",
             "Deutschland WM 2026 Kader – die 26 DFB-Spieler mit Musiala und Wirtz als Leistungsträger"),
            ("photo-1508098682722-e99c43a406b2",
             "Deutschland WM 2026 Spielplan – alle Anstoßzeiten und Gruppenspiele im Überblick"),
        ]
    },
    "deutschland-wm-2026-spieler-kader": {
        "focusKeyword": "Deutschland WM 2026 Spieler Kader",
        "images": [
            ("photo-1574629810360-7efbbe195018",
             "Deutschland WM 2026 Spieler Kader – die 26 Spieler der deutschen Nationalmannschaft 2026"),
            ("photo-1508098682722-e99c43a406b2",
             "DFB Kader WM 2026 Training – Deutschland bereitet sich auf die Weltmeisterschaft vor"),
        ]
    },
    "deutschland-wm-iptv-stream": {
        "focusKeyword": "Deutschland WM 2026 IPTV Stream",
        "images": [
            ("photo-1461151304267-38231e0cb52d",
             "Deutschland WM 2026 IPTV Stream – alle Deutschland-Spiele live in HD auf dem Smart TV"),
            ("photo-1593784991095-a205069470b6",
             "WM 2026 live streamen Smart TV – IPTV einrichten für Deutschland Österreich Schweiz"),
        ]
    },
    "florian-wirtz-wm-2026": {
        "focusKeyword": "Florian Wirtz WM 2026",
        "images": [
            ("photo-1574629810360-7efbbe195018",
             "Florian Wirtz WM 2026 – Bayer Leverkusen Star als wichtigster Spieler der deutschen Nationalmannschaft"),
            ("photo-1508098682722-e99c43a406b2",
             "Florian Wirtz DFB 2026 – WM-Kader Deutschland mit Wirtz als entscheidendem Spielmacher"),
        ]
    },
    "guenstigstes-iptv-abo": {
        "focusKeyword": "Günstigstes IPTV Abo Deutschland 2026",
        "images": [
            ("photo-1554224155-6726b3ff858f",
             "Günstigstes IPTV Abo Deutschland 2026 – Preisvergleich ab €4,83 pro Monat für alle Sender"),
            ("photo-1593784991095-a205069470b6",
             "IPTV günstig Deutschland – Smart TV Streaming ohne teure Kabelabo ab €15 monatlich"),
        ]
    },
    "iptv-anbieter-deutschland-2026": {
        "focusKeyword": "IPTV Anbieter Deutschland 2026",
        "images": [
            ("photo-1593784991095-a205069470b6",
             "IPTV Anbieter Deutschland 2026 – Smart TV mit bestem deutschen IPTV-Dienst in HD und 4K"),
            ("photo-1461151304267-38231e0cb52d",
             "IPTV Deutschland Test 2026 – Vergleich der besten Anbieter für Kanalauswahl und Streamqualität"),
        ]
    },
    "iptv-anbieter-vergleich-dach": {
        "focusKeyword": "IPTV Anbieter Vergleich DACH",
        "images": [
            ("photo-1461151304267-38231e0cb52d",
             "IPTV Anbieter Vergleich DACH – Deutschland Österreich Schweiz Streaming-Dienste im direkten Test"),
            ("photo-1554224155-6726b3ff858f",
             "IPTV DACH Preisvergleich 2026 – günstigster Anbieter für DE AT CH ab €4,83 pro Monat"),
        ]
    },
    "iptv-app-android-iphone": {
        "focusKeyword": "IPTV App Android iPhone 2026",
        "images": [
            ("photo-1512941937669-90a1b58e7e9c",
             "IPTV App Android iPhone 2026 – IPTV auf dem Smartphone einrichten in unter 3 Minuten"),
            ("photo-1461151304267-38231e0cb52d",
             "IPTV Handy App Deutschland – Sender auf Android und iPhone streamen ohne Puffer"),
        ]
    },
    "iptv-berlin": {
        "focusKeyword": "IPTV Berlin 2026",
        "images": [
            ("photo-1560969184-10fe8719e047",
             "IPTV Berlin 2026 – Berliner Fernsehturm, bester IPTV-Anbieter für Berlin in HD-Qualität"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Smart TV Berlin – stabiler Stream ohne Puffer für Berliner Haushalte 2026"),
        ]
    },
    "iptv-deutschland-anbieter-vergleich": {
        "focusKeyword": "IPTV Deutschland Anbieter Vergleich 2026",
        "images": [
            ("photo-1593784991095-a205069470b6",
             "IPTV Deutschland Anbieter Vergleich 2026 – welcher Dienst liefert HD ohne Puffer in Deutschland"),
            ("photo-1554224155-6726b3ff858f",
             "IPTV Preise Deutschland vergleichen – alle Anbieter im Test mit Preis und Kanalanzahl"),
        ]
    },
    "iptv-deutschland-komplett-guide": {
        "focusKeyword": "IPTV Deutschland 2026",
        "images": [
            ("photo-1461151304267-38231e0cb52d",
             "IPTV Deutschland 2026 Komplett-Guide – Smart TV Streaming einrichten für Anfänger und Profis"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Deutschland Setup 2026 – Schritt-für-Schritt Anleitung für alle Geräte"),
        ]
    },
    "iptv-einrichten-anleitung": {
        "focusKeyword": "IPTV einrichten Anleitung 2026",
        "images": [
            ("photo-1522869635100-9f4c5e86aa37",
             "IPTV einrichten Anleitung 2026 – Schritt-für-Schritt Setup für Smart TV Firestick und Router"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Installation Deutschland – Smart TV IPTV konfigurieren in 5 Minuten ohne Vorkenntnisse"),
        ]
    },
    "iptv-firestick-einrichten": {
        "focusKeyword": "IPTV Firestick einrichten 2026",
        "images": [
            ("photo-1558618666-fcd25c85cd64",
             "IPTV Firestick einrichten 2026 – Amazon Fire TV Stick mit IPTV in 5 Minuten konfigurieren"),
            ("photo-1522869635100-9f4c5e86aa37",
             "Firestick IPTV Setup Deutschland – alle Sender in HD auf dem Amazon Streaming-Stick"),
        ]
    },
    "iptv-internet-geschwindigkeit": {
        "focusKeyword": "IPTV Internet Geschwindigkeit Mbit 2026",
        "images": [
            ("photo-1558618047-3c8c76d2e6a0",
             "IPTV Internet Geschwindigkeit 2026 – wie viel Mbit braucht man für störungsfreies HD-Streaming"),
            ("photo-1522869635100-9f4c5e86aa37",
             "IPTV Speedtest Deutschland – optimale Internetgeschwindigkeit für 4K IPTV-Stream ermitteln"),
        ]
    },
    "iptv-legal-deutschland": {
        "focusKeyword": "IPTV legal Deutschland 2026",
        "images": [
            ("photo-1589829085413-56de8ae18c73",
             "IPTV legal Deutschland 2026 – rechtliche Lage für IPTV-Nutzer in Deutschland klar erklärt"),
            ("photo-1593784991095-a205069470b6",
             "Legales IPTV Deutschland – welche Anbieter du 2026 bedenkenlos nutzen kannst"),
        ]
    },
    "iptv-legal-oesterreich": {
        "focusKeyword": "IPTV legal Österreich 2026",
        "images": [
            ("photo-1589829085413-56de8ae18c73",
             "IPTV legal Österreich 2026 – österreichisches Recht und IPTV-Nutzung verständlich erklärt"),
            ("photo-1516550135131-fe3dcb0bedc1",
             "IPTV Österreich Wien legal – was du in Österreich beim IPTV-Streaming beachten musst"),
        ]
    },
    "iptv-legal-schweiz": {
        "focusKeyword": "IPTV legal Schweiz 2026",
        "images": [
            ("photo-1506905925346-21bda4d32df4",
             "IPTV legal Schweiz 2026 – Schweizer Recht und IPTV klar und ohne Panik erklärt"),
            ("photo-1589829085413-56de8ae18c73",
             "Legales IPTV Schweiz – welche Anbieter in der Schweiz 2026 erlaubt und sicher sind"),
        ]
    },
    "iptv-preise-vergleich-2026": {
        "focusKeyword": "IPTV Preise Vergleich 2026",
        "images": [
            ("photo-1554224155-6726b3ff858f",
             "IPTV Preise Vergleich 2026 – alle Pakete von 1 Monat bis Lifetime ab €4,83 pro Monat"),
            ("photo-1593784991095-a205069470b6",
             "IPTV günstigstes Abo Deutschland 2026 – Preistabelle aller Pakete im direkten Vergleich"),
        ]
    },
    "iptv-puffer-probleme-loesen": {
        "focusKeyword": "IPTV Puffer Probleme lösen 2026",
        "images": [
            ("photo-1522869635100-9f4c5e86aa37",
             "IPTV Puffer Probleme lösen 2026 – 5 Tricks für flüssiges Streaming ohne Unterbrechungen"),
            ("photo-1558618047-3c8c76d2e6a0",
             "IPTV Stream ruckelt – Internetgeschwindigkeit optimieren für stabiles HD-Streaming"),
        ]
    },
    "iptv-schweiz-legal": {
        "focusKeyword": "IPTV Schweiz legal 2026",
        "images": [
            ("photo-1506905925346-21bda4d32df4",
             "IPTV Schweiz legal 2026 – Alpenpanorama Schweiz, sicheres Streaming ohne Abmahnrisiko"),
            ("photo-1589829085413-56de8ae18c73",
             "Legales IPTV Schweiz Zürich – was erlaubt ist und welche Anbieter sicher sind"),
        ]
    },
    "iptv-smart-tv-einrichten": {
        "focusKeyword": "IPTV Smart TV einrichten Samsung LG 2026",
        "images": [
            ("photo-1593784991095-a205069470b6",
             "IPTV Smart TV einrichten Samsung LG 2026 – direkt auf dem Fernseher ohne Extra-Gerät"),
            ("photo-1461151304267-38231e0cb52d",
             "Samsung LG Smart TV IPTV Setup – IPTV-App auf dem Fernseher installieren Schritt für Schritt"),
        ]
    },
    "iptv-testbericht-top-anbieter": {
        "focusKeyword": "IPTV Testbericht Top Anbieter 2026",
        "images": [
            ("photo-1461151304267-38231e0cb52d",
             "IPTV Testbericht Top Anbieter 2026 – monatelanger Test von 5 Anbietern mit klarem Sieger"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Qualitätstest Deutschland 2026 – Streamqualität Kanalanzahl und Preis im Vergleich"),
        ]
    },
    "iptv-vs-kabelfernsehen": {
        "focusKeyword": "IPTV vs Kabelfernsehen Deutschland 2026",
        "images": [
            ("photo-1593784991095-a205069470b6",
             "IPTV vs Kabelfernsehen Deutschland 2026 – Vergleich Kosten Kanalanzahl und Qualität"),
            ("photo-1554224155-6726b3ff858f",
             "IPTV günstiger als Kabel – warum Millionen Deutsche ihren Kabelvertrag 2026 kündigen"),
        ]
    },
    "iptv-wien-oesterreich": {
        "focusKeyword": "IPTV Wien Österreich 2026",
        "images": [
            ("photo-1516550135131-fe3dcb0bedc1",
             "IPTV Wien Österreich 2026 – Wiener Innenstadt, bester IPTV-Anbieter für Wien getestet"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Österreich Smart TV 2026 – stabiler Stream in Wien und ganz Österreich"),
        ]
    },
    "iptv-zuerich-schweiz": {
        "focusKeyword": "IPTV Zürich Schweiz 2026",
        "images": [
            ("photo-1506905925346-21bda4d32df4",
             "IPTV Zürich Schweiz 2026 – bester IPTV-Anbieter für Zürich und die ganze Schweiz"),
            ("photo-1593784991095-a205069470b6",
             "IPTV Schweiz Smart TV einrichten – stabiles Streaming in Zürich Bern Genf 2026"),
        ]
    },
    "jamal-musiala-wm-2026": {
        "focusKeyword": "Jamal Musiala WM 2026",
        "images": [
            ("photo-1574629810360-7efbbe195018",
             "Jamal Musiala WM 2026 – Bayern München Star als gefährlichster Spieler der DFB-Nationalmannschaft"),
            ("photo-1508098682722-e99c43a406b2",
             "Musiala Deutschland WM 2026 – kann Jamal Musiala Deutschland zum Weltmeistertitel schießen"),
        ]
    },
    "wm-2026-alle-teams-qualifiziert": {
        "focusKeyword": "WM 2026 alle Teams qualifiziert",
        "images": [
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 alle Teams qualifiziert – 48 Nationen bei der Weltmeisterschaft in USA Kanada Mexiko"),
            ("photo-1508098682722-e99c43a406b2",
             "WM 2026 Teilnehmer Überblick – alle 48 qualifizierten Mannschaften und ihre Gruppe"),
        ]
    },
    "wm-2026-alle-teams": {
        "focusKeyword": "WM 2026 alle Teams",
        "images": [
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 alle Teams – Weltmeisterschaft 2026 mit 48 Mannschaften aus aller Welt"),
            ("photo-1508098682722-e99c43a406b2",
             "WM 2026 Gruppen und Teams – Favoriten Außenseiter und Überraschungsmannschaften im Überblick"),
        ]
    },
    "wm-2026-favoriten-wer-gewinnt": {
        "focusKeyword": "WM 2026 Favoriten wer gewinnt",
        "images": [
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 Favoriten wer gewinnt – Analyse der 5 stärksten Teams für den Weltmeistertitel 2026"),
            ("photo-1574629810360-7efbbe195018",
             "WM 2026 Weltmeister Favoriten – Deutschland Frankreich Argentinien Brasilien im Vergleich"),
        ]
    },
    "wm-2026-favoriten": {
        "focusKeyword": "WM 2026 Favoriten",
        "images": [
            ("photo-1508098682722-e99c43a406b2",
             "WM 2026 Favoriten – die 5 stärksten Mannschaften kämpfen um den Weltmeistertitel"),
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 Titelkandidaten Stadion – wer hat die besten Chancen auf den WM-Titel 2026"),
        ]
    },
    "wm-2026-kostenlos-schauen": {
        "focusKeyword": "WM 2026 kostenlos schauen Deutschland",
        "images": [
            ("photo-1461151304267-38231e0cb52d",
             "WM 2026 kostenlos schauen Deutschland – alle Spiele legal und gratis auf ARD ZDF und IPTV"),
            ("photo-1593784991095-a205069470b6",
             "WM 2026 gratis streamen Smart TV – kostenlose Sender für Deutschland Österreich Schweiz"),
        ]
    },
    "wm-2026-live-iptv": {
        "focusKeyword": "WM 2026 live IPTV Deutschland",
        "images": [
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 live IPTV Deutschland – alle 64 WM-Spiele live in HD ohne teure Abos streamen"),
            ("photo-1461151304267-38231e0cb52d",
             "WM 2026 IPTV Stream Smart TV – Weltmeisterschaft live auf dem Fernseher ab €4,83 Monat"),
        ]
    },
    "wm-2026-spielorte": {
        "focusKeyword": "WM 2026 Spielorte Stadien",
        "images": [
            ("photo-1540747913346-19e32dc3e97e",
             "WM 2026 Spielorte Stadien – die 16 Arenen in USA Kanada Mexiko für die Weltmeisterschaft"),
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 Finalstadion USA – größte Stadien der Weltmeisterschaft 2026 im Überblick"),
        ]
    },
    "wm-2026-spielplan": {
        "focusKeyword": "WM 2026 Spielplan Deutschland",
        "images": [
            ("photo-1508098682722-e99c43a406b2",
             "WM 2026 Spielplan Deutschland – alle Anstoßzeiten Gruppenspiele und K.o.-Runden Übersicht"),
            ("photo-1551698618-1dfe5d97d256",
             "WM 2026 Terminplan – kompletter Spielplan mit allen 64 Spielen und deutschen Zeiten"),
        ]
    },
}

def inject_images_into_article(content, images):
    """Insert images after every 2nd H2 section in the article body."""
    # Split into frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    frontmatter = parts[1]
    body = parts[2]

    # Find all H2 positions
    h2_positions = [m.start() for m in re.finditer(r'^## ', body, re.MULTILINE)]

    if len(h2_positions) < 2:
        return content

    # Build image markdown blocks
    img_blocks = []
    for photo_id, alt in images:
        url = f"https://images.unsplash.com/{photo_id}?w=900&q=80&auto=format&fit=crop"
        img_blocks.append(f'\n\n![{alt}]({url})\n')

    # Insert images after H2 sections (1st img after 1st H2, 2nd after 2nd H2)
    insertions = []
    for i, img_block in enumerate(img_blocks):
        h2_idx = i  # after 1st, 2nd H2
        if h2_idx < len(h2_positions):
            pos = h2_positions[h2_idx]
            # Find end of this H2 line
            end_of_line = body.find('\n', pos)
            if end_of_line == -1:
                end_of_line = len(body)
            insertions.append((end_of_line, img_block))

    # Apply insertions in reverse order
    for pos, block in sorted(insertions, reverse=True):
        body = body[:pos] + block + body[pos:]

    return f'---{frontmatter}---{body}'

def add_focus_keyword(frontmatter_block, focus_keyword):
    """Add focusKeyword to frontmatter if not present."""
    if 'focusKeyword:' in frontmatter_block:
        return re.sub(r'^focusKeyword:.*$', f'focusKeyword: "{focus_keyword}"', frontmatter_block, flags=re.MULTILINE)
    # Insert after description line
    return re.sub(
        r'^(description:.*)',
        r'\1\nfocusKeyword: "' + focus_keyword + '"',
        frontmatter_block,
        count=1,
        flags=re.MULTILINE
    )

updated = 0
for fname in os.listdir(BLOG_DIR):
    if not fname.endswith('.md'):
        continue
    slug = fname[:-3]
    if slug not in ARTICLES:
        continue

    path = os.path.join(BLOG_DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = ARTICLES[slug]

    # Step 1: Add focusKeyword to frontmatter
    parts = content.split('---', 2)
    if len(parts) >= 3:
        parts[1] = add_focus_keyword(parts[1], data['focusKeyword'])
        content = '---'.join(parts)

    # Step 2: Inject inline images
    content = inject_images_into_article(content, data['images'])

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {slug}")
    updated += 1

print(f"\n✅ {updated} articles updated with focusKeyword + inline images")
