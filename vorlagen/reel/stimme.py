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


def straffen(src, out, phrasen, pausen=None, tempo=TEMPO):
    pausen = pausen or {}
    tmp = out + '.roh.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(SR), tmp], check=True)
    w = wave.open(tmp)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    teile, t, zeiten = [], 0.0, {}
    fade = int(0.008 * SR)
    for i, (name, a, b) in enumerate(phrasen):
        if i > 0:
            g = np.zeros(int(pausen.get(name, 0.15) * SR), dtype=np.float32)
            teile.append(g); t += len(g) / SR
        seg = x[int(a * SR):int(b * SR)].copy()
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        zeiten[name] = [t, t + len(seg) / SR]
        teile.append(seg); t += len(seg) / SR
    y = np.concatenate(teile)
    w2 = wave.open(tmp + '2.wav', 'wb'); w2.setnchannels(1); w2.setsampwidth(2); w2.setframerate(SR)
    w2.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w2.close()
    # Kompressor bewusst sanft (ratio 1.6): die Regeln verlangen einen Lautstaerke-Bogen
    # ueber das Video. Ein harter Kompressor plus loudnorm im Einzeldurchlauf buegelt
    # alles platt (gemessen LRA 1.4 LU am 07.10.2026) und klingt robotisch.
    vor = f'atempo={tempo},highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=2.5,acompressor=threshold=-14dB:ratio=1.6:attack=12:release=160'
    ziel = 'I=-14:TP=-1.5:LRA=11'
    # Durchlauf 1: messen
    mess = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp + '2.wav', '-af',
                           vor + f',loudnorm={ziel}:print_format=json', '-f', 'null', '-'],
                          capture_output=True, text=True, errors='replace').stderr
    linear = ''
    try:
        roh = mess[mess.rindex('{'):mess.rindex('}') + 1]
        m = json.loads(roh)
        linear = (':measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:linear=true'
                  % (m['input_i'], m['input_tp'], m['input_lra'], m['input_thresh']))
    except Exception:
        pass   # ohne Messwerte faellt es auf den Einzeldurchlauf zurueck
    # Durchlauf 2: anwenden, linear verstaerken statt dynamisch nachregeln
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', tmp + '2.wav',
                    '-af', vor + f',loudnorm={ziel}{linear}', '-ar', str(SR), '-ac', '1', out], check=True)
    return {k: [round(v[0] / tempo, 3), round(v[1] / tempo, 3)] for k, v in zeiten.items()}


def energie(src, schritt=0.05):
    """Text-Karte der Lautstärke, um Phrasengrenzen von Hand zu bestimmen."""
    tmp = src + '.16k.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-ar', '16000', tmp], check=True)
    w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    hop = int(schritt * 16000)
    db = [10 * np.log10(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)]
    z = ''.join('@' if d > -22 else '#' if d > -30 else '+' if d > -40 else '.' for d in db)
    return '\n'.join(f'{i * schritt:5.1f}s {z[i:i + 100]}' for i in range(0, len(z), 100))
