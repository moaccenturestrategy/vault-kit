# Changelog

## 1.0.0 — 2026-08-20

First release. Installable, portable setup for a file-based knowledge vault with Claude Code.

**Vault**
- `CLAUDE.md` chain with work rules, project routing table and operating protocol
- numbered project folders via the `vault-init` skill
- deliverable skills: `dashboard`, `analysis`, `standalone-html`, `automation`
- system skills: `vault-init`, `memory-write`, `context-audit`
- agents: `scout`, `verifier`, `librarian`
- commands: `/method`, `/sources`, `/memory-review`, `/memory-benchmark`
- egress guards in `settings.json` (`ask` on curl/wget/git push/WebFetch/rm; `deny` on `.env`/`~/.ssh`)

**Knowledge graph (two levels)**
- level 1: `vault-index.py` builds the vault index graph with a standalone, offline viewer
- level 2: Graphify code graphs per code folder, plus `graph-viewer.py` for a themed viewer that survives `graphify update`
- vault house rules for Graphify (two-level rule, local-only for client material)

**Memory layer**
- native auto-memory bound to the `memory-write` format authority
- hard confidentiality rule (no client / `06_Restricted` content in memory, auto-memory included)
- `memory-hygiene.py` + SessionEnd reminder; `/memory-review` (librarian) and `/memory-benchmark` (recall)

**Automation & portability**
- SessionEnd hooks rebuild the index graph and check memory hygiene
- self-healing `graphify()` wrapper re-applies the vault house rules after any Graphify update
- `install.sh` derives all paths, substitutes `__VAULT__`/`__MEMDIR__`, is idempotent, and never overwrites an existing `CLAUDE.md` / `settings.json`
