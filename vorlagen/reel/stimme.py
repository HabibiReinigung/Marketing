#!/usr/bin/env python3
"""Stimme straffen: Pausen kürzen, Tempo leicht erhöhen, Lautheit angleichen.

Aufruf (aus Python):
    from stimme import straffen
    times = straffen('roh.mp3', 'stimme.wav', phrasen, pausen)
phrasen: Liste (name, start_s, ende_s) im Original
pausen:  dict name -> Pause in Sekunden VOR dieser Phrase (Standard 0.15)
Rückgabe: dict name -> [start, ende] in Sekunden im fertigen File.
"""
import subprocess, wave, json
import numpy as np

SR = 48000
TEMPO = 1.08


def _stille_karte(x, sr, schwelle_db=-42.0, hop=0.01):
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
        letzter = None
        for o, nn, laenge in karte:
            if o <= t_roh < o + laenge * tempo:
                return nn + (t_roh - o) / tempo
            if o <= t_roh:
                letzter = (o, nn, laenge)
            elif o > t_roh:
                # Der Zeitpunkt lag in einer gekuerzten Pause: an den Anfang
                # des naechsten behaltenen Abschnitts setzen.
                return nn
        if letzter:
            return letzter[1] + letzter[2]
        return 0.0

    zeiten = {}
    for (name, aa, bb) in phrasen:
        zeiten[name] = [round(um(aa), 3), round(um(bb), 3)]
    return zeiten, karte


def energie(src, schritt=0.05):
    """Text-Karte der Lautstärke, um Phrasengrenzen von Hand zu bestimmen."""
    tmp = src + '.16k.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-ar', '16000', tmp], check=True)
    w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    hop = int(schritt * 16000)
    db = [10 * np.log10(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)]
    z = ''.join('@' if d > -22 else '#' if d > -30 else '+' if d > -40 else '.' for d in db)
    return '\n'.join(f'{i * schritt:5.1f}s {z[i:i + 100]}' for i in range(0, len(z), 100))
