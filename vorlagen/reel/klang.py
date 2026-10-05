#!/usr/bin/env python3
"""Soundeffekte (selbst erzeugt, lizenzfrei) und Endmischung: Stimme + Effekte, KEINE Musik."""
import wave
import numpy as np

SR = 48000
_rng = np.random.default_rng(42)


def _env(n, tau):
    return np.exp(-(np.arange(n) / SR) / tau)


def _band(n, lo, hi):
    x = _rng.standard_normal(n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)


def _sweep(n, f0, f1, q=0.25):
    out = np.zeros(n); c = 960
    for s in range(0, n, c):
        fc = f0 * (f1 / f0) ** (s / max(1, n - 1))
        seg = _band(c, fc * (1 - q), fc * (1 + q))
        out[s:s + c] = seg[:len(out[s:s + c])]
    return out


def whoosh(d=0.3, f0=400, f1=3500):
    n = int(d * SR); return _sweep(n, f0, f1) * np.sin(np.linspace(0, np.pi, n)) ** 2


def thump(d=0.25, f0=120, f1=45):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.07)


def impact(d=1.2):
    n = int(d * SR); t = np.arange(n) / SR
    f = 90 * (35 / 90) ** (t / 0.5)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.35)
    return np.tanh(1.6 * (sub + 0.55 * _band(n, 200, 6000) * _env(n, 0.05)))


def pop(d=0.09, f0=900, f1=1900):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 + (f1 - f0) * (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.018)


def tick():
    n = int(0.02 * SR); return _band(n, 2500, 9000) * _env(n, 0.003)


def boing(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR
    f = 180 + 260 * np.sin(np.pi * np.clip(t / 0.22, 0, 1)) * np.exp(-t * 3) + 25 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.18)


def squeak(d=0.6, f0=900, f1=1700):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / d) + 40 * np.sin(2 * np.pi * 23 * t)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35
    return (tone + _band(n, 1500, 7000) * 0.5) * np.sin(np.linspace(0, np.pi, n)) ** 1.5


def smear(d=0.42):
    n = int(d * SR); return _sweep(n, 700, 1400, 0.4) * np.sin(np.linspace(0, np.pi, n)) ** 2


def scratch(d=0.35):
    """Filzstift-Strich (Durchstreichen)."""
    n = int(d * SR); t = np.arange(n) / SR
    am = 0.6 + 0.4 * np.sin(2 * np.pi * 38 * t)
    return _band(n, 1800, 8000) * am * np.sin(np.linspace(0, np.pi, n)) ** 0.7


def chime(freqs=(1568, 2093, 2637, 3136), gap=0.06):
    out = np.zeros(int(1.4 * SR))
    for i, f in enumerate(freqs):
        n = int(1.2 * SR); t = np.arange(n) / SR
        s = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.01 * t)) * _env(n, 0.35)
        st = int(i * gap * SR); out[st:st + n] += s[:len(out) - st]
    return out / np.abs(out).max()


def ding():
    return chime((1318.5, 1975.5), 0.09)


def riser(d=0.45):
    n = int(d * SR); return _sweep(n, 300, 6000, 0.3) * np.linspace(0, 1, n) ** 2


def stamp():
    return np.tanh(1.4 * (thump(0.3, 160, 50) + 0.4 * _band(int(0.3 * SR), 300, 3000) * _env(int(0.3 * SR), 0.03)))


EFFEKTE = {
    'whoosh': lambda: whoosh(), 'whoosh_lang': lambda: whoosh(0.35, 300, 2500), 'whoosh_hoch': lambda: whoosh(0.3, 1200, 5000),
    'whoosh_runter': lambda: whoosh(0.25, 2000, 500), 'thump': lambda: thump(), 'thump_klein': lambda: thump(0.2, 140, 60),
    'impact': impact, 'pop': lambda: pop(), 'pop_tief': lambda: pop(0.1, 600, 1300), 'pop_hoch': lambda: pop(0.1, 900, 2000),
    'tick': tick, 'boing': lambda: boing(), 'boing_kurz': lambda: boing(0.4), 'squeak': lambda: squeak(), 'smear': lambda: smear(),
    'scratch': lambda: scratch(), 'chime': lambda: chime(), 'glitzer': lambda: chime((2637, 3136, 3951), 0.05), 'ding': ding,
    'riser': lambda: riser(), 'stamp': stamp,
}


def mischen(stimme_wav, ereignisse, dauer, v0, out):
    """ereignisse: Liste (name, zeit_s, lautstaerke[, pan])."""
    N = int(dauer * SR)
    mix = np.zeros((N, 2))
    for e in ereignisse:
        name, t, g = e[0], e[1], e[2]; pan = e[3] if len(e) > 3 else 0.0
        sig = EFFEKTE[name](); i = int(max(0, t) * SR)
        if i >= N: continue
        sig = sig[:N - i]; l = np.cos((pan + 1) * np.pi / 4) * 1.414; r = np.sin((pan + 1) * np.pi / 4) * 1.414
        mix[i:i + len(sig), 0] += sig * g * l; mix[i:i + len(sig), 1] += sig * g * r
    w = wave.open(stimme_wav); assert w.getframerate() == SR
    vx = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    voice = np.zeros(N); i0 = int(v0 * SR); n = min(len(vx), N - i0); voice[i0:i0 + n] = vx[:n]
    k = int(0.03 * SR); env = np.convolve(np.abs(voice), np.ones(k) / k, mode='same')
    duck = 1 - 0.35 * np.clip(env * 6, 0, 1)
    out_m = mix * duck[:, None] * 0.9 + voice[:, None]
    peak = np.abs(out_m).max()
    if peak > 0.93: out_m = out_m / peak * 0.93
    pcm = (np.clip(out_m, -1, 1) * 32767).astype(np.int16)
    with wave.open(out, 'wb') as o:
        o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes(pcm.tobytes())
