# -*- coding: utf-8 -*-
"""Lehren aus der Rueckmeldung vom 07.10.2026 (zweite Runde)."""
import io

R = r'C:\Users\habib\Documents\Habibi-Repo\vorlagen\reel'

# ---------------------------------------------------------------- szenen.py
p = R + r'\szenen.py'
s = io.open(p, encoding='utf-8').read()

# 1. Rauschen am Schluss: whoosh_lang ist gefiltertes weisses Rauschen -> kuerzer und leiser
a = "sfx = [('whoosh_lang', start - .1, .25), ('boing_kurz', t_marke + .35, .2), ('pop', t_knopf, .3), ('ding', t_knopf + .6, .2)]"
b = ("# whoosh_lang ist gefiltertes weisses Rauschen. In voller Laenge und Lautstaerke\n"
     "    # hoert man es am Schluss als Rauschen (Rueckmeldung 07.10.2026).\n"
     "    sfx = [('whoosh_lang', start - .08, .16, .30), ('boing_kurz', t_marke + .35, .2, .55), "
     "('pop', t_knopf, .3, .6), ('ding', t_knopf + .6, .2, .5)]")
assert s.count(a) == 1
s = s.replace(a, b)

# 2. Neue Szene: hotspots. Ein Raum von oben, vergessene Stellen pulsieren nacheinander auf.
NEU = '''

def hotspots(reel, sid, start, ende, titel_html, punkte, t_titel=None, bg='var(--navy-deep)'):
    """Grundriss von oben, auf dem vergessene Stellen nacheinander aufleuchten.

    punkte: Liste dict(x, y, text, t)  -- x,y in Prozent des Grundrisses.
    Fuer Checklisten: das Bild zeigt WO, der Text sagt WAS.
    """
    css = f\'\'\'#{sid}-t {{ position:absolute; left:70px; right:70px; top:260px; text-align:center; color:#fff; font-size:96px; line-height:1.1; }}
#{sid}-t .serif {{ color:var(--blue); }}
#{sid}-raum {{ position:absolute; left:110px; right:110px; top:560px; height:760px; border:9px solid var(--steel);
  border-radius:30px; background:rgba(159,211,238,.07); }}
#{sid}-raum .moebel {{ position:absolute; background:var(--steel); opacity:.45; border-radius:10px; }}
#{sid}-raum .m1 {{ left:7%; top:12%; width:34%; height:19%; }}
#{sid}-raum .m2 {{ right:7%; top:12%; width:26%; height:30%; }}
#{sid}-raum .m3 {{ left:7%; bottom:12%; width:44%; height:22%; }}
#{sid}-raum .m4 {{ right:9%; bottom:14%; width:22%; height:17%; border-radius:50%; }}
#{sid}-raum .pin {{ position:absolute; width:96px; height:96px; margin:-48px 0 0 -48px; border-radius:50%;
  background:var(--rot); display:flex; align-items:center; justify-content:center; color:#fff;
  font-weight:900; font-size:52px; opacity:0; }}
#{sid}-raum .ring {{ position:absolute; width:96px; height:96px; margin:-48px 0 0 -48px; border-radius:50%;
  border:7px solid var(--rot); opacity:0; }}
#{sid}-liste {{ position:absolute; left:80px; right:80px; top:1390px; }}
#{sid}-liste .z {{ display:flex; align-items:center; gap:26px; margin-bottom:18px; opacity:0; }}
#{sid}-liste .n {{ flex:0 0 68px; height:68px; border-radius:50%; background:var(--rot); color:#fff;
  font-weight:900; font-size:40px; display:flex; align-items:center; justify-content:center; }}
#{sid}-liste .x {{ font-weight:700; font-size:62px; color:#fff; line-height:1.1; }}\'\'\'

    pins = ''.join(
        f'<div class="ring" id="{sid}-r{i}" style="left:{p["x"]}%;top:{p["y"]}%"></div>'
        f'<div class="pin" id="{sid}-p{i}" style="left:{p["x"]}%;top:{p["y"]}%">{i + 1}</div>'
        for i, p in enumerate(punkte))
    zeilen = ''.join(
        f'<div class="z" id="{sid}-z{i}"><div class="n">{i + 1}</div><div class="x">{p["text"]}</div></div>'
        for i, p in enumerate(punkte))

    inhalt = f\'\'\'<div id="{sid}-t" data-layout-allow-overflow>{titel_html}</div>
<div id="{sid}-raum" data-layout-allow-overflow>
  <div class="moebel m1"></div><div class="moebel m2"></div><div class="moebel m3"></div><div class="moebel m4"></div>
  {pins}
</div>
<div id="{sid}-liste" data-layout-allow-overflow>{zeilen}</div>\'\'\'

    tt = r(t_titel if t_titel is not None else start + .05)
    js = [f'tl.fromTo("#{sid}-t", {{ y: 54, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .32, ease: "back.out(1.7)" }}, {tt});',
          f'tl.fromTo("#{sid}-raum", {{ scale: .9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .38, ease: "back.out(1.4)" }}, {r(tt + .12)});']
    sfx = [('whoosh_hoch', tt - .05, .18, .3)]
    for i, p in enumerate(punkte):
        t = r(p['t'])
        js.append(f'tl.fromTo("#{sid}-p{i}", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .26, ease: "back.out(2.4)" }}, {t});')
        js.append(f'tl.fromTo("#{sid}-r{i}", {{ scale: 1, opacity: .9 }}, {{ scale: 2.4, opacity: 0, duration: .9, ease: "power2.out", repeat: 2 }}, {t});')
        js.append(f'tl.fromTo("#{sid}-z{i}", {{ x: -70, opacity: 0 }}, {{ x: 0, opacity: 1, duration: .3, ease: "power3.out" }}, {r(t + .08)});')
        sfx += [('pop_hoch', p['t'], .18, .55), ('tick', p['t'] + .1, .1, .3)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\\n'.join(js), sfx=sfx)
'''
anker = "\n\ndef abschluss(reel, sid, start, ende, t_marke, t_zeile, t_knopf, bg='var(--navy-deep)'):"
assert s.count(anker) == 1
s = s.replace(anker, NEU + anker)
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# ---------------------------------------------------------------- Regeln
LEHREN = """

---

## 16. Lehren aus der Rückmeldung vom 07.10.2026 (zweite Runde)

### 16.1 Die Marke gehört auf alles, was wir selbst zeichnen

Jeder Gegenstand, den eine Szene erzeugt (Sprühflasche, Eimer, Tuch, Schild), trägt das
Habibi-Abzeichen aus `assets/hr_icon.png`. Das kostet nichts und zeigt die Marke ein
zweites Mal im selben Video. Neu seit 07.10.2026 in der Szene `spruehen` umgesetzt.

### 16.2 Der gesprochene Schluss

- **Das Rauschen am Schluss** kam vom Soundeffekt `whoosh_lang`. Die Whoosh-Effekte in
  `klang.py` sind gefiltertes weisses Rauschen. In `abschluss` läuft er jetzt kürzer
  (0.16 s statt 0.25 s) und leiser (30 Prozent).
- **Die Webadresse wird getrennt gesprochen:** «auf habibi reinigung punkt c h».
  Zusammengeschrieben ist «habibireinigung» für das Sprachmodell ein Kunstwort und klingt
  abgehackt. Geschrieben bleibt es in der Caption natürlich `habibireinigung.ch`.
- **Die Tonkette** bügelte vorher alles platt (gemessen LRA 1.4 LU). `stimme.py` misst jetzt
  in einem ersten Durchlauf und verstärkt im zweiten linear (`linear=true`), der Kompressor
  ist sanfter (ratio 1.6 statt 2). Die Lautstärke darf einen Bogen haben, das verlangt
  Abschnitt 4.2.
- Der Schluss bleibt inhaltlich gleich. Eine Abweichung ist nur erlaubt, wenn ein Trend
  oder ein Format es verlangt, und auch dann bleiben Wortmarke und Knopf.

### 16.3 Mehr Abwechslung, aber nach den Regeln von Social Media

Jedes Reel braucht einen Grund, warum jemand es zu Ende schaut: ein Learning mit Zahl, ein
Trend oder Humor. Hintergrundfarbe, Szenenfolge und die thematische Szene wechseln von Reel
zu Reel. Neue Szene seit 07.10.2026: `hotspots` (Grundriss von oben, vergessene Stellen
leuchten nacheinander auf, dazu die Liste). Gedacht für Checklisten.
"""
for pfad in [R + r'\VIDEO-REGELN.md', r'C:\Users\habib\Documents\Habibi-Marketing\claude\VIDEO-REGELN.md']:
    t = io.open(pfad, encoding='utf-8').read()
    t = t.replace('**Version 1.2, 07.10.2026.**', '**Version 1.3, 07.10.2026.**')
    t = t.replace('| 1.2 | 07.10.2026 |',
                  '| 1.3 | 07.10.2026 | Markenabzeichen auf erzeugte Gegenstaende, Rauschen im Abschluss behoben, Webadresse getrennt sprechen, Tonkette mit Zweidurchlauf, neue Szene hotspots. |\n| 1.2 | 07.10.2026 |')
    t = t.replace('| `maskottchen_tipp` | Figur springt rein',
                  '| `spruehen` | Sprühflasche mit Markenabzeichen, Nebel, nasse Fläche, Sekundenzähler. Für Einwirkzeiten und Mittel. |\n| `hotspots` | Grundriss von oben, vergessene Stellen leuchten auf, dazu die Liste. Für Checklisten. |\n| `maskottchen_tipp` | Figur springt rein')
    t = t.rstrip() + LEHREN
    io.open(pfad, 'w', encoding='utf-8', newline='').write(t)

print('szenen.py (Rauschen, hotspots) und VIDEO-REGELN 1.3 aktualisiert.')
