---
name: memory-write
description: Einen Fakt als eine Memory-Datei plus eine Indexzeile schreiben. Nutzen, wenn etwas Nicht-Offensichtliches festgehalten werden soll, das über diese Session hinaus gilt und nirgends sonst steht. Trigger: "merk dir", "remember", "als Memory speichern", "festhalten", "note to self".
---

# memory-write

Schreibt genau einen Fakt in genau eine Datei im Memory-Verzeichnis des Vaults und ergänzt eine Indexzeile in `MEMORY.md`.

Memory-Verzeichnis (aus dem Vault-Pfad abgeleitet): `__MEMDIR__/`.

**Diese Datei ist die Format-Autorität** — sie gilt für manuell geschriebene Memory UND für Claude Codes **native Auto-Memory** (standardmäßig an; Claude schreibt selbst Dateien nach eigenem Ermessen). Vor dem Anlegen prüfen, ob — auch nativ — schon eine Datei den Fakt abdeckt (Dubletten vermeiden).

## Hard rules
1. **Ein Fakt, eine Datei.** Keine Sammeldateien. Was in zwei Kontexten gebraucht wird, wird zwei Dateien mit Querverweis `[[name]]`.
2. **Die Indexzeile ist Routing, keine Zusammenfassung.** Sie entscheidet allein, ob die Datei geladen wird — ein Haken, der die Abfrage entscheidbar macht, keine Nacherzählung.
3. **Grund mitschreiben, nicht nur die Regel.** Eine Regel ohne Grund wird an der ersten Ausnahme gebrochen.
4. **Nur absolute Daten.** "Nächste Woche" ist in einem Monat falsch.
5. **Nichts speichern, was ableitbar ist** aus den Vault-Dateien. Memory ist für das, was nirgends geschrieben steht.
6. **Memory altert.** Nennt ein Eintrag Datei/Tool/Preis/Pfad, vor Gebrauch prüfen, ob es noch existiert.
7. **Falsches löschen.** Zwei widersprechende Einträge sind schlimmer als keiner.
8. **Vertraulichkeit (hart).** Nie Kunden-/`06_Restricted`-Inhalte oder Mandantenzahlen in Memory — auch nicht durch native Auto-Memory. Nur nicht-sensible, wiederverwendbare Fakten (Toolchain, Konventionen, Rechner-Setup, Projekt-Zeiger); Mandantenfakten auf Projekt/Datei verweisen, nie Restricted-Zahlen kopieren.

## Dateiformat
```markdown
---
name: <kurzer-kebab-slug>
description: <eine Zeile, entscheidet über Relevanz beim Abruf>
metadata:
  type: user | feedback | project | reference
---

<der Fakt. Bei feedback/project danach **Warum:** und **Wie anwenden:**. Verwandtes mit [[name]] verlinken.>
```

## Procedure
1. Prüfen, ob eine Datei den Fakt schon abdeckt — dann die aktualisieren statt duplizieren.
2. Datei schreiben, `[[verweise]]` auf Verwandtes setzen (auch auf noch nicht existierende Slugs — markiert Nachholenswertes).
3. Eine Zeile in `MEMORY.md` ergänzen: `- [Titel](datei.md) — Haken`. Index unter ~40 Zeilen halten.
4. Nach neuen Memory-Dateien den Index-Graph auffrischen: `python3 ~/.claude/tools/vault-index.py __VAULT__`.

## Pitfalls
- Der Index veraltet mit jeder neuen Datei — daher Schritt 4 nicht vergessen.
- Eine isolierte Memory-Datei (kein `[[verweis]]` von/zu ihr) taucht im Graph gestrichelt auf: entweder überflüssig oder falsch benannt.
