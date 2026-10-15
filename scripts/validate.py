#!/usr/bin/env python3
"""Prüft Beitrags-JSONs in posts/ gegen die Regeln aus CLAUDE.md.

Aufruf:
    python3 scripts/validate.py                 # alle Beiträge
    python3 scripts/validate.py posts/2026-10-20-nestle-q3.json
    python3 scripts/validate.py --ready-only    # nur status ready

Exit-Code 0 = alles in Ordnung, 1 = mindestens ein Fehler.
Warnungen (W) blockieren nicht, Fehler (E) schon.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from PIL import Image
except ImportError:  # Pillow fehlt, Bildmasse werden dann nicht geprüft
    Image = None

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts"
TZ = ZoneInfo("Europe/Zurich")

REQUIRED_FIELDS = [
    "slug", "status", "type", "publish_at", "timezone", "caption",
    "first_comment", "media", "media_alt", "ai_generated_media",
    "sources", "metricool_uuid", "notes",
]
STATUSES = {"draft", "ready", "scheduled", "published"}
TYPES = {"POST", "REEL", "STORY"}
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
DISCLAIMER = "Keine Anlageberatung. Eigene Recherche."
REQUIRED_TAGS = {"#schweizeraktien", "#smi", "#börseschweiz"}
MAX_CAPTION = 2200
MAX_HOOK = 125
MAX_TAGS = 30
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_VIDEO_BYTES = 100 * 1024 * 1024

FORBIDDEN_PHRASES = [
    "jetzt einsteigen", "klarer kauf", "kaufchance", "nachkaufen",
    "verkaufssignal", "abstossen", "kursziel", "wird steigen", "wird fallen",
    "dürfte zulegen", "dürfte steigen", "dürfte fallen", "rallye voraus",
    "geheimtipp", "schnäppchen", "to the moon", "garantiert", "risikolos",
    "kaufempfehlung", "verkaufsempfehlung", "kaufen!", "verkaufen!",
]
FORBIDDEN_CHARS = {
    "–": "Gedankenstrich (en dash)",
    "—": "Gedankenstrich (em dash)",
    "ß": "ß, Schweizer Schreibweise verlangt ss",
    "„": "deutsches Anführungszeichen, bitte «»",
    "“": "deutsches Anführungszeichen, bitte «»",
    "”": "englisches Anführungszeichen, bitte «»",
}


class Report:
    def __init__(self, name):
        self.name = name
        self.errors = []
        self.warnings = []

    def e(self, msg):
        self.errors.append(msg)

    def w(self, msg):
        self.warnings.append(msg)

    def print(self):
        status = "FEHLER" if self.errors else ("WARNUNG" if self.warnings else "OK")
        print(f"[{status}] {self.name}")
        for m in self.errors:
            print(f"  E {m}")
        for m in self.warnings:
            print(f"  W {m}")


def check_text_rules(text, label, rep):
    for ch, why in FORBIDDEN_CHARS.items():
        if ch in text:
            rep.e(f"{label} enthält {why}")
    low = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in low:
            rep.e(f"{label} enthält verbotene Formulierung «{phrase}»")


def check_media_file(path_str, post_type, idx, rep):
    path = ROOT / path_str
    if path_str.startswith(("http://", "https://")):
        rep.w(f"media[{idx}] ist eine externe URL, Erreichbarkeit nicht geprüft")
        return
    if not path_str.startswith("media/"):
        rep.e(f"media[{idx}] muss unter media/ liegen: {path_str}")
    if not path.exists():
        rep.e(f"media[{idx}] fehlt im Repo: {path_str}")
        return
    size = path.stat().st_size
    ext = path.suffix.lower()
    if post_type == "REEL":
        if ext != ".mp4":
            rep.e(f"media[{idx}] REEL verlangt MP4, gefunden {ext}")
        if size > MAX_VIDEO_BYTES:
            rep.e(f"media[{idx}] grösser als 100 MB ({size / 1e6:.1f} MB), extern hosten")
        return
    if ext not in (".jpg", ".jpeg", ".png"):
        rep.e(f"media[{idx}] muss JPG oder PNG sein, gefunden {ext}")
        return
    if size > MAX_IMAGE_BYTES:
        rep.e(f"media[{idx}] grösser als 8 MB ({size / 1e6:.1f} MB)")
    if Image is None:
        rep.w(f"media[{idx}] Bildmasse nicht geprüft (Pillow fehlt)")
        return
    with Image.open(path) as im:
        w, h = im.size
    ratio = w / h
    if post_type == "POST":
        if not (0.8 - 0.005 <= ratio <= 1.91 + 0.005):
            rep.e(f"media[{idx}] Seitenverhältnis {w}x{h} ({ratio:.2f}) liegt ausserhalb 4:5 bis 1.91:1")
        if (w, h) not in ((1080, 1350), (1080, 1080)):
            rep.w(f"media[{idx}] ist {w}x{h}, bevorzugt 1080x1350 oder 1080x1080")
    elif post_type == "STORY":
        if abs(ratio - 9 / 16) > 0.01:
            rep.w(f"media[{idx}] Story ist {w}x{h}, bevorzugt 1080x1920 (9:16)")


def validate(path):
    rep = Report(path.relative_to(ROOT).as_posix())
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        rep.e(f"kein gültiges JSON: {ex}")
        return rep

    for f in REQUIRED_FIELDS:
        if f not in data:
            rep.e(f"Feld fehlt: {f}")
    if rep.errors:
        return rep

    # Slug und Dateiname
    slug = data["slug"]
    if not SLUG_RE.match(slug):
        rep.e(f"slug ungültig: {slug} (Muster YYYY-MM-DD-slug, nur a-z 0-9 -)")
    if path.stem != slug:
        rep.e(f"Dateiname {path.stem} passt nicht zu slug {slug}")

    # Status und Typ
    if data["status"] not in STATUSES:
        rep.e(f"status ungültig: {data['status']}")
    if data["type"] not in TYPES:
        rep.e(f"type ungültig: {data['type']}")
    if data["timezone"] != "Europe/Zurich":
        rep.e(f"timezone muss Europe/Zurich sein, ist {data['timezone']}")

    # publish_at
    try:
        if re.search(r"(Z|[+-]\d{2}:\d{2})$", data["publish_at"]):
            rep.e("publish_at darf keinen Offset enthalten (lokale Zeit)")
        pub = datetime.fromisoformat(data["publish_at"]).replace(tzinfo=TZ)
        if pub <= datetime.now(TZ) and data["status"] in ("draft", "ready"):
            rep.e(f"publish_at liegt in der Vergangenheit: {data['publish_at']}")
        if not slug.startswith(pub.strftime("%Y-%m-%d")):
            rep.w(f"Datum im slug ({slug[:10]}) weicht von publish_at ({pub.date()}) ab")
    except ValueError:
        rep.e(f"publish_at kein gültiges ISO-Datum: {data['publish_at']}")

    # Caption
    cap = data["caption"]
    if not cap.strip():
        rep.e("caption ist leer")
    else:
        if len(cap) > MAX_CAPTION:
            rep.e(f"caption hat {len(cap)} Zeichen, max. {MAX_CAPTION}")
        if not cap.rstrip().endswith(DISCLAIMER):
            rep.e(f"caption endet nicht mit «{DISCLAIMER}»")
        if "#" in cap:
            rep.e("caption enthält Hashtags, die gehören in first_comment")
        hook = cap.split("\n", 1)[0].strip()
        if len(hook) > MAX_HOOK:
            rep.w(f"erste Zeile (Hook) hat {len(hook)} Zeichen, Instagram kürzt bei {MAX_HOOK}")
        check_text_rules(cap, "caption", rep)
        if re.search(r"\d", cap) and not data["sources"]:
            rep.e("caption enthält Zahlen, aber sources ist leer")

    # First Comment / Hashtags
    fc = data["first_comment"]
    tags = re.findall(r"#[\wäöüÄÖÜ]+", fc)
    tagset = {t.lower() for t in tags}
    missing = REQUIRED_TAGS - tagset
    if missing:
        rep.e(f"Pflicht-Hashtags fehlen in first_comment: {' '.join(sorted(missing))}")
    if len(tags) > MAX_TAGS:
        rep.e(f"first_comment hat {len(tags)} Hashtags, max. {MAX_TAGS}")
    if len(tags) != len(tagset):
        rep.w("first_comment enthält doppelte Hashtags")
    check_text_rules(fc, "first_comment", rep)

    # Medien
    media = data["media"]
    alt = data["media_alt"]
    if not isinstance(media, list) or not isinstance(alt, list):
        rep.e("media und media_alt müssen Listen sein")
    else:
        if data["type"] == "POST" and not (1 <= len(media) <= 10):
            rep.e(f"POST braucht 1 bis 10 Medien, hat {len(media)}")
        if data["type"] == "REEL" and len(media) != 1:
            rep.e(f"REEL braucht genau 1 Video, hat {len(media)}")
        if data["type"] == "STORY" and len(media) != 1:
            rep.e(f"STORY braucht genau 1 Medium, hat {len(media)}")
        if len(alt) != len(media):
            rep.e(f"media_alt hat {len(alt)} Einträge, media hat {len(media)}")
        for i, a in enumerate(alt):
            if not str(a).strip():
                rep.e(f"media_alt[{i}] ist leer")
            elif len(a) > 200:
                rep.w(f"media_alt[{i}] hat {len(a)} Zeichen, max. 200 empfohlen")
        expected_dir = f"media/{slug}/"
        for i, m in enumerate(media):
            if not str(m).startswith(("http://", "https://")) and not str(m).startswith(expected_dir):
                rep.e(f"media[{i}] muss in {expected_dir} liegen: {m}")
            check_media_file(str(m), data["type"], i, rep)

    if not isinstance(data["ai_generated_media"], bool):
        rep.e("ai_generated_media muss true oder false sein")

    # Quellen
    for i, s in enumerate(data["sources"]):
        if not re.match(r"^https?://", str(s)):
            rep.e(f"sources[{i}] ist keine URL: {s}")

    # Status-Konsistenz
    if data["status"] in ("scheduled", "published") and not data["metricool_uuid"]:
        rep.e(f"status {data['status']} verlangt eine metricool_uuid")
    if data["status"] in ("draft", "ready") and data["metricool_uuid"]:
        rep.w("metricool_uuid gesetzt, aber status ist noch nicht scheduled")

    return rep


def main(argv):
    ready_only = "--ready-only" in argv
    files = [Path(a) for a in argv if not a.startswith("--")]
    if not files:
        files = sorted(POSTS.glob("*.json"))
    if not files:
        print("Keine Beiträge in posts/ gefunden.")
        return 0
    failed = 0
    for f in files:
        f = f if f.is_absolute() else ROOT / f
        rep = validate(f)
        if ready_only:
            try:
                if json.loads(f.read_text(encoding="utf-8")).get("status") != "ready":
                    continue
            except Exception:
                pass
        rep.print()
        if rep.errors:
            failed += 1
    print(f"\n{len(files)} geprüft, {failed} mit Fehlern.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
