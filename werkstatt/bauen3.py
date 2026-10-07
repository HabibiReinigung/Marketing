# -*- coding: utf-8 -*-
"""Baut drei Reels in einem Durchgang.

Neu: die Phrasen werden den Saetzen automatisch zugeordnet. Bisher habe ich das
von Hand gemacht, was pro Video einen eigenen Durchgang kostete.
"""
import io, json, os, subprocess, sys, urllib.request

W = r'C:\Users\habib\Documents\Habibi-Repo'
R = W + r'\vorlagen\reel'
PY = sys.executable
FFB = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages'
                         r'\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin')
ND = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages'
                        r'\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64')
os.environ['PATH'] = ND + os.pathsep + FFB + os.pathsep + os.environ['PATH']
os.environ['HYPERFRAMES_BROWSER_PATH'] = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
sys.path.insert(0, R)

B = 'https://storage.googleapis.com/xi-backend/database/workspace/4095d2d2f32842c780c3296604a2dabb/content_generation/'
Q = ('?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=xi-backend-prod%40xi-labs.iam.gserviceaccount.com'
     '%2F20261007%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20261007T{z}Z&X-Goog-Expires=7200'
     '&X-Goog-SignedHeaders=host&X-Goog-Signature={s}')

AUDIO = {
 'IG-2026-10-14-r1': ('SQVXdxWf1N8JZr50AnIs/CF0tLiEXPVgrUP41FWEf', '123652', '242599dce072a030e3a998e653e3383a743bb0111a878f99b5371e20c6190f2ed660b361ecc3d9a84947cfe22c6b0523b65a474ef0dfdd99d7d39e2d0351fe55deaaf8466c580c92efa6647914aa16851cf7c48efb74a098d8f2a7d5ece6900e32ef8990584d35cba3360607b95981f79c1749000a43d6a36e9c58233e834237a7c76fedef4e9620bdfb85f11b461140c1e6960f35c65cf0025bb450a3dd16ca9ea7c76360225b127cd282aa6812f8bea3be276baca3c7c683b801cd42dfc95e6a775b7dd2db76036a5a429aea0350d021617da0581bba698de6fa49f188c4f0239b377feaf30788122bbfd58ff537f9c4f1f70866355a4a59ccf4a9b714a4a8'),
 'IG-2026-10-16-r1': ('bkdLA9ecCD5ODNojRdNY/bvXqqEeuqWiRdVSG9D4E', '123703', '5be71e32905e0c44dee03f1aaf5ac0d95f82971841ffcce2acf225aeeb9a968aea3cbef493bb4ff3922404d76095003ce7e3752ea9beaac2ee535071e21a791405f0b098001964fc17bdbae6975a0d697cef7b99443a11612f4bcab1ed35207049e24ae1a4235d083a83eb35601e9c4b34f4822d275b8fd8e99c149729ba233380371758e9f101c5dce07fd7c62987db48b6b6a8a0df39294097e2d081e2e30b0c511a356195564b53e8e2476a473526727c252f7eedeb19678a8fed2176153e7656b2e0f1a69f9fc51a7767f2e60ee36ca519e6496dc694e206e73e993eb7a4b0b318c309c5c0625063abf42a860de37ff454e4ed12c3e255ba38baa251e980'),
 'IG-2026-10-18-r1': ('uMP0UnMSaS9RmPRXPmg3/lDuAVnX7IrnZD7Fnt3jJ', '123720', '259d7632efb697432b927c95b4b20632479b5fe3452b181e4a35b95fa7aaa1c09c00ce05eb87642567301adea12357e4f197aefcf127aa10b54d4c3aa263291b376b65d1c91c59e235b4db75058f7d023fbb530a1cc6bfe106db31e24c2b4992f8d22e75f5b7d9083fc9f6d36571cbeb2d5977114532e0c0b98c0c146d76cc9d2a66440c2eb4aef875bc5251b1d938d6eb30350d152df03a0463f93ab63df88b3f62a3c78138bba9bfe91e34e9416c7b890381e7c7283dbe13ed1a6704e7bdd5780142d5415183fc88db7d888afdbd7c4c205c1749411f18a662cc8a8c0cf9176f7c35a6bd44452c060db8a58846f8a0061783d24a97b479dbd8a0fa6f98be60'),
}

# Saetze je Reel: nur fuer die automatische Zuordnung, Laenge entscheidet
SAETZE = {
 'IG-2026-10-14-r1': ["Drei Stellen im Büro putzt fast niemand.",
   "Und genau die fasst ihr am häufigsten an!",
   "Nummer eins: der Lichtschalter.", "Nummer zwei: die Türklinke.",
   "Nummer drei: die Abtropfschale der Kaffeemaschine!",
   "Einmal am Tag feucht abwischen, zehn Sekunden pro Raum.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
 'IG-2026-10-16-r1': ["Euer Büro liegt ausserhalb von Chur?",
   "Dann kommt jetzt der Aufschlag. Kennt man ja.",
   "Bei uns: bis fünf Kilometer ab Chur kein Zuschlag!",
   "Danach fünfzehn Franken pro Einsatz. Weiter draussen fünfunddreissig.",
   "Mehr kommt nicht dazu. Fester Monatspreis, keine Mindestlaufzeit.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
 'IG-2026-10-18-r1': ["Du benutzt nur ein Viertel von deinem Putztuch.",
   "Der Rest ist noch sauber, und du spülst trotzdem aus!",
   "Zweimal falten gibt vier Lagen. Vorne und hinten sind das acht saubere Flächen!",
   "Ist eine Seite grau: umklappen statt auswaschen.",
   "Ein Tuch reicht so für acht Räume.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
}


def zuordnen(stuecke, saetze):
    """Erkannte Sprechstuecke auf die Saetze verteilen, nach Anteil an der Textlaenge.

    Die Stuecke kommen in Lesereihenfolge. Fuer jede Satzgrenze wird das Stueck
    gesucht, dessen Ende dem erwarteten Zeitanteil am naechsten liegt.
    """
    n, m = len(stuecke), len(saetze)
    if n < m:
        raise SystemExit('Nur %d Sprechstuecke fuer %d Saetze gefunden.' % (n, m))
    gesamt_zeichen = float(sum(len(x) for x in saetze))
    gesamt_zeit = stuecke[-1]['ende'] - stuecke[0]['start']
    t0 = stuecke[0]['start']
    grenzen, benutzt, lauf = [], 0, 0.0
    for i, satz in enumerate(saetze[:-1]):
        lauf += len(satz) / gesamt_zeichen
        ziel = t0 + lauf * gesamt_zeit
        # bestes Stueck-Ende ab dem letzten Schnitt, mindestens eines pro Satz
        kand = range(benutzt, n - (m - 1 - i))
        best = min(kand, key=lambda k: abs(stuecke[k]['ende'] - ziel))
        grenzen.append(best)
        benutzt = best + 1
    aus, ab = [], 0
    for i in range(m):
        bis = grenzen[i] if i < len(grenzen) else n - 1
        aus.append(['P%d' % (i + 1), round(stuecke[ab]['start'], 2), round(stuecke[bis]['ende'], 2)])
        ab = bis + 1
    return aus


def phrasen_lesen(mp3):
    t = subprocess.run([PY, R + r'\fabrik.py', 'phrasen', mp3],
                       capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
    o, _ = json.JSONDecoder().raw_decode(t[t.index('['):])
    return o


# ------------------------------------------------------------------ Szenenfolgen
def bauen_14(T, ordner):
    from szenen import Reel, hook, hotspots, maskottchen_tipp, abschluss, schreiben
    V0 = 0.15
    A = lambda k, o=0.0: V0 + T[k][0] + o
    END = V0 + T['P7'][1] + 0.85
    reel = Reel('Drei Stellen, die niemand putzt', END)
    hook(reel, 's1', 0, A('P2', -.08), label='Checkliste', bg='var(--ice)', farbe='var(--navy)', zeilen=[
        dict(text='Drei Stellen', groesse=120, t=A('P1')),
        dict(text='putzt fast niemand.', art='serif', groesse=128, t=A('P1', .6))])
    hotspots(reel, 's2', A('P2', -.08), A('P6', -.1),
             titel_html='Und ihr fasst sie <span class="serif">täglich</span> an.',
             t_titel=A('P2'), punkte=[
                 dict(x=14, y=28, text='Lichtschalter', t=A('P3', .15)),
                 dict(x=52, y=70, text='Türklinke', t=A('P4', .15)),
                 dict(x=82, y=34, text='Abtropfschale', t=A('P5', .15))])
    maskottchen_tipp(reel, 's3', A('P6', -.1), A('P7', -.1), karten=[
        ('<div class="a">Einmal am Tag</div><div class="a"><span class="serif">feucht abwischen.</span></div>', A('P6', .15)),
        ('<div class="b">Zehn Sekunden</div><div class="b"><span class="serif">pro Raum.</span></div>', A('P6', 1.6))])
    abschluss(reel, 's4', A('P7', -.1), END, t_marke=A('P7'), t_zeile=A('P7', .8), t_knopf=A('P7', 2.1))
    schreiben(reel, ordner)
    return END


def bauen_16(T, ordner):
    from szenen import Reel, hook, durchstreichen, zone, maskottchen_tipp, abschluss, schreiben
    V0 = 0.15
    A = lambda k, o=0.0: V0 + T[k][0] + o
    END = V0 + T['P6'][1] + 0.85
    reel = Reel('Zonen ohne Zuschlag', END)
    hook(reel, 's1', 0, A('P2', -.08), label='Chur und Umgebung', bg='var(--navy)', farbe='#fff', zeilen=[
        dict(text='Euer Büro liegt', groesse=98, t=A('P1')),
        dict(text='ausserhalb von Chur?', art='serif', groesse=126, t=A('P1', .55))])
    durchstreichen(reel, 's2', A('P2', -.08), A('P3', -.1), label='Kennt man ja',
                   karte='Anfahrts&shy;pauschale', t_karte=A('P2', .1), t_strich=A('P2', .95),
                   unter='Bei uns nicht.', t_unter=A('P2', 1.3))
    zone(reel, 's3', A('P3', -.1), A('P5', -.1), t_ring=A('P3', .2),
         abzeichen='ohne Zuschlag', t_abz=A('P3', 1.1),
         titel_html='Bis <span class="serif">5 km</span> ab Chur')
    maskottchen_tipp(reel, 's4', A('P5', -.1), A('P6', -.1), label='So arbeiten wir', karten=[
        ('<div class="a">Fester Monatspreis.</div><div class="a"><span class="serif">Keine Mindestlaufzeit.</span></div>', A('P5', .15))])
    abschluss(reel, 's5', A('P6', -.1), END, t_marke=A('P6'), t_zeile=A('P6', .8), t_knopf=A('P6', 2.1))
    schreiben(reel, ordner)
    return END


def bauen_18(T, ordner):
    from szenen import Reel, hook, stempel, punch, maskottchen_tipp, abschluss, schreiben
    V0 = 0.15
    A = lambda k, o=0.0: V0 + T[k][0] + o
    END = V0 + T['P6'][1] + 0.85
    reel = Reel('Ein Tuch, acht Flächen', END)
    hook(reel, 's1', 0, A('P2', -.08), label='Tipp vom Profi', bg='var(--blue)', zeilen=[
        dict(text='Du benutzt nur', groesse=96, t=A('P1')),
        dict(text='ein Viertel', art='serif', groesse=150, t=A('P1', .5)),
        dict(text='von deinem Tuch.', groesse=84, t=A('P1', 1.0))])
    stempel(reel, 's2', A('P2', -.08), A('P3', -.1), label='So geht es fast allen',
            zeilen=[dict(text='Einmal wischen,', groesse=108, t=A('P2')),
                    dict(text='dann auswaschen.', groesse=108, t=A('P2', .45))],
            wort='SCHADE', t_stempel=A('P2', 1.2), farbe_stempel='var(--steel)',
            unter='Der Rest ist noch sauber.', t_unter=A('P2', 1.55))
    punch(reel, 's3', A('P3', -.1), A('P4', -.1), wort='ACHT', t_wort=A('P3', 1.5),
          klein='Zweimal falten, vier Lagen', t_klein=A('P3', .15),
          unter='saubere Flächen', t_unter=A('P3', 2.1))
    maskottchen_tipp(reel, 's4', A('P4', -.1), A('P6', -.1), karten=[
        ('<div class="a">Seite grau?</div><div class="a"><span class="serif">Umklappen.</span></div>', A('P4', .15)),
        ('<div class="b">Ein Tuch reicht für</div><div class="b"><span class="serif">acht Räume.</span></div>', A('P5', .1))])
    abschluss(reel, 's5', A('P6', -.1), END, t_marke=A('P6'), t_zeile=A('P6', .8), t_knopf=A('P6', 2.1))
    schreiben(reel, ordner)
    return END


BAUER = {'IG-2026-10-14-r1': bauen_14, 'IG-2026-10-16-r1': bauen_16, 'IG-2026-10-18-r1': bauen_18}
TERMIN = {'IG-2026-10-14-r1': ('2026-10-14', '18:00', 'checkliste', 'Drei Stellen, die niemand putzt'),
          'IG-2026-10-16-r1': ('2026-10-16', '12:00', 'transparenz', 'Zonen: bis 5 km ohne Zuschlag'),
          'IG-2026-10-18-r1': ('2026-10-18', '10:00', 'tipp', 'Ein Mikrofasertuch, acht Flächen')}
CAPTION = {
 'IG-2026-10-14-r1': """Drei Stellen im Büro putzt fast niemand. Und genau die fasst ihr täglich an.

Den Lichtschalter.
Die Türklinke.
Die Abtropfschale der Kaffeemaschine.

Einmal am Tag feucht abwischen, zehn Sekunden pro Raum.

Speichern für später

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung""",
 'IG-2026-10-16-r1': """Euer Büro liegt ausserhalb von Chur? Dann kommt jetzt der Aufschlag. Bei uns nicht.

Bis 5 km ab Chur: kein Zuschlag.
Danach CHF 15 pro Einsatz, weiter draussen CHF 35.
Mehr kommt nicht dazu.

Fester Monatspreis, keine Mindestlaufzeit.

Richtpreis in 1 Minute: Link in der Bio

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung""",
 'IG-2026-10-18-r1': """Du benutzt nur ein Viertel von deinem Putztuch.

Zweimal falten gibt vier Lagen.
Vorne und hinten sind das acht saubere Flächen.
Ist eine Seite grau: umklappen statt auswaschen.

Ein Tuch reicht so für acht Räume.

Speichern für später

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #putztipp #habibireinigung""",
}

bericht = []
idx = json.load(io.open(W + r'\instagram\reels\index.json', encoding='utf-8'))

for pid, (pfad, zeit, sig) in AUDIO.items():
    mp3 = W + r'\werkstatt\audio\%s.mp3' % pid
    urllib.request.urlretrieve(B + pfad + '/content.mp3' + Q.format(z=zeit, s=sig), mp3)
    ordner = W + r'\werkstatt\%s' % pid
    os.makedirs(ordner, exist_ok=True)

    phr = zuordnen(phrasen_lesen(mp3), SAETZE[pid])
    io.open(ordner + r'\phrasen.json', 'w', encoding='utf-8').write(json.dumps(phr))
    subprocess.run([PY, R + r'\fabrik.py', 'straffen', mp3, ordner + r'\phrasen.json', ordner],
                   check=True, capture_output=True)
    subprocess.run([PY, R + r'\fabrik.py', 'projekt', ordner], check=True, capture_output=True)

    T = json.load(io.open(ordner + r'\zeiten.json', encoding='utf-8'))
    dauer = BAUER[pid](T, ordner)

    rend = subprocess.run([PY, R + r'\fabrik.py', 'render', ordner],
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    if rend.returncode != 0:
        fehler = [z for z in (rend.stdout or '').splitlines() if '✗' in z][:4]
        bericht.append('FEHLER  %s  %s' % (pid, ' | '.join(fehler) or (rend.stderr or '')[-200:]))
        continue
    ziel = W + r'\instagram\%s' % pid
    fert = subprocess.run([PY, R + r'\fabrik.py', 'fertig', ordner, pid, ziel, '1.6'],
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    if fert.returncode != 0:
        bericht.append('FEHLER  %s  Mischung: %s' % (pid, (fert.stderr or '')[-160:]))
        continue

    datum, uhr, saeule, thema = TERMIN[pid]
    daten = {"post_id": pid, "datum": datum, "zeit": uhr, "format": "reel", "thema": thema,
             "saeule": saeule, "caption": CAPTION[pid],
             "spec": {"szenen": [{"text": x} for x in SAETZE[pid][:-1]],
                      "schluss": {"text": "Richtpreis für euer Büro in 1 Minute", "knopf": "habibireinigung.ch"},
                      "sprechtext": ' '.join(SAETZE[pid])},
             "medien": [{"datei": pid + ".mp4", "typ": "video"}, {"datei": pid + "_titel.jpg", "typ": "titelbild"}],
             "ordner": "instagram/" + pid, "warnungen": []}
    io.open(ziel + r'\ig_post.json', 'w', encoding='utf-8').write(json.dumps(daten, ensure_ascii=False, indent=1))
    idx['reels'].append({"post_id": pid, "datum": datum, "zeit": uhr, "thema": thema, "saeule": saeule,
                         "sprechtext": daten['spec']['sprechtext'], "erstellt_am": "2026-10-07",
                         "version": 1, "import_noetig": True})
    zeile = [z for z in (fert.stdout or '').splitlines() if z.startswith('Fertig')]
    bericht.append('ok      %s  %.1f s  %s' % (pid, dauer, zeile[0][40:] if zeile else ''))

io.open(W + r'\instagram\reels\index.json', 'w', encoding='utf-8').write(json.dumps(idx, ensure_ascii=False, indent=2))
print('\n'.join(bericht))
