# vault-kit

**A file-based knowledge vault for Claude Code — installable on any machine with one command.**

Turns the folder Claude Code opens into a structured, rule-governed knowledge base: a local
two-level knowledge graph, a memory layer bound to both a format *and* a confidentiality rule,
automatic hygiene, egress guards, and a **self-healing** Graphify integration.

> **Local-first by design.** No cloud, no vector database, no hosted index. Everything is a
> readable file next to your vault, and it works offline.

[Why](#why-it-exists) · [Requirements](#requirements) · [Install](#install) · [Architecture](#architecture) ·
[Knowledge graph](#knowledge-graph--two-levels) · [Memory](#memory-layer) · [Automation](#automation--self-healing) ·
[Updating](#updating) · [Daily use](#daily-use) · [Security](#security--confidentiality) · [Troubleshooting](#troubleshooting)

## Why it exists

Claude Code loads its context from files: a `CLAUDE.md` chain plus a memory directory, **both derived
from the working directory**. That is powerful and easy to get wrong — open a subfolder once and you
create an invisible, empty memory island; let the root `CLAUDE.md` grow and every turn gets more
expensive.

vault-kit turns that mechanism into a system:

- **Knowledge accumulates instead of evaporating in chat.** Results go to files, facts go to memory, and both have rules.
- **Structure and code stay navigable** through a knowledge graph that is the first source for "how does this connect?" — before `grep`.
- **Client material stays put.** Confidentiality is a written rule that governs automatic memory too, backed by egress guards.
- **It survives updates.** Tool upgrades that would overwrite local customizations are detected and repaired automatically.

No plugin server, no retrieval service — just files and small scripts.

## Requirements

| | |
|---|---|
| **Python 3** | required — index graph, hygiene, viewer |
| **uv** | optional, for Graphify (`uv tool install graphifyy`); skipped if absent |
| **zsh** | for the `claude` / `graphify` launchers (otherwise `cd` into the vault yourself) |
| **git** | to clone and update |
| **OS** | macOS / Linux |

## Install

```bash
git clone https://github.com/<owner>/vault-kit && cd vault-kit
./install.sh                    # default vault: ~/Claude
#   ./install.sh ~/MyVault      # custom location
#   ./install.sh --no-graphify  # skip Graphify
```

`install.sh` is idempotent and does the deterministic work:

1. derives the **vault path** and — exactly as Claude Code does — the **memory directory** (every non-alphanumeric char → `-`);
2. creates folders, copies tools to `~/.claude/tools/`, skills/agents/commands to `<vault>/.claude/`;
3. renders `CLAUDE.md` and `settings.json`, substituting `__VAULT__` / `__MEMDIR__` (via Python, not `sed`, so BSD/GNU differences can't bite);
4. appends the two-line pointer to `~/.claude/CLAUDE.md` and the `claude()` / `graphify()` functions to `~/.zshrc`;
5. installs Graphify (if `uv` is present) and applies the vault house rules;
6. builds the index graph.

Then open a **new terminal → `claude`** (starts inside the vault) and paste the prompt from
[`SETUP.md`](SETUP.md) into that session for the judgement-dependent part: tailoring the deliverable
skills to *your* work and running acceptance checks.

## Architecture

**The `CLAUDE.md` chain** — context by proximity; each level loads only when it is relevant:

| Level | File | Loaded |
|---|---|---|
| Global | `~/.claude/CLAUDE.md` | always, every project (just a pointer to the vault) |
| Vault | `<vault>/CLAUDE.md` | always in this session (work rules, routing, memory, graph) |
| Project | `<vault>/<project>/CLAUDE.md` | only while working on it |
| Area | `<vault>/<project>/07_Build/CLAUDE.md` | only while working inside it |

**Where things live:** tools centrally in `~/.claude/tools/`; memory in `~/.claude/projects/<slug>/memory/`
(derived from the vault path); vault configuration in `<vault>/.claude/` (skills, agents, commands, settings).

> **The one habit everything depends on:** always open the **vault root**, never a subfolder — otherwise
> you create an empty, invisible memory island.

Numbered project folders keep routing decidable: `01_Architecture`, `02_DataModel`, `03_Subject`,
`04_Output`, `05_Data`, `06_Restricted`, `07_Build`, `08_Reference`, `09_Rules` — create only the ones a
project actually needs (`vault-init` does this for you).

## Knowledge graph — two levels

Two levels, because one graph over everything produces noise: a run across mixed folders drowns code
in markdown nodes (measured: 1,585 markdown vs. 350 code nodes — useless for code questions).

- **Level 1 · index graph** — `python3 ~/.claude/tools/vault-index.py <vault>` → `<vault>/_Index/graph.html`
  (standalone, offline). Maps the *connective layer* of the vault: memory ↔ skills ↔ projects ↔ the `CLAUDE.md`
  chain. Answers "what do I know, where is it, what is connected?"
- **Level 2 · code graph** — `graphify update <code-folder>`, per folder that holds code. Purely local
  (tree-sitter AST, no API, nothing leaves the machine). Prettier viewer:
  `python3 ~/.claude/tools/graph-viewer.py <folder>` → `graph.viewer.html` (clusters by community, edges by
  relation type; survives `graphify update`).
- **Rules:** never run at the vault root or across a whole project; where a `graphify-out/graph.json` exists it is
  the **first source before `grep`**; for client material stay local (no semantic document pass to external providers).

Queries: `graphify query "<question>" --budget N` · `graphify path "A" "B"` · `graphify explain "X"` · `graphify god-nodes`

## Memory layer

- **Native auto-memory is on** — Claude writes memory files on its own judgement. The `memory-write` skill is the
  **format authority** both paths follow.
- `MEMORY.md` is the **index** (only the first ~200 lines / 25 KB load per session ⇒ keep it ≤ ~40 lines).
- **Format:** front matter `name` / `description` / `metadata.type`; **one fact = one file**; relate with `[[wikilinks]]`.
- **Confidentiality (hard rule):** never put client / `06_Restricted` content or client figures into memory — this
  governs auto-memory too. Memory is for reusable, non-sensitive facts (toolchain, conventions, machine setup, pointers).
- **Hygiene:** `/memory-review` runs the `librarian` agent (duplicates, orphans, dead index lines, stale entries);
  `/memory-benchmark` measures whether the right memory is retrieved. `memory-hygiene.py` runs at session end and
  **reminds** you when cleanup is due.

## Automation & self-healing

The system keeps itself current:

- **SessionEnd hooks** (`<vault>/.claude/settings.json`) rebuild the **index graph** and check **memory hygiene** at the end of every session — no action required.
- **Graphify self-healing** (`graphify()` in `~/.zshrc`): a Graphify update overwrites its `SKILL.md` and would strip our **vault house rules** (two-level and local-only rules). The wrapper notices the missing marker after *any* `graphify` call and **re-applies the rules automatically** — whether the overwrite came from `graphify install`, an upgrade, or a reinstall. After `graphify update` it also rebuilds the custom viewer. Canonical source: `~/.claude/tools/graphify-vault-houserules.md`.
- **Re-running `install.sh`** updates tools, skills and the zsh launcher block (between its markers) but **leaves an existing `CLAUDE.md` / `settings.json` untouched** — your project routing and local settings survive.

## Updating

```bash
cd vault-kit && git pull && ./install.sh     # idempotent; pulls tool, wrapper and template updates
uv tool upgrade graphifyy                   # Graphify itself; house rules are restored automatically
```

## Daily use

- **Always open the vault:** new terminal → `claude`. Use `claude --here` for the current folder instead.
- `/clear` on every topic change — whatever should persist is already in a file.
- **Skills:** `dashboard`, `analysis`, `standalone-html`, `automation` (deliverables); `vault-init` (new project), `memory-write`, `context-audit`.
- **Commands:** `/method`, `/sources`, `/memory-review`, `/memory-benchmark`.
- **Agents:** `scout` (broad read-only search), `verifier` (adversarially check one claim), `librarian` (memory & source hygiene).

## Security & confidentiality

- **Egress guards** in `settings.json`: `ask` on `curl`, `wget`, `git push`, `WebFetch`, `rm`; `deny` on `.env` and `~/.ssh`.
- **`06_Restricted/` denotes provenance** ("received in confidence") — never quote verbatim, never send externally.
- The **memory confidentiality rule** applies to native auto-memory as well.
- For client material, no semantic document pass to external providers (keep `GEMINI_API_KEY` unset for vault work).

## Troubleshooting

| Symptom | Fix |
|---|---|
| `claude` doesn't start in the vault | open a new terminal or `source ~/.zshrc`; check the trust prompt shows the vault path |
| Memory seems empty / not loading | you opened a subfolder — always open the vault root |
| Graphify house rules gone after an upgrade | run any `graphify` command (the wrapper repairs it), or `python3 ~/.claude/tools/graphify-reapply-houserules.py` |
| `graphify: command not found` | `uv tool install graphifyy && graphify install`, then re-apply house rules |
| Index graph looks stale | `python3 ~/.claude/tools/vault-index.py <vault>` (the SessionEnd hook normally does this) |
| Sessions feel slow / expensive | run the `context-audit` skill; keep root `CLAUDE.md` < 100 lines and `MEMORY.md` ≤ ~40 lines |

## What's not included

No client or project data, and none of the originating machine's memory content. vault-kit is the
**empty, rule-governed structure** — content appears as you work.

## Layout

```
install.sh          bootstrap (derives paths, substitutes placeholders, idempotent)
SETUP.md            prompt for the judgement-dependent finishing steps
tools/              vault-index.py, graph.template.html, graph-viewer.py (+template),
                    memory-hygiene.py, graphify-reapply-houserules.py, graphify-vault-houserules.md
templates/          vault-CLAUDE.md, settings.json, zshrc-functions.sh, global-CLAUDE-pointer.md
skills/             vault-init, memory-write, context-audit, dashboard, analysis, standalone-html, automation
agents/             scout, verifier, librarian
commands/           method, sources, memory-review, memory-benchmark
```

## Teams & roadmap

Keep the repository private and add teammates as collaborators (or move it into an organisation).
**Roadmap — team memory:** a shared, synchronised memory layer across several users (not included yet).

## Credits

Built around [Claude Code](https://claude.com/claude-code) and [Graphify](https://github.com/safishamsi/graphify)
(`graphifyy` on PyPI). The vault structure, memory governance, hygiene tooling and viewers are this kit's own.
