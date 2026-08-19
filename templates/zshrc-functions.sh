# === vault-kit: Claude-Code-Launcher (eingefügt von install.sh) ===
# claude          -> öffnet im Vault __VAULT__
# claude --here   -> öffnet im aktuellen Ordner
# (Optional: ein Modell erzwingen — hier bewusst NICHT gesetzt; per --model oder /model.)
claude() {
  local dir="__VAULT__"
  if [[ "$1" == "--here" ]]; then
    shift
    command claude "$@"
    return
  fi
  if [[ -d "$dir" ]]; then
    ( cd "$dir" && command claude "$@" )
  else
    echo "⚠️  $dir nicht gefunden — starte im aktuellen Ordner"
    command claude "$@"
  fi
}

# graphify: nach `install` die Vault-Hausregeln wieder einsetzen; nach `update`
# den eigenen Betrachter (graph.viewer.html) mitbauen.
graphify() {
  command graphify "$@"
  local rc=$?
  if [[ "$1" == "install" ]]; then
    python3 "$HOME/.claude/tools/graphify-reapply-houserules.py" 2>/dev/null
  elif [[ "$1" == "update" ]]; then
    local tgt="${2:-.}"; [[ "$tgt" == -* ]] && tgt="."
    python3 "$HOME/.claude/tools/graph-viewer.py" "$tgt" >/dev/null 2>&1 \
      && echo "↳ eigener Betrachter aktualisiert (graph.viewer.html)"
  fi
  return $rc
}
# === /vault-kit ===
