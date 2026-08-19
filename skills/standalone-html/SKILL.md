---
name: standalone-html
description: Eine HTML-Seite oder kleine Website bauen — standalone, offline-fähig, ohne CDN. Nutzen bei "HTML", "Webseite", "Website erstellen", "Landing Page", "Standalone-Seite", "eine Seite bauen", "Micro-Site".
---

# standalone-html

Baut eine einzelne, in sich geschlossene HTML-Seite (oder wenige verlinkte Seiten), die ohne Netz aufgeht.

## Hard rules
- **Kein CDN, keine externe Bibliothek, kein Remote-Font, kein Analytics.** Alles inline oder lokal daneben. Grund: soll in Jahren ohne Netz und ohne installierte Abhängigkeiten aufgehen — dieselbe Doktrin wie der Graph-Betrachter des Vaults.
- **Bei Charts erst `dataviz` lesen**, dann die `dashboard`-Regeln anwenden.
- **Inline-JS von Anfang an so strukturieren, dass es in eine `.js`-Datei ziehbar ist**, falls die Seite gegraphed werden soll — Graphify parst kein HTML. Die `.js` ist dann ein abgeleitetes Artefakt; Änderungen gehören ins HTML zurück, nie nur in die `.js`.
- Output nach `<projekt>/04_Output/`; wiederverwendbarer Code/Skripte nach `07_Build/`.

## Procedure
1. Semantisches HTML-Gerüst → CSS (Custom Properties für Farben/Typo) → JS.
2. Offline testen: vor Abgabe nach `http(s)://`-Ladeverweisen greppen, es dürfen keine übrig sein.
3. Light/Dark und schmale (mobile) Breite prüfen.

## Pitfalls
- Versteckte externe Referenz (Google Font, Icon-Set, Tracking-Pixel) → greppen, nicht darauf verlassen, „nichts eingebaut" zu haben.
- Große Inline-Daten blähen die Datei → in eine separate `.json`/`.js` daneben auslagern.
