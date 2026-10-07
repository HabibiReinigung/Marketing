#!/usr/bin/env python3
"""Reel: Desinfektion braucht 30 Sekunden (IG-2026-10-12-r1, Fassung 2)

Fassung 1 nannte die Zeit nicht («steht auf der Flasche») und hatte damit kein
Learning. Fassung 2 nennt die Zahl und zeigt sie als Zaehler im Bild.
"""
import json, sys, os
sys.path.insert(0, r'C:\Users\habib\Documents\Habibi-Repo\vorlagen\reel')
from szenen import *

T = json.load(open(sys.argv[1])); ORDNER = sys.argv[2]
V0 = 0.15
A = lambda k, o=0.0: V0 + T[k][0] + o
E = lambda k, o=0.0: V0 + T[k][1] + o
END = E('P6') + 0.85

reel = Reel('Desinfektion braucht 30 Sekunden', END)

# 1 Haken
hook(reel, 's1', 0, A('P2', -.08), label='Praxis und Büro', zeilen=[
    dict(text='Dein Desinfektionsmittel', groesse=92, t=A('P1')),
    dict(text='wirkt gar nicht.', art='serif', groesse=144, t=A('P1', .7))])

# 2 Der Fehler, gestempelt
stempel(reel, 's2', A('P2', -.08), A('P3', -.1), label='So macht es fast jeder',
        zeilen=[dict(text='Sprühen.', groesse=116, t=A('P2')),
                dict(text='Sofort wegwischen.', groesse=104, t=A('P2', .45))],
        wort='FALSCH', t_stempel=A('P2', 1.15),
        unter='Dann desinfiziert gar nichts.', t_unter=A('P2', 1.5))

# 3 Die Zahl, die haengen bleiben soll: Spruehflasche, nasse Flaeche, Zaehler
spruehen(reel, 's3', A('P3', -.1), A('P4', -.1), label='So wirkt es wirklich',
         zeilen=[dict(text='Es braucht', groesse=86, t=A('P3')),
                 dict(text='mindestens', art='serif', groesse=112, t=A('P3', .35))],
         sekunden=30, t_spray=A('P3', .5), t_zaehler=A('P3', 1.1),
         unten='Manche Mittel sogar 60.', t_unten=A('P3', 2.3))

# 4 Was das praktisch heisst
maskottchen_tipp(reel, 's4', A('P4', -.1), A('P6', -.1), karten=[
    ('<div class="a">So lange muss sie</div><div class="a"><span class="serif">nass bleiben.</span></div>', A('P4', .15)),
    ('<div class="b">Von selbst trocken?</div><div class="b"><span class="serif">Dann ist sie bereit.</span></div>', A('P5', .1))])

# 5 Abschluss, bleibt immer gleich (Wiedererkennung)
abschluss(reel, 's5', A('P6', -.1), END, t_marke=A('P6'), t_zeile=A('P6', .8), t_knopf=A('P6', 2.1))

schreiben(reel, ORDNER)
print('Dauer', round(END, 2))
