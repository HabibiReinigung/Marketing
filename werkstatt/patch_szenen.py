# -*- coding: utf-8 -*-
"""Zwei Ergaenzungen am Szenen-Baukasten:
1. punch passt die Schriftgroesse an die Wortlaenge an (EINWIRKZEIT lief aus dem Bild).
2. Neue Szene `spruehen`: Spruehflasche, Nebel, nasse Flaeche und ein Zaehler.
   Sie traegt das Learning im Bild statt nur im Text."""
import io

P = r'C:\Users\habib\Documents\Habibi-Repo\vorlagen\reel\szenen.py'
s = io.open(P, encoding='utf-8').read()

# ---------------------------------------------------------------- 1. punch skaliert mit
alt = "def punch(reel, sid, start, ende, wort, t_wort, klein=None, t_klein=None, unter=None, t_unter=None, bg='var(--navy)', klein_px=64):"
neu = """def punch(reel, sid, start, ende, wort, t_wort, klein=None, t_klein=None, unter=None, t_unter=None, bg='var(--navy)', klein_px=64, px=None):
    # Die Schrift richtet sich nach der Wortlaenge, sonst laeuft ein langes Wort
    # aus dem Bild (Fehler bei EINWIRKZEIT, 07.10.2026). 960 px nutzbare Breite,
    # ein Grossbuchstabe in Poppins 900 ist rund 0.62 der Schriftgroesse breit.
    if px is None:
        px = max(90, min(250, int(960 / max(1, len(str(wort))) / 0.62)))"""
assert s.count(alt) == 1
s = s.replace(alt, neu)

alt2 = """<div id="{sid}-b" class="blk big" style="font-size:250px;color:#fff;letter-spacing:-0.05em;line-height:1">{wort}</div>"""
neu2 = """<div id="{sid}-b" class="blk big" style="font-size:{px}px;color:#fff;letter-spacing:-0.05em;line-height:1">{wort}</div>"""
assert s.count(alt2) == 1
s = s.replace(alt2, neu2)

# ---------------------------------------------------------------- 2. Neue Szene: spruehen
NEU_SZENE = '''

def spruehen(reel, sid, start, ende, zeilen, sekunden, t_spray, t_zaehler, label=None,
             unten=None, t_unten=None, bg='var(--navy)'):
    """Spruehflasche nebelt eine Flaeche ein, die Flaeche glaenzt nass, ein Zaehler laeuft.

    zeilen: wie bei hook, Liste dict(text, art, groesse, t)
    sekunden: Zahl, auf die der Zaehler hochlaeuft (das Learning, z.B. 30)
    """
    d = ende - start
    css = f\'\'\'#{sid}-txt {{ position:absolute; left:70px; right:70px; top:330px; text-align:center; color:#fff; }}
#{sid}-txt .big {{ display:block; line-height:1.08; }}
#{sid}-txt .serif {{ display:block; color:var(--blue); line-height:1.12; margin-top:8px; }}
#{sid}-flasche {{ position:absolute; left:120px; top:860px; width:230px; height:430px; }}
#{sid}-koerper {{ position:absolute; left:0; bottom:0; width:230px; height:300px; border-radius:34px 34px 26px 26px;
  background:linear-gradient(160deg, var(--steel), var(--navy-deep)); box-shadow:inset 0 0 0 7px rgba(255,255,255,.16); }}
#{sid}-fuell {{ position:absolute; left:26px; right:26px; bottom:26px; height:150px; border-radius:18px; background:var(--blue); opacity:.55; }}
#{sid}-hals {{ position:absolute; left:74px; top:96px; width:82px; height:90px; background:var(--steel); border-radius:12px; }}
#{sid}-kopf {{ position:absolute; left:40px; top:34px; width:150px; height:76px; background:#fff; border-radius:20px 8px 8px 20px; }}
#{sid}-duese {{ position:absolute; left:186px; top:56px; width:44px; height:24px; background:#fff; border-radius:6px; }}
#{sid}-hebel {{ position:absolute; left:30px; top:110px; width:96px; height:30px; background:#fff; border-radius:10px; transform-origin:left center; }}
#{sid}-nebel {{ position:absolute; left:330px; top:820px; width:660px; height:220px; }}
#{sid}-nebel i {{ position:absolute; display:block; border-radius:50%; background:var(--blue); opacity:0; }}
#{sid}-flaeche {{ position:absolute; left:300px; right:70px; top:1120px; height:200px; border-radius:26px;
  background:linear-gradient(180deg, #e9f2f8, #cfe2ef); overflow:hidden; }}
#{sid}-nass {{ position:absolute; inset:0; opacity:0;
  background:linear-gradient(115deg, rgba(255,255,255,0) 20%, rgba(255,255,255,.95) 42%, rgba(159,211,238,.75) 56%, rgba(255,255,255,0) 78%); }}
#{sid}-uhr {{ position:absolute; left:0; right:0; top:1400px; text-align:center; }}
#{sid}-zahl {{ font-weight:900; font-size:290px; color:#fff; letter-spacing:-0.05em; line-height:.9; display:block; }}
#{sid}-einh {{ font-weight:700; font-size:76px; color:var(--blue); letter-spacing:.04em; display:block; margin-top:-6px; }}
#{sid}-u {{ position:absolute; left:60px; right:60px; top:1680px; text-align:center; font-size:72px; color:var(--blue); line-height:1.12; }}\'\'\'

    zt = ''.join(
        f'<div id="{sid}-z{i}" class="{"big" if z.get("art", "big") == "big" else "serif"}" '
        f'style="font-size:{z.get("groesse", 104)}px">{z["text"]}</div>'
        for i, z in enumerate(zeilen))

    inhalt = (f'<div id="{sid}-lab" class="label top-label" style="color:var(--blue)">{label}</div>' if label else '') + f\'\'\'
<div id="{sid}-txt" data-layout-allow-overflow>{zt}</div>
<div id="{sid}-flasche" data-layout-allow-overflow>
  <div id="{sid}-koerper"><div id="{sid}-fuell"></div></div>
  <div id="{sid}-hals"></div><div id="{sid}-kopf"></div><div id="{sid}-duese"></div><div id="{sid}-hebel"></div>
</div>
<div id="{sid}-nebel" data-layout-allow-overflow></div>
<div id="{sid}-flaeche"><div id="{sid}-nass"></div></div>
<div id="{sid}-uhr"><span id="{sid}-zahl">0</span><span id="{sid}-einh">SEKUNDEN</span></div>\'\'\' + \\
        (f'<div id="{sid}-u" class="serif">{unten}</div>' if unten else '')

    ts, tz = r(t_spray), r(t_zaehler)
    js = []
    if label:
        js.append(f'tl.fromTo("#{sid}-lab", {{ opacity: 0, y: -26 }}, {{ opacity: 1, y: 0, duration: .28, ease: "power3.out" }}, {r(start + .02)});')
    for i, z in enumerate(zeilen):
        js.append(f'tl.fromTo("#{sid}-z{i}", {{ y: 54, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(1.8)" }}, {r(z["t"])});')
    # Flasche faehrt von links herein und drueckt ab
    js.append(f'tl.fromTo("#{sid}-flasche", {{ x: -340, rotation: -14, opacity: 0 }}, {{ x: 0, rotation: 0, opacity: 1, duration: .34, ease: "back.out(1.5)" }}, {r(ts - .34)});')
    js.append(f'tl.to("#{sid}-hebel", {{ keyframes: [{{ rotation: 16, duration: .08 }}, {{ rotation: 0, duration: .12 }}], transformOrigin: "left center" }}, {ts});')
    # Nebel: Tropfen fliegen zur Flaeche
    js.append(f\'\'\'(() => {{
  const n = document.getElementById("{sid}-nebel");
  for (let i = 0; i < 26; i++) {{
    const e = document.createElement("i");
    const gr = 10 + rnd() * 26;
    e.style.width = gr + "px"; e.style.height = gr + "px";
    e.style.left = "0px"; e.style.top = (70 + rnd() * 80) + "px";
    n.appendChild(e);
    tl.fromTo(e, {{ x: 0, y: 0, opacity: 0, scale: .4 }},
      {{ x: 260 + rnd() * 380, y: 90 + rnd() * 130, opacity: .85, scale: 1, duration: .5 + rnd() * .35, ease: "power2.out" }}, {ts} + rnd() * .3);
    tl.to(e, {{ opacity: 0, duration: .3 }}, {ts} + .55 + rnd() * .35);
  }}
}})();\'\'\')
    # Flaeche wird nass und glaenzt, solange der Zaehler laeuft
    js.append(f'tl.fromTo("#{sid}-nass", {{ opacity: 0, x: -420 }}, {{ opacity: 1, x: 0, duration: .45, ease: "power2.out" }}, {r(ts + .35)});')
    js.append(f'tl.to("#{sid}-nass", {{ x: 160, duration: {r(max(0.6, ende - ts - 1.0))}, ease: "sine.inOut" }}, {r(ts + .8)});')
    # Zaehler laeuft hoch: das ist die Zahl, die haengen bleiben soll
    js.append(f'tl.fromTo("#{sid}-uhr", {{ y: 70, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "back.out(2)" }}, {r(tz - .25)});')
    js.append(f'tl.fromTo("#{sid}-zahl", {{ innerText: 0 }}, {{ innerText: {sekunden}, snap: {{ innerText: 1 }}, duration: .95, ease: "power2.out" }}, {tz});')
    js.append(f'tl.fromTo("#{sid}-zahl", {{ scale: .55 }}, {{ scale: 1, duration: .95, ease: "back.out(1.7)" }}, {tz});')
    js.append(f'tl.to("#{sid}-zahl", {{ keyframes: [{{ scale: 1.12, duration: .1 }}, {{ scale: 1, duration: .14 }}] }}, {r(tz + .95)});')
    if unten:
        js.append(f'tl.fromTo("#{sid}-u", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "power3.out" }}, {r(t_unten if t_unten else tz + 1.1)});')

    sfx = [('whoosh_hoch', ts - .34, .3, .35), ('squeak', ts, .18, .5), ('smear', ts + .05, .6, .55)]
    sfx += [('tick', tz + i * 0.085, .12, .35) for i in range(11)]
    sfx += [('ding', tz + .95, .4, .6)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\\n'.join(js), sfx=sfx)
'''

anker = "\n\ndef abschluss(reel, sid, start, ende, t_marke, t_zeile, t_knopf, bg='var(--navy-deep)'):"
assert s.count(anker) == 1
s = s.replace(anker, NEU_SZENE + anker)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('szenen.py: punch skaliert jetzt, Szene `spruehen` ergaenzt.')
