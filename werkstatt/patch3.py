# -*- coding: utf-8 -*-
"""Neue Szene `enthuellen` und die Regel zum Warum (Rueckmeldung 07.10.2026)."""
import io

R = r'C:\Users\habib\Documents\Habibi-Repo\vorlagen\reel'
p = R + r'\szenen.py'
s = io.open(p, encoding='utf-8').read()

NEU = '''

# Gegenstaende als reine CSS-Form. Keine Fotos, keine KI-Bilder.
_DINGE = {
    'schalter': '<div class="d-rahmen"><div class="d-wippe"></div></div>',
    'klinke': '<div class="d-rosette"></div><div class="d-griff"></div>',
    'schale': '<div class="d-schale"><i></i><i></i><i></i><i></i><i></i><i></i></div>',
    'tastatur': '<div class="d-tast"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>'
                '<i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>'
                '<b></b></div>',
    'tuch': '<div class="d-tuch"><s></s><s></s><s></s></div>',
}

_DINGE_CSS = """
.ding {{ position:absolute; left:50%; top:50%; width:460px; height:460px; margin:-230px 0 0 -230px; }}
.ding .d-rahmen {{ position:absolute; inset:60px 110px; background:#f2f6f9; border-radius:26px; box-shadow:0 16px 40px rgba(0,0,0,.35); }}
.ding .d-wippe {{ position:absolute; left:18%; right:18%; top:16%; bottom:16%; background:#dbe6ee; border-radius:16px; border-bottom:10px solid #b9cbd9; }}
.ding .d-rosette {{ position:absolute; left:70px; top:170px; width:120px; height:120px; border-radius:50%; background:#cfdbe6; box-shadow:0 14px 34px rgba(0,0,0,.35); }}
.ding .d-griff {{ position:absolute; left:120px; top:198px; width:290px; height:64px; border-radius:32px; background:linear-gradient(180deg,#f2f6f9,#c3d3e0); }}
.ding .d-schale {{ position:absolute; inset:120px 40px; background:#dbe6ee; border-radius:22px; display:grid; grid-template-columns:repeat(3,1fr); gap:16px; padding:22px; }}
.ding .d-schale i {{ display:block; background:#9fb6c7; border-radius:8px; }}
.ding .d-tast {{ position:absolute; inset:110px 20px; background:#e7eef4; border-radius:20px; display:grid; grid-template-columns:repeat(6,1fr); gap:12px; padding:20px; align-content:start; }}
.ding .d-tast i {{ display:block; height:54px; background:#c3d3e0; border-radius:8px; }}
.ding .d-tast b {{ grid-column:2/6; height:46px; background:#c3d3e0; border-radius:8px; display:block; }}
.ding .d-tuch {{ position:absolute; inset:90px 50px; background:#bcd9ec; border-radius:18px; padding:30px; }}
.ding .d-tuch s {{ display:block; height:26px; background:rgba(255,255,255,.55); border-radius:13px; margin-bottom:26px; text-decoration:none; }}
"""


def enthuellen(reel, sid, start, ende, punkte, titel_html=None, t_titel=None, bg='var(--navy-deep)'):
    """Ein Gegenstand liegt unscharf da, beim gesprochenen Wort wird er scharf.

    punkte: Liste dict(ding, name, warum, t)   ding aus _DINGE.
    Das Bild zeigt WAS gemeint ist, der Untertitel sagt WARUM es geputzt gehoert.
    """
    css = _DINGE_CSS.replace('.ding', f'#{sid} .ding') + f\'\'\'
#{sid}-t {{ position:absolute; left:70px; right:70px; top:250px; text-align:center; color:#fff; font-size:84px; line-height:1.12; }}
#{sid}-t .serif {{ color:var(--blue); }}
#{sid}-buehne {{ position:absolute; left:120px; right:120px; top:520px; height:620px; border-radius:34px;
  background:rgba(159,211,238,.10); border:6px solid rgba(159,211,238,.28); overflow:hidden; }}
#{sid}-name {{ position:absolute; left:60px; right:60px; top:1200px; text-align:center; font-weight:900;
  font-size:118px; color:#fff; line-height:1.05; }}
#{sid}-warum {{ position:absolute; left:80px; right:80px; top:1350px; text-align:center;
  font-size:68px; color:var(--blue); line-height:1.15; }}\'\'\'

    dinge = ''.join(f'<div class="ding" id="{sid}-d{i}" style="opacity:0">{_DINGE[p["ding"]]}</div>'
                    for i, p in enumerate(punkte))
    inhalt = (f'<div id="{sid}-t" data-layout-allow-overflow>{titel_html}</div>' if titel_html else '') + f\'\'\'
<div id="{sid}-buehne" data-layout-allow-overflow>{dinge}</div>
<div id="{sid}-name" data-layout-allow-overflow></div>
<div id="{sid}-warum" class="serif" data-layout-allow-overflow></div>\'\'\'

    js, sfx = [], []
    if titel_html:
        tt = r(t_titel if t_titel is not None else start + .05)
        js.append(f'tl.fromTo("#{sid}-t", {{ y: 48, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(1.7)" }}, {tt});')
    for i, pk in enumerate(punkte):
        t = r(pk['t'])
        # Erst unscharf und klein, auf dem Wort wird es scharf
        js.append(f'tl.fromTo("#{sid}-d{i}", {{ opacity: 0, scale: .82, filter: "blur(34px)" }}, '
                  f'{{ opacity: 1, scale: 1, filter: "blur(22px)", duration: .22, ease: "power2.out", immediateRender: {"true" if i == 0 else "false"} }}, {r(t - .3)});')
        js.append(f'tl.to("#{sid}-d{i}", {{ filter: "blur(0px)", scale: 1.04, duration: .34, ease: "back.out(2)" }}, {t});')
        js.append(f'tl.to("#{sid}-d{i}", {{ scale: 1, duration: .25, ease: "power2.out" }}, {r(t + .34)});')
        if i + 1 < len(punkte):
            js.append(f'tl.to("#{sid}-d{i}", {{ opacity: 0, filter: "blur(28px)", duration: .18 }}, {r(punkte[i + 1]["t"] - .34)});')
        js.append(f'tl.set("#{sid}-name", {{ innerText: "{pk["name"]}" }}, {t});')
        js.append(f'tl.fromTo("#{sid}-name", {{ y: 44, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .24, ease: "power3.out", immediateRender: false }}, {t});')
        js.append(f'tl.set("#{sid}-warum", {{ innerText: "{pk["warum"]}" }}, {r(t + .35)});')
        js.append(f'tl.fromTo("#{sid}-warum", {{ y: 34, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .26, ease: "power3.out", immediateRender: false }}, {r(t + .35)});')
        sfx += [('whoosh_hoch', pk['t'] - .3, .2, .3), ('pop', pk['t'], .22, .6), ('tick', pk['t'] + .35, .1, .3)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\\n'.join(js), sfx=sfx)
'''
anker = "\n\ndef abschluss(reel, sid, start, ende, t_marke, t_zeile, t_knopf, bg='var(--navy-deep)'):"
assert s.count(anker) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(anker, NEU + anker))

REGEL = """

---

## 17. Das Warum (Rückmeldung 07.10.2026, dritte Runde)

Mortaza hat die Reels vom 14., 16. und 18.10. zurückgewiesen: «Ich wüsste nicht, was ich daraus lernen sollte.» Der Mangel war in allen drei derselbe. Sie sagten **was** zu tun ist, aber nicht **warum**.

### 17.1 Jedes Reel braucht einen Grund, nicht nur eine Anweisung

«Diese Stelle geht oft vergessen» ist kein Grund. «Auf dem Schreibtisch sitzen rund 400-mal mehr Bakterien als auf einer Toilettenbrille, weil die Toilette täglich geputzt wird und der Schreibtisch nie» ist einer.

Aufbau, der funktioniert:

1. **Überraschender Fakt** mit Quelle. Er ist der Hook.
2. **Warum das so ist.** Ein Satz Erklärung, der den Fakt plausibel macht.
3. **Was man dagegen tut**, mit Zahl (Abschnitt 15.1).

Findet sich kein Fakt, der einen Zuschauer überrascht, taugt das Thema nicht. Dann ein anderes nehmen.

### 17.2 Das Bild zeigt den Gegenstand, nicht nur das Wort

Wird eine Türklinke genannt, erscheint eine Türklinke. Neue Szene `enthuellen`: der Gegenstand liegt zuerst unscharf da und wird genau auf dem gesprochenen Wort scharf, darunter steht in einer Zeile, warum er geputzt gehört. Gegenstände sind reine CSS-Formen in den Markenfarben, keine Fotos und keine KI-Bilder.

### 17.3 Transparenz-Themen brauchen einen Konflikt

Ein Reel, das nur Konditionen aufzählt (Zonen, Zuschläge), ist Werbung ohne Inhalt. Ein Transparenz-Reel braucht eine Aussage, die man nicht erwartet: warum wir höchstens vier neue Objekte im Monat annehmen, warum der Preis offen auf der Website steht, wer den Schlüssel zu euren Räumen hat. Die Konditionen sind dann der Beleg, nicht das Thema.

### 17.4 Immer dieselbe Stimme, immer dasselbe Tag-Muster

Im Zonen-Reel klang die Stimme anders als in den übrigen. Ursache war der Tag `[sarcastic]`, den nur dieses Reel benutzte: ElevenLabs v3 ändert damit hörbar die Klangfarbe. **`[sarcastic]` wird nicht mehr verwendet.** Erlaubt bleiben `[curious]`, `[intense]`, `[excited]`, `[warmly]`, und zwar in jedem Reel in derselben Reihenfolge, damit alle Videos gleich klingen.
"""
for pfad in [R + r'\VIDEO-REGELN.md', r'C:\Users\habib\Documents\Habibi-Marketing\claude\VIDEO-REGELN.md']:
    t = io.open(pfad, encoding='utf-8').read()
    t = t.replace('**Version 1.3, 07.10.2026.**', '**Version 1.4, 07.10.2026.**')
    t = t.replace('| 1.3 | 07.10.2026 |',
                  '| 1.4 | 07.10.2026 | Abschnitt 17: jedes Reel braucht das Warum mit Fakt, Gegenstaende werden gezeigt (Szene enthuellen), Transparenz braucht Konflikt, [sarcastic] verboten. |\n| 1.3 | 07.10.2026 |')
    t = t.replace('| `hotspots` | Grundriss von oben',
                  '| `enthuellen` | Gegenstand liegt unscharf, wird auf dem gesprochenen Wort scharf, darunter das Warum. |\n| `hotspots` | Grundriss von oben')
    t = t.replace('| `sarcastic` | Wenn die Branchenüblichkeit vorgeführt wird («Preis auf Anfrage») |', '')
    io.open(pfad, 'w', encoding='utf-8', newline='').write(t.rstrip() + REGEL)

print('Szene enthuellen ergaenzt, VIDEO-REGELN 1.4.')
