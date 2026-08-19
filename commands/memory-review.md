---
description: Memory-Hygiene — der librarian-Agent räumt das Memory-Verzeichnis auf
argument-hint: [fokus]
---

Beauftrage den `librarian`-Agent (Read/Write/Grep/Glob) mit einer Hygiene-Runde über das Vault-Memory.

Memory-Verzeichnis: `__MEMDIR__/` (+ `MEMORY.md`).
Als Orientierung zuerst `python3 ~/.claude/tools/memory-hygiene.py` laufen lassen und die Befunde übergeben.

Auftrag an den librarian:
- **Dubletten** zusammenführen (ein Fakt = eine Datei), Querverweis `[[..]]` setzen.
- **Veraltetes/Widersprüche** melden (Datei/Tool/Preis/Pfad prüfen, ob noch gültig).
- **Verwaiste Dateien** (keine `MEMORY.md`-Zeile / kein `[[wikilink]]`) anbinden.
- **Tote Index-Zeilen** (Datei fehlt) entfernen.
- `MEMORY.md` unter ~40 Zeilen halten; Format gegen den `memory-write`-Skill prüfen.
- **Vertraulichkeit:** keine `06_Restricted`-/Mandantenzahlen in Memory — falls entdeckt, melden statt behalten.

Regeln: nichts löschen ohne Bestätigung; Vorschläge klar von durchgeführten Korrekturen trennen.
Danach den Index-Graph neu bauen: `python3 ~/.claude/tools/vault-index.py __VAULT__`.

Fokus (optional): $ARGUMENTS
