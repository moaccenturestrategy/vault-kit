# vault-kit

Portables, versioniertes Setup für einen **datei-basierten Wissens-Vault mit Claude Code** —
inklusive Zwei-Ebenen-Wissensgraph (Graphify + eigener Index-Graph), geregeltem Memory-Layer
(native Auto-Memory an Standards + Vertraulichkeit gebunden), Auto-Hygiene, Egress-Schutz und
zsh-Launcher. Auf jedem Rechner mit einem Befehl aufsetzbar; Pfade werden abgeleitet.

## Voraussetzungen
- **Python 3** (Pflicht — Index-Graph, Hygiene, Viewer).
- **uv** (optional, für Graphify: `uv tool install graphifyy`). Ohne uv wird Graphify übersprungen.
- **zsh** (für den `claude`-Launcher; sonst manuell in den Vault wechseln).
- macOS/Linux.

## Schnellstart
```bash
git clone <repo-url> vault-kit && cd vault-kit
./install.sh                 # Vault-Default: ~/Claude
#   oder:  ./install.sh ~/MeinVault
#   ohne Graphify:  ./install.sh --no-graphify
```
Danach: **neues Terminal → `claude`** (öffnet im Vault). Für den Feinschliff (Domain-Skills an
deine Deliverables anpassen + Abnahme) den Prompt aus [`SETUP.md`](SETUP.md) in die Vault-Session einfügen.

## Was installiert wird
| Ziel | Inhalt |
|---|---|
| `~/.claude/tools/` | `vault-index.py` (Index-Graph L1), `graph.template.html`, `graph-viewer.py` (+Template, eigener L2-Viewer), `memory-hygiene.py`, `graphify-reapply-houserules.py`, `graphify-vault-houserules.md` |
| `<vault>/CLAUDE.md` | Arbeitsregeln, Operating-Protocol, **Memory-Governance** (inkl. Vertraulichkeitsregel), Graphify-Zwei-Ebenen |
| `<vault>/.claude/skills` | `vault-init`, `memory-write`, `context-audit`, `dashboard`, `analysis`, `standalone-html`, `automation` |
| `<vault>/.claude/agents` | `scout`, `verifier`, `librarian` |
| `<vault>/.claude/commands` | `method`, `sources`, `memory-review`, `memory-benchmark` |
| `<vault>/.claude/settings.json` | Egress-Schutz + zwei `SessionEnd`-Hooks (Index-Neubau + Memory-Hygiene) |
| `~/.claude/CLAUDE.md` | Zwei-Zeilen-Zeiger auf den Vault |
| `~/.zshrc` | `claude()`/`graphify()`-Launcher (idempotent, per Marker) |

## Zwei-Ebenen-Wissensgraph
- **Ebene 1 (Index):** `python3 ~/.claude/tools/vault-index.py <vault>` → `<vault>/_Index/graph.html`. Verbindungsschicht des Vaults (Memory, CLAUDE.md-Kette, Projekte, Skills).
- **Ebene 2 (Code):** `graphify update <code-ordner>` (lokal, tree-sitter-AST). Eigener Betrachter: `python3 ~/.claude/tools/graph-viewer.py <ordner>` → `graph.viewer.html` (überlebt `graphify update`).

## Memory-Layer
Native Auto-Memory (an) + `memory-write`-Skill als Format-Autorität; `MEMORY.md` als Index.
`/memory-review` (librarian räumt auf), `/memory-benchmark` (Recall), SessionEnd-Hook erinnert.
**Vertraulichkeit:** nie Kunden-/`06_Restricted`-Inhalte in Memory (gilt auch für Auto-Memory).

## Aktualisieren
`git pull`, dann `./install.sh` erneut (idempotent). Graphify nach Upgrade: der `graphify install`-Aufruf über den zsh-Wrapper setzt die Vault-Hausregeln automatisch neu.

## Nicht enthalten
Keine Mandanten-/Projektdaten, keine Memory-Inhalte des Ursprungsrechners — das Kit ist die
**leere, geregelte Struktur**. Inhalt entsteht beim Arbeiten.

## Roadmap
- **Team-Memory:** geteilter/synchronisierter Memory-Layer über mehrere Nutzer (noch nicht enthalten).
