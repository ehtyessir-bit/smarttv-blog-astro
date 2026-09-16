#!/usr/bin/env python3
import os, re

BLOG_DIR = "src/content/blog"

# Unsplash photo IDs per article
IMAGES = {
    "argentinien-wm-2026":              "photo-1574629810360-7efbbe195018",  # soccer ball
    "bester-iptv-anbieter-test":        "photo-1593784991095-a205069470b6",  # smart TV
    "bestes-iptv-oesterreich":          "photo-1516550135131-fe3dcb0bedc1",  # Vienna
    "bestes-iptv-wm-2026":             "photo-1551698618-1dfe5d97d256",     # stadium
    "deutschland-gegner-wm-2026-gruppe":"photo-1508098682722-e99c43a406b2",  # soccer field
    "deutschland-gegner-wm-2026":       "photo-1508098682722-e99c43a406b2",  # soccer field
    "deutschland-wm-2026-kader-spielplan":"photo-1551698618-1dfe5d97d256",   # stadium
    "deutschland-wm-2026-spieler-kader":"photo-1574629810360-7efbbe195018",  # soccer ball
    "deutschland-wm-iptv-stream":       "photo-1461151304267-38231e0cb52d",  # TV screen
    "florian-wirtz-wm-2026":           "photo-1508098682722-e99c43a406b2",  # soccer field
    "guenstigstes-iptv-abo":           "photo-1554224155-6726b3ff858f",     # money/price
    "iptv-anbieter-deutschland-2026":  "photo-1593784991095-a205069470b6",  # smart TV
    "iptv-anbieter-vergleich-dach":    "photo-1461151304267-38231e0cb52d",  # TV screen
    "iptv-app-android-iphone":         "photo-1512941937669-90a1b58e7e9c",  # smartphone
    "iptv-berlin":                      "photo-1560969184-10fe8719e047",     # Berlin
    "iptv-deutschland-anbieter-vergleich":"photo-1593784991095-a205069470b6",# smart TV
    "iptv-deutschland-komplett-guide":  "photo-1461151304267-38231e0cb52d",  # TV screen
    "iptv-einrichten-anleitung":        "photo-1522869635100-9f4c5e86aa37",  # streaming setup
    "iptv-firestick-einrichten":        "photo-1558618666-fcd25c85cd64",     # fire stick
    "iptv-internet-geschwindigkeit":    "photo-1558618047-3c8c76d2e6a0",     # internet speed
    "iptv-legal-deutschland":           "photo-1589829085413-56de8ae18c73",  # legal
    "iptv-legal-oesterreich":          "photo-1589829085413-56de8ae18c73",  # legal
    "iptv-legal-schweiz":              "photo-1506905925346-21bda4d32df4",  # Switzerland
    "iptv-preise-vergleich-2026":      "photo-1554224155-6726b3ff858f",     # money
    "iptv-puffer-probleme-loesen":     "photo-1522869635100-9f4c5e86aa37",  # streaming
    "iptv-schweiz-legal":              "photo-1506905925346-21bda4d32df4",  # Switzerland
    "iptv-smart-tv-einrichten":        "photo-1593784991095-a205069470b6",  # smart TV
    "iptv-testbericht-top-anbieter":   "photo-1461151304267-38231e0cb52d",  # TV
    "iptv-vs-kabelfernsehen":          "photo-1593784991095-a205069470b6",  # TV
    "iptv-wien-oesterreich":           "photo-1516550135131-fe3dcb0bedc1",  # Vienna
    "iptv-zuerich-schweiz":            "photo-1506905925346-21bda4d32df4",  # Zurich
    "jamal-musiala-wm-2026":           "photo-1574629810360-7efbbe195018",  # soccer
    "wm-2026-alle-teams-qualifiziert": "photo-1551698618-1dfe5d97d256",     # stadium
    "wm-2026-alle-teams":              "photo-1551698618-1dfe5d97d256",     # stadium
    "wm-2026-favoriten-wer-gewinnt":   "photo-1508098682722-e99c43a406b2",  # soccer
    "wm-2026-favoriten":               "photo-1508098682722-e99c43a406b2",  # soccer
    "wm-2026-kostenlos-schauen":       "photo-1461151304267-38231e0cb52d",  # TV
    "wm-2026-live-iptv":               "photo-1551698618-1dfe5d97d256",     # stadium
    "wm-2026-spielorte":               "photo-1540747913346-19e32dc3e97e",  # stadium US
    "wm-2026-spielplan":               "photo-1508098682722-e99c43a406b2",  # soccer field
}

# Clickbait German descriptions
DESCRIPTIONS = {
    "argentinien-wm-2026":
        "Kann Messi 2026 nochmal Weltmeister werden? Wir analysieren Argentiniens Chancen — und zeigen dir, wo du jedes Spiel live und kostenlos schaust.",
    "bester-iptv-anbieter-test":
        "Wir haben 58 IPTV-Anbieter getestet — nur 3 haben wirklich überzeugt. Das Ergebnis wird dich überraschen. Jetzt ehrlichen Test lesen.",
    "bestes-iptv-oesterreich":
        "Welcher IPTV-Anbieter ist 2026 der beste für Österreich? Wir haben alle getestet und verraten dir, wer wirklich liefert — ab €4,83/Monat.",
    "bestes-iptv-wm-2026":
        "WM 2026 live ohne teure Sky-Abo? Wir zeigen dir die 5 besten IPTV-Anbieter, die alle Spiele in HD streamen — ab nur €4,83 im Monat.",
    "deutschland-gegner-wm-2026-gruppe":
        "Deutschland gegen wen? Wir verraten dir alle Gruppengegner, die Chancen auf das Halbfinale — und wie du kein einziges Spiel verpasst.",
    "deutschland-gegner-wm-2026":
        "Wer sind Deutschlands Gegner bei der WM 2026? Alle Infos zur Gruppe, Spielplan und Chancen — plus: so schaust du live ohne Abo.",
    "deutschland-wm-2026-kader-spielplan":
        "Der komplette DFB-Kader 2026 mit allen Spielern, Spielplan und Anstoßzeiten. So verpasst du kein einziges Deutschlandspiel bei der WM.",
    "deutschland-wm-2026-spieler-kader":
        "Wer fährt zur WM 2026? Der endgültige 26-Mann-Kader der deutschen Nationalmannschaft — mit Überraschungen, die niemand erwartet hat.",
    "deutschland-wm-iptv-stream":
        "Alle Deutschland-Spiele bei der WM 2026 live schauen — ohne Kabel, ohne teure Abos. So geht's mit IPTV ab €4,83/Monat.",
    "florian-wirtz-wm-2026":
        "Florian Wirtz bei der WM 2026: Kann Deutschlands bester Spieler den Titel holen? Wir analysieren seine Chancen und verraten alles.",
    "guenstigstes-iptv-abo":
        "Du zahlst zu viel für IPTV. Das günstigste Abo in Deutschland kostet nur €4,83/Monat — wir zeigen dir, wo und wie du sparst.",
    "iptv-anbieter-deutschland-2026":
        "Die besten IPTV-Anbieter in Deutschland 2026 im Vergleich — Preise, Qualität, Kanäle. Wir nennen dir den klaren Sieger.",
    "iptv-anbieter-vergleich-dach":
        "IPTV in Deutschland, Österreich und der Schweiz: Wir haben 4 Länder verglichen und zeigen, wer wirklich das beste Angebot hat.",
    "iptv-app-android-iphone":
        "Die beste IPTV-App für Android & iPhone 2026 — kostenlos & ohne technische Kenntnisse. Setup in unter 3 Minuten erklärt.",
    "iptv-berlin":
        "IPTV in Berlin 2026: Welcher Anbieter liefert die besten Streams ohne Puffer? Unser ehrlicher Test zeigt den klaren Gewinner.",
    "iptv-deutschland-anbieter-vergleich":
        "Wir haben alle großen IPTV-Anbieter in Deutschland verglichen. Wer liefert wirklich HD ohne Puffer? Das Ergebnis überrascht.",
    "iptv-deutschland-komplett-guide":
        "IPTV in Deutschland 2026: Alles, was du wissen musst — Setup, Preise, Legalität. Der kompletteste Guide, den du finden wirst.",
    "iptv-einrichten-anleitung":
        "IPTV einrichten in 3 Minuten? So geht's — Schritt-für-Schritt-Anleitung für jeden Router, jeden TV und jedes Gerät.",
    "iptv-firestick-einrichten":
        "IPTV auf dem Firestick einrichten: So läuft's in 5 Minuten — ohne technische Kenntnisse, ohne Puffer, in HD & 4K.",
    "iptv-internet-geschwindigkeit":
        "Reichen 50 Mbit für IPTV wirklich aus? Die ehrliche Antwort überrascht die meisten — und so optimierst du deinen Stream.",
    "iptv-legal-deutschland":
        "Ist IPTV in Deutschland 2026 legal? Was Anwälte wirklich sagen — und welche Anbieter du bedenkenlos nutzen kannst.",
    "iptv-legal-oesterreich":
        "IPTV legal in Österreich? Das musst du 2026 wissen — klare Antworten statt juristischem Kauderwelsch. Lies es jetzt.",
    "iptv-legal-schweiz":
        "IPTV Schweiz 2026: Wann ist es legal, wann nicht? Der einzige Guide, der dir die ehrliche Antwort gibt — ohne Panik.",
    "iptv-preise-vergleich-2026":
        "Wir haben 58 IPTV-Preise verglichen — der günstigste kostet nur €4,83/Monat. Hier ist, warum du zu viel bezahlst.",
    "iptv-puffer-probleme-loesen":
        "IPTV ruckelt dauernd? Mit diesen 5 Tricks läuft dein Stream sofort flüssig — in HD, ohne ein einziges Mal neu starten.",
    "iptv-schweiz-legal":
        "IPTV in der Schweiz legal nutzen 2026: Was erlaubt ist, was nicht — und wo du sicher streamst ohne Abmahnrisiko.",
    "iptv-smart-tv-einrichten":
        "IPTV auf Samsung & LG Smart TV einrichten: Anleitung in 5 Minuten. Kein Extra-Gerät nötig — direkt auf dem TV.",
    "iptv-testbericht-top-anbieter":
        "Wir haben 5 IPTV-Anbieter monatelang getestet — 2 haben komplett versagt. Hier ist der ehrliche Testbericht mit Sieger.",
    "iptv-vs-kabelfernsehen":
        "IPTV vs. Kabel: Wer gewinnt 2026? Preise, Qualität, Kanäle — wir rechnen dir vor, warum Millionen den Kabelvertrag kündigen.",
    "iptv-wien-oesterreich":
        "Die 3 besten IPTV-Anbieter in Wien & ganz Österreich 2026 — getestet, verglichen und ehrlich bewertet. Klarer Sieger gefunden.",
    "iptv-zuerich-schweiz":
        "IPTV in Zürich: Wir haben den besten Anbieter für die Schweiz gefunden — schnell, stabil, günstig. Alle Details hier.",
    "jamal-musiala-wm-2026":
        "Jamal Musiala schießt Deutschland zum WM-Titel? Warum er 2026 der gefährlichste Spieler der Welt sein könnte — alle Fakten.",
    "wm-2026-alle-teams-qualifiziert":
        "Alle 48 qualifizierten Teams der WM 2026 auf einen Blick — und welche Überraschungen uns das Turnier bescheren wird.",
    "wm-2026-alle-teams":
        "48 Teams, ein Titel: Wer sind die Favoriten bei der WM 2026? Alle Gruppen, alle Spieler, alle Chancen — komplett erklärt.",
    "wm-2026-favoriten-wer-gewinnt":
        "Wer wird Weltmeister 2026? Unsere Experten haben alle 48 Teams analysiert — und kommen zu einem klaren, überraschenden Ergebnis.",
    "wm-2026-favoriten":
        "5 Teams kämpfen wirklich um den WM-Titel 2026. Deutschland ist dabei — aber wer ist wirklich der Favorit? Analyse & Quoten.",
    "wm-2026-kostenlos-schauen":
        "WM 2026 kostenlos & legal schauen in Deutschland, Österreich und der Schweiz — alle Sender, alle Spiele, ohne einen Cent.",
    "wm-2026-live-iptv":
        "WM 2026 live per IPTV in HD schauen — so geht's in Deutschland. Kein Sky, kein Dazn, nur €4,83/Monat für alle Spiele.",
    "wm-2026-spielorte":
        "Die 16 WM-Stadien 2026 in USA, Kanada und Mexiko: Welche Arenen Weltklasse sind — und wo das Finale stattfindet.",
    "wm-2026-spielplan":
        "Der komplette WM 2026 Spielplan mit allen Anstoßzeiten für Deutschland — alle Gruppenspiele, K.o.-Runden und das Finale.",
}

def fix_frontmatter(slug, content):
    photo_id = IMAGES.get(slug)
    desc = DESCRIPTIONS.get(slug)

    if photo_id:
        image_url = f"https://images.unsplash.com/{photo_id}?w=1200&q=80&auto=format&fit=crop"
        # Replace or add image field
        if re.search(r'^image:', content, re.MULTILINE):
            content = re.sub(r'^image:.*$', f'image: "{image_url}"', content, flags=re.MULTILINE)
        else:
            content = content.replace('---\n', '---\n', 1)
            # Insert image before closing ---
            content = re.sub(r'(\nkeywords:.*?\n)', r'\1image: "' + image_url + '"\n', content, count=1)

    if desc:
        # Replace description field
        content = re.sub(r'^description:.*$', f'description: "{desc}"', content, flags=re.MULTILINE)

    return content

for fname in os.listdir(BLOG_DIR):
    if not fname.endswith('.md'):
        continue
    slug = fname[:-3]
    path = os.path.join(BLOG_DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    updated = fix_frontmatter(slug, content)
    if updated != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"✓ {slug}")
    else:
        print(f"- {slug} (no change)")

print("\nDone!")
