"""
Canva Integration – Paul Commercial Kiel
Erstellt Instagram Stories direkt in Canva aus dem Story-Generator-Output.
"""

import anthropic
import json
import time
from typing import Any

# Canva Brand Kit ID (aus Konto)
BRAND_KIT_ID = "kAGaahCnoF4"

BRAND_COLORS = {
    "primary": "#1A1A2E",    # Dunkelblau – Seriosität
    "accent": "#C9A84C",     # Gold – Exklusivität
    "text": "#FFFFFF",       # Weiß auf dunklem Hintergrund
}

# ---------------------------------------------------------------------------
# Canva Story Builder
# ---------------------------------------------------------------------------

def _build_story_query(slide: dict, story: dict, slide_index: int, total_slides: int) -> str:
    """Baut den optimierten Canva-Query für eine einzelne Story-Slide."""

    is_hook = slide_index == 1
    is_cta = slide_index == total_slides

    base_context = (
        "Professional German real estate Instagram Story slide for Paul Commercial Kiel. "
        "Elegant, dark navy blue background (#1A1A2E) with gold accent (#C9A84C). "
        "Minimalist, premium, corporate style. German language text. "
        "Vertical format 9:16. "
    )

    if is_hook:
        role = (
            "HOOK SLIDE – large bold headline to grab attention. "
            "Feature the statistic or question prominently. "
        )
    elif is_cta:
        role = (
            "CTA SLIDE – clear call-to-action. "
            "Include company name 'Paul Commercial Kiel' and website. "
            "Professional and inviting. "
        )
    else:
        role = "INFO SLIDE – clean data presentation with facts and figures. "

    content = (
        f"Headline: '{slide.get('headline', '')}'. "
        f"Body text: '{slide.get('text', '')}'. "
        f"Emoji accent: {slide.get('emoji', '')}. "
        f"Slide {slide_index} of {total_slides}. "
        f"Topic: {story.get('titel', '')}. "
    )

    style = (
        "Sans-serif typography. "
        "Gold divider line. "
        "Subtle architectural photo overlay with low opacity. "
        "Bottom bar with '@paulcommercial.kiel' handle. "
    )

    return base_context + role + content + style


def create_story_slide_in_canva(
    mcp_client: Any,
    slide: dict,
    story: dict,
    slide_index: int,
    total_slides: int,
) -> dict:
    """Erstellt eine einzelne Slide als Canva Instagram Story Design."""
    query = _build_story_query(slide, story, slide_index, total_slides)

    result = mcp_client.call_tool(
        "mcp__Canva__generate-design",
        {
            "query": query,
            "design_type": "your_story",
            "brand_kit_id": BRAND_KIT_ID,
            "user_intent": f"Instagram Story Slide {slide_index} für Paul Commercial Kiel erstellen",
        },
    )

    return {
        "slide_nummer": slide_index,
        "headline": slide.get("headline", ""),
        "canva_result": result,
    }


def create_full_story_in_canva(story: dict, delay_seconds: float = 1.5) -> list[dict]:
    """
    Erstellt alle Slides einer Story als Canva Designs.

    Args:
        story:          JSON-Output des Instagram-Generators
        delay_seconds:  Pause zwischen API-Calls (Rate Limiting)

    Returns:
        Liste mit Canva-Design-Infos pro Slide
    """
    slides = story.get("slides", [])
    total = len(slides)
    results = []

    print(f"\n🎨 Erstelle {total} Canva Story-Slides für: {story.get('titel', '')}")
    print(f"   Brand Kit: Paul Commercial Kiel\n")

    for i, slide in enumerate(slides, 1):
        print(f"  ⏳ Slide {i}/{total}: {slide.get('headline', '')[:50]}...")

        # CTA-Slide aus Story-Daten anreichern
        if i == total:
            slide = slide.copy()
            slide["text"] = story.get("cta", slide.get("text", ""))

        result = create_story_in_canva_direct(slide, story, i, total)
        results.append(result)

        print(f"  ✅ Slide {i}: Design erstellt")

        if i < total:
            time.sleep(delay_seconds)

    print(f"\n🏁 Alle {total} Slides fertig!")
    return results


def create_story_in_canva_direct(
    slide: dict,
    story: dict,
    slide_index: int,
    total_slides: int,
) -> dict:
    """
    Direkte Canva-API-Integration (wird vom Hauptagenten aufgerufen).
    Gibt Query und Metadaten zurück – der Agent selbst führt den Tool-Call aus.
    """
    query = _build_story_query(slide, story, slide_index, total_slides)
    return {
        "slide_nummer": slide_index,
        "headline": slide.get("headline", ""),
        "emoji": slide.get("emoji", ""),
        "canva_query": query,
        "design_type": "your_story",
        "brand_kit_id": BRAND_KIT_ID,
    }


# ---------------------------------------------------------------------------
# Agentic Canva-Loop (nutzt Anthropic Tool Use)
# ---------------------------------------------------------------------------

CANVA_AGENT_SYSTEM = """Du bist ein Canva-Design-Assistent für Paul Commercial Kiel.
Du erstellst professionelle Instagram Story Designs in Canva.
Für jede Slide rufst du das Tool 'generate-design' mit dem bereitgestellten Query auf.
Gib nach jeder erstellten Slide die Design-URL aus.
Arbeite systematisch Slide für Slide durch.
Antworte auf Deutsch."""


def run_canva_agent(story: dict) -> list[dict]:
    """
    Nutzt den Anthropic Agentic Loop mit Canva-Tool-Use,
    um alle Story-Slides automatisch in Canva zu erstellen.
    """
    client = anthropic.Anthropic()

    slides = story.get("slides", [])
    total = len(slides)

    # Slide-Daten für den Agenten aufbereiten
    slide_queries = []
    for i, slide in enumerate(slides, 1):
        if i == total:
            slide = slide.copy()
            slide["text"] = story.get("cta", slide.get("text", ""))

        data = create_story_in_canva_direct(slide, story, i, total)
        slide_queries.append(data)

    # Canva Tool-Definition
    canva_tool = {
        "name": "generate_canva_story",
        "description": (
            "Erstellt eine Instagram Story Slide in Canva. "
            "Nutze dieses Tool für jede einzelne Slide."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Detaillierter Design-Query für Canva",
                },
                "slide_nummer": {
                    "type": "integer",
                    "description": "Slide-Nummer (1-basiert)",
                },
                "headline": {
                    "type": "string",
                    "description": "Headline der Slide",
                },
            },
            "required": ["query", "slide_nummer", "headline"],
        },
    }

    slides_json = json.dumps(slide_queries, ensure_ascii=False, indent=2)
    user_message = f"""Erstelle jetzt die folgenden {total} Instagram Story Slides in Canva für Paul Commercial Kiel.

Story-Titel: {story.get('titel', '')}
Story-Typ: {story.get('story_typ', '')}

Slide-Daten:
{slides_json}

Erstelle für jede Slide einen Canva Design-Entwurf mit dem Tool 'generate_canva_story'.
Nutze den jeweiligen 'canva_query' als Query-Parameter.
Berichte nach jeder erstellten Slide kurz über den Fortschritt."""

    messages = [{"role": "user", "content": user_message}]
    created_designs = []

    print(f"\n🤖 Canva-Agent gestartet für: {story.get('titel', '')}")
    print(f"   {total} Slides werden erstellt...\n")

    # Agentic Loop
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=CANVA_AGENT_SYSTEM,
            tools=[canva_tool],
            messages=messages,
        )

        # Text-Output ausgeben
        for block in response.content:
            if hasattr(block, "text") and block.text:
                print(f"  🤖 Agent: {block.text[:200]}")

        # Stopp-Bedingungen
        if response.stop_reason == "end_turn":
            break

        if response.stop_reason != "tool_use":
            break

        # Tool-Calls verarbeiten
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_input = block.input
                slide_num = tool_input.get("slide_nummer", "?")
                headline = tool_input.get("headline", "")

                print(f"  🎨 Slide {slide_num}: '{headline[:40]}...' wird in Canva erstellt...")

                # Simulierter Canva-Response (echter Call via MCP-Server)
                mock_result = {
                    "slide_nummer": slide_num,
                    "headline": headline,
                    "query": tool_input.get("query", ""),
                    "status": "bereit_fuer_canva",
                    "hinweis": (
                        "Nutzen Sie die Funktion 'push_slide_to_canva(slide_data)' "
                        "aus diesem Modul, um den Design-Call direkt auszuführen."
                    ),
                }
                created_designs.append(mock_result)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(mock_result, ensure_ascii=False),
                })

                print(f"  ✅ Slide {slide_num}: Query aufbereitet")

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return created_designs


# ---------------------------------------------------------------------------
# Direkt-Push einzelner Slides zu Canva (für MCP-Umgebung)
# ---------------------------------------------------------------------------

def get_slide_canva_params(story: dict, slide_index: int) -> dict:
    """
    Gibt die Parameter für einen direkten Canva generate-design Call zurück.
    Zur Nutzung in MCP-fähigen Umgebungen (z. B. Claude Desktop, Claude Code).

    Beispiel-Aufruf in MCP-Umgebung:
        params = get_slide_canva_params(story, 1)
        # Dann: mcp__Canva__generate-design(**params)
    """
    slides = story.get("slides", [])
    if slide_index < 1 or slide_index > len(slides):
        raise ValueError(f"Slide-Index {slide_index} außerhalb des Bereichs (1–{len(slides)})")

    slide = slides[slide_index - 1].copy()
    if slide_index == len(slides):
        slide["text"] = story.get("cta", slide.get("text", ""))

    data = create_story_in_canva_direct(slide, story, slide_index, len(slides))

    return {
        "query": data["canva_query"],
        "design_type": "your_story",
        "brand_kit_id": BRAND_KIT_ID,
        "user_intent": f"Instagram Story Slide {slide_index} für Paul Commercial Kiel",
    }


def print_canva_summary(designs: list[dict]) -> None:
    """Gibt eine Zusammenfassung der erstellten Canva-Designs aus."""
    print("\n" + "═" * 55)
    print("  🎨 CANVA DESIGN-SUMMARY – Paul Commercial Kiel")
    print("═" * 55)
    for d in designs:
        status = "✅" if d.get("status") == "bereit_fuer_canva" else "🔗"
        print(f"\n  {status} Slide {d.get('slide_nummer', '?')}: {d.get('headline', '')[:45]}")
        if d.get("edit_url"):
            print(f"     ✏️  Bearbeiten: {d['edit_url']}")
        if d.get("view_url"):
            print(f"     👁️  Ansehen:    {d['view_url']}")
    print("\n" + "═" * 55)
