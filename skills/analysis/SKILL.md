---
name: analysis
description: Eine Analyse oder Auswertung erstellen — Recherche, Vergleich, Bewertung, Empfehlung — als schriftliches Deliverable. Nutzen bei "analysiere", "Analyse erstellen", "auswerten", "vergleiche", "Bewertung", "Recherche zusammenfassen", "Empfehlung ableiten".
---

# analysis

Erstellt eine belastbare Analyse, in der Beleg und Vermutung getrennt bleiben.

## Hard rules
- **Zahlen und Behauptungen nie aus dem Gedächtnis.** Jede zitiert eine Datei in `<projekt>/08_Reference` mit Ort. Unbelegtes wird als offene Frage markiert, nicht als Fakt verkauft.
- **Beleg vor Vermutung sichtbar trennen.** Was geschätzt oder gefolgert ist, kennzeichnen — dieselbe Regel wie im Graph (Beleg ≠ Vermutung); sonst verleitet die Analyse zu falschen Schlüssen.
- **Strittige Einzelbehauptungen an den `verifier`-Agent** geben (Vorgabe „nicht belegt" bei Unsicherheit). Breite Quellensuche an den `scout`-Agent.
- **Vertraulich erhaltenes Material** gehört nach `06_Restricted`, wird nie wörtlich zitiert und verlässt den Rechner nicht.
- Output nach `<projekt>/04_Output/`; Quellen nach `08_Reference`; wiederverwendbare Inputs mit Registerzeile in `00_Sources`.

## Procedure
1. Auftrag in Teilfragen zerlegen.
2. Quellen sammeln → `08_Reference`, je Quelle Herkunft + absolutes Abrufdatum.
3. `scout` für Breite, `verifier` für die strittigen Punkte.
4. Schreiben: Kernaussage zuerst, dann Beleg, dann Grenzen/offene Fragen.

## Pitfalls
- Runde Zahl aus dem Kopf → zurück zur Quelle.
- „Sensibel" ist kein Ort — entscheidbar ist Herkunft (`06_Restricted`), nicht ein Gefühl.
