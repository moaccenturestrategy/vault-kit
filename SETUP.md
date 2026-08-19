# Vault-Kit — Feinschliff-Prompt

`install.sh` hat den deterministischen Teil erledigt (Ordner, Tools, Skills/Agents/Commands,
CLAUDE.md, Settings/Hooks, zsh-Launcher, Index-Graph). Dieses Dokument ist der Rest, der
**Urteil** braucht. Alles unterhalb der Linie in eine Claude-Code-Session einfügen, die im
Vault (`claude` im Vault-Ordner) geöffnet ist.

---

Du richtest das per `install.sh` gelegte Vault-System fertig ein. Arbeite die Phasen der Reihe nach ab, behaupte nichts als fertig, was du nicht geprüft hast.

## Phase 1 — Audit (nur lesen)
1. Bestätige die Wurzel: In welchem Ordner ist diese Session gewurzelt? Steht dort eine `CLAUDE.md`? Wie viele Zeilen (Ziel < 100)?
2. Memory-Verzeichnis: aus dem Pfad abgeleitet (`~/.claude/projects/<slug>/memory/`). Wie viele Dateien, wie viele `MEMORY.md`-Zeilen (Ziel ≤ ~40)?
3. Skills/Agents/Commands: liste, was unter `<vault>/.claude/` liegt.
4. Graphify installiert? (`graphify --version`) Python 3 vorhanden?
Berichte in unter 10 Zeilen. Frage nur, was du nicht selbst ermitteln kannst.

## Phase 2 — Domain-Skills an DEINE Deliverables anpassen
Das Kit liefert generische Skills (`dashboard`, `analysis`, `standalone-html`, `automation`). Frag den Nutzer nach seinen **drei häufigsten Deliverables** und passe die vorhandenen Skills an bzw. lege je Deliverable einen zu (Format-Standard, harte Regeln mit Grund, bekannte Fallen). Erfinde keinen generischen Satz — leite ihn aus den Antworten ab.

## Phase 3 — Verankern & Abnahme
1. **Index-Graph:** `python3 ~/.claude/tools/vault-index.py <vault>` — nenne die Kontrollzahlen (Knoten, Kanten, je Abteilung, je Herkunft, isolierte Knoten). Öffne `<vault>/_Index/graph.html` und bestätige, dass er **ohne Netz** lädt.
2. **Memory-Governance:** zitiere die Vertraulichkeitsregel aus der Vault-`CLAUDE.md` zurück. Native Auto-Memory ist an — bestätige, dass sie an die Regeln gebunden ist.
3. **Hooks:** bestätige die beiden SessionEnd-Hooks (Index-Neubau + Hygiene) in `<vault>/.claude/settings.json` (valides JSON).
4. **Hygiene:** `/memory-review` (librarian) einmal trocken laufen lassen; `/memory-benchmark` für den Recall.
5. **Graphify:** falls Code vorhanden, `graphify update <code-ordner>` (rein lokal) und eine echte `graphify query` zeigen. Erinnerung: kein semantischer Doc-Pass über Kundenmaterial; für Vault-Arbeit `GEMINI_API_KEY` ungesetzt lassen.

## Phase 4 — Betrieb erklären (unter 12 Zeilen)
Welchen Ordner öffnen (immer den Vault, nie einen Unterordner), wann `/clear`, wohin neue Fakten (Memory-Regeln), die Zwei-Ebenen-Graph-Regel, und dass `/memory-review` bei Bedarf aufräumt.

**Nicht enthalten (bewusst):** Mandanten-/Projektdaten und Memory-Inhalte des Ursprungsrechners. Dieses Kit ist die leere, geregelte Struktur — Inhalt entsteht beim Arbeiten.
