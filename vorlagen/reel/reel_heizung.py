#!/usr/bin/env python3
"""Reel: Heizung läuft wieder? (IG-2026-10-11-2)"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from szenen import *
T = json.load(open(sys.argv[1]))['heizung']; ORDNER = sys.argv[2]
V0 = 0.15
A = lambda k, o=0.0: V0 + T[k][0] + o
E = lambda k: V0 + T[k][1]
END = E('H7') + 0.85
reel = Reel('Heizung läuft wieder?', END)
heizung(reel, 's1', 0, A('H2', -.05), 'waerme', label='Oktober in Chur', t_aktion=A('H1', .2), zeilen=[
    dict(text='Heizung', t=A('H1')), dict(text='läuft wieder?', art='serif', t=A('H1', .45))])
heizung(reel, 's2', A('H2', -.05), A('H3', -.1), 'staub', t_aktion=A('H2', .3), zeilen=[
    dict(text='Staub vom', t=A('H2', .9)), dict(text='ganzen Sommer', t=A('H2', 1.6)), dict(text='wirbelt durchs Büro.', art='serif', t=A('H2', 2.4))])
maskottchen_tipp(reel, 's3', A('H3', -.1), A('H5', -.1), karten=[
    ('<div class="a">Jetzt</div><div class="a">abstauben!</div>', A('H3', .25)),
    ('<div class="b">Auch</div><div class="b"><span class="serif">zwischen den Rippen.</span></div>', A('H4'))])
heizung(reel, 's4', A('H5', -.1), A('H6', -.1), 'buerste', label='So geht es', t_aktion=A('H5', .15), zeilen=[
    dict(text='Von oben', t=A('H5')), dict(text='nach unten.', art='serif', t=A('H5', .7))])
abschluss(reel, 's5', A('H6', -.1), END, t_marke=A('H6'), t_zeile=A('H7', .1), t_knopf=A('H7', 1.0))
schreiben(reel, ORDNER)
print('Dauer', round(END, 2))
