---
name: automation
description: Eine Automatisierung oder ein Skript bauen — wiederkehrende Aufgabe, Datenpipeline, Batch-Job, geplanter Lauf. Nutzen bei "automatisieren", "Skript", "Pipeline", "Batch", "cron", "wiederkehrende Aufgabe", "Workflow bauen", "Job einrichten".
---

# automation

Baut Automatisierung, die lokal bleibt, idempotent ist und nicht still scheitert.

## Hard rules
- **Lokal-first.** Bevorzugt Python (über `uv run`) oder Shell. Nichts verlässt den Rechner ohne ausdrückliche Bestätigung — der Vault-Egress-Schutz (`ask` auf `curl`/`wget`/`git push`/`WebFetch`) gilt; das Skript darf ihn nicht umgehen.
- **Idempotent und trocken lauffähig.** Erst `--dry-run`/Vorschau, dann Ausführung. Destruktives (löschen, überschreiben) nie ohne Bestätigung und nie ohne vorher das Ziel anzusehen.
- **Secrets nie ins Skript.** Aus Umgebung oder Keychain lesen; `.env` und `.ssh` sind per `settings.json` auf `deny`.
- Code nach `<projekt>/07_Build/`; erzeugte Artefakte nach `04_Output/` oder `05_Data/`.

## Procedure
1. Auslöser, Eingang, Ausgang und Fehlerfall benennen — vor dem ersten Code.
2. Kleinste lauffähige Version, dann härten: Logging, Wiederholung, Idempotenz.
3. Wiederkehrend? Den Aufrufweg in der Area-`CLAUDE.md` dokumentieren, nicht im Kopf behalten.

## Pitfalls
- Stiller Teilerfolg → Exit-Code und Log prüfen, nicht „lief durch" annehmen.
- Pfad-Annahmen → absolute Pfade oder ein explizit gesetztes Arbeitsverzeichnis, nie auf das cwd hoffen.
- Ein Cron/Watcher, der doppelt feuert → Lauf serialisieren (Lockfile) oder Idempotenz sicherstellen.
