#!/usr/bin/env bash
# vault-kit installer — richtet Vault + Graphify + Memory-Layer auf diesem Rechner ein.
# Portabel: Pfade werden abgeleitet, Platzhalter (__VAULT__/__MEMDIR__) per Python ersetzt
# (kein sed — vermeidet BSD/GNU-Unterschiede). Idempotent, wo möglich.
#
#   ./install.sh [vault-pfad]        # Default: ~/Claude
#   ./install.sh ~/MeinVault --no-graphify
set -euo pipefail

KIT="$(cd "$(dirname "$0")" && pwd)"
VAULT_IN="${1:-$HOME/Claude}"
case "${1:-}" in --*) VAULT_IN="$HOME/Claude";; esac
VAULT="${VAULT_IN/#\~/$HOME}"
NO_GRAPHIFY=0; for a in "$@"; do [ "$a" = "--no-graphify" ] && NO_GRAPHIFY=1; done

# Memory-Verzeichnis wie Claude Code es ableitet: jedes Nicht-alnum -> '-'
MEMSLUG="$(python3 -c "import re,sys;print(re.sub(r'[^A-Za-z0-9]','-',sys.argv[1]))" "$VAULT")"
MEMDIR="$HOME/.claude/projects/$MEMSLUG/memory"

echo "▶ Vault:   $VAULT"
echo "▶ Memory:  $MEMDIR"
echo "▶ Tools:   $HOME/.claude/tools"
echo

subst() { # Platzhalter in einer bereits abgelegten Datei ersetzen
  VAULT="$VAULT" MEMDIR="$MEMDIR" python3 - "$1" <<'PY'
import os,sys,pathlib
p=pathlib.Path(sys.argv[1]); t=p.read_text(encoding="utf-8")
t=t.replace("__VAULT__",os.environ["VAULT"]).replace("__MEMDIR__",os.environ["MEMDIR"])
p.write_text(t,encoding="utf-8")
PY
}

# 1) Verzeichnisse
mkdir -p "$VAULT/00_Method" "$VAULT/00_Sources" \
         "$VAULT/.claude/skills" "$VAULT/.claude/agents" "$VAULT/.claude/commands" \
         "$HOME/.claude/tools" "$MEMDIR"

# 2) Tools (portabel, leiten Pfade selbst ab)
cp "$KIT/tools/"* "$HOME/.claude/tools/"
chmod +x "$HOME/.claude/tools/"*.py 2>/dev/null || true

# 3) Skills / Agents / Commands
cp -R "$KIT/skills/"* "$VAULT/.claude/skills/"
cp "$KIT/agents/"*.md "$VAULT/.claude/agents/"
cp "$KIT/commands/"*.md "$VAULT/.claude/commands/"

# 4) Templates rendern — bestehende NIE überschreiben (gefüllter Vault bleibt unangetastet)
if [ -f "$VAULT/CLAUDE.md" ]; then
  echo "• $VAULT/CLAUDE.md existiert — unverändert gelassen (deine Projekt-Routing-Tabelle bleibt)"
else
  cp "$KIT/templates/vault-CLAUDE.md" "$VAULT/CLAUDE.md"; subst "$VAULT/CLAUDE.md"; echo "✓ CLAUDE.md angelegt"
fi
if [ -f "$VAULT/.claude/settings.json" ]; then
  echo "• $VAULT/.claude/settings.json existiert — unverändert gelassen"
else
  cp "$KIT/templates/settings.json" "$VAULT/.claude/settings.json"; subst "$VAULT/.claude/settings.json"; echo "✓ settings.json angelegt"
fi

# 5) Platzhalter in kopierten Assets ersetzen
while IFS= read -r f; do subst "$f"; done < <(find "$VAULT/.claude/skills" "$VAULT/.claude/commands" "$VAULT/.claude/agents" -name '*.md'; echo "$HOME/.claude/tools/graphify-vault-houserules.md")

# 6) Globaler Zeiger in ~/.claude/CLAUDE.md (idempotent)
GLOBAL="$HOME/.claude/CLAUDE.md"; touch "$GLOBAL"
if ! grep -q "aufhebenswerte Artefakte" "$GLOBAL" 2>/dev/null; then
  { echo; cat "$KIT/templates/global-CLAUDE-pointer.md"; } >> "$GLOBAL"; subst "$GLOBAL"
  echo "✓ Vault-Zeiger in $GLOBAL ergänzt"
else echo "• Vault-Zeiger schon vorhanden — übersprungen"; fi

# 7) zsh-Launcher — Block zwischen Markern EINFÜGEN oder bei Re-Lauf ERSETZEN
#    (so zieht `git pull && ./install.sh` auch Wrapper-Updates durch)
ZRC="$HOME/.zshrc"; touch "$ZRC"
TMP_LAUNCH="$(mktemp)"; cp "$KIT/templates/zshrc-functions.sh" "$TMP_LAUNCH"; subst "$TMP_LAUNCH"
ZRC="$ZRC" BLOCK="$TMP_LAUNCH" python3 - <<'PY'
import os, pathlib
zrc = pathlib.Path(os.environ["ZRC"])
block = pathlib.Path(os.environ["BLOCK"]).read_text(encoding="utf-8").strip("\n")
t = zrc.read_text(encoding="utf-8") if zrc.exists() else ""
start = "# === vault-kit: Claude-Code-Launcher"
end = "# === /vault-kit ==="
if start in t and end in t:
    pre = t[:t.index(start)]
    post = t[t.index(end) + len(end):]
    t = pre.rstrip("\n") + "\n" + block + "\n" + post.lstrip("\n")
    action = "aktualisiert"
else:
    t = (t.rstrip("\n") + "\n\n" if t.strip() else "") + block + "\n"
    action = "ergänzt"
zrc.write_text(t, encoding="utf-8")
print(f"✓ zsh-Launcher {action} in {zrc} (neues Terminal oder: source ~/.zshrc)")
PY
rm -f "$TMP_LAUNCH"

# 8) Graphify (optional)
if [ "$NO_GRAPHIFY" -eq 0 ]; then
  if command -v uv >/dev/null 2>&1; then
    echo "▶ Graphify installieren…"
    uv tool install graphifyy >/dev/null 2>&1 || echo "  (uv tool install graphifyy fehlgeschlagen — später manuell)"
    command -v graphify >/dev/null 2>&1 && graphify install --platform claude >/dev/null 2>&1 || true
    python3 "$HOME/.claude/tools/graphify-reapply-houserules.py" 2>/dev/null || true
    echo "✓ Graphify + Vault-Hausregeln"
  else
    echo "• uv nicht gefunden — Graphify übersprungen. Später: 'uv tool install graphifyy && graphify install', dann 'python3 ~/.claude/tools/graphify-reapply-houserules.py'"
  fi
fi

# 9) Index-Graph bauen
python3 "$HOME/.claude/tools/vault-index.py" "$VAULT" > "$HOME/.claude/tools/last-index.log" 2>&1 || true
echo "✓ Index-Graph gebaut ($VAULT/_Index/graph.html)"

echo
echo "FERTIG. Nächste Schritte:"
echo "  1) Neues Terminal öffnen (oder: source ~/.zshrc), dann:  claude"
echo "     → öffnet im Vault $VAULT; im Trust-Check muss $VAULT stehen."
echo "  2) Für den nicht-deterministischen Feinschliff (Domain-Skills an DEINE Deliverables"
echo "     anpassen, Abnahme): in der Vault-Session den Prompt aus SETUP.md einfügen."
