# Beitragsqueue @schweizer_aktien

Warteschlange für Instagram-Beiträge. Regeln und Workflow stehen in [CLAUDE.md](CLAUDE.md), der Caption-Stil in [templates/caption-style.md](templates/caption-style.md).

## Einrichtung

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Werkzeuge

```bash
# Alle Beiträge gegen die Regeln prüfen (Exit 1 bei Fehlern)
python3 scripts/validate.py
python3 scripts/validate.py --ready-only
python3 scripts/validate.py posts/2026-10-20-nestle-q3.json

# Diagramm im Format 1080x1350 rendern (Spezifikation siehe Docstring im Skript)
.venv/bin/python scripts/render_chart.py spec.json media/<slug>/02.png
```

## Neuer Beitrag in Kürze

1. `templates/post.template.json` nach `posts/YYYY-MM-DD-slug.json` kopieren.
2. Bilder nach `media/YYYY-MM-DD-slug/` legen (01.png, 02.png, …).
3. Caption nach `templates/caption-style.md` schreiben, Quellen eintragen.
4. `python3 scripts/validate.py` ausführen, bis keine Fehler mehr gemeldet werden.
5. `status` auf `ready` setzen, committen mit `post: <slug> ready`, pushen.
