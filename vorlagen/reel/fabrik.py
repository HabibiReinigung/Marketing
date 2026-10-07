#!/usr/bin/env python3
"""Hilfsbefehle der Reel-Fabrik (Habibi Reinigung). Ablauf siehe FABRIK.md.

  python3 fabrik.py umgebung                      HyperFrames installieren, Browser finden, Umgebung prüfen
  python3 fabrik.py projekt <ordner>               Projektordner mit assets/ anlegen
  python3 fabrik.py phrasen <audio> [min_pause]    Sprechpausen finden -> Phrasen (JSON) + Lautstärke-Karte
  python3 fabrik.py straffen <audio> <phrasen.json> <ordner>
                                                   Pausen kürzen, Tempo 1.08, Lautheit -> <ordner>/stimme.wav, zeiten.json
  python3 fabrik.py render <ordner>                hyperframes check + render -> <ordner>/renders/video.mp4
  python3 fabrik.py bilder <ordner> <t1> <t2> ...  Einzelbilder (PNG) aus dem gerenderten Video zum Ansehen
  python3 fabrik.py fertig <ordner> <post_id> <ziel> [titel_s]
                                                   Ton mischen (Stimme + Effekte, keine Musik), Video + Ton
                                                   zusammenführen, Titelbild, Prüfungen -> <ziel>/<post_id>.mp4 und _titel.jpg
"""
import glob, json, os, shutil, subprocess, sys, wave

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
V0 = 0.15  # Stimme beginnt 0.15 s nach Videostart (wie in den Beispielen)
NODE = os.path.expanduser('~/reel')
HF_VERSION = '0.8.133'


def sh(cmd, **kw):
    print('$', cmd if isinstance(cmd, str) else ' '.join(cmd), flush=True)
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, **kw)


def browser():
    kand = sorted(glob.glob('/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell')) + \
        sorted(glob.glob('/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell'))
    return kand[-1] if kand else None


def env():
    e = dict(os.environ)
    b = browser()
    if b: e['HYPERFRAMES_BROWSER_PATH'] = b
    e['PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD'] = '1'
    return e


def umgebung():
    os.makedirs(NODE, exist_ok=True)
    if not os.path.exists(os.path.join(NODE, 'node_modules', 'hyperframes')):
        if not os.path.exists(os.path.join(NODE, 'package.json')):
            open(os.path.join(NODE, 'package.json'), 'w').write('{"name":"reel","private":true}')
        sh(['npm', 'i', '--prefix', NODE, f'hyperframes@{HF_VERSION}', '--no-audit', '--no-fund'], env=env())
    b = browser()
    print('Browser:', b or 'NICHT GEFUNDEN (ls /opt/pw-browsers)')
    print('ffmpeg:', shutil.which('ffmpeg') or 'FEHLT (apt-get install -y ffmpeg)')
    try:
        import numpy  # noqa
        print('numpy: ok')
    except ImportError:
        sh([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', 'numpy'])


def projekt(ordner):
    os.makedirs(ordner, exist_ok=True)
    ziel = os.path.join(ordner, 'assets')
    if os.path.exists(ziel): shutil.rmtree(ziel)
    shutil.copytree(os.path.join(HIER, 'assets'), ziel)
    print('Projekt bereit:', ordner)


def _pcm(src, sr=16000):
    tmp = src + f'.{sr}.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(sr), tmp], check=True)
    import numpy as np
    w = wave.open(tmp)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    return x, sr


def phrasen(src, min_pause=0.16):
    """Findet Sprechpausen. Gibt Phrasen (start, ende in s im Original) aus. Namen vergibst du danach selbst."""
    import numpy as np
    x, sr = _pcm(src)
    hop = int(0.01 * sr)
    db = np.array([10 * np.log10(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    ref = np.percentile(db[db > -80], 95) if np.any(db > -80) else -20
    still = db < ref - 30
    seg, an = [], None
    i = 0
    n = len(db)
    while i < n:
        if not still[i]:
            if an is None: an = i
            i += 1
            continue
        j = i
        while j < n and still[j]: j += 1
        if an is not None and (j - i) * 0.01 >= min_pause:
            seg.append([an, i]); an = None
        i = j
    if an is not None: seg.append([an, n])
    out = []
    for k, (a, b) in enumerate(seg):
        s = max(0.0, a * 0.01 - 0.04); e = min(len(x) / sr, b * 0.01 + 0.06)
        if e - s < 0.12: continue
        out.append({'name': f'X{k + 1}', 'start': round(s, 3), 'ende': round(e, 3)})
    print(json.dumps(out, indent=1))
    z = ''.join('@' if d > ref - 8 else '#' if d > ref - 16 else '+' if d > ref - 30 else '.' for d in db[::5])
    print('\nLautstärke (1 Zeichen = 0.05 s):')
    for i in range(0, len(z), 100):
        print(f'{i * 0.05:5.1f}s {z[i:i + 100]}')
    print(f'\nDauer {len(x) / sr:.2f} s, {len(out)} Phrasen. Tipp: Phrasen-Namen (P1, P2, ...) passend zum Skript vergeben, '
          'zu kurze Teile zusammenlegen, dann als Liste [[name, start, ende], ...] in phrasen.json speichern.')
    return out


def straffen_cmd(src, phr_json, ordner, tempo=1.08):
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


def render(ordner):
    hf = os.path.join(NODE, 'node_modules', '.bin', 'hyperframes')
    if not os.path.exists(hf): umgebung()
    sh(f'cd "{ordner}" && npx --prefix "{NODE}" hyperframes check', env=env())
    os.makedirs(os.path.join(ordner, 'renders'), exist_ok=True)
    sh(f'cd "{ordner}" && npx --prefix "{NODE}" hyperframes render -o renders/video.mp4 --fps 30 --quality delivery --quiet', env=env())
    print('Video:', os.path.join(ordner, 'renders', 'video.mp4'))


def bilder(ordner, zeiten):
    vid = os.path.join(ordner, 'renders', 'video.mp4')
    os.makedirs(os.path.join(ordner, 'bilder'), exist_ok=True)
    for t in zeiten:
        out = os.path.join(ordner, 'bilder', f'bild_{float(t):05.2f}.png')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(t), '-i', vid, '-frames:v', '1', '-vf', 'scale=540:960', out], check=True)
        print(out)


def _dauer(pfad):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', pfad], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def fertig(ordner, post_id, ziel, titel_s=None):
    from klang import mischen
    vid = os.path.join(ordner, 'renders', 'video.mp4')
    stimme = os.path.join(ordner, 'stimme.wav')
    sfx = json.load(open(os.path.join(ordner, 'sfx.json')))
    d = _dauer(vid)
    mix = os.path.join(ordner, 'mix.wav')
    mischen(stimme, sfx, d, V0, mix)
    os.makedirs(ziel, exist_ok=True)
    out = os.path.join(ziel, f'{post_id}.mp4')
    sh(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', vid, '-i', mix, '-map', '0:v:0', '-map', '1:a:0',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', '30',
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out])
    t = float(titel_s) if titel_s is not None else min(2.0, d / 3)
    titel = os.path.join(ziel, f'{post_id}_titel.jpg')
    sh(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(t), '-i', out, '-frames:v', '1', '-q:v', '2', titel])
    # Prüfungen
    fehler = []
    groesse = os.path.getsize(out)
    dd = _dauer(out)
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', out], capture_output=True, text=True)
    wh = r.stdout.strip()
    ra = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', out], capture_output=True, text=True)
    if groesse > 19_500_000: fehler.append(f'Datei zu gross ({groesse / 1e6:.1f} MB, höchstens 19.5 MB): crf erhöhen')
    if not (3 <= dd <= 60): fehler.append(f'Dauer {dd:.1f} s (erlaubt 3 bis 60 s)')
    if wh != '1080,1920': fehler.append(f'Auflösung {wh} statt 1080x1920')
    if 'aac' not in ra.stdout: fehler.append('Tonspur fehlt')
    lu = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    il = [l for l in lu.splitlines() if l.strip().startswith('I:')]
    print(f'Fertig: {out} ({groesse / 1e6:.1f} MB, {dd:.2f} s, {wh}), Titelbild {titel} bei {t:.2f} s')
    if il: print('Lautheit', il[-1].strip())
    if fehler:
        print('FEHLER:', ' | '.join(fehler)); sys.exit(2)
    print('Prüfungen OK')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    k = a[0]
    if k == 'umgebung': umgebung()
    elif k == 'projekt': projekt(a[1])
    elif k == 'phrasen': phrasen(a[1], float(a[2]) if len(a) > 2 else 0.16)
    elif k == 'straffen': straffen_cmd(a[1], a[2], a[3])
    elif k == 'render': render(a[1])
    elif k == 'bilder': bilder(a[1], a[2:])
    elif k == 'fertig': fertig(a[1], a[2], a[3], a[4] if len(a) > 4 else None)
    else: print(__doc__); sys.exit(1)
