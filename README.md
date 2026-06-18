# Instagram Story Generator – Paul Commercial Kiel

Automatischer KI-Agent zur Erstellung professioneller Instagram Stories für **Paul Commercial Kiel** – Immobilienexperten in Kiel & Schleswig-Holstein.

---

## Funktionen

| Feature | Beschreibung |
|---|---|
| 10 Story-Typen | Markt, Kapitalanlage, Neubau, Gewerbe, Bewertung u. v. m. |
| Wochenplan | Automatisch 5 Stories für Mo–Fr |
| Zielgruppen | Investoren, Eigentümer, Käufer, Mieter, Allgemein |
| CTA-Rotation | 6 wechselnde Handlungsaufforderungen |
| Hashtag-Auswahl | 15 Branchen-Hashtags, 8 pro Story zufällig gewählt |
| JSON-Export | Alle Stories werden als `.json` gespeichert |
| Interaktiver Modus | Geführter Dialog im Terminal |

---

## Voraussetzungen

```bash
pip install -r requirements.txt
```

Umgebungsvariable setzen:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Nutzung

### Interaktiver Modus (empfohlen)

```bash
python paul_commercial_instagram_agent.py
```

Menü:
```
 1. Marktupdate & aktuelle Zahlen
 2. Profi-Tipp für Investoren & Eigentümer
 3. Immobilienbewertung & Wertermittlung
 4. Kapitalanlage & Rendite
 5. Neubau & Bauträger
 6. Gewerbeimmobilien
 7. Vermietung & Mietrendite
 8. Verkauf & Marktpreise
 9. FAQ – Häufige Fragen
10. Mehrfamilienhäuser & Wohn-/Geschäftshäuser
 0. Eigenes Thema eingeben
 W. Wochenplan generieren (5 Stories)
```

### Demo-Story

```bash
python paul_commercial_instagram_agent.py --demo
```

### Wochenplan

```bash
python paul_commercial_instagram_agent.py --wochenplan
```

---

## Ausgabe-Beispiel

```
───────────────────────────────────────────────────────
  🏢 PAUL COMMERCIAL KIEL – Instagram Story
  Typ: Kapitalanlage & Rendite
  Titel: Warum Mehrfamilienhäuser 2025 rentabel bleiben
───────────────────────────────────────────────────────

  📱 Slide 1  💰
  ► Wussten Sie? Ø-Rendite MFH Kiel: 4,2 % p. a.
  Mehrfamilienhäuser zählen weiterhin zu den
  stabilsten Kapitalanlagen in Deutschland.

  📱 Slide 2  📊
  ► Stabile Nachfrage in Schleswig-Holstein
  Leerstandsquote Kiel: < 1,5 % – eine der
  niedrigsten im norddeutschen Vergleich.
  ...

───────────────────────────────────────────────────────
  📣 CTA:
  📊 Kostenfreie Immobilienbewertung – Link in Bio!

  #️⃣  Hashtags:
  #PaulCommercial #Kapitalanlage #Kiel ...

  🕐 Beste Uhrzeit: Di–Do, 18–20 Uhr
───────────────────────────────────────────────────────
```

---

## Story-Typen im Detail

| Typ | Inhalt | Zielgruppe |
|---|---|---|
| `markt_update` | Aktuelle Preise, Trends | Alle |
| `tipp` | Expertentipps | Eigentümer, Investoren |
| `bewertung` | Wertermittlung, Faktoren | Eigentümer |
| `kapitalanlage` | Rendite, ROI, Kennzahlen | Investoren |
| `neubau` | Bauträger, Projektentwicklung | Käufer, Investoren |
| `gewerbe` | Gewerbeflächen, Miete | Unternehmer |
| `vermietung` | Mietmarkt, Mietrendite | Vermieter |
| `verkauf` | Verkaufsprozess, Preise | Eigentümer |
| `faq` | Häufige Fragen | Allgemein |
| `mehrfamilienhaus` | MFH, WGH Besonderheiten | Investoren |

---

## Unternehmen

**Paul Commercial Kiel**  
Immobilienexperten für Mehrfamilienhäuser, Wohn- & Geschäftshäuser,
Kapitalanlagen, Bauträger, Neubau und Gewerbeimmobilien.
