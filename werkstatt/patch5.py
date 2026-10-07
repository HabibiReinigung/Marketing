# -*- coding: utf-8 -*-
"""Zwei Mängel aus der Rückmeldung vom 07.10.2026 (vierte Runde):
1. Pausen waren zu lang. Jetzt werden sie im ganzen Stück gekürzt, nicht nur
   zwischen den Phrasen. Dazu entsteht eine Zeitkarte, damit die Wort-Zeitstempel
   weiterhin stimmen.
2. Es gab Momente ohne Bewegung im Bild. Jetzt laeuft hinter jeder Szene eine
   ruhige Bewegung, und bei `enthuellen` bleibt nie eine leere Buehne stehen.
"""
import io

R = r'C:\Users\habib\Documents\Habibi-Repo\vorlagen\reel'

# ================================================================ 1. stimme.py
p = R + r'\stimme.py'
s = io.open(p, encoding='utf-8').read()
a = s.index('def straffen(')
b = s.index('def energie(')
NEU = '''def _stille_karte(x, sr, schwelle_db=-42.0, hop=0.01):
    """Pro Zeitfenster: ist hier Stille?"""
    import numpy as np
    n = int(hop * sr)
    if n < 1:
        n = 1
    anzahl = len(x) // n
    db = []
    for i in range(anzahl):
        teil = x[i * n:(i + 1) * n]
        db.append(10 * np.log10(float(np.mean(teil ** 2)) + 1e-12))
    return [d < schwelle_db for d in db], n


def straffen(src, out, phrasen, pausen=None, tempo=TEMPO, max_pause=0.10):
    """Pausen im ganzen Stueck auf max_pause kuerzen, Tempo anheben, Lautheit angleichen.

    Rueckgabe: (zeiten, karte)
      zeiten: name -> [start, ende] im fertigen File
      karte:  Liste [orig_start, neu_start, laenge] der behaltenen Abschnitte,
              alle Werte im fertigen File (also schon durch tempo geteilt).
              Damit laesst sich jeder Zeitpunkt der Rohaufnahme umrechnen.
    """
    tmp = out + '.roh.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src,
                    '-ac', '1', '-ar', str(SR), tmp], check=True)
    w = wave.open(tmp)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    w.close()

    still, n = _stille_karte(x, SR)
    max_fenster = max(1, int(max_pause / 0.01))
    behalten = []            # (von, bis) in Fenstern
    i, F = 0, len(still)
    while i < F:
        if not still[i]:
            j = i
            while j < F and not still[j]:
                j += 1
            behalten.append((i, j))
            i = j
        else:
            j = i
            while j < F and still[j]:
                j += 1
            behalten.append((i, min(j, i + max_fenster)))   # Pause kuerzen
            i = j

    teile, karte, neu = [], [], 0.0
    fade = int(0.006 * SR)
    for (v, bis) in behalten:
        a0, b0 = v * n, bis * n
        seg = x[a0:b0]
        if len(seg) < 2:
            continue
        if len(seg) > 2 * fade:
            seg = seg.copy()
            seg[:fade] *= np.linspace(0, 1, fade)
            seg[-fade:] *= np.linspace(1, 0, fade)
        karte.append([a0 / SR, neu, len(seg) / SR])
        teile.append(seg)
        neu += len(seg) / SR
    y = np.concatenate(teile) if teile else x

    w2 = wave.open(tmp + '2.wav', 'wb')
    w2.setnchannels(1); w2.setsampwidth(2); w2.setframerate(SR)
    w2.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w2.close()

    vor = f'atempo={tempo},highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=2.5,acompressor=threshold=-14dB:ratio=1.6:attack=12:release=160'
    ziel = 'I=-14:TP=-1.5:LRA=11'
    mess = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp + '2.wav', '-af',
                           vor + f',loudnorm={ziel}:print_format=json', '-f', 'null', '-'],
                          capture_output=True, text=True, errors='replace').stderr
    linear = ''
    try:
        m = json.loads(mess[mess.rindex('{'):mess.rindex('}') + 1])
        linear = (':measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:linear=true'
                  % (m['input_i'], m['input_tp'], m['input_lra'], m['input_thresh']))
    except Exception:
        pass
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', tmp + '2.wav',
                    '-af', vor + f',loudnorm={ziel}{linear}', '-ar', str(SR), '-ac', '1', out], check=True)

    karte = [[k[0], k[1] / tempo, k[2] / tempo] for k in karte]

    def um(t_roh):
        for o, nn, laenge in karte:
            if o <= t_roh < o + laenge * tempo:
                return nn + (t_roh - o) / tempo
        return karte[-1][1] + karte[-1][2] if karte else 0.0

    zeiten = {}
    for (name, aa, bb) in phrasen:
        zeiten[name] = [round(um(aa), 3), round(um(bb), 3)]
    return zeiten, karte


'''
s = s[:a] + NEU + s[b:]
if 'import json' not in s.split('\n')[10]:
    s = s.replace('import subprocess, wave, json', 'import subprocess, wave, json')
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# ================================================================ 2. fabrik.py
p = R + r'\fabrik.py'
s = io.open(p, encoding='utf-8').read()
a = s.index('def straffen_cmd(')
b = s.index('def render(')
NEU = '''def straffen_cmd(src, phr_json, ordner, tempo=1.08):
    from stimme import straffen
    phrasen = [tuple(x) for x in json.load(open(phr_json, encoding='utf-8'))]
    os.makedirs(ordner, exist_ok=True)
    zeiten, karte = straffen(src, os.path.join(ordner, 'stimme.wav'), phrasen, tempo=tempo)
    with open(os.path.join(ordner, 'zeiten.json'), 'w', encoding='utf-8') as fh:
        json.dump(zeiten, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(ordner, 'karte.json'), 'w', encoding='utf-8') as fh:
        json.dump(karte, fh)
    laenge = max(v[1] for v in zeiten.values())
    print('Stimme: %.2f s. Zeiten und Zeitkarte in %s.' % (laenge, ordner))


'''
s = s[:a] + NEU + s[b:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# ================================================================ 3. szenen.py
p = R + r'\szenen.py'
s = io.open(p, encoding='utf-8').read()

# 3a. Dauerbewegung hinter jeder Szene
alt = '<div id="root" data-composition-id="main" data-start="0" data-duration="{self.dauer}" data-width="1080" data-height="1920">'
neu = ('<div id="root" data-composition-id="main" data-start="0" data-duration="{self.dauer}" data-width="1080" data-height="1920">\\n'
       '<div id="leben" data-layout-allow-overflow><i></i><i></i><i></i><i></i><i></i></div>')
assert s.count(alt) == 1
s = s.replace(alt, neu)

alt2 = 'self.html, self.css, self.js, self.sfx = [], [BASIS_CSS], [BASIS_JS], []'
neu2 = ('self.html, self.css, self.js, self.sfx = [], [BASIS_CSS, LEBEN_CSS], [BASIS_JS], []\n'
        '        # Hinter allen Szenen laeuft eine ruhige Bewegung, damit nie ein Bild stillsteht.\n'
        '        self.js.append(LEBEN_JS % {\'d\': r(self.dauer)})')
assert s.count(alt2) == 1
s = s.replace(alt2, neu2)

# Konstanten direkt vor der Reel-Klasse einfuegen
LEBEN = '''
LEBEN_CSS = """
#leben { position:absolute; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
#leben i { position:absolute; display:block; border-radius:50%; background:radial-gradient(circle at 35% 35%, rgba(159,211,238,.22), rgba(159,211,238,0) 70%); }
.clip { z-index:1; }
"""

LEBEN_JS = """// Dauerbewegung: fuenf weiche Formen ziehen langsam durch das Bild.
(() => {
  const n = document.getElementById('leben');
  const gr = [520, 380, 640, 300, 460];
  for (let i = 0; i < 5; i++) {
    const e = n.children[i];
    e.style.width = gr[i] + 'px'; e.style.height = gr[i] + 'px';
    e.style.left = (-200 + rnd() * 900) + 'px';
    e.style.top = (-150 + rnd() * 1700) + 'px';
    tl.fromTo(e, { x: -120 + rnd() * 60, y: 0, scale: .9 },
      { x: 120 + rnd() * 80, y: -140 + rnd() * 280, scale: 1.12, duration: %(d)s, ease: 'none' }, 0);
  }
})();
"""

'''
anker = '\nclass Reel:'
assert s.count(anker) == 1
s = s.replace(anker, LEBEN + '\nclass Reel:')

# 3b. enthuellen: Buehne nie leer, Gegenstand bleibt bis der naechste da ist
alt3 = """        if i + 1 < len(punkte):
            js.append(f'tl.to("#{sid}-d{i}", {{ opacity: 0, filter: "blur(28px)", duration: .18 }}, {r(punkte[i + 1]["t"] - .34)});')"""
neu3 = """        if i + 1 < len(punkte):
            # Erst ausblenden, wenn der naechste schon einblendet: nie eine leere Buehne.
            js.append(f'tl.to("#{sid}-d{i}", {{ opacity: 0, filter: "blur(26px)", duration: .20 }}, {r(punkte[i + 1]["t"] - .16)});')
        # Der Gegenstand atmet leicht, solange er steht.
        js.append(f'tl.to("#{sid}-d{i}", {{ y: -14, duration: 1.6, yoyo: true, repeat: -1, ease: "sine.inOut" }}, {r(t + .4)});')"""
assert s.count(alt3) == 1
s = s.replace(alt3, neu3)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('stimme.py, fabrik.py und szenen.py angepasst.')
