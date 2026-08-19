# Vault

**Zweck:** Datei-basierter Speicher- und Kontext-Layer für Claude Code. Alles mit Bestand lebt hier in Dateien, nicht im Chat.

## Arbeitsregeln
- Ergebnisse werden in Dateien geschrieben, nicht im Chat gelassen.
- Zahlen nie aus dem Gedächtnis nennen: eine Datei in `08_Reference` zitieren.
- Nichts verlässt diesen Rechner ohne ausdrückliche Bestätigung.
- `/clear` bei jedem Themenwechsel. Was bleiben soll, steht in einer Datei.
- Diesen Vault immer als Arbeitsverzeichnis öffnen (`__VAULT__`), nie einen Unterordner — sonst entsteht eine leere, unsichtbare Memory-Insel.

## Projekte (Routing, keine Doku — eine Zeile je Eintrag)
| Ordner | Was | Status |
|---|---|---|
| 00_Method | Standards, Vorlagen, Formate | living |
| 00_Sources | wiederverwendbare Inputs + Register | living |

## Operating protocol
**Route before writing.** Jede Datei gehört zu einem Projekt und einem nummerierten Ordner. Beides vor dem Anlegen bestimmen. Nie in die Vault-Wurzel schreiben. Ist der Zielordner echt unklar, eine Frage stellen — keine Diskussion.

**Propose structure for new work.** Wenn eine Anfrage ein Deliverable erzeugt, diese Session überdauert oder aufhebenswerte Dateien produziert und kein Projekt passt: `vault-init` anbieten, den Projektnamen nennen, dann so oder so weiterarbeiten. Einmal fragen; bei Ablehnung für diese Session fallenlassen. Nicht bei Einmalfragen, Lookups oder Arbeit in einem bestehenden Projekt.

**Capture at the end.** Wenn Arbeit abschließt, in einer Zeile anbieten, Dauerhaftes festzuhalten: eine Memory-Datei für einen nicht-offensichtlichen Fakt, einen Area-`CLAUDE.md`-Eintrag für eine gelernte Konvention oder Falle, eine `00_Sources`-Registerzeile für einen wiederverwendbaren Input. Nichts sagen, wenn nichts qualifiziert.

Nie auf einem dieser Punkte blockieren. Vorschlagen, Default nennen, weiterarbeiten.

## Skills
- **Deliverables:** `dashboard` (KPI/Charts — liest zuerst dataviz), `analysis` (belegte Auswertung — nutzt scout/verifier), `standalone-html` (offline-Seiten ohne CDN), `automation` (lokale, idempotente Skripte).
- **System:** `vault-init` (neues Projekt), `memory-write` (ein Fakt → eine Datei), `context-audit` (persistenten Kontext messen).

## Memory
Speicher: `__MEMDIR__`; `MEMORY.md` ist der Index (nur die ersten ~200 Zeilen/25 KB werden je Session geladen — **≤ ~40 Zeilen halten**). Native Auto-Memory ist an: Claude schreibt selbst Memory-Dateien — es gelten dieselben Regeln wie für den `memory-write`-Skill (die Format-Autorität).
- **Format:** Frontmatter `name`/`description`/`metadata.type` ∈ `user|feedback|project|reference`; **ein Fakt = eine Datei**; bei feedback/project `**Warum:**`/`**Wie anwenden:**`; Verwandtes mit `[[wikilinks]]`.
- **Index-Disziplin:** jede Memory-Datei bekommt genau eine `MEMORY.md`-Zeile (Routing-Haken, keine Zusammenfassung).
- **Vertraulichkeit (hart):** Nie Kunden-/`06_Restricted`-Inhalte oder Mandantenzahlen in Memory — auch nicht durch Auto-Memory. Memory ist für nicht-sensible, wiederverwendbare Fakten (Toolchain, Konventionen, Rechner-Setup, Projekt-Zeiger); Mandantenfakten verweisen auf Projekt/Datei, kopieren nie Restricted-Zahlen.
- **Hygiene:** `/memory-review` (librarian räumt auf), `/memory-benchmark` (Recall prüfen). Der SessionEnd-Hook erinnert, wenn Hygiene fällig ist.

## Wissensgraph (Graphify) — zwei Ebenen
- **Ebene 1, Index-Graph:** einmal für den ganzen Vault unter `_Index/`. Neubau: `python3 ~/.claude/tools/vault-index.py __VAULT__`. Bildet die Verbindungsschicht ab (Memory, CLAUDE.md-Kette, Projekte, Skills), nicht den Inhalt. Betrachter: `_Index/graph.html` (standalone, offline).
- **Ebene 2, Container-Graph:** je Ordner mit Code — nie über ein ganzes Projekt, nie an der Wurzel: `graphify update <ordner>` (rein lokal, tree-sitter-AST, keine API-Kosten). Eigener, hübscher Betrachter: `python3 ~/.claude/tools/graph-viewer.py <ordner>` → `graph.viewer.html` (überlebt `graphify update`).
- **Erste Quelle vor `grep`:** Wo ein `graphify-out/graph.json` existiert, ist er die erste Quelle für Fragen nach Struktur und Zusammenhängen.
- **Abfragen:** `graphify query "<Frage>" --budget N` · `graphify path "A" "B"` · `graphify explain "X"` · `graphify god-nodes`
- **Grenzen (gemessen):** HTML wird nicht geparst — Inline-JS vorher in eine `.js`-Datei ziehen. Konstanten nur flach erfasst — dafür weiter greppen; Funktionen und Aufrufketten sind zuverlässig. Semantischer Doc-Pass über Kundenmaterial nur lokal/über den Host-Agenten, nie Gemini (`GEMINI_API_KEY` in Vault-Arbeit ungesetzt lassen). `graphify update` (Code-AST, lokal) bleibt der Default.
