# vault-kit

Ein **installierbares, versioniertes Setup für einen datei-basierten Wissens-Vault mit Claude Code**:
lokaler Zwei-Ebenen-Wissensgraph, ein an Format **und Vertraulichkeit** gebundener Memory-Layer,
Auto-Hygiene, Egress-Schutz und eine **selbstheilende** Graphify-Integration. Ein Befehl auf jedem
Rechner — alle Pfade werden abgeleitet, nichts ist fest verdrahtet.

> Es ist bewusst **local-first**: keine Cloud, keine Vektor-DB, kein Hosted-Index. Alles liegt als
> lesbare Datei neben dem Vault und funktioniert offline.

## Inhalt
- [Idee](#idee) · [Voraussetzungen](#voraussetzungen) · [Installation](#installation)
- [Architektur](#architektur) · [Wissensgraph](#wissensgraph--zwei-ebenen) · [Memory-Layer](#memory-layer)
- [Automatik & Selbstheilung](#automatik--selbstheilung) · [Updaten](#updaten) · [Tägliche Nutzung](#tägliche-nutzung)
- [Sicherheit](#sicherheit--vertraulichkeit) · [Nicht enthalten](#nicht-enthalten) · [Teams & Roadmap](#teams--roadmap)

## Idee
Claude Code lädt seinen Kontext datei-basiert: eine `CLAUDE.md`-Kette plus ein Memory-Verzeichnis,
beide **aus dem Arbeitsverzeichnis abgeleitet**. vault-kit gibt dieser Ablage Struktur, Regeln und
Werkzeuge, damit Wissen **akkumuliert statt im Chat zu versickern** — und ein Wissensgraph macht
Struktur und Code navigierbar. Kein Plugin-Server, kein Retrieval-Dienst: nur Dateien + kleine Skripte.

## Voraussetzungen
| | |
|---|---|
| **Python 3** | Pflicht — Index-Graph, Hygiene, Viewer |
| **uv** | optional, für Graphify (`uv tool install graphifyy`); ohne uv wird Graphify übersprungen |
| **zsh** | für den `claude`/`graphify`-Launcher (sonst manuell in den Vault wechseln) |
| **git** | zum Klonen/Aktualisieren |
| OS | macOS / Linux |

## Installation
```bash
git clone https://github.com/<owner>/vault-kit && cd vault-kit
./install.sh                 # Vault-Default: ~/Claude
#   ./install.sh ~/MeinVault      # anderer Ort
#   ./install.sh --no-graphify    # ohne Graphify
```
`install.sh` ist idempotent und macht deterministisch:
1. leitet **Vault-Pfad** und (wie Claude Code) das **Memory-Verzeichnis** ab (jedes Nicht-alnum → `-`);
2. legt Ordner an, kopiert Tools nach `~/.claude/tools/`, Skills/Agents/Commands nach `<vault>/.claude/`;
3. rendert `CLAUDE.md` + `settings.json` und ersetzt die Platzhalter `__VAULT__`/`__MEMDIR__` (per Python, nicht `sed`);
4. ergänzt den Zwei-Zeilen-Zeiger in `~/.claude/CLAUDE.md` und die `claude()`/`graphify()`-Funktionen in `~/.zshrc`;
5. installiert Graphify (falls `uv` da) und setzt die Vault-Hausregeln;
6. baut den Index-Graph.

Danach: **neues Terminal → `claude`** (öffnet im Vault) und für den Feinschliff den Prompt aus
[`SETUP.md`](SETUP.md) in die Vault-Session einfügen (Domain-Skills an deine Deliverables anpassen + Abnahme).

## Architektur
**CLAUDE.md-Kette** — Kontext nach Nähe, jede Ebene lädt nur, wenn relevant:

| Ebene | Datei | geladen |
|---|---|---|
| Global | `~/.claude/CLAUDE.md` | immer, jedes Projekt (nur ein Zeiger auf den Vault) |
| Vault | `<vault>/CLAUDE.md` | immer in dieser Session (Regeln, Routing, Memory, Graphify) |
| Projekt | `<vault>/<projekt>/CLAUDE.md` | nur bei Arbeit daran |
| Area | `<vault>/<projekt>/07_Build/CLAUDE.md` | nur bei Arbeit darin |

**Speicherorte:** Tools zentral in `~/.claude/tools/`; Memory in `~/.claude/projects/<slug>/memory/`
(aus dem Vault-Pfad abgeleitet); Vault-Konfiguration in `<vault>/.claude/` (skills/agents/commands/settings).
**Regel:** immer den **Vault-Wurzelordner** öffnen, nie einen Unterordner — sonst entsteht eine leere, unsichtbare Memory-Insel.

## Wissensgraph — zwei Ebenen
- **Ebene 1 · Index-Graph** (`~/.claude/tools/vault-index.py`): einmal über den ganzen Vault → `<vault>/_Index/graph.html`
  (standalone, offline). Zeigt die *Verbindungsschicht*: Memory ↔ Skills ↔ Projekte ↔ CLAUDE.md-Kette. Beantwortet „was weiß ich, wo liegt es, was hängt zusammen".
- **Ebene 2 · Code-Graph** (`graphify update <code-ordner>`): je Ordner mit Code, rein lokal (tree-sitter-AST, keine API).
  Eigener, hübscher Betrachter: `python3 ~/.claude/tools/graph-viewer.py <ordner>` → `graph.viewer.html`
  (Cluster nach Community, Kanten nach Beziehungstyp; überlebt `graphify update`).
- **Regeln:** nie an der Vault-Wurzel oder über ein ganzes Projekt laufen; wo ein `graphify-out/graph.json`
  existiert, ist er die erste Quelle **vor `grep`**; bei Kundenmaterial nur lokal (kein Doc-Pass an externe Anbieter).

## Memory-Layer
- **Native Auto-Memory** ist an — Claude schreibt selbst Memory-Dateien; der `memory-write`-Skill ist die **Format-Autorität**, an die sich beide Wege halten.
- `MEMORY.md` ist der **Index** (nur die ersten ~200 Zeilen/25 KB werden je Session geladen ⇒ ≤ ~40 Zeilen halten).
- **Format:** Frontmatter `name`/`description`/`metadata.type`; **ein Fakt = eine Datei**; Verwandtes mit `[[wikilinks]]`.
- **Vertraulichkeit (hart):** nie Kunden-/`06_Restricted`-Inhalte oder Mandantenzahlen in Memory — auch nicht durch Auto-Memory.
- **Hygiene:** `/memory-review` (der `librarian`-Agent räumt auf: Dubletten, Waisen, tote Index-Zeilen, veraltet),
  `/memory-benchmark` (misst, ob die richtige Memory zu Fragen geladen wird). `memory-hygiene.py` läuft am SessionEnd und **erinnert**, wenn Aufräumen fällig ist.

## Automatik & Selbstheilung
Das System hält sich weitgehend selbst aktuell:
- **SessionEnd-Hooks** (`<vault>/.claude/settings.json`): bauen den **Index-Graph** neu und prüfen die **Memory-Hygiene** — bei jedem Sitzungsende, ohne Zutun.
- **Graphify-Selbstheilung** (`graphify()` in `~/.zshrc`): Ein Graphify-Update überschreibt die `SKILL.md` und würde unsere **Vault-Hausregeln** (Zwei-Ebenen-/Lokal-only-Regeln) entfernen. Der Wrapper erkennt das **nach jedem `graphify`-Aufruf** (fehlender Marker) und **setzt die Hausregeln automatisch neu** — egal ob durch `graphify install`, ein Upgrade oder eine Neuinstallation. Nach `graphify update` baut er zusätzlich den eigenen Betrachter neu. Kanonische Quelle der Regeln: `~/.claude/tools/graphify-vault-houserules.md`.
- **`install.sh` bei erneutem Lauf**: aktualisiert Tools/Skills und ersetzt den zsh-Launcher-Block zwischen seinen Markern (Updates greifen wirklich), lässt aber eine **bereits vorhandene** `CLAUDE.md`/`settings.json` unangetastet — dein Projekt-Routing und lokale Einstellungen bleiben erhalten.

## Updaten
```bash
cd vault-kit && git pull && ./install.sh      # zieht Tool-/Wrapper-/Template-Updates durch (idempotent)
```
Graphify selbst: `uv tool upgrade graphifyy` — die Vault-Hausregeln stellt der `graphify`-Wrapper beim nächsten Aufruf automatisch wieder her.

## Tägliche Nutzung
- **Immer den Vault öffnen:** neues Terminal → `claude` (der Launcher wechselt in den Vault). `claude --here` für den aktuellen Ordner.
- `/clear` bei jedem Themenwechsel — was bleiben soll, steht in einer Datei.
- **Skills:** `dashboard`, `analysis`, `standalone-html`, `automation` (Deliverables); `vault-init` (neues Projekt), `memory-write`, `context-audit`.
- **Commands:** `/method`, `/sources`, `/memory-review`, `/memory-benchmark`.

## Sicherheit & Vertraulichkeit
- **Egress-Schutz** in `settings.json`: `ask` bei `curl`/`wget`/`git push`/`WebFetch`/`rm`; `deny` auf `.env`/`~/.ssh`.
- **`06_Restricted/`** kennzeichnet *Herkunft* („vertraulich erhalten"), nie wörtlich zitieren/senden.
- **Memory-Vertraulichkeitsregel** gilt auch für native Auto-Memory.
- Bei Kundenmaterial kein semantischer Doc-Pass an externe Anbieter (`GEMINI_API_KEY` in Vault-Arbeit ungesetzt lassen).

## Nicht enthalten
Keine Mandanten-/Projektdaten, keine Memory-Inhalte des Ursprungsrechners. vault-kit ist die
**leere, geregelte Struktur** — Inhalt entsteht beim Arbeiten.

## Teams & Roadmap
- Repo privat halten und Teammitglieder als Collaborator hinzufügen (oder in eine Organisation legen).
- **Roadmap — Team-Memory:** ein geteilter/synchronisierter Memory-Layer über mehrere Nutzer (noch nicht enthalten).

## Dateiübersicht
```
install.sh              Bootstrap (leitet Pfade ab, ersetzt Platzhalter, idempotent + updatend)
SETUP.md                Claude-Prompt für den Feinschliff (Domain-Skills + Abnahme)
tools/                  vault-index.py, graph.template.html, graph-viewer.py (+template),
                        memory-hygiene.py, graphify-reapply-houserules.py, graphify-vault-houserules.md
templates/              vault-CLAUDE.md, settings.json, zshrc-functions.sh, global-CLAUDE-pointer.md
skills/                 vault-init, memory-write, context-audit, dashboard, analysis, standalone-html, automation
agents/                 scout, verifier, librarian
commands/               method, sources, memory-review, memory-benchmark
```
