#!/usr/bin/env python3
"""Baut den Index-Graphen eines Claude-Code-Vaults.

Aufruf im Vault-Wurzelordner:      python3 vault-index.py
Oder mit ausdrücklichem Pfad:     python3 vault-index.py ~/Vault

Erzeugt <vault>/_Index/graphify-out/graph.json und, falls graph.template.html
daneben liegt, gleich den fertigen Betrachter <vault>/_Index/graph.html.

Portabel: Der Vault-Pfad kommt aus dem Argument oder dem Arbeitsverzeichnis,
das Memory-Verzeichnis wird daraus abgeleitet. Nichts ist fest verdrahtet.
"""
import json, pathlib, re, collections, sys

H = pathlib.Path.home()

# --- Pfade bestimmen ---------------------------------------------------------
VAULT = pathlib.Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 \
        else pathlib.Path.cwd().resolve()

# Claude Code leitet das Memory-Verzeichnis aus dem Pfad ab: jedes Zeichen
# außer Buchstaben und Ziffern wird zu '-'. /Users/x/Vault  ->  -Users-x-Vault
SLUG = re.sub(r'[^A-Za-z0-9]', '-', str(VAULT))
MEM  = H/'.claude/projects'/SLUG/'memory'
OUT  = VAULT/'_Index/graphify-out'
TMPL = pathlib.Path(__file__).resolve().parent/'graph.template.html'
HTML = VAULT/'_Index/graph.html'

if not VAULT.is_dir():
    sys.exit(f"Vault-Ordner nicht gefunden: {VAULT}")
if not MEM.is_dir():
    print(f"Hinweis: kein Memory-Verzeichnis unter {MEM}")
    print("         Der Graph entsteht dann ohne die Abteilung Memory.")

nodes, edges = {}, []
def node(nid, label, dept, kind, **kw):
    nodes[nid] = dict(id=nid, label=label, dept=dept, kind=kind, **kw); return nid
def edge(s, t, rel, origin):
    if s in nodes and t in nodes and s != t:
        edges.append(dict(source=s, target=t, relation=rel, origin=origin))

# --- Skills ------------------------------------------------------------------
skill_ids = {}
for root, scope in [(H/'.claude/skills','global'), (VAULT/'.claude/skills','vault')]:
    if not root.exists(): continue
    for sk in sorted(root.iterdir()):
        f = sk/'SKILL.md'
        if not f.is_file(): continue
        t = f.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'^---\n(.*?)\n---', t, re.S); fm = m.group(1) if m else ''
        nm = re.search(r'^name:\s*(.+)$', fm, re.M)
        name = nm.group(1).strip() if nm else sk.name
        dm = re.search(r'^description:\s*(.+(?:\n\s+.+)*)$', fm, re.M)
        desc = re.sub(r'\s+', ' ', dm.group(1)).strip().strip('"') if dm else ''
        nid = 'skill:'+name
        node(nid, name, 'Skills', 'skill', scope=scope, lines=len(t.splitlines()),
             desc=desc, path=str(sk))
        skill_ids[name] = nid; skill_ids[sk.name] = nid

# --- Projekte ----------------------------------------------------------------
proj_ids = {}
EXT = {'.md','.txt','.html','.js','.json','.csv','.xlsx','.pptx','.pdf'}
for p in sorted(VAULT.iterdir()):
    if not p.is_dir() or p.name.startswith('.') or p.name == '_Index': continue
    files = [f for f in p.rglob('*') if f.is_file() and f.suffix.lower() in EXT]
    words = sum(len(f.read_text(encoding='utf-8',errors='ignore').split())
                for f in files if f.suffix.lower() in {'.md','.txt'})
    nid = 'projekt:'+p.name
    node(nid, p.name.replace('_',' ').strip(), 'Projekte', 'projekt',
         files=len(files), words=words, path=str(p),
         desc=f"{len(files)} Dateien, {words:,} Wörter".replace(',','.'))
    proj_ids[p.name] = nid

# --- Anweisungen (CLAUDE.md-Kette) -------------------------------------------
chain = []
if (H/'.claude/CLAUDE.md').is_file():
    chain.append((H/'.claude/CLAUDE.md','Global','anw:global'))
for cand in (VAULT/'.claude/CLAUDE.md', VAULT/'CLAUDE.md'):
    if cand.is_file():
        chain.append((cand,'Vault','anw:vault')); break
for f in sorted(VAULT.glob('*/CLAUDE.md')):
    chain.append((f, f.parent.name.replace('_',' '), 'anw:'+f.parent.name))
for f, label, nid in chain:
    t = f.read_text(encoding='utf-8', errors='ignore')
    node(nid, label, 'Anweisungen', 'anweisung', lines=len(t.splitlines()),
         path=str(f), desc=re.sub(r'\s+',' ',t.strip().splitlines()[0] if t.strip() else '')[:150])
for a, b in zip(chain, chain[1:2]):
    edge(a[2], b[2], 'gilt weiter in', 'STRUKTUR')
for f, label, nid in chain[2:]:
    edge('anw:vault', nid, 'gilt weiter in', 'STRUKTUR')
    if f.parent.name in proj_ids: edge(nid, proj_ids[f.parent.name], 'steuert', 'STRUKTUR')

# --- Memory ------------------------------------------------------------------
mem_ids = {}
mem_files = sorted(MEM.rglob('*.md')) if MEM.is_dir() else []
for f in mem_files:
    if f.name == 'MEMORY.md': continue
    t = f.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'^---\n(.*?)\n---', t, re.S); fm = m.group(1) if m else ''
    nm = re.search(r'^name:\s*(.+)$', fm, re.M)
    name = nm.group(1).strip() if nm else f.stem
    dm = re.search(r'^description:\s*(.+)$', fm, re.M)
    tm = re.search(r'^\s*type:\s*(\w+)\s*$', fm, re.M)
    archived = '_archiv' in f.parts
    nid = 'mem:'+f.stem
    node(nid, name, 'Memory', 'memory', archived=archived,
         mtype=(tm.group(1) if tm else 'unbekannt'),
         desc=re.sub(r'\s+',' ',dm.group(1)).strip() if dm else '',
         path=str(f), lines=len(t.splitlines()))
    mem_ids[f.stem] = nid; mem_ids[name] = nid

# --- Kanten aus Text ---------------------------------------------------------
def mentioned(key, text, low):
    """Eindeutige Nennung: in Backticks, als /kommando, oder mehrteiliger Name."""
    k = re.escape(key)
    ambig = re.match(r'^[a-zäöü]+$', key) and len(key) < 12
    if ambig:
        # `animate` ist auch ein gewöhnliches Wort. Backticks reichen hier nicht,
        # nur der Slash-Aufruf oder der Pfad belegen eine Nennung des Skills.
        return (re.search(r'(?<![\w-])/'+k+r'(?![\w-])', text, re.I) is not None
                or re.search(r'skills/'+k+r'(?![\w-])', text, re.I) is not None)
    if re.search(r'`/?'+k+r'`', text, re.I): return True
    if re.search(r'(?<![\w-])/'+k+r'(?![\w-])', text, re.I): return True
    return re.search(r'(?<![\w-])'+k.lower()+r'(?![\w-])', low) is not None

def scan(text, src, exclude=()):
    low = text.lower()
    for key, nid in list(skill_ids.items()):
        if nid == src or nid in exclude: continue
        if mentioned(key, text, low):
            edge(src, nid, 'nennt', 'EXTRAHIERT')
    for key, nid in list(proj_ids.items()):
        if nid == src: continue
        plain = key.lower().replace('_',' ').strip()
        if len(plain) < 5: continue
        if re.search(r'(?<![\w-])'+re.escape(plain)+r'(?![\w-])', low) or key.lower() in low:
            edge(src, nid, 'gehört zu', 'EXTRAHIERT')

for f in mem_files:
    if f.name == 'MEMORY.md': continue
    src = 'mem:'+f.stem
    t = f.read_text(encoding='utf-8', errors='ignore')
    for wl in sorted(set(re.findall(r'\[\[([^\]]+)\]\]', t))):
        tgt = mem_ids.get(wl) or mem_ids.get(wl.strip())
        if tgt: edge(src, tgt, 'verweist auf', 'WIKILINK')
    scan(t, src)

for f, label, nid in chain:
    scan(f.read_text(encoding='utf-8', errors='ignore'), nid)

for name, nid in list(skill_ids.items()):
    p = pathlib.Path(nodes[nid]['path'])/'SKILL.md'
    if p.is_file(): scan(p.read_text(encoding='utf-8', errors='ignore'), nid, exclude={nid})

# --- Dubletten, Grad ---------------------------------------------------------
seen, uniq = set(), []
for e in edges:
    k = (e['source'], e['target'], e['relation'])
    if k in seen: continue
    seen.add(k); uniq.append(e)
edges = sorted(uniq, key=lambda e: (e['source'], e['target'], e['relation']))

deg = collections.Counter()
for e in edges: deg[e['source']] += 1; deg[e['target']] += 1
for n in nodes.values(): n['degree'] = deg.get(n['id'], 0)

# --- Schreiben ---------------------------------------------------------------
payload = {'nodes': list(nodes.values()), 'links': edges,
           'departments': ['Memory','Skills','Projekte','Anweisungen']}
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'graph.json').write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                              encoding='utf-8')

# Betrachter gleich mitrendern, damit kein Handschritt dazwischenliegt
if TMPL.is_file():
    t = TMPL.read_text(encoding='utf-8')
    if '__GRAPH_DATA__' not in t:
        print("Warnung: Platzhalter __GRAPH_DATA__ fehlt im Template, HTML nicht erzeugt.")
    else:
        compact = json.dumps(payload, ensure_ascii=False, separators=(',',':'))
        HTML.write_text(t.replace('__GRAPH_DATA__', compact), encoding='utf-8')
        print(f"Betrachter: {HTML}")
else:
    print(f"Kein Template unter {TMPL}, nur graph.json geschrieben.")

# --- Kontrollzahlen ----------------------------------------------------------
print(f"Vault:  {VAULT}")
print(f"Memory: {MEM}{'' if MEM.is_dir() else '  (nicht vorhanden)'}")
print(f"Knoten: {len(nodes)}  Kanten: {len(edges)}")
print("Je Abteilung:", dict(collections.Counter(n['dept'] for n in nodes.values())))
print("Je Herkunft:", dict(collections.Counter(e['origin'] for e in edges)))
iso = [f"{n['label']} ({n['dept']})" for n in nodes.values() if n['degree']==0]
print(f"Isoliert ({len(iso)}):", iso[:12], "..." if len(iso) > 12 else "")
# Abteilung mitausgeben: Projekt und zugehörige CLAUDE.md tragen dasselbe Label
print("Naben:", [(f"{nodes[k]['label']} ({nodes[k]['dept']})", v) for k,v in deg.most_common(8)])
