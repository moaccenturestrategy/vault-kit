---
name: dashboard
description: Ein Dashboard bauen — KPI-Zeilen, Charts, Meter, Tabellen — als standalone HTML oder React-Artefakt. Nutzen bei "Dashboard", "KPI-Übersicht", "Kennzahlen visualisieren", "Auswertungs-Dashboard", "Analytics-Board", "Report-Dashboard". Vor dem ersten Chart-Code den dataviz-Skill lesen.
---

# dashboard

Baut ein Dashboard, das als System liest, nicht als Konfetti.

## Hard rules
- **Vor der ersten Zeile Chart-Code den `dataviz`-Skill lesen.** Farbformel, Chart-Wahl (Form-Heuristik), Stat-Tiles, Legenden und Layout kommen von dort. Grund: bei mehreren Serien/Farben entscheidet die Ruhe der Palette, ob man Struktur sieht — selbst erfundene Farben werden Konfetti.
- **Keine Kennzahl aus dem Gedächtnis.** Jedes Tile/jeder Datenpunkt zitiert eine Datei in `<projekt>/08_Reference` oder `05_Data`. Steht die Zahl nirgends, gibt es dafür kein Tile.
- **Standalone-first:** kein CDN, keine externe Bibliothek — inline. Ein Dashboard soll auch in Jahren ohne Netz aufgehen (gleiche Doktrin wie der Vault-Graph-Betrachter). Ausnahme nur, wenn ausdrücklich ein React-Artefakt gewünscht ist.
- **Inline-JS so strukturieren, dass es in eine `.js` ziehbar ist**, falls die Seite später gegraphed wird — Graphify parst kein HTML (siehe `__VAULT__/CLAUDE.md`).
- Output nach `<projekt>/04_Output/`.

## Procedure
1. `dataviz`-Skill lesen.
2. Datenquelle(n) in `05_Data`/`08_Reference` feststellen, Provenienz je Zahl notieren.
3. Layout: KPI-Zeile oben, darunter Charts nach der Form-Heuristik aus dataviz.
4. Bauen; Light und Dark prüfen; jede Zahl gegen ihre Quelle gegenchecken.

## Pitfalls
- Zu viele Farben/Serien → den Palette-Validator aus dataviz nutzen.
- Kennzahl ohne Quelle → weglassen, nie schätzen.
- Versteckte externe Referenz (Font, Icon-Set) → vor Abgabe nach `http(s)://` greppen.
