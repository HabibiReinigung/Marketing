#!/usr/bin/env python3
"""Szenen-Baukasten für Habibi-Reinigung-Reels (HyperFrames + GSAP, 1080x1920).

Jede Szene liefert HTML, CSS, GSAP-Code und Soundeffekt-Ereignisse.
Ein Reel = Liste von Szenen + Stimme. Siehe reel_*.py für Beispiele.
"""
import json

BASIS_CSS = """
@font-face { font-family: "Poppins"; font-weight: 900; src: url("assets/fonts/Poppins-Black.ttf") format("truetype"); }
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/Poppins-Bold.ttf") format("truetype"); }
@font-face { font-family: "Poppins"; font-weight: 500; src: url("assets/fonts/Poppins-Medium.ttf") format("truetype"); }
@font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; src: url("assets/fonts/instrument-serif-latin-400-italic.woff2") format("woff2"); }
:root { --navy:#152a43; --navy-deep:#0a1826; --steel:#2c6693; --ice:#eef3f7; --blue:#9fd3ee; --white:#fff; --rot:#e5484d; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:var(--navy-deep); }
#root { position:relative; width:100%; height:100%; overflow:hidden; font-family:"Poppins", sans-serif; }
.clip { position:absolute; inset:0; overflow:hidden; }
.fill { position:absolute; inset:0; }
.center { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.serif { font-family:"Instrument Serif", serif; font-style:italic; font-weight:400; }
.label { font-weight:700; font-size:34px; letter-spacing:0.32em; text-transform:uppercase; }
.top-label { position:absolute; top:230px; left:0; right:0; text-align:center; }
.blk { display:block; }
.bubble { position:absolute; border-radius:50%; display:block;
  background: radial-gradient(circle at 30% 28%, rgba(255,255,255,.95) 0 7%, rgba(255,255,255,0) 15%),
  radial-gradient(circle at 70% 75%, rgba(255,255,255,.35) 0 4%, rgba(255,255,255,0) 10%),
  radial-gradient(circle at 50% 50%, rgba(255,255,255,.04) 0 58%, rgba(255,255,255,.28) 66%, rgba(180,220,255,.55) 70%, rgba(255,200,240,.35) 72%, rgba(255,255,255,0) 74%);
  box-shadow: inset 0 0 18px rgba(255,255,255,.35); }
.grain { position:absolute; inset:-50%; background:url("assets/grain.png"); opacity:.07; mix-blend-mode:overlay; pointer-events:none; }
.big { font-weight:900; letter-spacing:-0.02em; line-height:1.02; }
.spark { position:absolute; width:90px; height:90px; display:block; }
"""

BASIS_JS = """
let seed = 20261005;
const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
function makeBubbles(container, n, minS, maxS) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const b = document.createElement("div"); b.className = "bubble";
    const s = minS + rnd() * (maxS - minS);
    b.style.width = s + "px"; b.style.height = s + "px";
    b.style.left = (rnd() * 1080 - s / 2) + "px"; b.style.top = (300 + rnd() * 1700) + "px";
    container.appendChild(b); out.push({ el: b, drift: 600 + rnd() * 900, sway: 30 + rnd() * 60 });
  }
  return out;
}
function sparks(container, pts, t0, tl) {
  pts.forEach(([x, y], i) => {
    const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("viewBox", "0 0 100 100"); s.setAttribute("class", "spark");
    s.style.left = (x - 45) + "px"; s.style.top = (y - 45) + "px";
    s.innerHTML = '<path d="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z" fill="#ffffff"/>';
    container.appendChild(s);
    tl.fromTo(s, { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.32, ease: "back.out(3)" }, t0 + i * 0.1);
    tl.to(s, { scale: 0, rotation: 90, duration: 0.28, ease: "power2.in" }, t0 + 0.6 + i * 0.08);
  });
}
const tl = gsap.timeline({ paused: true });
"""

MASKOTTCHEN_W, MASKOTTCHEN_H = 524, 619  # Seitenverhältnis von assets/maskottchen.png


def r(x):
    return round(float(x), 3)


class Reel:
    def __init__(self, titel, dauer):
        self.titel, self.dauer = titel, r(dauer)
        self.html, self.css, self.js, self.sfx = [], [BASIS_CSS], [BASIS_JS], []

    def szene(self, sid, start, ende, bg, inhalt, css='', js='', sfx=()):
        self.html.append(f'<section id="{sid}" class="clip" data-start="{r(start)}" data-duration="{r(ende - start)}" data-track-index="0" style="background:{bg}">\n{inhalt}\n<div class="grain"></div>\n</section>')
        if css: self.css.append(css)
        if js: self.js.append(f'// ---- {sid}\n{{\n{js}\n}}')
        self.sfx.extend(sfx)

    def bauen(self):
        return f"""<!doctype html>
<html lang="de" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<title>{self.titel}</title>
<script src="assets/gsap.min.js"></script>
<style>{''.join(self.css)}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{self.dauer}" data-width="1080" data-height="1920">
{chr(10).join(self.html)}
</div>
<script>
{chr(10).join(self.js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>"""


# ------------------------------------------------------------------ Szenen

def hook(reel, sid, start, ende, zeilen, label=None, bg='var(--blue)', farbe='var(--navy)', blasen=True):
    """zeilen: Liste dict(text, art='big'|'serif', groesse, farbe, t)."""
    teile = []
    for i, z in enumerate(zeilen):
        cls = 'big' if z.get('art', 'big') == 'big' else 'serif'
        teile.append(f'<div id="{sid}-z{i}" class="blk {cls}" style="font-size:{z["groesse"]}px;color:{z.get("farbe", farbe)};{"line-height:1.05;margin-top:6px;" if cls == "serif" else ""}">{z["text"]}</div>')
    inhalt = (f'<div id="{sid}-bl" class="fill" data-layout-allow-overflow></div>' if blasen else '') + \
        (f'<div id="{sid}-lab" class="label top-label" style="color:{farbe}">{label}</div>' if label else '') + \
        f'<div id="{sid}-w" class="center" style="padding:0 60px" data-layout-allow-overflow>{"".join(teile)}</div>'
    d = ende - start
    js = []
    if blasen:
        js.append(f'makeBubbles(document.getElementById("{sid}-bl"), 14, 60, 210).forEach((b, i) => tl.fromTo(b.el, {{ y: 0, x: 0, opacity: 0 }}, {{ y: -b.drift, x: (i % 2 ? 1 : -1) * b.sway, opacity: .95, duration: {r(d)}, ease: "none" }}, {r(start)}));')
    if label:
        js.append(f'tl.fromTo("#{sid}-lab", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: .3, ease: "power3.out" }}, {r(start + .02)});')
    sfx = []
    for i, z in enumerate(zeilen):
        t = r(z['t'])
        if z.get('art', 'big') == 'big':
            js.append(f'tl.fromTo("#{sid}-z{i}", {{ scale: 2.2, opacity: 0, filter: "blur(18px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: .28, ease: "back.out(2.2)" }}, {t});')
            sfx += [('whoosh', t - .1, .22), ('thump', t, .32)]
        else:
            js.append(f'tl.fromTo("#{sid}-z{i}", {{ y: 80, opacity: 0, rotation: -6 }}, {{ y: 0, opacity: 1, rotation: 0, duration: .4, ease: "back.out(2.6)" }}, {t});')
            sfx += [('pop', t, .3, .2)]
    t_last = zeilen[-1]['t']
    js.append(f'tl.to("#{sid}-w", {{ scale: 1.06, duration: {r(max(.3, ende - t_last))}, ease: "none" }}, {r(t_last)});')
    reel.szene(sid, start, ende, bg, inhalt, js='\n'.join(js), sfx=sfx)


def punch(reel, sid, start, ende, wort, t_wort, klein=None, t_klein=None, unter=None, t_unter=None, bg='var(--navy)', klein_px=64):
    inhalt = f'''<div id="{sid}-w" class="center" data-layout-allow-overflow>
{f'<div id="{sid}-k" class="blk big" style="font-size:{klein_px}px;color:var(--blue);margin-bottom:10px">{klein}</div>' if klein else ''}
<div id="{sid}-b" class="blk big" style="font-size:250px;color:#fff;letter-spacing:-0.05em;line-height:1">{wort}</div>
<div id="{sid}-bar" style="width:600px;height:26px;background:var(--blue);border-radius:13px;margin-top:28px;transform-origin:left center;display:block"></div>
{f'<div id="{sid}-u" class="label blk" style="color:var(--blue);margin-top:64px">{unter}</div>' if unter else ''}
</div>'''
    js = []
    sfx = []
    if klein:
        js.append(f'tl.fromTo("#{sid}-k", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "power3.out" }}, {r(t_klein)});')
        sfx.append(('whoosh_hoch', t_klein - .05, .15, .3))
    tw = r(t_wort)
    js.append(f'tl.fromTo("#{sid}-b", {{ scale: 3.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .16, ease: "power4.in" }}, {tw});')
    js.append(f'tl.fromTo("#{sid}-w", {{ x: 0, y: 0 }}, {{ keyframes: [{{ x: -26, y: 14, duration: .04 }}, {{ x: 22, y: -18, duration: .04 }}, {{ x: -14, y: 10, duration: .04 }}, {{ x: 8, y: -6, duration: .04 }}, {{ x: 0, y: 0, duration: .05 }}] }}, {r(tw + .16)});')
    js.append(f'tl.fromTo("#{sid}-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: .35, ease: "expo.out" }}, {r(tw + .25)});')
    if unter:
        js.append(f'tl.fromTo("#{sid}-u", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .3, ease: "power3.out" }}, {r(t_unter)});')
    js.append(f'tl.to("#{sid}-w", {{ scale: 1.08, duration: {r(max(.3, ende - tw - .3))}, ease: "none" }}, {r(tw + .3)});')
    sfx += [('riser', tw - .45, .2), ('impact', tw + .16, .6)]
    reel.szene(sid, start, ende, bg, inhalt, js='\n'.join(js), sfx=sfx)


def durchstreichen(reel, sid, start, ende, karte, t_karte, t_strich, unter, t_unter, label=None, bg='var(--ice)'):
    """Graue Karte («Preis auf Anfrage») fällt rein, roter Strich, sarkastischer Untertitel."""
    css = f'''#{sid}-card {{ position:absolute; left:120px; right:120px; top:640px; height:330px; background:#fff; border-radius:40px;
  box-shadow:0 30px 60px rgba(21,42,67,.18); display:flex; align-items:center; justify-content:center; }}
#{sid}-ct {{ font-weight:700; font-size:74px; color:#8a97a6; letter-spacing:-0.02em; }}
#{sid}-st {{ position:absolute; left:60px; right:60px; top:150px; height:22px; background:var(--rot); border-radius:11px; transform-origin:left center; display:block; transform:rotate(-4deg); }}
#{sid}-u {{ position:absolute; left:0; right:0; top:1060px; text-align:center; font-size:130px; color:var(--steel); }}
#{sid}-q1, #{sid}-q2 {{ position:absolute; font-weight:900; font-size:150px; color:rgba(44,102,147,.25); display:block; }}'''
    inhalt = f'''{f'<div id="{sid}-lab" class="label top-label" style="color:var(--steel)">{label}</div>' if label else ''}
<div id="{sid}-q1" style="left:120px;top:430px">?</div><div id="{sid}-q2" style="left:860px;top:1180px">?</div>
<div id="{sid}-card" data-layout-allow-overflow><div id="{sid}-ct">{karte}</div><div id="{sid}-st"></div></div>
<div id="{sid}-u" class="serif">{unter}</div>'''
    js = [f'tl.fromTo("#{sid}-card", {{ y: -900, rotation: -8 }}, {{ y: 0, rotation: 2, duration: .55, ease: "bounce.out" }}, {r(t_karte)});',
          f'tl.fromTo("#{sid}-q1", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: .4, ease: "back.out(3)" }}, {r(t_karte + .3)});',
          f'tl.fromTo("#{sid}-q2", {{ scale: 0, rotation: 30 }}, {{ scale: 1, rotation: 0, duration: .4, ease: "back.out(3)" }}, {r(t_karte + .45)});',
          f'tl.fromTo("#{sid}-st", {{ scaleX: 0 }}, {{ scaleX: 1, duration: .32, ease: "power2.inOut" }}, {r(t_strich)});',
          f'tl.fromTo("#{sid}-u", {{ y: 60, opacity: 0, rotation: 4 }}, {{ y: 0, opacity: 1, rotation: -2, duration: .45, ease: "back.out(2.4)" }}, {r(t_unter)});',
          f'tl.to("#{sid}-card", {{ rotation: -6, y: 40, duration: {r(max(.3, ende - t_unter))}, ease: "power1.in" }}, {r(t_unter)});']
    if label:
        js.insert(0, f'tl.fromTo("#{sid}-lab", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, {r(start)});')
    sfx = [('whoosh_runter', t_karte - .05, .25), ('thump', t_karte + .4, .3), ('scratch', t_strich, .35), ('pop_tief', t_unter, .25)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def preis(reel, sid, start, ende, wert, t_zahl, stempel, t_stempel, oben='ab CHF', unten='pro Monat', bg='var(--blue)'):
    css = f'''#{sid}-o {{ font-weight:700; font-size:70px; color:var(--navy); }}
#{sid}-n {{ font-weight:900; font-size:380px; color:var(--navy); letter-spacing:-0.06em; line-height:.95; display:block; min-width:760px; text-align:center; }}
#{sid}-u {{ font-size:120px; color:#fff; line-height:1; }}
#{sid}-st {{ position:absolute; left:170px; right:170px; top:1290px; height:150px; border:10px solid var(--navy); border-radius:24px; display:flex; align-items:center; justify-content:center;
  font-weight:900; font-size:66px; color:var(--navy); letter-spacing:.06em; background:rgba(255,255,255,.35); transform:rotate(-7deg); }}'''
    inhalt = f'''<div id="{sid}-bl" class="fill" data-layout-allow-overflow></div>
<div id="{sid}-w" class="center" style="padding-bottom:260px" data-layout-allow-overflow>
<div id="{sid}-o" class="blk">{oben}</div><div id="{sid}-n">0</div><div id="{sid}-u" class="serif blk">{unten}</div></div>
<div id="{sid}-st" data-layout-allow-overflow>{stempel}</div>'''
    tz, ts = r(t_zahl), r(t_stempel)
    js = [f'makeBubbles(document.getElementById("{sid}-bl"), 8, 50, 160).forEach((b, i) => tl.fromTo(b.el, {{ y: 0, opacity: 0 }}, {{ y: -b.drift * .7, x: (i % 2 ? 1 : -1) * b.sway, opacity: .7, duration: {r(ende - start)}, ease: "none" }}, {r(start)}));',
          f'tl.fromTo("#{sid}-o", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .3, ease: "power3.out" }}, {r(start + .02)});',
          f'tl.fromTo("#{sid}-n", {{ innerText: 0 }}, {{ innerText: {wert}, snap: {{ innerText: 1 }}, duration: .9, ease: "power3.out" }}, {tz});',
          f'tl.fromTo("#{sid}-n", {{ scale: .6 }}, {{ scale: 1, duration: .9, ease: "back.out(1.6)" }}, {tz});',
          f'tl.fromTo("#{sid}-u", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .35, ease: "back.out(2)" }}, {r(tz + .7)});',
          f'tl.fromTo("#{sid}-st", {{ scale: 2.6, opacity: 0, rotation: -18 }}, {{ scale: 1, opacity: 1, rotation: -7, duration: .22, ease: "power4.in" }}, {ts});',
          f'tl.fromTo("#{sid}-w", {{ x: 0 }}, {{ keyframes: [{{ x: -10, duration: .04 }}, {{ x: 8, duration: .04 }}, {{ x: 0, duration: .05 }}] }}, {r(ts + .22)});']
    sfx = [('tick', tz + i * 0.07, .14) for i in range(12)] + [('thump', tz + .9, .3), ('stamp', ts + .2, .55)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def maskottchen_tipp(reel, sid, start, ende, karten, label='Tipp vom Profi', bg='var(--blue)', t_rein=None):
    """karten: Liste (html, t). Figur springt rein, Sprechblase wechselt Text."""
    t_rein = start if t_rein is None else t_rein
    mh = 760; mw = round(mh * MASKOTTCHEN_W / MASKOTTCHEN_H)
    css = f'''#{sid}-glow {{ position:absolute; left:40px; top:760px; width:1000px; height:1000px; border-radius:50%;
  background:radial-gradient(circle, rgba(255,255,255,.75) 0%, rgba(255,255,255,.25) 40%, rgba(255,255,255,0) 68%); display:block; }}
#{sid}-card {{ position:absolute; left:90px; right:90px; top:330px; height:470px; background:#fff; border-radius:48px; box-shadow:0 30px 60px rgba(21,42,67,.25); display:block; }}
#{sid}-tail {{ position:absolute; left:520px; bottom:-46px; width:0; height:0; border-left:40px solid transparent; border-right:40px solid transparent; border-top:50px solid #fff; }}
.{sid}-txt {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:0 60px; color:var(--navy); }}
.{sid}-txt .a {{ font-weight:900; font-size:104px; letter-spacing:-0.02em; line-height:1.04; }}
.{sid}-txt .b {{ font-weight:700; font-size:70px; line-height:1.12; letter-spacing:-0.01em; }}
.{sid}-txt .serif {{ font-size:96px; color:var(--steel); }}
#{sid}-m {{ position:absolute; left:{round((1080 - mw) / 2)}px; top:830px; width:{mw}px; height:{mh}px; display:block; transform-origin:50% 100%; }}
#{sid}-m img {{ width:100%; height:100%; display:block; filter:drop-shadow(0 34px 40px rgba(21,42,67,.35)); }}'''
    kt = ''.join(f'<div id="{sid}-t{i}" class="{sid}-txt">{h}</div>' for i, (h, _) in enumerate(karten))
    inhalt = f'''<div id="{sid}-glow"></div>
<div class="label top-label" id="{sid}-lab" style="color:var(--navy)">{label}</div>
<div id="{sid}-card" data-layout-allow-occlusion><div id="{sid}-tail" data-layout-allow-overflow></div>{kt}</div>
<div id="{sid}-m" data-layout-allow-overflow><img src="assets/maskottchen.png" alt="Habibi Maskottchen" /></div>'''
    tr = r(t_rein); t0 = r(karten[0][1])
    js = [f'tl.fromTo("#{sid}-glow", {{ scale: .8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .7, ease: "power2.out" }}, {tr});',
          f'tl.fromTo("#{sid}-lab", {{ opacity: 0, y: -24 }}, {{ opacity: 1, y: 0, duration: .3, ease: "power3.out" }}, {r(tr + .05)});',
          f'tl.fromTo("#{sid}-m", {{ y: 1100, scaleY: 1.15, scaleX: .9 }}, {{ y: 0, scaleY: 1, scaleX: 1, duration: .5, ease: "back.out(1.7)" }}, {tr});',
          f'tl.to("#{sid}-m", {{ keyframes: [{{ scaleY: .92, scaleX: 1.06, duration: .09 }}, {{ scaleY: 1.04, scaleX: .97, duration: .12 }}, {{ scaleY: 1, scaleX: 1, duration: .12 }}] }}, {r(tr + .5)});',
          f'tl.fromTo("#{sid}-card", {{ scale: 0, transformOrigin: "50% 100%" }}, {{ scale: 1, duration: .35, ease: "back.out(2.2)" }}, {r(t0 - .2)});']
    wob = max(.6, ende - (tr + .85))
    js.append(f'tl.to("#{sid}-m", {{ keyframes: [{{ rotation: -4, duration: {r(wob * .18)}, ease: "sine.inOut" }}, {{ rotation: 3, duration: {r(wob * .22)}, ease: "sine.inOut" }}, {{ rotation: -3, duration: {r(wob * .22)}, ease: "sine.inOut" }}, {{ rotation: 2, duration: {r(wob * .2)}, ease: "sine.inOut" }}, {{ rotation: 0, duration: {r(wob * .18)}, ease: "sine.inOut" }}] }}, {r(tr + .85)});')
    sfx = [('boing', tr, .35), ('pop', t0 - .2, .3)]
    for i, (_, t) in enumerate(karten):
        js.append(f'tl.fromTo("#{sid}-t{i}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .25, ease: "power3.out" }}, {r(t)});')
        if i + 1 < len(karten):
            js.append(f'tl.to("#{sid}-t{i}", {{ opacity: 0, y: -30, duration: .18, ease: "power2.in" }}, {r(karten[i + 1][1] - .18)});')
        if i > 0:
            js.append(f'tl.to("#{sid}-m", {{ y: -30, duration: .22, yoyo: true, repeat: 1, ease: "power2.out" }}, {r(t)});')
            sfx.append(('pop_hoch', t, .25))
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def zone(reel, sid, start, ende, t_ring, abzeichen, t_abz, titel_html, ort='Chur', ring='5 km', bg='var(--navy)'):
    css = f'''#{sid}-grid {{ position:absolute; inset:0; background-image:linear-gradient(rgba(159,211,238,.08) 2px, transparent 2px), linear-gradient(90deg, rgba(159,211,238,.08) 2px, transparent 2px); background-size:90px 90px; }}
#{sid}-ti {{ position:absolute; left:60px; right:60px; top:290px; text-align:center; color:#fff; }}
#{sid}-ti .a {{ font-weight:900; font-size:112px; letter-spacing:-0.02em; line-height:1.22; display:block; }}
#{sid}-ti .serif {{ font-size:120px; color:var(--blue); display:block; line-height:1.18; margin-top:4px; }}
#{sid}-ring {{ position:absolute; left:190px; top:760px; width:700px; height:700px; border-radius:50%; border:8px dashed var(--blue); background:rgba(159,211,238,.10); display:block; }}
#{sid}-pin {{ position:absolute; left:500px; top:1050px; width:80px; height:80px; border-radius:50% 50% 50% 0; transform:rotate(-45deg); background:#fff; display:block; box-shadow:0 10px 30px rgba(0,0,0,.3); }}
#{sid}-ort {{ position:absolute; left:0; right:0; top:1150px; text-align:center; font-weight:700; font-size:54px; color:#fff; }}
#{sid}-km {{ position:absolute; left:820px; top:800px; font-weight:900; font-size:62px; color:var(--blue); display:block; }}
#{sid}-abz {{ position:absolute; left:200px; right:200px; top:1500px; height:130px; border-radius:70px; background:var(--blue); color:var(--navy);
  font-weight:900; font-size:58px; display:flex; align-items:center; justify-content:center; }}'''
    inhalt = f'''<div id="{sid}-grid"></div><div id="{sid}-ti">{titel_html}</div>
<div id="{sid}-ring" data-layout-allow-overflow></div><div id="{sid}-pin"></div><div id="{sid}-ort">{ort}</div>
<div id="{sid}-km" data-layout-allow-overflow>{ring}</div><div id="{sid}-abz" data-layout-allow-overflow>{abzeichen}</div>'''
    trg = r(t_ring)
    js = [f'tl.fromTo("#{sid}-ti", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .35, ease: "back.out(2)" }}, {r(start + .02)});',
          f'tl.fromTo("#{sid}-pin", {{ y: -400, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .45, ease: "bounce.out" }}, {r(start + .1)});',
          f'tl.fromTo("#{sid}-ort", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, {r(start + .45)});',
          f'tl.fromTo("#{sid}-ring", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: .8, ease: "expo.out" }}, {trg});',
          f'tl.fromTo("#{sid}-km", {{ scale: 0 }}, {{ scale: 1, duration: .35, ease: "back.out(3)" }}, {r(trg + .5)});',
          f'tl.to("#{sid}-ring", {{ rotation: 25, duration: {r(max(.5, ende - trg - .8))}, ease: "none" }}, {r(trg + .8)});',
          f'tl.fromTo("#{sid}-abz", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .38, ease: "back.out(2.6)" }}, {r(t_abz)});']
    sfx = [('whoosh_runter', start, .2), ('thump_klein', start + .4, .3), ('whoosh_lang', trg, .25), ('pop', trg + .5, .25), ('ding', t_abz, .25)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


RADIATOR_SVG = '''<svg viewBox="0 0 760 440" width="760" height="440">
<defs><linearGradient id="RID-fin" x1="0" x2="1"><stop offset="0" stop-color="#d6dee6"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="#c3cdd8"/></linearGradient></defs>
<rect x="20" y="30" width="720" height="34" rx="17" fill="#c9d3dd"/>
<rect x="20" y="380" width="720" height="34" rx="17" fill="#c9d3dd"/>
FINS
<rect x="60" y="414" width="26" height="26" rx="6" fill="#9aa8b6"/><rect x="674" y="414" width="26" height="26" rx="6" fill="#9aa8b6"/>
<circle cx="725" cy="70" r="16" fill="#8a97a6"/>
</svg>'''


def _radiator(rid):
    fins = ''.join(f'<rect x="{40 + i * 68}" y="20" width="54" height="404" rx="27" fill="url(#{rid}-fin)" stroke="#b5c1cc" stroke-width="2"/>' for i in range(10))
    return RADIATOR_SVG.replace('RID', rid).replace('FINS', fins)


def heizung(reel, sid, start, ende, modus, zeilen, label=None, t_aktion=None, bg='var(--ice)'):
    """modus: 'waerme' (Hitzewellen), 'staub' (Staub wirbelt hoch), 'buerste' (Bürste putzt von oben nach unten)."""
    css = f'''#{sid}-rad {{ position:absolute; left:160px; top:1060px; width:760px; height:440px; display:block; }}
#{sid}-txt {{ position:absolute; left:60px; right:60px; top:330px; text-align:center; color:var(--navy); }}
#{sid}-txt .a {{ font-weight:900; font-size:108px; letter-spacing:-0.02em; line-height:1.22; display:block; }}
#{sid}-txt .serif {{ font-size:130px; color:var(--steel); display:block; line-height:1.18; margin-top:4px; }}
.{sid}-d {{ position:absolute; border-radius:50%; background:#6b5b4b; display:block; }}
#{sid}-coat {{ position:absolute; left:160px; top:1060px; width:760px; height:440px; display:block; }}
#{sid}-brush {{ position:absolute; left:120px; top:1000px; width:840px; height:60px; border-radius:30px; background:linear-gradient(#2c6693, #152a43); display:block; box-shadow:0 14px 30px rgba(21,42,67,.35); }}
#{sid}-brush::after {{ content:""; position:absolute; left:30px; right:30px; top:52px; height:40px; background:repeating-linear-gradient(90deg, #9fd3ee 0 6px, transparent 6px 14px); }}
#{sid}-arrow {{ position:absolute; left:960px; top:1080px; width:60px; height:380px; display:block; }}'''
    zt = ''.join(f'<div id="{sid}-z{i}" class="{"a" if z.get("art", "big") == "big" else "serif"}">{z["text"]}</div>' for i, z in enumerate(zeilen))
    wellen = ''
    if modus == 'waerme':
        wellen = f'<svg id="{sid}-wl" viewBox="0 0 760 300" width="760" height="300" style="position:absolute;left:160px;top:760px" data-layout-allow-overflow>' + ''.join(
            f'<path class="{sid}-w" d="M{90 + i * 150} 290 C {60 + i * 150} 230, {120 + i * 150} 190, {90 + i * 150} 130 S {60 + i * 150} 40, {90 + i * 150} 0" fill="none" stroke="rgba(229,72,77,.55)" stroke-width="14" stroke-linecap="round"/>' for i in range(5)) + '</svg>'
    extra = ''
    if modus == 'buerste':
        extra = f'<svg id="{sid}-coat" viewBox="0 0 760 440" data-layout-allow-overflow><g fill="#7d6b58" opacity=".55">' + ''.join(
            f'<circle cx="{(i * 97) % 740 + 10}" cy="{(i * 53) % 420 + 10}" r="{3 + (i * 7) % 6}"/>' for i in range(160)) + '</g></svg>' + \
            f'<div id="{sid}-brush" data-layout-allow-overflow></div>' + \
            f'<svg id="{sid}-arrow" viewBox="0 0 60 380"><path d="M30 0 V340" stroke="#2c6693" stroke-width="12" stroke-linecap="round"/><path d="M5 320 L30 370 L55 320" fill="none" stroke="#2c6693" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    inhalt = (f'<div class="label top-label" id="{sid}-lab" style="color:var(--steel)">{label}</div>' if label else '') + \
        f'<div id="{sid}-txt">{zt}</div>{wellen}<div id="{sid}-rad">{_radiator(sid)}</div>{extra}<div id="{sid}-dust" class="fill" data-layout-allow-overflow></div>'
    js = [f'tl.fromTo("#{sid}-rad", {{ y: 500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .5, ease: "back.out(1.6)" }}, {r(start + .02)});']
    if label:
        js.append(f'tl.fromTo("#{sid}-lab", {{ opacity: 0, y: -24 }}, {{ opacity: 1, y: 0, duration: .3 }}, {r(start + .02)});')
    sfx = [('whoosh_lang', start - .05, .22)]
    for i, z in enumerate(zeilen):
        t = r(z['t'])
        if z.get('art', 'big') == 'big':
            js.append(f'tl.fromTo("#{sid}-z{i}", {{ scale: 2, opacity: 0, filter: "blur(14px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: .28, ease: "back.out(2.2)" }}, {t});')
            sfx.append(('thump_klein', t, .25))
        else:
            js.append(f'tl.fromTo("#{sid}-z{i}", {{ y: 70, opacity: 0, rotation: -5 }}, {{ y: 0, opacity: 1, rotation: 0, duration: .4, ease: "back.out(2.4)" }}, {t});')
            sfx.append(('pop', t, .25))
    ta = r(t_aktion if t_aktion is not None else start + .4)
    if modus == 'waerme':
        js.append(f'document.querySelectorAll(".{sid}-w").forEach((p, i) => {{ const L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; tl.to(p, {{ strokeDashoffset: 0, duration: .6, ease: "power2.out" }}, {ta} + i * .08); tl.to(p, {{ y: -40, opacity: .2, duration: {r(max(.5, ende - ta - .6))}, ease: "none" }}, {ta} + .6); }});')
        sfx.append(('whoosh_hoch', ta, .2))
    if modus == 'staub':
        js.append(f'''const dl = document.getElementById("{sid}-dust");
for (let i = 0; i < 70; i++) {{ const d = document.createElement("div"); d.className = "{sid}-d"; const s = 6 + rnd() * 16;
  d.style.width = s + "px"; d.style.height = s + "px"; d.style.left = (200 + rnd() * 680) + "px"; d.style.top = (1080 + rnd() * 380) + "px"; dl.appendChild(d);
  const up = 600 + rnd() * 700, sw = (rnd() - .5) * 400, t0 = {ta} + rnd() * .9, dd = 1.2 + rnd() * .8;
  tl.fromTo(d, {{ x: 0, y: 0, opacity: 0 }}, {{ keyframes: [{{ x: sw * .5, y: -up * .4, opacity: .9, duration: dd * .4, ease: "sine.out" }}, {{ x: -sw * .3, y: -up * .75, duration: dd * .3, ease: "sine.inOut" }}, {{ x: sw, y: -up, opacity: .5, duration: dd * .3, ease: "sine.in" }}] }}, t0); }}''')
        sfx += [('whoosh_hoch', ta, .25), ('smear', ta + .3, .12, -.4), ('smear', ta + .6, .12, .4)]
    if modus == 'buerste':
        dur = r(max(.8, min(1.4, ende - ta - .3)))
        js.append(f'tl.fromTo("#{sid}-brush", {{ y: 0 }}, {{ y: 420, duration: {dur}, ease: "power1.inOut" }}, {ta});')
        js.append(f'tl.fromTo("#{sid}-coat", {{ clipPath: "inset(0% 0 0 0)" }}, {{ clipPath: "inset(100% 0 0 0)", duration: {dur}, ease: "power1.inOut" }}, {ta});')
        js.append(f'tl.fromTo("#{sid}-arrow", {{ scaleY: 0, transformOrigin: "50% 0%" }}, {{ scaleY: 1, duration: .4, ease: "power2.out" }}, {r(ta - .1)});')
        js.append(f'sparks(document.getElementById("{sid}-dust"), [[230, 1130], [850, 1180], [540, 1300]], {r(ta + dur)}, tl);')
        sfx += [('squeak', ta, .2), ('glitzer', ta + dur, .15)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def abschluss(reel, sid, start, ende, t_marke, t_zeile, t_knopf, bg='var(--navy-deep)'):
    mh = 330; mw = round(mh * MASKOTTCHEN_W / MASKOTTCHEN_H)
    css = f'''#{sid}-mark {{ width:900px; display:block; margin-top:-380px; }}
#{sid}-line {{ color:#fff; font-weight:700; font-size:58px; line-height:1.2; margin-top:90px; }}
#{sid}-line .serif {{ color:var(--blue); font-size:78px; }}
#{sid}-btn {{ margin-top:60px; background:var(--blue); color:var(--navy); font-weight:900; font-size:54px; padding:26px 64px; border-radius:80px; display:block; }}
#{sid}-tag {{ color:rgba(238,243,247,.7); position:absolute; top:300px; left:0; right:0; font-size:28px; }}
#{sid}-m {{ position:absolute; left:{round((1080 - mw) / 2)}px; top:1290px; width:{mw}px; height:{mh}px; display:block; transform-origin:50% 100%; }}
#{sid}-m img {{ width:100%; height:100%; display:block; }}'''
    inhalt = f'''<div id="{sid}-bl" class="fill" data-layout-allow-overflow></div>
<div class="center"><img id="{sid}-mark" src="assets/wortmarke.png" alt="Habibi Reinigung" />
<div id="{sid}-line" class="blk"><div class="blk">Richtpreis für euer Büro</div><div class="blk serif">in 1 Minute</div></div>
<div id="{sid}-btn">habibireinigung.ch</div><div id="{sid}-tag" class="label blk">Büros · Praxen · Studios · Chur</div></div>
<div id="{sid}-m"><img src="assets/maskottchen.png" alt="" /></div>'''
    js = [f'makeBubbles(document.getElementById("{sid}-bl"), 10, 50, 170).forEach((b, i) => tl.fromTo(b.el, {{ y: 0, opacity: 0 }}, {{ y: -b.drift * .8, x: (i % 2 ? 1 : -1) * b.sway, opacity: .6, duration: {r(ende - start)}, ease: "none" }}, {r(start)}));',
          f'tl.fromTo("#{sid}-mark", {{ y: -60, opacity: 0, scale: .9 }}, {{ y: 0, opacity: 1, scale: 1, duration: .42, ease: "back.out(1.8)" }}, {r(t_marke)});',
          f'tl.fromTo("#{sid}-m", {{ y: 500 }}, {{ y: 0, duration: .42, ease: "back.out(1.8)" }}, {r(t_marke + .35)});',
          f'tl.to("#{sid}-m", {{ keyframes: [{{ rotation: -8, duration: .25 }}, {{ rotation: 6, duration: .25 }}, {{ rotation: -6, duration: .25 }}, {{ rotation: 0, duration: .25 }}] }}, {r(t_marke + .8)});',
          f'tl.fromTo("#{sid}-line", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .38, ease: "power3.out" }}, {r(t_zeile)});',
          f'tl.fromTo("#{sid}-tag", {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, {r(t_zeile + .5)});',
          f'tl.fromTo("#{sid}-btn", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .38, ease: "back.out(2.5)" }}, {r(t_knopf)});',
          f'tl.to("#{sid}-btn", {{ scale: 1.06, duration: .25, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {r(t_knopf + .6)});']
    sfx = [('whoosh_lang', start - .1, .25), ('boing_kurz', t_marke + .35, .2), ('pop', t_knopf, .3), ('ding', t_knopf + .6, .2)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def stempel(reel, sid, start, ende, zeilen, wort, t_stempel, label=None, farbe_stempel='var(--rot)', unter=None, t_unter=None, bg='var(--ice)'):
    """Mythos-Check: Behauptung erscheint (zeilen wie bei hook, mit t), dann knallt ein Stempel (z.B. FALSCH) darüber.
    zeilen: Liste dict(text, art='big'|'serif', groesse=110, t). Stempel-Farbe z.B. var(--rot) oder var(--steel)."""
    css = f'''#{sid}-w {{ position:absolute; left:70px; right:70px; top:470px; text-align:center; color:var(--navy); }}
#{sid}-w .big {{ display:block; line-height:1.12; }}
#{sid}-w .serif {{ display:block; color:var(--steel); line-height:1.15; margin-top:6px; }}
#{sid}-st {{ position:absolute; left:150px; right:150px; top:1180px; height:230px; border:16px solid {farbe_stempel}; border-radius:34px;
  display:flex; align-items:center; justify-content:center; font-weight:900; font-size:150px; letter-spacing:.04em; color:{farbe_stempel};
  background:rgba(255,255,255,.55); transform:rotate(-8deg); }}
#{sid}-u {{ position:absolute; left:60px; right:60px; top:1530px; text-align:center; font-size:96px; color:var(--navy); line-height:1.1; }}'''
    zt = ''.join(f'<div id="{sid}-z{i}" class="{"big" if z.get("art", "big") == "big" else "serif"}" style="font-size:{z.get("groesse", 110 if z.get("art", "big") == "big" else 120)}px">{z["text"]}</div>' for i, z in enumerate(zeilen))
    inhalt = (f'<div id="{sid}-lab" class="label top-label" style="color:var(--steel)">{label}</div>' if label else '') + \
        f'<div id="{sid}-w" data-layout-allow-overflow>{zt}</div><div id="{sid}-st" data-layout-allow-overflow>{wort}</div>' + \
        (f'<div id="{sid}-u" class="serif">{unter}</div>' if unter else '')
    js, sfx = [], []
    if label:
        js.append(f'tl.fromTo("#{sid}-lab", {{ opacity: 0, y: -24 }}, {{ opacity: 1, y: 0, duration: .3 }}, {r(start + .02)});')
    for i, z in enumerate(zeilen):
        t = r(z['t'])
        if z.get('art', 'big') == 'big':
            js.append(f'tl.fromTo("#{sid}-z{i}", {{ scale: 1.8, opacity: 0, filter: "blur(12px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: .28, ease: "back.out(2.2)" }}, {t});')
            sfx += [('whoosh', t - .08, .18), ('thump_klein', t, .25)]
        else:
            js.append(f'tl.fromTo("#{sid}-z{i}", {{ y: 70, opacity: 0, rotation: -5 }}, {{ y: 0, opacity: 1, rotation: 0, duration: .4, ease: "back.out(2.4)" }}, {t});')
            sfx.append(('pop', t, .25))
    ts = r(t_stempel)
    js.append(f'tl.fromTo("#{sid}-st", {{ scale: 3, opacity: 0, rotation: -25 }}, {{ scale: 1, opacity: 1, rotation: -8, duration: .2, ease: "power4.in" }}, {ts});')
    js.append(f'tl.fromTo("#{sid}-w", {{ x: 0, y: 0 }}, {{ keyframes: [{{ x: -22, y: 12, duration: .04 }}, {{ x: 18, y: -14, duration: .04 }}, {{ x: -10, y: 8, duration: .04 }}, {{ x: 0, y: 0, duration: .05 }}] }}, {r(ts + .2)});')
    js.append(f'tl.to("#{sid}-w", {{ opacity: .35, duration: .3 }}, {r(ts + .25)});')
    sfx += [('riser', ts - .4, .15), ('stamp', ts + .18, .6)]
    if unter:
        tu = r(t_unter if t_unter is not None else ts + .6)
        js.append(f'tl.fromTo("#{sid}-u", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .4, ease: "back.out(2.2)" }}, {tu});')
        sfx.append(('pop_tief', tu, .22))
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def liste(reel, sid, start, ende, titel_html, punkte, t_titel=None, bg='var(--navy)'):
    """Checkliste: Titel oben (HTML mit <span class="a"> und <span class="serif">), darunter 2 bis 4 Punkte,
    die nacheinander mit Häkchen erscheinen. punkte: Liste (text, t). Text kurz halten (höchstens rund 22 Zeichen pro Punkt)."""
    n = len(punkte)
    y0 = 760 if n <= 3 else 700
    gap = 230 if n <= 3 else 200
    css = f'''#{sid}-ti {{ position:absolute; left:60px; right:60px; top:290px; text-align:center; color:#fff; }}
#{sid}-ti .a {{ font-weight:900; font-size:104px; letter-spacing:-0.02em; line-height:1.15; display:block; }}
#{sid}-ti .serif {{ font-size:116px; color:var(--blue); display:block; line-height:1.15; margin-top:4px; }}
.{sid}-p {{ position:absolute; left:110px; right:80px; height:160px; display:flex; align-items:center; }}
.{sid}-box {{ width:118px; height:118px; border-radius:30px; border:9px solid var(--blue); flex:0 0 auto; position:relative; display:block; }}
.{sid}-box svg {{ position:absolute; left:6px; top:6px; width:88px; height:88px; }}
.{sid}-t {{ margin-left:44px; color:#fff; font-weight:700; font-size:68px; line-height:1.12; letter-spacing:-0.01em; }}'''
    rows = ''.join(f'''<div id="{sid}-p{i}" class="{sid}-p" style="top:{y0 + i * gap}px" data-layout-allow-overflow>
<div class="{sid}-box"><svg viewBox="0 0 100 100"><path id="{sid}-h{i}" d="M18 52 L42 76 L84 26" fill="none" stroke="#9fd3ee" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="{sid}-t">{txt}</div></div>''' for i, (txt, _) in enumerate(punkte))
    inhalt = f'<div id="{sid}-ti">{titel_html}</div>{rows}'
    tt = r(t_titel if t_titel is not None else start + .05)
    js = [f'tl.fromTo("#{sid}-ti", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .35, ease: "back.out(2)" }}, {tt});']
    sfx = [('whoosh_runter', tt - .05, .2)]
    for i, (_, t) in enumerate(punkte):
        t = r(t)
        js.append(f'tl.fromTo("#{sid}-p{i}", {{ x: -700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: .35, ease: "back.out(1.6)" }}, {t});')
        js.append(f'{{ const p = document.getElementById("{sid}-h{i}"); const L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; tl.to(p, {{ strokeDashoffset: 0, duration: .25, ease: "power2.out" }}, {r(t + .3)}); }}')
        sfx += [('whoosh', t - .05, .15, -.3), ('tick', t + .3, .3), ('pop_hoch', t + .32, .2)]
    reel.szene(sid, start, ende, bg, inhalt, css=css, js='\n'.join(js), sfx=sfx)


def schreiben(reel, ordner):
    import io, os
    os.makedirs(ordner, exist_ok=True)
    # encoding ausdruecklich: unter Windows waere der Standard cp1252, die Seite
    # erklaert sich aber als UTF-8, und jeder Umlaut wuerde zu U+FFFD.
    io.open(os.path.join(ordner, 'index.html'), 'w', encoding='utf-8', newline='').write(reel.bauen())
    json.dump(reel.sfx, io.open(os.path.join(ordner, 'sfx.json'), 'w', encoding='utf-8'), ensure_ascii=False)
