"""
Instagram Story Generator – Paul Commercial Kiel
Immobilienmakler | Mehrfamilienhäuser | Gewerbeimmobilien | Kapitalanlagen
"""

import anthropic
import json
import random
from datetime import datetime
from typing import Literal

from canva_integration import (
    get_slide_canva_params,
    run_canva_agent,
    print_canva_summary,
    BRAND_KIT_ID,
)

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

BRAND = {
    "name": "Paul Commercial Kiel",
    "handle": "@paulcommercial.kiel",
    "slogan": "Ihre Immobilienexperten in Kiel & Schleswig-Holstein",
    "website": "www.paul-commercial.de",
    "cta_options": [
        "📩 Jetzt kostenfrei beraten lassen – Link in Bio!",
        "📞 Rufen Sie uns an – Erstberatung kostenlos!",
        "🔗 Mehr erfahren: Link in Bio",
        "📬 Schreiben Sie uns – wir antworten innerhalb von 24 h!",
        "📊 Kostenfreie Immobilienbewertung – Link in Bio!",
        "🤝 Vereinbaren Sie Ihr persönliches Beratungsgespräch!",
    ],
    "hashtags": [
        "#PaulCommercial",
        "#Immobilien",
        "#Kiel",
        "#SchleswigHolstein",
        "#Mehrfamilienhaus",
        "#Kapitalanlage",
        "#Gewerbeimmobilien",
        "#Immobilieninvestment",
        "#Bauträger",
        "#Neubau",
        "#WohnUndGeschäftshaus",
        "#Immobilienbewertung",
        "#Vermietung",
        "#Immobilienverkauf",
        "#Norddeutschland",
    ],
}

STORY_TYPES = {
    "markt_update": "Marktupdate & aktuelle Zahlen",
    "tipp": "Profi-Tipp für Investoren & Eigentümer",
    "bewertung": "Immobilienbewertung & Wertermittlung",
    "kapitalanlage": "Kapitalanlage & Rendite",
    "neubau": "Neubau & Bauträger",
    "gewerbe": "Gewerbeimmobilien",
    "vermietung": "Vermietung & Mietrendite",
    "verkauf": "Verkauf & Marktpreise",
    "faq": "FAQ – Häufige Fragen",
    "mehrfamilienhaus": "Mehrfamilienhäuser & Wohn-/Geschäftshäuser",
}

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _pick_cta() -> str:
    return random.choice(BRAND["cta_options"])


def _pick_hashtags(n: int = 8) -> str:
    tags = random.sample(BRAND["hashtags"], min(n, len(BRAND["hashtags"])))
    return " ".join(tags)


def _today() -> str:
    return datetime.now().strftime("%B %Y")


# ---------------------------------------------------------------------------
# System-Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = f"""Du bist ein erfahrener Social-Media-Experte und Copywriter für Immobilienunternehmen.
Du erstellst professionelle, informative Instagram-Story-Texte für **{BRAND['name']}** ({BRAND['handle']}).

**Über das Unternehmen:**
{BRAND['name']} ist ein Immobilienunternehmen mit Sitz in Kiel. Kernkompetenzen:
- Verkauf & Bewertung von Mehrfamilienhäusern
- Wohn- und Geschäftshäuser
- Kapitalanlagen & Anlageimmobilien
- Bauträgergeschäfte & Neubauvorhaben
- Gewerbeimmobilien (Vermarktung, Vermietung, Verkauf)

**Schreibstil & Vorgaben:**
- Förmlich (Sie-Form), professionell und seriös
- Kurz, prägnant – maximal 5–7 Slides pro Story
- Jede Slide hat max. 3–4 Zeilen Text
- Überzeugen mit Zahlen, Daten, Fakten (reale Marktdaten aus Deutschland/Schleswig-Holstein)
- Emojis gezielt einsetzen (1–2 pro Slide, passend zum Inhalt)
- Jede Story endet mit einem klaren, handlungsorientierten CTA
- Keine Übertreibungen oder unrealistische Versprechen
- Sprache: Deutsch

**Story-Struktur (Slides):**
1. Hook-Slide: Aufmerksamkeit wecken (Frage oder starke Zahl)
2. Info-Slides 1–4: Fakten, Tipps, Marktdaten
3. CTA-Slide: Klare Handlungsaufforderung + Kontakt

**Ausgabe als JSON:**
{{
  "story_typ": "...",
  "titel": "...",
  "slides": [
    {{"nummer": 1, "emoji": "🏢", "headline": "...", "text": "..."}},
    ...
  ],
  "cta": "...",
  "hashtags": "...",
  "posting_empfehlung": "Beste Uhrzeit: ..."
}}
"""

# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

def generate_story(
    story_type: str | None = None,
    thema: str | None = None,
    zielgruppe: Literal["Investoren", "Eigentümer", "Käufer", "Mieter", "Allgemein"] = "Allgemein",
    slides: int = 5,
) -> dict:
    """
    Generiert eine vollständige Instagram Story für Paul Commercial Kiel.

    Args:
        story_type: Schlüssel aus STORY_TYPES (z. B. 'kapitalanlage')
        thema:      Freies Thema (überschreibt story_type)
        zielgruppe: Zielgruppe der Story
        slides:     Anzahl der Slides (3–7)
    """
    client = anthropic.Anthropic()

    # Thema zusammenstellen
    if thema:
        topic = thema
    elif story_type and story_type in STORY_TYPES:
        topic = STORY_TYPES[story_type]
    else:
        topic = random.choice(list(STORY_TYPES.values()))

    cta = _pick_cta()
    hashtags = _pick_hashtags(8)

    user_prompt = f"""Erstelle eine Instagram Story für Paul Commercial Kiel.

**Thema:** {topic}
**Zielgruppe:** {zielgruppe}
**Anzahl Slides:** {slides} (inklusive Hook und CTA)
**Monat:** {_today()}
**CTA:** {cta}
**Hashtags:** {hashtags}

Nutze aktuelle, realistische Marktdaten für Schleswig-Holstein / Norddeutschland / Deutschland.
Erstelle die vollständige Story als JSON gemäß den Vorgaben."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()

    # JSON aus Antwort extrahieren
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    return json.loads(raw)


# ---------------------------------------------------------------------------
# Batch-Generator
# ---------------------------------------------------------------------------

def generate_weekly_plan(zielgruppen: list[str] | None = None) -> list[dict]:
    """Erstellt einen Wochenplan mit 5 Stories (Mo–Fr)."""
    if zielgruppen is None:
        zielgruppen = ["Investoren", "Eigentümer", "Käufer", "Allgemein", "Investoren"]

    story_keys = random.sample(list(STORY_TYPES.keys()), 5)
    plan = []

    print("🏢 Paul Commercial Kiel – Wochenplan wird generiert...\n")
    for i, (key, zg) in enumerate(zip(story_keys, zielgruppen)):
        day = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"][i]
        print(f"  ⏳ {day}: {STORY_TYPES[key]} ({zg})...")
        story = generate_story(story_type=key, zielgruppe=zg)
        story["wochentag"] = day
        plan.append(story)
        print(f"  ✅ {day}: Fertig!")

    return plan


# ---------------------------------------------------------------------------
# Ausgabe-Formatierung
# ---------------------------------------------------------------------------

def print_story(story: dict) -> None:
    """Gibt eine Story lesbar im Terminal aus."""
    divider = "─" * 55

    print(f"\n{divider}")
    print(f"  🏢 PAUL COMMERCIAL KIEL – Instagram Story")
    print(f"  Typ: {story.get('story_typ', '–')}")
    print(f"  Titel: {story.get('titel', '–')}")
    print(divider)

    for slide in story.get("slides", []):
        print(f"\n  📱 Slide {slide.get('nummer', '?')}  {slide.get('emoji', '')}")
        print(f"  ► {slide.get('headline', '')}")
        print(f"  {slide.get('text', '')}")

    print(f"\n{divider}")
    print(f"  📣 CTA:\n  {story.get('cta', '')}")
    print(f"\n  #️⃣  Hashtags:\n  {story.get('hashtags', '')}")
    print(f"\n  🕐 {story.get('posting_empfehlung', '')}")
    print(divider)


def save_stories(stories: list[dict], filename: str = "stories_output.json") -> None:
    """Speichert generierte Stories als JSON-Datei."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    print(f"\n💾 {len(stories)} Story/Stories gespeichert: {filename}")


# ---------------------------------------------------------------------------
# Interaktiver Modus
# ---------------------------------------------------------------------------

def interactive_mode() -> None:
    """Geführter Dialog zur Story-Generierung."""
    print("\n" + "═" * 55)
    print("  🏢 PAUL COMMERCIAL KIEL – Instagram Story Generator")
    print("  Immobilienexperten | Kiel & Schleswig-Holstein")
    print("═" * 55)

    print("\n📋 Verfügbare Story-Typen:")
    for i, (key, label) in enumerate(STORY_TYPES.items(), 1):
        print(f"  {i:2}. {label}")

    print("\n  0. Eigenes Thema eingeben")
    print("  W. Wochenplan generieren (5 Stories)")

    choice = input("\n➤ Ihre Auswahl: ").strip().lower()

    if choice == "w":
        plan = generate_weekly_plan()
        for story in plan:
            print_story(story)
        save_stories(plan, "wochenplan.json")
        return

    # Zielgruppe
    print("\n👥 Zielgruppe:")
    zielgruppen = ["Investoren", "Eigentümer", "Käufer", "Mieter", "Allgemein"]
    for i, zg in enumerate(zielgruppen, 1):
        print(f"  {i}. {zg}")
    zg_choice = input("➤ Zielgruppe (1–5, Standard: 5): ").strip()
    zielgruppe = zielgruppen[int(zg_choice) - 1] if zg_choice.isdigit() and 1 <= int(zg_choice) <= 5 else "Allgemein"

    # Slides
    slides_input = input("➤ Anzahl Slides (3–7, Standard: 5): ").strip()
    slides = int(slides_input) if slides_input.isdigit() and 3 <= int(slides_input) <= 7 else 5

    # Thema oder Typ
    if choice == "0":
        thema = input("➤ Geben Sie Ihr Thema ein: ").strip()
        story = generate_story(thema=thema, zielgruppe=zielgruppe, slides=slides)
    elif choice.isdigit() and 1 <= int(choice) <= len(STORY_TYPES):
        key = list(STORY_TYPES.keys())[int(choice) - 1]
        story = generate_story(story_type=key, zielgruppe=zielgruppe, slides=slides)
    else:
        print("❌ Ungültige Eingabe. Zufälliges Thema wird gewählt.")
        story = generate_story(zielgruppe=zielgruppe, slides=slides)

    print_story(story)

    # Speichern?
    save = input("\n💾 Story speichern? (j/n, Standard: j): ").strip().lower()
    if save != "n":
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_stories([story], f"story_{ts}.json")

    # Canva-Push?
    canva = input("\n🎨 Story direkt in Canva erstellen? (j/n, Standard: n): ").strip().lower()
    if canva == "j":
        print("\n" + "─" * 55)
        designs = run_canva_agent(story)
        print_canva_summary(designs)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"canva_designs_{ts}.json", "w", encoding="utf-8") as f:
            json.dump(designs, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Canva-Design-Daten gespeichert: canva_designs_{ts}.json")


# ---------------------------------------------------------------------------
# Canva-Direktfunktionen (Programmatischer Zugriff)
# ---------------------------------------------------------------------------

def generate_and_push_to_canva(
    story_type: str | None = None,
    thema: str | None = None,
    zielgruppe: str = "Allgemein",
    slides: int = 5,
) -> tuple[dict, list[dict]]:
    """
    Kompletter Workflow: Story generieren + direkt in Canva pushen.

    Returns:
        (story_json, canva_designs_liste)

    Beispiel:
        story, designs = generate_and_push_to_canva(
            story_type="kapitalanlage",
            zielgruppe="Investoren"
        )
    """
    print("🔄 Schritt 1/2: Story-Text wird generiert...")
    story = generate_story(story_type=story_type, thema=thema, zielgruppe=zielgruppe, slides=slides)
    print_story(story)

    print("\n🎨 Schritt 2/2: Canva-Designs werden erstellt...")
    designs = run_canva_agent(story)
    print_canva_summary(designs)

    return story, designs


def get_canva_params_for_story(story: dict) -> list[dict]:
    """
    Gibt alle Canva-Parameter für eine Story zurück –
    zur direkten Nutzung mit dem Canva MCP-Server.

    Beispiel (in Claude Code / MCP-Umgebung):
        params = get_canva_params_for_story(story)
        for p in params:
            # mcp__Canva__generate-design(**p)
            print(p)
    """
    slides = story.get("slides", [])
    return [get_slide_canva_params(story, i) for i in range(1, len(slides) + 1)]


# ---------------------------------------------------------------------------
# CLI-Einstiegspunkt
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    if "--demo" in args:
        print("🔄 Generiere Demo-Story...")
        story = generate_story(story_type="kapitalanlage", zielgruppe="Investoren", slides=5)
        print_story(story)
        save_stories([story], "demo_story.json")

    elif "--demo-canva" in args:
        print("🔄 Generiere Demo-Story + Canva-Integration...")
        story, designs = generate_and_push_to_canva(
            story_type="kapitalanlage", zielgruppe="Investoren", slides=5
        )
        save_stories([story], "demo_story_canva.json")

    elif "--wochenplan" in args:
        plan = generate_weekly_plan()
        for s in plan:
            print_story(s)
        save_stories(plan, "wochenplan.json")

    elif "--canva-params" in args:
        # Gibt Canva-Parameter für eine Demo-Story aus (für MCP-Nutzung)
        print("🔄 Generiere Canva-Parameter...")
        story = generate_story(story_type="markt_update", zielgruppe="Allgemein", slides=5)
        params = get_canva_params_for_story(story)
        print(json.dumps(params, ensure_ascii=False, indent=2))

    else:
        interactive_mode()
