---
description: Recall-Benchmark des Memory-Index (read-only, ändert nichts)
argument-hint: [anzahl fragen]
---

Read-only Eval des Memory-Retrievals. **Nichts ändern.**

1. Lies `MEMORY.md` und alle Memory-Dateien in `__MEMDIR__/`.
2. Formuliere je Memory-Datei **eine** realistische Frage (wie ein Nutzer sie stellen würde) plus 2–3 **Cross-Fragen**, die mehrere Dateien berühren oder bewusst mehrdeutig sind.
3. Für jede Frage: entscheide **nur anhand der `MEMORY.md`-Indexzeilen** (nicht der Dateiinhalte!), welche Datei geladen würde. Vergleiche mit der tatsächlich richtigen Datei.
4. Report:
   - **Recall-Score** (richtige Treffer / Fragen).
   - Fehltreffer mit Grund (welche Indexzeile war zu schwach/mehrdeutig).
   - Liste **schwacher/mehrdeutiger Indexzeilen** mit konkretem Umschreib-Vorschlag (bessere Routing-Haken).
5. Fazit: Ist der Recall hoch, ist semantisches Retrieval **nicht** nötig — das explizit feststellen. Nur bei niedrigem Recall einen **lokalen** (egress-freien) Embedding-Index erwägen.

Anzahl zusätzlicher Cross-Fragen (optional): $ARGUMENTS
