#!/usr/bin/env python3
"""Reel: Desinfektionsmittel wirkt nicht ohne Einwirkzeit (IG-2026-10-12-r1)"""
import json, sys, os
sys.path.insert(0, r'C:\Users\habib\Documents\Habibi-Repo\vorlagen\reel')
from szenen import *

T = json.load(open(sys.argv[1])); ORDNER = sys.argv[2]
V0 = 0.15
A = lambda k, o=0.0: V0 + T[k][0] + o
E = lambda k, o=0.0: V0 + T[k][1] + o
END = E('P7') + 0.85

reel = Reel('Desinfektion braucht Einwirkzeit', END)

# 1 Haken: die steile Behauptung, sofort im Bild
hook(reel, 's1', 0, A('P2', -.08), label='Praxis und Büro', zeilen=[
    dict(text='Dein Desinfektionsmittel', groesse=96, t=A('P1')),
    dict(text='wirkt gar nicht.', art='serif', groesse=150, t=A('P1', .75))])

# 2 Der Grund, als Mythos gestempelt
stempel(reel, 's2', A('P2', -.08), A('P3', -.1), label='So macht es fast jeder',
        zeilen=[dict(text='Sprühen.', groesse=120, t=A('P2')),
                dict(text='Sofort trocken wischen.', groesse=108, t=A('P2', .5))],
        wort='FALSCH', t_stempel=A('P2', 1.25),
        unter='Dann desinfiziert gar nichts.', t_unter=A('P2', 1.6))

# 3 Die Auflösung als ein Wort
punch(reel, 's3', A('P3', -.1), A('P4', -.1), wort='EINWIRKZEIT',
      t_wort=A('P3', .55), klein='Desinfektion braucht', t_klein=A('P3', .1))

# 4 Was man konkret tun muss
maskottchen_tipp(reel, 's4', A('P4', -.1), A('P6', -.1), karten=[
    ('<div class="a">Die Fläche muss</div><div class="a"><span class="serif">nass bleiben.</span></div>', A('P4', .2)),
    ('<div class="b">Wie lange?</div><div class="b"><span class="serif">Steht auf der Flasche.</span></div>', A('P5'))])

# 5 Abschluss
abschluss(reel, 's5', A('P6', -.1), END, t_marke=A('P6'), t_zeile=A('P7', .1), t_knopf=A('P7', 1.4))

schreiben(reel, ORDNER)
print('Dauer', round(END, 2))
