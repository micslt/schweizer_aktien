# Caption-Stil @schweizer_aktien

Diese Vorlage ergänzt die Regeln in `CLAUDE.md`. Bei Widerspruch gilt `CLAUDE.md`.

## Tonalität

- Sachlich, knapp, ohne Hype. Wir berichten, wir empfehlen nicht.
- Du-Form gegenüber der Leserschaft, aber sparsam. Lieber neutral formulieren.
- Schweizer Schreibweise: ss statt ß, Guillemets «so», Tausendertrennung mit Apostroph (1'234'567), Dezimaltrennung mit Punkt (3.5 %), Prozentzeichen mit Leerschlag.
- Währung immer als CHF, Mio. und Mrd. abgekürzt: «CHF 2.3 Mrd.»
- Keine Gedankenstriche als Stilmittel. Punkt, Komma, Doppelpunkt, Klammern.
- Keine Emojis in Zahlenaussagen. Höchstens ein Emoji am Anfang der Caption, bei Ergebnismeldungen keines.

## Aufbau einer Caption

1. **Hook (max. 125 Zeichen)**: Die Kernaussage in einem Satz. Muss ohne den Rest verständlich sein, Instagram kürzt dort ab.
2. **Fakten (3 bis 5 kurze Absätze)**: Je ein Gedanke pro Absatz. Zahlen immer mit Zeitbezug («Q3 2026», «per 30.9.2026»).
3. **Einordnung**: Was bedeutet das im Kontext? Vergleich mit Vorjahr, Branche oder Erwartung des Unternehmens. Keine Prognose.
4. **Frage an die Community (optional)**: Eine offene Frage, die kein Kauf- oder Verkaufsurteil verlangt.
5. **Abschluss (Pflicht)**: `Keine Anlageberatung. Eigene Recherche.`

## Beitragstypen

| Typ | Beispiel-Slug | Hook-Muster |
|---|---|---|
| Quartalszahlen | `2026-10-20-nestle-q3` | «Nestlé meldet für Q3 2026 ein organisches Wachstum von X %.» |
| Wochenrückblick SMI | `2026-10-24-smi-wochenrueckblick` | «SMI-Woche 43: Der Index schliesst bei X Punkten, Y % zur Vorwoche.» |
| Firmenporträt | `2026-11-02-portraet-geberit` | «Geberit in 60 Sekunden: Was der Sanitärkonzern aus Rapperswil-Jona macht.» |
| Dividenden | `2026-03-15-dividenden-smi` | «Diese SMI-Firmen haben für 2025 eine Dividende angekündigt.» |
| Begriffserklärung | `2026-11-10-erklaert-kgv` | «KGV erklärt: Was die Kennzahl aussagt und was nicht.» |
| Börsengang / Event | `2026-09-05-ipo-xy` | «Xy geht an die SIX: Das Wichtigste zum Börsengang.» |

## Verbotene Formulierungen

Niemals verwenden, auch nicht in Fragen oder Zitaten ohne Quelle:

- «jetzt einsteigen», «klarer Kauf», «Kaufchance», «nachkaufen», «Verkaufssignal», «abstossen»
- «Kursziel», «Potenzial von X %», «wird steigen», «wird fallen», «dürfte zulegen», «Rallye voraus»
- «Geheimtipp», «unterbewertet» (ohne Quelle, die das genau so sagt), «Schnäppchen»
- «to the moon», «garantiert», «sicher», «risikolos»

Zulässig ist die Wiedergabe von Analystenmeinungen nur mit Quelle und Absender: «Die ZKB stuft die Aktie laut Bericht vom 12.10.2026 mit ‹Übergewichten› ein.» Auch dann kein eigenes Urteil anhängen.

## Hashtags (im `first_comment`)

Immer dabei: `#schweizeraktien #smi #börseschweiz`

Danach 10 bis 20 beitragsspezifische Hashtags, in dieser Reihenfolge:

1. Firma und Ticker: `#nestle #nesn`
2. Branche: `#nahrungsmittel #konsumgüter`
3. Thema: `#quartalszahlen #q3`
4. Allgemein: `#aktien #investieren #finanzen #schweiz #six #börse #finanzbildung #geldanlage #dividenden`

Maximal 30 Hashtags. Keine Hashtags in der Caption selbst.

## Quellen

- Primärquellen bevorzugen: Medienmitteilungen und Investor-Relations-Seiten der Firma, SIX Swiss Exchange, SNB, BFS.
- Sekundärquellen (NZZ, Finanz und Wirtschaft, cash.ch, SRF) nur, wenn keine Primärquelle vorliegt oder sie die Einordnung liefert.
- Jede Zahl in der Caption muss einer URL in `sources` zuordenbar sein. Im Zweifel die Zahl streichen.
- Kursdaten mit Datum und Uhrzeit des Standes nennen («Schlusskurs 14.10.2026»).

## Alt-Texte (`media_alt`)

- Beschreiben, was zu sehen ist, inklusive der Kernzahl im Bild: «Balkendiagramm Umsatz Nestlé 2024 bis 2026 in CHF Mrd., Quelle Nestlé Geschäftsbericht».
- 1 bis 2 Sätze, max. 200 Zeichen, keine Hashtags.

## Beispiel

**Caption**

```
Nestlé meldet für die ersten neun Monate 2026 ein organisches Wachstum von 2.8 %.

Der Umsatz lag bei CHF 65.9 Mrd. Das interne Realwachstum betrug 0.6 %, die Preiserhöhungen trugen 2.2 % bei.

Am stärksten wuchs das Geschäft mit Tiernahrung (Purina) mit 5.1 %. Die Zone Europa legte 1.9 % zu.

Nestlé bestätigt die Jahresprognose: organisches Wachstum von rund 3 %, operative Marge zwischen 16.0 und 16.5 %.

Zum Vergleich: Im Vorjahreszeitraum lag das organische Wachstum bei 2.0 %.

Welche Sparte von Nestlé verfolgst du am genauesten?

Keine Anlageberatung. Eigene Recherche.
```

**First Comment**

```
#schweizeraktien #smi #börseschweiz #nestle #nesn #nahrungsmittel #konsumgüter #quartalszahlen #q3 #neunmonatszahlen #aktien #investieren #finanzen #schweiz #six #börse #finanzbildung #geldanlage
```

Hinweis: Die Zahlen im Beispiel sind Platzhalter und illustrieren nur das Format. Für einen echten Beitrag jede Zahl aus der Medienmitteilung übernehmen und in `sources` belegen.
