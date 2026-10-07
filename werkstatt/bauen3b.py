# -*- coding: utf-8 -*-
"""Die drei Reels neu, Fassung 2: mit dem Warum, Gegenstaenden im Bild und
einheitlichem Tag-Muster (kein [sarcastic] mehr)."""
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
 'IG-2026-10-14-r1': ('HZDqSiTK3Y8uA5qOnOk0/iEGOAp671MlYTHAKV9pc', '130353', 'b8feb240b51a2053b0639c0fe5e67f626cb47d7be327a33a91592aae911cf7fc5017a85b34dd3261a48d18576c4d50f7b0f89297fa30e59ff5264050cc9aab01be1704db04a241e29c73e86c3f9b6f3ce94a69c3db11ba26a44ff3c82946090d7645acaf83a417f1ccd9e7320b9a1b74a56c4e5269bf7d1ba1fdf0e3f80b17877e2b775ab8408e10750f2913904f6a204c87eaf2fb096f1522b9948b944fb314180a6f3378062f15ec0b64d26dbbf903a0d60f3319e38ed68b770e3c83d03848559b612f4121866af769c7303df257258cfa985d2adba10cc375ba3cde07f130c4823de79b4805c71822d87271fdc4b227137b93133a8baa33ea35e2f40540f1'),
 'IG-2026-10-16-r1': ('AAKc5mvNc2QSR6oq67iC/nohgJCpbciuyKJEXQDXY', '130403', '9e6a469fc5adb68a75f5805b13319f5b1e551368cb29bc08579c4b5c764db69d72af65c6932c6a9ebac0e56644f2821ae0a29547d73f8053167bf56fb66dcd39233485f6d6365a3389fa970c6043d3e1789a89859c99ff22c126e467045743e1d575cfacf5dd3262231d18a8355b47c353e04711b117a1a4b49fdbbd1ea11c3983cd2e0105e62b64f53e70514c4fc7a30ecbd4c0c95a31577ac94959fc2f482de348f20a938ab78236c80a807d32f182e90609ff1c3df82ff04d1eb1f15ecbf089dcca9eb9cc8067b9b8b2787d8929d8d535f8a82ff3b6348e10a3871a02eb0b3c173c20d6ff2bcb81bef33068f061bc19c9d5f903811602e9165cd6de83769e'),
 'IG-2026-10-18-r1': ('1aWK8kAFvG2bIeh2R16V/UCk40BLOeBEqpG8mDc5k', '130415', '3e4e866a882b6d4de3a4ab6e324bf78b846456495beba36897296a46f6423296aca4bedf9a7940970101a10fd1bc1948a6938c8273c156cc36b6c281ed2466824cd57da8ccd9b9602069860329225403dd2c94abff437c59c5d7a334a3ccccefddf9849febb85dfc94f56b1e4fe510ddb42fb6ef40d5e80911d590d16b5f467d96b45efb0ddf54395ed749fdf80ee8e04619aa4f69c76f6dad59779f1bd1abcc1e60768daf2a5063891bda87333a0f8ba5912835f665a8663d7e41f587856015e8a41b6a020ee2a75aeb3a959d0298f17527bfd641641f69eeb04c80696af0bd5077345455cf8c5517fc49d225e1150599ee0730423cc898d7b277455e68881b'),
}

SAETZE = {
 'IG-2026-10-14-r1': [
   "Dein Schreibtisch hat mehr Bakterien als eine Toilettenbrille.",
   "Vierhundert mal mehr. Gemessen von der Uni Arizona.",
   "Der Grund ist simpel: Die Toilette wird jeden Tag geputzt. Der Schreibtisch nie.",
   "Genauso diese drei: der Lichtschalter.", "Die Türklinke.",
   "Die Abtropfschale der Kaffeemaschine.",
   "Viele Hände, nie ein Tuch. Einmal am Tag feucht drüber, zehn Sekunden pro Raum.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
 'IG-2026-10-16-r1': [
   "Wir nehmen höchstens vier neue Büros pro Monat an.",
   "Das ist kein Versehen. Das ist Absicht.",
   "Für jedes Objekt ist ein festes Team eingeteilt. Die kennen euren Schlüssel, eure Räume, eure Regeln.",
   "Wer schneller wächst, schickt jede Woche jemand Neues. Mit eurem Schlüssel.",
   "Bei Ferien kommt bei uns jemand, der das Objekt schon kennt.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
 'IG-2026-10-18-r1': [
   "Mit einem grauen Putztuch machst du es schlimmer.",
   "Du nimmst die Keime vom WC mit an den Schreibtisch.",
   "Darum falten Profis zweimal: vier Lagen, acht saubere Flächen.",
   "Eine Fläche pro Bereich, nie zweimal dieselbe.",
   "Ist eine Seite grau: umklappen statt weiterwischen. So reicht ein Tuch für acht Räume, und nichts wandert mit.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
}


def zuordnen(stuecke, saetze):
    n, m = len(stuecke), len(saetze)
    if n < m:
        raise SystemExit('Nur %d Sprechstuecke fuer %d Saetze.' % (n, m))
    gz = float(sum(len(x) for x in saetze))
    t0, spanne = stuecke[0]['start'], stuecke[-1]['ende'] - stuecke[0]['start']
    grenzen, benutzt, lauf = [], 0, 0.0
    for i, satz in enumerate(saetze[:-1]):
        lauf += len(satz) / gz
        ziel = t0 + lauf * spanne
        kand = range(benutzt, n - (m - 1 - i))
        best = min(kand, key=lambda k: abs(stuecke[k]['ende'] - ziel))
        grenzen.append(best); benutzt = best + 1
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


def bauen_14(T, ordner):
    from szenen import Reel, hook, punch, stempel, enthuellen, maskottchen_tipp, abschluss, schreiben
    V0 = 0.15
    A = lambda k, o=0.0: V0 + T[k][0] + o
    END = V0 + T['P8'][1] + 0.85
    reel = Reel('Mehr Bakterien als die Toilette', END)
    hook(reel, 's1', 0, A('P2', -.08), label='Büro-Hygiene', bg='var(--ice)', farbe='var(--navy)', zeilen=[
        dict(text='Dein Schreibtisch', groesse=104, t=A('P1')),
        dict(text='ist schmutziger als', groesse=78, t=A('P1', .5)),
        dict(text='die Toilette.', art='serif', groesse=132, t=A('P1', .95))])
    punch(reel, 's2', A('P2', -.08), A('P3', -.1), wort='400x', t_wort=A('P2', .1),
          klein='mehr Bakterien', t_klein=A('P2', .5),
          unter='Studie Uni Arizona', t_unter=A('P2', 1.5))
    stempel(reel, 's3', A('P3', -.1), A('P4', -.1), label='Warum eigentlich',
            zeilen=[dict(text='Die Toilette wird', groesse=98, t=A('P3')),
                    dict(text='täglich geputzt.', groesse=98, t=A('P3', .4))],
            wort='DER TISCH NIE', t_stempel=A('P3', 1.5), farbe_stempel='var(--rot)')
    enthuellen(reel, 's4', A('P4', -.1), A('P7', -.1),
               titel_html='Dieselben drei <span class="serif">jeden Tag</span>', t_titel=A('P4', -.05),
               punkte=[dict(ding='schalter', name='Lichtschalter', warum='Zehn Hände am Tag, nie ein Tuch.', t=A('P4', .55)),
                       dict(ding='klinke', name='Türklinke', warum='Jeder fasst sie an, keiner wischt sie.', t=A('P5', .15)),
                       dict(ding='schale', name='Abtropfschale', warum='Dauernd feucht und dauernd warm.', t=A('P6', .15))])
    maskottchen_tipp(reel, 's5', A('P7', -.1), A('P8', -.1), karten=[
        ('<div class="a">Einmal am Tag</div><div class="a"><span class="serif">feucht drüber.</span></div>', A('P7', .15)),
        ('<div class="b">Zehn Sekunden</div><div class="b"><span class="serif">pro Raum.</span></div>', A('P7', 2.2))])
    abschluss(reel, 's6', A('P8', -.1), END, t_marke=A('P8'), t_zeile=A('P8', .8), t_knopf=A('P8', 2.1))
    schreiben(reel, ordner)
    return END


def bauen_16(T, ordner):
    from szenen import Reel, hook, punch, maskottchen_tipp, stempel, abschluss, schreiben
    V0 = 0.15
    A = lambda k, o=0.0: V0 + T[k][0] + o
    END = V0 + T['P6'][1] + 0.85
    reel = Reel('Wer hat euren Schlüssel', END)
    hook(reel, 's1', 0, A('P2', -.08), label='So arbeiten wir', bg='var(--navy)', farbe='#fff', zeilen=[
        dict(text='Wir nehmen nur', groesse=92, t=A('P1')),
        dict(text='vier neue Büros', art='serif', groesse=128, t=A('P1', .5)),
        dict(text='pro Monat an.', groesse=86, t=A('P1', 1.0))])
    punch(reel, 's2', A('P2', -.08), A('P3', -.1), wort='ABSICHT', t_wort=A('P2', .75),
          klein='Kein Versehen.', t_klein=A('P2', .15))
    maskottchen_tipp(reel, 's3', A('P3', -.1), A('P4', -.1), label='Für euer Objekt', karten=[
        ('<div class="a">Immer</div><div class="a"><span class="serif">dasselbe Team.</span></div>', A('P3', .15)),
        ('<div class="b">Kennt euren Schlüssel,</div><div class="b"><span class="serif">eure Räume, eure Regeln.</span></div>', A('P3', 2.0))])
    stempel(reel, 's4', A('P4', -.1), A('P6', -.1), label='Wer schneller wächst',
            zeilen=[dict(text='Jede Woche', groesse=112, t=A('P4')),
                    dict(text='ein neues Gesicht.', groesse=104, t=A('P4', .45))],
            wort='NIE', t_stempel=A('P4', 1.5),
            unter='Bei Ferien kommt jemand, der es kennt.', t_unter=A('P5', .1))
    abschluss(reel, 's5', A('P6', -.1), END, t_marke=A('P6'), t_zeile=A('P6', .8), t_knopf=A('P6', 2.1))
    schreiben(reel, ordner)
    return END


def bauen_18(T, ordner):
    from szenen import Reel, hook, enthuellen, punch, maskottchen_tipp, abschluss, schreiben
    V0 = 0.15
    A = lambda k, o=0.0: V0 + T[k][0] + o
    END = V0 + T['P6'][1] + 0.85
    reel = Reel('Das graue Tuch macht es schlimmer', END)
    hook(reel, 's1', 0, A('P2', -.08), label='Tipp vom Profi', bg='var(--blue)', zeilen=[
        dict(text='Ein graues Putztuch', groesse=88, t=A('P1')),
        dict(text='putzt nicht.', art='serif', groesse=140, t=A('P1', .5)),
        dict(text='Es verteilt.', groesse=86, t=A('P1', 1.0))])
    enthuellen(reel, 's2', A('P2', -.08), A('P3', -.1),
               titel_html='Was wirklich passiert', t_titel=A('P2', -.05),
               punkte=[dict(ding='tuch', name='Das graue Tuch', warum='Die Keime vom WC landen auf dem Schreibtisch.', t=A('P2', .5))])
    punch(reel, 's3', A('P3', -.1), A('P4', -.1), wort='ACHT', t_wort=A('P3', 1.4),
          klein='Zweimal falten, vier Lagen', t_klein=A('P3', .15),
          unter='saubere Flächen', t_unter=A('P3', 2.0))
    maskottchen_tipp(reel, 's4', A('P4', -.1), A('P6', -.1), karten=[
        ('<div class="a">Eine Fläche</div><div class="a"><span class="serif">pro Bereich.</span></div>', A('P4', .15)),
        ('<div class="b">Grau?</div><div class="b"><span class="serif">Umklappen, nicht weiterwischen.</span></div>', A('P5', .15))])
    abschluss(reel, 's5', A('P6', -.1), END, t_marke=A('P6'), t_zeile=A('P6', .8), t_knopf=A('P6', 2.1))
    schreiben(reel, ordner)
    return END


BAUER = {'IG-2026-10-14-r1': bauen_14, 'IG-2026-10-16-r1': bauen_16, 'IG-2026-10-18-r1': bauen_18}
TERMIN = {'IG-2026-10-14-r1': ('2026-10-14', '18:00', 'mythos', 'Schreibtisch schmutziger als die Toilette'),
          'IG-2026-10-16-r1': ('2026-10-16', '12:00', 'transparenz', 'Nur vier neue Büros pro Monat, und warum'),
          'IG-2026-10-18-r1': ('2026-10-18', '10:00', 'tipp', 'Das graue Tuch verteilt statt zu putzen')}
CAPTION = {
 'IG-2026-10-14-r1': """Dein Schreibtisch hat rund 400 mal mehr Bakterien als eine Toilettenbrille.

Der Grund ist simpel: die Toilette wird jeden Tag geputzt, der Schreibtisch nie.
Dasselbe gilt für den Lichtschalter, die Türklinke und die Abtropfschale der Kaffeemaschine.
Viele Hände, nie ein Tuch.

Einmal am Tag feucht drüber, zehn Sekunden pro Raum.

Quelle: Studie der University of Arizona, Charles Gerba

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung""",
 'IG-2026-10-16-r1': """Wir nehmen höchstens vier neue Büros pro Monat an. Das ist kein Versehen.

Für jedes Objekt ist ein festes Team eingeteilt.
Die kennen euren Schlüssel, eure Räume und eure Regeln.
Wer schneller wächst, schickt jede Woche jemand Neues. Mit eurem Schlüssel.

Bei Ferien kommt bei uns jemand, der das Objekt schon kennt.

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung""",
 'IG-2026-10-18-r1': """Mit einem grauen Putztuch machst du es schlimmer.

Du nimmst die Keime vom WC mit an den Schreibtisch.
Darum falten Profis zweimal: vier Lagen, acht saubere Flächen.
Eine Fläche pro Bereich, nie zweimal dieselbe.

Ist eine Seite grau: umklappen statt weiterwischen.

Speichern für später

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #putztipp #habibireinigung""",
}

bericht = []
idx = json.load(io.open(W + r'\instagram\reels\index.json', encoding='utf-8'))

for pid, (pfad, zeit, sig) in [(k, v) for k, v in AUDIO.items() if k in ('IG-2026-10-14-r1', 'IG-2026-10-18-r1')]:
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
        f = [z.strip()[:150] for z in (rend.stdout or '').splitlines() if '✗' in z][:4]
        bericht.append('FEHLER %s  %s' % (pid, ' | '.join(f) or (rend.stderr or '')[-200:]))
        continue
    ziel = W + r'\instagram\%s' % pid
    fert = subprocess.run([PY, R + r'\fabrik.py', 'fertig', ordner, pid, ziel, '1.5'],
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    if fert.returncode != 0:
        bericht.append('FEHLER %s  Mischung: %s' % (pid, (fert.stderr or '')[-150:]))
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
    for e in idx['reels']:
        if e['post_id'] == pid:
            e.update({"thema": thema, "saeule": saeule, "sprechtext": daten['spec']['sprechtext'],
                      "version": 2, "import_noetig": True})
    bericht.append('ok     %s  %.1f s' % (pid, dauer))

io.open(W + r'\instagram\reels\index.json', 'w', encoding='utf-8').write(json.dumps(idx, ensure_ascii=False, indent=2))
print('\n'.join(bericht))
