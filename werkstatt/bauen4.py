# -*- coding: utf-8 -*-
"""Drei Reels, Bild auf das Wort genau.

Neu gegenueber bauen3b.py: die Szenen haengen nicht mehr an Phrasengrenzen,
sondern an den **Zeitstempeln einzelner Woerter** aus der Transkription.
Damit erscheint die Tuerklinke genau dann, wenn 'Tuerklinke' gesagt wird.
"""
import io, json, os, re, subprocess, sys, urllib.request

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

ERGEBNIS = (r'C:\Users\habib\.claude\projects\C--Users-habib-Documents-Habibi-Marketing'
            r'\ca4bb46e-b0be-4022-bfee-85c9951cb8cc\tool-results'
            r'\mcp-53875fb1-0b63-4c65-abbd-eea2f2a8bdf1-creative_show_flow_results-1791380194631.txt')

TON_SESSION = {'IG-2026-10-14-r1': 'FjLGORO2rsBquBdUPGqv',
               'IG-2026-10-16-r1': 'GBvdboOfvO5xIjJmHhLI',
               'IG-2026-10-18-r1': 'F6JNEi5hEI1lQPBWkZNn'}
TEXT_SESSION = {'IG-2026-10-14-r1': '08bk5kYRBH0M6mvg7d6S',
                'IG-2026-10-16-r1': 'F4fA8sV4DoRJSJkFfqKr',
                'IG-2026-10-18-r1': 'wA0589uWBh2CEUlRkep0'}
V0, TEMPO = 0.15, 1.08


# ------------------------------------------------------------------ Ergebnisdatei auswerten
# Die Datei ist flach: generations (erst 3 Audio, dann 3 Text) und transcripts,
# beide in der Reihenfolge, in der die Auftraege abgeschickt wurden.
REIHE = ['IG-2026-10-14-r1', 'IG-2026-10-16-r1', 'IG-2026-10-18-r1']


def lade_ergebnis():
    roh = io.open(ERGEBNIS, encoding='utf-8', errors='replace').read()
    d, _ = json.JSONDecoder().raw_decode(roh[roh.index('{'):])
    tonspuren = [g['content_url'] for g in d['generations']
                 if g.get('modality') == 'audio' and g.get('content_url')]
    transkripte = [t.get('words') or [] for t in d.get('transcripts', [])]
    if len(tonspuren) < 3 or len(transkripte) < 3:
        raise SystemExit('Erwartet 3 Tonspuren und 3 Transkripte, gefunden %d und %d.'
                         % (len(tonspuren), len(transkripte)))
    return ({pid: tonspuren[i] for i, pid in enumerate(REIHE)},
            {pid: transkripte[i] for i, pid in enumerate(REIHE)})


# ------------------------------------------------------------------ Phrasen fuer das Straffen
SAETZE = {
 'IG-2026-10-14-r1': [
   "Auf deinem Schreibtisch sitzen mehr Bakterien als auf einer Toilettenbrille.",
   "Rund vierhundert mal mehr. Das hat die Universität von Arizona in echten Büros gemessen.",
   "Der Grund ist nicht Ekel, sondern Gewohnheit. Die Toilette putzt jemand jeden Tag. Den Schreibtisch putzt niemand, weil er sauber aussieht.",
   "Genau so läuft es bei drei weiteren Stellen.",
   "Erstens, der Lichtschalter. Jeder im Büro drückt ihn, mehrmals am Tag, und niemand wischt ihn ab.",
   "Zweitens, die Türklinke. Sie ist das Erste, was eine fremde Hand bei euch berührt.",
   "Drittens, die Abtropfschale unter der Kaffeemaschine. Sie steht dauernd feucht und warm, und genau das mögen Bakterien.",
   "Du brauchst dafür kein Spezialmittel. Ein feuchtes Tuch, einmal am Tag, zehn Sekunden pro Raum.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
 'IG-2026-10-16-r1': [
   "Wir nehmen höchstens vier neue Büros pro Monat an. Obwohl wir mehr Anfragen bekommen.",
   "Das ist kein Versehen, sondern eine Entscheidung. Und sie hat mit eurem Schlüssel zu tun.",
   "Für jedes Objekt teilen wir ein festes Team ein. Dieselben Leute, jede Woche.",
   "Die wissen, wo der Schlüssel hängt, welche Tür zu bleibt und welche Unterlagen niemand anfasst.",
   "Eine Firma, die viel schneller wächst, kann das nicht halten. Dort steht jede Woche jemand anderes in euren Räumen, abends, wenn längst niemand mehr da ist.",
   "Wenn bei uns jemand in den Ferien ist, kommt kein Fremder. Es kommt jemand, der euer Objekt schon kennt.",
   "Habibi Reinigung! Richtpreis in einer Minute, auf habibi reinigung punkt c h!"],
 'IG-2026-10-18-r1': [
   "Ein graues Putztuch putzt nicht mehr. Es verteilt.",
   "Alles, was du vorher aufgenommen hast, Fett, Staub und Keime vom WC, wischst du damit auf den nächsten Tisch.",
   "Profis lösen das mit einer einfachen Falttechnik. Du faltest das Tuch einmal, dann noch einmal. Dadurch liegen vier Lagen übereinander.",
   "Jede Lage hat eine Vorderseite und eine Rückseite, das ergibt acht saubere Flächen aus einem einzigen Tuch.",
   "Für jeden Bereich nimmst du eine frische Fläche, nie zweimal dieselbe.",
   "Sobald eine Fläche grau ist, klappst du um, statt weiterzuwischen. So reicht ein Tuch für acht Räume, und nichts wandert von einem Raum in den nächsten.",
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


def wortuhr(worte, phrasen, zeiten):
    """Gibt eine Funktion, die zu einem Wort die Zeit IM FERTIGEN REEL liefert."""
    liste = []
    for w in worte:
        txt = (w.get('text') or w.get('word') or '').strip()
        if not txt:
            continue
        s = w.get('start', w.get('start_time'))
        if s is None:
            continue
        liste.append((re.sub(r'[^0-9a-zäöüß]', '', txt.lower()), float(s)))

    def zeit(wort, nr=1):
        ziel = re.sub(r'[^0-9a-zäöüß]', '', wort.lower())
        treffer = [t for (x, t) in liste if x == ziel]
        if len(treffer) < nr:
            treffer = [t for (x, t) in liste if ziel in x]
        if len(treffer) < nr:
            raise SystemExit('Wort "%s" (Nr %d) nicht in der Transkription gefunden.' % (wort, nr))
        roh = treffer[nr - 1]
        for name, a, b in phrasen:
            if a - 0.25 <= roh <= b + 0.25:
                return V0 + zeiten[name][0] + (roh - a) / TEMPO
        # ausserhalb aller Phrasen: linear schaetzen
        name, a, b = phrasen[-1]
        return V0 + zeiten[name][0] + (roh - a) / TEMPO
    return zeit


# ------------------------------------------------------------------ Die drei Reels
def bauen_14(Z, T, ordner):
    from szenen import Reel, hook, punch, stempel, enthuellen, maskottchen_tipp, abschluss, schreiben
    a2, a3, a4 = Z('Rund'), Z('Grund'), Z('Erstens')
    w1, w2, w3 = Z('Lichtschalter'), Z('Türklinke'), Z('Abtropfschale')
    a5, a6 = Z('brauchst'), Z('Habibi')
    END = V0 + T['P9'][1] + 0.85
    reel = Reel('Schmutziger als die Toilette', END)
    hook(reel, 's1', 0, a2 - .1, label='Büro-Hygiene', bg='var(--ice)', farbe='var(--navy)', zeilen=[
        dict(text='Dein Schreibtisch', groesse=102, t=Z('deinem') - .15),
        dict(text='hat mehr Bakterien als', groesse=72, t=Z('Bakterien') - .3),
        dict(text='eine Toilettenbrille.', art='serif', groesse=112, t=Z('Toilettenbrille') - .25)])
    punch(reel, 's2', a2 - .1, a3 - .5, wort='400x', t_wort=a2 + .05,
          klein='mehr Bakterien', t_klein=a2 - .05,
          unter='Studie Universität Arizona', t_unter=Z('Universität') - .2)
    stempel(reel, 's3', a3 - .5, a4 - .25, label='Warum eigentlich',
            zeilen=[dict(text='Toilette täglich. Schreibtisch nie.', groesse=76, t=Z('Toilette', 2) - .3)],
            wort='DARUM', t_stempel=Z('niemand') - .1, farbe_stempel='var(--rot)',
            unter='Er sieht ja sauber aus.', t_unter=Z('aussieht') - .4)
    enthuellen(reel, 's4', a4 - .25, a5 - .35,
               titel_html='Dieselben drei <span class="serif">jeden Tag</span>', t_titel=a4 - .2,
               punkte=[dict(ding='schalter', name='Lichtschalter',
                            warum='Jeder drückt ihn mehrmals am Tag. Niemand wischt ihn ab.', t=w1),
                       dict(ding='klinke', name='Türklinke',
                            warum='Das Erste, was eine fremde Hand bei euch berührt.', t=w2),
                       dict(ding='schale', name='Abtropfschale',
                            warum='Dauernd feucht und warm. Genau das mögen Bakterien.', t=w3)])
    maskottchen_tipp(reel, 's5', a5 - .35, a6 - .2, karten=[
        ('<div class="a">Kein Spezialmittel.</div><div class="a"><span class="serif">Ein feuchtes Tuch.</span></div>', a5 - .1),
        ('<div class="b">Einmal am Tag,</div><div class="b"><span class="serif">zehn Sekunden pro Raum.</span></div>', Z('einmal', 1) - .2)])
    abschluss(reel, 's6', a6 - .2, END, t_marke=a6 - .05, t_zeile=Z('Richtpreis') - .15, t_knopf=Z('habibi', 2) - .2)
    schreiben(reel, ordner)
    return END


def bauen_16(Z, T, ordner):
    from szenen import Reel, hook, punch, maskottchen_tipp, stempel, abschluss, schreiben
    b2, b3, b4, b6 = Z('Versehen'), Z('teilen'), Z('Firma'), Z('Habibi')
    END = V0 + T['P7'][1] + 0.85
    reel = Reel('Wer hat euren Schlüssel', END)
    hook(reel, 's1', 0, b2 - .55, label='So arbeiten wir', bg='var(--navy)', farbe='#fff', zeilen=[
        dict(text='Wir nehmen nur', groesse=88, t=Z('nehmen') - .2),
        dict(text='vier neue Büros', art='serif', groesse=124, t=Z('vier') - .2),
        dict(text='pro Monat an.', groesse=82, t=Z('Monat') - .25)])
    punch(reel, 's2', b2 - .55, b3 - .5, wort='ABSICHT', t_wort=Z('Entscheidung') - .25,
          klein='Kein Versehen.', t_klein=b2 - .3,
          unter='Es geht um euren Schlüssel.', t_unter=Z('Schlüssel') - .3)
    maskottchen_tipp(reel, 's3', b3 - .5, b4 - .4, label='Für euer Objekt', karten=[
        ('<div class="a">Immer</div><div class="a"><span class="serif">dieselben Leute.</span></div>', b3 - .2),
        ('<div class="b">Sie wissen, wo der Schlüssel hängt</div><div class="b"><span class="serif">und welche Tür zu bleibt.</span></div>', Z('wissen') - .25)])
    stempel(reel, 's4', b4 - .4, b6 - .2, label='Wer schneller wächst',
            zeilen=[dict(text='Jede Woche', groesse=110, t=b4 - .1),
                    dict(text='jemand anderes bei euch.', groesse=92, t=Z('anderes') - .3)],
            wort='NIE', t_stempel=Z('halten') - .1,
            unter='Bei Ferien kommt jemand, der euer Objekt kennt.', t_unter=Z('Ferien') - .3)
    abschluss(reel, 's5', b6 - .2, END, t_marke=b6 - .05, t_zeile=Z('Richtpreis') - .15, t_knopf=Z('habibi', 2) - .2)
    schreiben(reel, ordner)
    return END


def bauen_18(Z, T, ordner):
    from szenen import Reel, hook, enthuellen, punch, maskottchen_tipp, abschluss, schreiben
    c2, c3, c5 = Z('Alles'), Z('Profis'), Z('Habibi')
    c4 = Z('Bereich')
    END = V0 + T['P7'][1] + 0.85
    reel = Reel('Das graue Tuch verteilt', END)
    hook(reel, 's1', 0, c2 - .45, label='Tipp vom Profi', bg='var(--blue)', zeilen=[
        dict(text='Ein graues Putztuch', groesse=86, t=Z('graues') - .3),
        dict(text='putzt nicht.', art='serif', groesse=138, t=Z('putzt', 2) - .2),
        dict(text='Es verteilt.', groesse=86, t=Z('verteilt') - .2)])
    enthuellen(reel, 's2', c2 - .45, c3 - .4,
               titel_html='Was wirklich passiert', t_titel=c2 - .35,
               punkte=[dict(ding='tuch', name='Das graue Tuch',
                            warum='Fett, Staub und Keime vom WC landen auf dem nächsten Tisch.', t=c2 + .05)])
    punch(reel, 's3', c3 - .4, c4 - .5, wort='ACHT', t_wort=Z('acht') - .1,
          klein='Zweimal falten, vier Lagen', t_klein=Z('faltest') - .3,
          unter='saubere Flächen aus einem Tuch', t_unter=Z('saubere') - .2)
    maskottchen_tipp(reel, 's4', c4 - .5, c5 - .2, karten=[
        ('<div class="a">Pro Bereich</div><div class="a"><span class="serif">eine frische Fläche.</span></div>', c4 - .25),
        ('<div class="b">Grau?</div><div class="b"><span class="serif">Umklappen statt weiterwischen.</span></div>', Z('grau') - .25)])
    abschluss(reel, 's5', c5 - .2, END, t_marke=c5 - .05, t_zeile=Z('Richtpreis') - .15, t_knopf=Z('habibi', 2) - .2)
    schreiben(reel, ordner)
    return END


BAUER = {'IG-2026-10-14-r1': bauen_14, 'IG-2026-10-16-r1': bauen_16, 'IG-2026-10-18-r1': bauen_18}
TERMIN = {'IG-2026-10-14-r1': ('2026-10-14', '18:00', 'mythos', 'Schreibtisch schmutziger als die Toilette'),
          'IG-2026-10-16-r1': ('2026-10-16', '12:00', 'transparenz', 'Nur vier neue Büros pro Monat, und warum'),
          'IG-2026-10-18-r1': ('2026-10-18', '10:00', 'tipp', 'Das graue Tuch verteilt statt zu putzen')}
CAPTION = {
 'IG-2026-10-14-r1': """Auf deinem Schreibtisch sitzen rund 400 mal mehr Bakterien als auf einer Toilettenbrille.

Der Grund ist nicht Ekel, sondern Gewohnheit: die Toilette putzt jemand jeden Tag, den Schreibtisch putzt niemand, weil er sauber aussieht.

Genau so läuft es bei drei weiteren Stellen:
Der Lichtschalter, den jeder mehrmals am Tag drückt.
Die Türklinke, das Erste, was eine fremde Hand bei euch berührt.
Die Abtropfschale unter der Kaffeemaschine, dauernd feucht und warm.

Ein feuchtes Tuch, einmal am Tag, zehn Sekunden pro Raum.

Quelle: Studie der University of Arizona, Charles Gerba

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung""",
 'IG-2026-10-16-r1': """Wir nehmen höchstens vier neue Büros pro Monat an, obwohl wir mehr Anfragen bekommen.

Das ist kein Versehen, sondern eine Entscheidung. Und sie hat mit eurem Schlüssel zu tun.

Für jedes Objekt teilen wir ein festes Team ein. Dieselben Leute, jede Woche. Sie wissen, wo der Schlüssel hängt, welche Tür zu bleibt und welche Unterlagen niemand anfasst.

Eine Firma, die viel schneller wächst, kann das nicht halten. Dort steht jede Woche jemand anderes in euren Räumen, abends, wenn längst niemand mehr da ist.

Bei uns kommt auch in den Ferien jemand, der euer Objekt schon kennt.

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung""",
 'IG-2026-10-18-r1': """Ein graues Putztuch putzt nicht mehr. Es verteilt.

Alles, was du vorher aufgenommen hast, Fett, Staub und Keime vom WC, wischst du damit auf den nächsten Tisch.

Profis lösen das mit einer Falttechnik: Tuch einmal falten, dann noch einmal. Dadurch liegen vier Lagen übereinander. Jede Lage hat eine Vorderseite und eine Rückseite, das ergibt acht saubere Flächen aus einem einzigen Tuch.

Für jeden Bereich eine frische Fläche. Ist sie grau: umklappen statt weiterwischen.

So reicht ein Tuch für acht Räume, und nichts wandert von einem Raum in den nächsten.

#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #putztipp #habibireinigung""",
}

TON, WORTE = lade_ergebnis()
bericht = []
idx = json.load(io.open(W + r'\instagram\reels\index.json', encoding='utf-8'))

for pid in ['IG-2026-10-14-r1', 'IG-2026-10-18-r1']:
    url, worte = TON.get(pid), WORTE.get(pid)
    if not url or not worte:
        bericht.append('FEHLER %s  Ton oder Transkription fehlt (url=%s, worte=%s)' % (pid, bool(url), bool(worte)))
        continue
    mp3 = W + r'\werkstatt\audio\%s.mp3' % pid
    urllib.request.urlretrieve(url, mp3)
    ordner = W + r'\werkstatt\%s' % pid
    os.makedirs(ordner, exist_ok=True)
    phr = zuordnen(phrasen_lesen(mp3), SAETZE[pid])
    io.open(ordner + r'\phrasen.json', 'w', encoding='utf-8').write(json.dumps(phr))
    subprocess.run([PY, R + r'\fabrik.py', 'straffen', mp3, ordner + r'\phrasen.json', ordner],
                   check=True, capture_output=True)
    subprocess.run([PY, R + r'\fabrik.py', 'projekt', ordner], check=True, capture_output=True)
    T = json.load(io.open(ordner + r'\zeiten.json', encoding='utf-8'))
    Z = wortuhr(worte, phr, T)
    dauer = BAUER[pid](Z, T, ordner)
    rend = subprocess.run([PY, R + r'\fabrik.py', 'render', ordner],
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    if rend.returncode != 0:
        f = [z.strip()[:140] for z in (rend.stdout or '').splitlines() if '\u2717' in z][:4]
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
                      "version": 3, "import_noetig": True})
    bericht.append('ok     %s  %.1f s' % (pid, dauer))

io.open(W + r'\instagram\reels\index.json', 'w', encoding='utf-8').write(json.dumps(idx, ensure_ascii=False, indent=2))
print(('\n'.join(bericht)).encode('ascii', 'replace').decode())
