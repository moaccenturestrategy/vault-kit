#!/usr/bin/env python3
"""Read-only Hygiene-Check des Vault-Memory-Verzeichnisses.
Gibt bei Handlungsbedarf eine kurze Erinnerung auf stderr aus (die Claude Code
am SessionEnd anzeigt), sonst nichts. Exit-Code immer 0 — blockiert nie.

Aufruf: python3 memory-hygiene.py <memory-verzeichnis>
Wird vom SessionEnd-Hook der Vault-settings.json aufgerufen (Pfad wird übergeben).
"""
import pathlib, re, sys

if len(sys.argv) < 2:
    print("usage: memory-hygiene.py <memory-verzeichnis>", file=sys.stderr)
    raise SystemExit(0)
MEM = pathlib.Path(sys.argv[1]).expanduser()
INDEX_MAX = 40

def main():
    if not MEM.is_dir():
        return
    files = sorted(p for p in MEM.glob("*.md") if p.name != "MEMORY.md")
    idx = MEM / "MEMORY.md"
    idx_text = idx.read_text(encoding="utf-8") if idx.is_file() else ""
    idx_lines = [l for l in idx_text.splitlines() if l.strip().startswith("- [")]

    # verlinkte Dateien aus den Indexzeilen: ...](name.md)
    referenced = set(re.findall(r"\]\(([^)]+\.md)\)", idx_text))
    stems = {p.name for p in files}

    orphans = sorted(p.name for p in files if p.name not in referenced)      # Datei ohne Index-Zeile
    dead = sorted(r for r in referenced if r not in stems)                    # Index-Zeile ohne Datei

    # Wikilink-Isolation: Datei ohne ausgehenden [[..]] UND von keinem [[..]] getroffen
    linked = set()
    for p in files:
        for t in re.findall(r"\[\[([^\]]+)\]\]", p.read_text(encoding="utf-8", errors="ignore")):
            linked.add(t.strip().lower())
    def isolated(p):
        body = p.read_text(encoding="utf-8", errors="ignore")
        has_out = "[[" in body
        stem = p.stem.lower()
        return not has_out and stem not in linked
    iso = sorted(p.name for p in files if isolated(p))

    issues = []
    if len(idx_lines) > INDEX_MAX:
        issues.append(f"MEMORY.md hat {len(idx_lines)} Index-Zeilen (>{INDEX_MAX}) — kürzen/archivieren")
    if orphans:
        issues.append(f"{len(orphans)} Memory-Datei(en) ohne Index-Zeile: {', '.join(orphans)}")
    if dead:
        issues.append(f"{len(dead)} tote Index-Zeile(n) (Datei fehlt): {', '.join(dead)}")
    if iso:
        issues.append(f"{len(iso)} isolierte Datei(en) (kein [[wikilink]]): {', '.join(iso)}")

    if issues:
        print("🧹 Memory-Hygiene fällig — `/memory-review` ausführen:", file=sys.stderr)
        for i in issues:
            print("   • " + i, file=sys.stderr)

main()
