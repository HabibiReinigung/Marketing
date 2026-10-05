#!/usr/bin/env python3
"""Reel: Preis auf Anfrage? Nicht bei uns. (IG-2026-10-08-2)"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from szenen import *
T = json.load(open(sys.argv[1]))['preis']; ORDNER = sys.argv[2]
V0 = 0.15
A = lambda k, o=0.0: V0 + T[k][0] + o
E = lambda k: V0 + T[k][1]
END = E('P12') + 0.85
reel = Reel('Preis auf Anfrage? Nicht bei uns.', END)
hook(reel, 's1', 0, A('P2', -.05), label='Preis-Check', zeilen=[
    dict(text='Was kostet', groesse=140, t=A('P1')),
    dict(text='Büroreinigung', groesse=110, t=A('P1', 1.0)),
    dict(text='in Chur?', art='serif', groesse=190, farbe='#fff', t=A('P1', 1.75))])
durchstreichen(reel, 's2', A('P2', -.05), A('P4', -.1), karte='«Preis auf Anfrage»', t_karte=A('P2', -.05), t_strich=A('P2', 1.0), unter='super hilfreich.', t_unter=A('P3'), label='So kennt man es')
punch(reel, 's3', A('P4', -.1), A('P5', -.1), wort='DA.', t_wort=A('P4', 1.15), klein='Bei uns steht der Preis', t_klein=A('P4'))
preis(reel, 's4', A('P5', -.1), A('P7', -.1), wert=650, t_zahl=A('P5', .5), stempel='ALLES INBEGRIFFEN', t_stempel=A('P6', .05), oben='Büros ab CHF', unten='pro Monat')
maskottchen_tipp(reel, 's5', A('P7', -.1), A('P9', -.1), label='So arbeiten wir', karten=[
    ('<div class="a">Fester</div><div class="a">Monatspreis.</div>', A('P7', .15)),
    ('<div class="a">Keine</div><div class="b"><span class="serif">Mindestlaufzeit.</span></div>', A('P8'))])
zone(reel, 's6', A('P9', -.1), A('P11', -.1), t_ring=A('P9', .6), abzeichen='ohne Zuschlag', t_abz=A('P10'), titel_html='<span class="a">Bis 5 km</span><span class="serif">ab Chur</span>')
abschluss(reel, 's7', A('P11', -.1), END, t_marke=A('P11'), t_zeile=A('P12', .2), t_knopf=A('P12', 3.0))
schreiben(reel, ORDNER)
print('Dauer', round(END, 2))
