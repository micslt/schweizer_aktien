# CLAUDE.md – Beitragsqueue @schweizer_aktien

Dieses Repo ist die Warteschlange für Instagram-Beiträge des Kontos @schweizer_aktien.
Claude Code bereitet Beiträge vor und committet sie. Das Scheduling in Metricool macht Claude (Chat) nach manueller Freigabe. Claude Code plant NICHT selbst.

## Repo-Struktur

```
posts/
  2026-10-20-nestle-q3.json
  2026-10-22-smi-wochenrueckblick.json
media/
  2026-10-20-nestle-q3/
    01.jpg
    02.jpg
templates/
  caption-style.md
```

Dateiname: `YYYY-MM-DD-slug.json`, Slug kleingeschrieben, nur a-z, 0-9 und Bindestrich. Medienordner trägt denselben Namen wie die JSON-Datei ohne Endung.

## JSON-Schema pro Beitrag

```json
{
  "slug": "2026-10-20-nestle-q3",
  "status": "ready",
  "type": "POST",
  "publish_at": "2026-10-20T07:30:00",
  "timezone": "Europe/Zurich",
  "caption": "…",
  "first_comment": "…",
  "media": ["media/2026-10-20-nestle-q3/01.jpg", "media/2026-10-20-nestle-q3/02.jpg"],
  "media_alt": ["Nestlé Logo mit Q3 Kennzahlen", "Umsatzentwicklung 2024 bis 2026 als Balken"],
  "ai_generated_media": false,
  "sources": ["https://www.nestle.com/investors/…"],
  "metricool_uuid": null,
  "notes": ""
}
```

Felder:
- `status`: `draft` → `ready` → `scheduled` → `published`. Claude Code setzt nur `draft` und `ready`. `scheduled` setzt Claude (Chat) oder Michael nach dem Planen.
- `type`: `POST` (Bild oder Karussell), `REEL` (Video), `STORY`.
- `publish_at`: lokale Zeit ohne Offset, Zeitzone immer `Europe/Zurich`.
- `media`: 1 bis 10 Einträge bei POST, genau 1 Video bei REEL. Pfade relativ zum Repo-Root. Die Datei muss im Repo liegen und committet sein, sonst kann Metricool sie nicht abrufen.
- `media_alt`: gleiche Länge wie `media`.
- `ai_generated_media`: `true`, wenn Bilder KI-generiert oder KI-verändert sind. Instagram verlangt diese Kennzeichnung.
- `sources`: Quellen für jede Zahl in der Caption. Keine Zahl ohne Quelle.
- `metricool_uuid`: bleibt `null`, wird nach dem Scheduling eingetragen.

## Anforderungen an Medien

- Format JPG oder PNG, max. 8 MB pro Bild.
- Feed-Post: 1080×1350 px (4:5) bevorzugt, sonst 1080×1080. Seitenverhältnis zwischen 4:5 und 1.91:1, sonst lehnt Instagram ab.
- Reel: MP4, 9:16, max. 90 s, max. 100 MB (grosse Videos ggf. extern hosten und als URL eintragen).
- Keine Logos oder Fotos verwenden, deren Rechte unklar sind. Bei Firmenlogos nur aus offiziellen Media-Kits der Firma.
- Keine Charts aus Drittquellen kopieren (TradingView, Bloomberg, SIX Screenshots). Charts selbst rendern, z.B. mit matplotlib, und die Datenquelle im Bild nennen.

## Anforderungen an Captions

- Sprache Deutsch, Schweizer Schreibweise (ss statt ß, keine Anführungszeichen „“ sondern «»).
- Max. 2200 Zeichen, erste 125 Zeichen müssen für sich stehen (Instagram kürzt dort ab).
- Keine Gedankenstriche als Stilmittel. Punkt, Komma, Doppelpunkt.
- Keine Kauf- oder Verkaufsempfehlungen. Keine Kursziele. Keine Formulierungen wie «jetzt einsteigen» oder «klarer Kauf».
- Jeder Beitrag endet mit: «Keine Anlageberatung. Eigene Recherche.»
- Hashtags in `first_comment`, nicht in der Caption. Max. 30, davon immer `#schweizeraktien #smi #börseschweiz`. Rest beitragsspezifisch (Ticker, Firma, Branche).
- Zahlen nur mit Quelle in `sources`. Keine Zahl erfinden oder schätzen. Wenn keine verlässliche Quelle vorliegt: Zahl weglassen.
- Kein Wording, das Kursbewegungen vorhersagt. Beschreiben, was war, nicht was kommt.

## Workflow für Claude Code

1. Thema entgegennehmen (von Michael).
2. Fakten recherchieren, Quellen in `sources` ablegen.
3. Bilder erzeugen oder beschaffen, nach `media/<slug>/` legen, Spezifikationen prüfen (Grösse, Format, Seitenverhältnis).
4. JSON schreiben, `status: "draft"`.
5. Selbstcheck gegen die Caption-Regeln oben. Erst dann `status: "ready"`.
6. Commit mit Message `post: <slug> ready` und push.
7. Michael kurz melden: Slug, geplantes Datum, Anzahl Bilder.

Niemals `status` auf `scheduled` oder `published` setzen. Niemals `publish_at` in der Vergangenheit. Niemals bestehende Beiträge mit `scheduled` oder `published` bearbeiten, ausser Michael sagt es explizit.

## Übergabe an Claude (Chat)

Repo: https://github.com/micslt/schweizer_aktien (public, Branch `main`). Raw-Basis: `https://raw.githubusercontent.com/micslt/schweizer_aktien/main/`, z.B. `…/main/posts/<slug>.json` und `…/main/media/<slug>/01.png`.

Claude (Chat) liest alle JSON-Dateien mit `status: "ready"` über die GitHub-API bzw. raw.githubusercontent.com, zeigt Michael die Captions zur Freigabe, plant die Beiträge in Metricool (Brand 7441902) und meldet pro Beitrag die `metricool_uuid` zurück. Michael oder Claude Code tragen danach die UUID ein und setzen `status: "scheduled"`.

## Werkzeuge im Repo

- `scripts/validate.py`: prüft alle JSONs in `posts/` gegen die Regeln oben (Schema, Slug, Datum, Caption-Regeln, Hashtags, Medien inkl. Bildmasse). Vor jedem `status: "ready"` ausführen, Exit-Code muss 0 sein.
- `scripts/render_chart.py`: rendert Balken- oder Liniendiagramme als 1080×1350 PNG mit Quellenangabe und Disclaimer im Bild. Läuft mit `.venv/bin/python` (matplotlib ist nur in der venv installiert, Einrichtung siehe README).
- `templates/post.template.json`: leeres Beitrags-JSON als Ausgangspunkt.
- `templates/caption-style.md`: Tonalität, Aufbau, Hashtag-Sets, verbotene Formulierungen, Beispiel.
