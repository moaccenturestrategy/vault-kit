---
name: context-audit
description: Messen, was gerade im persistenten Kontext liegt, und konkrete Verschiebungen in Skills oder Ordner-CLAUDE.md vorschlagen. Nutzen, wenn Sessions träge/teuer werden oder die Root-CLAUDE.md wächst. Trigger: "context audit", "was ist im Kontext", "CLAUDE.md zu groß", "Kontext aufräumen", "persistent context".
---

# context-audit

Misst den persistenten Kontext und schlägt Verschiebungen vor. Nichts wird ohne Bestätigung verschoben.

## Was persistenten Kontext kostet (jede Runde, jede Session)
- `~/.claude/CLAUDE.md` (global, alle Projekte)
- `__VAULT__/CLAUDE.md` (Vault-Wurzel, diese Session)
- `MEMORY.md` (der Index, nicht die einzelnen Dateien)
- die `description`-Zeile **jedes** verfügbaren Skills

## Procedure
1. Zeilen zählen: globale CLAUDE.md, Vault-CLAUDE.md, MEMORY.md.
2. Skills auflisten (`~/.claude/skills/` und `__VAULT__/.claude/skills/`), je Skill nur `name` + `description`.
3. Kandidaten benennen: Was steht im persistenten Kontext, gehört aber nicht dorthin?
   - Root-CLAUDE.md über ~100 Zeilen → Detail in Ordner-CLAUDE.md oder Skill verschieben.
   - MEMORY.md über ~40 Zeilen → geschlossene Projekte archivieren, Indexzeile entfernen.
   - Skills, die nie feuern → in einen Inaktiv-Ordner verschieben (nie löschen), jede Description kostet eine Zeile je Runde.
4. Als Vorschlag ausgeben, gruppiert nach "risikofrei" / "braucht Bestätigung", mit erwarteter Zeilenersparnis.

## Leitfrage
"Würde ich das geladen haben wollen, während ich an etwas völlig anderem arbeite?" Wenn nein → on-demand (Ordner-CLAUDE.md oder Skill), nicht persistent.

## Pitfalls
- Ein Skill mit schwacher `description` ("Skill für Reports") feuert nie — er kostet nur. Die Wörter schreiben, die man tatsächlich tippt.
- Nie löschen, um Kontext zu sparen — verschieben und berichten.
