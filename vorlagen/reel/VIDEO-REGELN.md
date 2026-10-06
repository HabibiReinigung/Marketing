# Video-Regeln Habibi Reinigung

**Version 1.0, 07.10.2026.** Verbindliche Regeln für jedes Video (Instagram Reel, TikTok, Shorts) von Habibi Reinigung, Mortaza Habibi, Chur.

**Für Claude:** Diese Datei vor jedem Video vollständig lesen. Sie entscheidet über Inhalt, Hook, Stimme, Emotion, Bild, Ton und Schnitt. Bei Widerspruch gilt: Faktenregister der Marketing-App (Zahlen und Aussagen) zuerst, dann diese Datei, dann `vorlagen/reel/FABRIK.md` (technischer Ablauf), dann die ANLEITUNG der App. Mortaza muss nichts davon im Chat wiederholen. Wenn etwas hier nicht geregelt ist: so entscheiden, wie es die Beispiele in Abschnitt 12 tun.

---

## 1. Der Qualitätsmassstab

Der Massstab ist das Referenz-Reel von @damianodesu (instagram.com/reel/Dd9fZsHSRy-), ein Motion-Design-Reel, komplett von einer KI gebaut. Mortaza hat es als Standard gesetzt. Die früheren Videos mit statischen Textkarten hat er als «grottenschlecht» abgelehnt. Die Reels «Preis auf Anfrage» und «Heizung läuft wieder» (Abschnitt 12) hat er angenommen.

Was das Referenz-Reel richtig macht, und was deshalb jedes Video können muss:

1. **Es steht nie still.** In jedem Moment bewegt sich etwas: Text fliegt ein, eine Zahl zählt hoch, ein Ring dreht, Staub wirbelt, die Figur wippt. Ein Standbild ist ein Fehler.
2. **Der Hook sitzt in der ersten Sekunde.** Kein Logo am Anfang, keine Begrüssung, kein Aufwärmen. Satz eins ist die Frage oder die Behauptung.
3. **Jeder betonte Begriff hat ein Bild.** Gesprochenes Wort und Einblendung kommen gleichzeitig, auf den Frame.
4. **Jede Bewegung hat ein Geräusch.** Whoosh, Thump, Pop, Stempel. Das macht aus Animation Wucht.
5. **Ein Gedanke pro Szene.** 4 bis 7 Szenen, jede mit genau einer Aussage.
6. **Die Stimme trägt das Video.** Energie, Betonung, Lautstärkewechsel. Keine Vorleserstimme.
7. **Der Schluss ist immer gleich.** Wortmarke, «Richtpreis in 1 Minute», Knopf habibireinigung.ch. Wiedererkennung schlägt Abwechslung.

---

## 2. Die harten Regeln (nie verletzen)

| # | Regel |
| --- | --- |
| 1 | **KEINE PAUSEN.** Siehe Abschnitt 3. Das ist der häufigste Fehler und der wichtigste Punkt. |
| 2 | **KEINE MUSIK.** Kein Beat, kein Jingle, kein Hintergrundbett. Nur Stimme und Soundeffekte. |
| 3 | **Kein Gesicht.** Mortaza wird nie gezeigt, keine Fotos oder Videos von Personen, keine KI-Menschen. |
| 4 | **Keine Stockvideos, keine KI-Bilder, die echte Arbeit vortäuschen.** Alles ist Motion Design in den Markenfarben plus das Maskottchen. |
| 5 | **Kein Vorher-Nachher, keine Kundennamen, keine Objekte von Kunden.** |
| 6 | **Nur Aussagen aus dem Faktenregister** über Habibi Reinigung. Beträge nur CHF 650, 15, 35. |
| 7 | **Keine erfundenen Zahlen, Studien oder Statistiken.** Eine Zahl ohne Quelle kommt nicht vor. |
| 8 | **Verbotene Themen und Wörter** nach Abschnitt 11 kommen in Sprechtext, Bildtext und Caption nicht vor. |
| 9 | **Schweizer Schreibweise (ss statt ß). Keine Gedankenstriche.** Weder im Bild noch in der Caption. |
| 10 | **Veröffentlicht wird nur, was Mortaza in der App freigegeben hat**, und nur um 10:00, 12:00 oder 18:00. |

---

## 3. KEINE PAUSEN (eigener Abschnitt, weil es der wichtigste Punkt ist)

Ein Reel verliert den Zuschauer in jeder Zehntelsekunde Stille. Deshalb:

**Im Sprechtext**
- Der Tag `[short pause]` ist **verboten**. Ebenso `[pause]`, `[long pause]`, Auslassungspunkte als Pause und leere Zeilen im Text.
- Keine Dramaturgie durch Schweigen. Spannung entsteht durch Betonung und Lautstärke, nicht durch Warten.

**In der Tonspur**
- Lücken zwischen den Phrasen: **Standard 0.10 s**, höchstens **0.18 s** und nur einmal pro Video, direkt vor der Pointe.
- Das Reel beginnt mit Stimme bei **0.15 s** (V0). Vorher keine Stille, der Ton des ersten Effekts läuft schon.
- Am Schluss nach dem letzten Wort höchstens **0.85 s** (für den Knopf), danach ist das Video zu Ende.
- Atemgeräusche und Zögerer («ähm», Einatmen vor einem Satz) wegschneiden. `fabrik.py phrasen` findet sie, `straffen` entfernt sie.
- Sprechtempo nach dem Straffen: **2.6 bis 3.2 Wörter pro Sekunde**. Darunter klingt es müde. Tempo 1.08 ist der Standard, bei der eigenen Stimme 1.04 bis 1.08 je nach Aufnahme.

**Im Bild**
- Keine Szene ohne Bewegung, auch nicht am Schluss (der Knopf pulsiert, die Figur wippt).
- Kein Schwarzbild, kein Ein- oder Ausblenden über Schwarz, kein Intro, kein Abspann.
- Keine Szene länger als rund 5 Sekunden ohne neues Element.

**Prüfung:** Nach dem Mischen die Tonspur ansehen. Jede Stille über 0.25 s ist ein Fehler und wird gekürzt.

---

## 4. Die Stimme

### 4.1 Welche Stimme

| Zweck | Stimme | voice_id |
| --- | --- | --- |
| **Standard** | «Mortaza» (eigene geklonte Stimme, energetisch) | `VKHUKjVIrEtrinPsbI1G` |
| Ausweichstimme | «Lenny – Casual Creator Voice» | `6IEvIqBOPOMUc5HwR9sQ` |

Modell: **`eleven_v3`**, Sprache Deutsch. Die eigene Stimme ist seit 06.10.2026 ausdrücklich erlaubt und erwünscht; das Gesicht bleibt trotzdem immer aussen vor. Nie eine andere Stimme nehmen, ohne dass Mortaza es sagt. Werkzeug: `creative_generate_speech`, danach `creative_get_flow_run_status` abfragen. `generations_count: 1` (Credits sparen), einen fehlgeschlagenen Aufruf **nie blind wiederholen**, das kostet doppelt.

### 4.2 Wie die Stimme klingen muss

Nicht vorlesen, sondern **erzählen und begeistern**. Mortaza hat eine erste Fassung als «zu flach» zurückgewiesen; es fehlten Motivation und Elan. Die drei Werkzeuge dafür:

1. **Betonung:** Pro Satz genau ein Wort in GROSSBUCHSTABEN. Das ist der Druckpunkt. Mehr als eines pro Satz hebt sich auf.
2. **Aussprache:** Zahlen und die Webadresse ausgeschrieben, damit die KI sie nicht verschluckt. «SECHSHUNDERTFÜNFZIG Franken», «habibireinigung Punkt C-H». Keine Abkürzungen, kein «ca.», kein «z.B.».
3. **Lautstärke:** Der Verlauf über das Video ist ein Bogen. Hook mittel und neugierig, Auflösung laut, Erklärung ruhiger, Schluss wieder laut.

### 4.3 Emotions-Tags

Erlaubt sind die Tags von ElevenLabs v3. Sie stehen **vor** dem Satz, auf den sie wirken. Nicht mehr als ein Tag pro Satz, und nicht in jedem Satz.

| Tag | Wofür |
| --- | --- |
| `[curious]` | Hook als Frage |
| `[sarcastic]` | Wenn die Branchenüblichkeit vorgeführt wird («Preis auf Anfrage») |
| `[excited]` | Auflösung, gute Nachricht, Markenname am Schluss |
| `[intense]` | Der harte Kern, die Warnung, das Problem |
| `[warmly]` | Die Zusage, der freundliche Zusatz |
| `[laughs]` | Sparsam, höchstens einmal, nur wenn der Satz wirklich lustig ist |

Verboten: `[short pause]` und jede andere Pausenanweisung (Abschnitt 3), Flüstern, Weinen, Schreien, Dialekt-Anweisungen.

### 4.4 Nachbearbeitung (macht `fabrik.py straffen`)

Pausen kürzen, Tempo 1.08, dann die Kette:
`highpass=f=80` (Rumpeln weg), `equalizer=f=3200:t=q:w=1.2:g=2.5` (Verständlichkeit), `acompressor=threshold=-18dB:ratio=2` (gleichmässig laut), `loudnorm=I=-14:TP=-1.2:LRA=11` (Instagram-Lautheit).

### 4.5 Lizenz und Credits

- Videos entstehen **nur, solange ein bezahltes ElevenLabs-Abo aktiv ist**. Der Gratisplan (10'000 Credits) enthält keine kommerzielle Lizenz, und ein Firmen-Reel ist kommerzielle Nutzung. Läuft das Abo aus: keine Stimme erzeugen, Mortaza melden.
- Verbrauch: etwa 1 Credit pro Zeichen Sprechtext. Ein Reel von 15 s kostet rund 270, eines von 24 s rund 450 Credits. Mit 30'000 Credits im Monat sind rund 60 Reels möglich, also reichlich für 4 pro Woche.
- Credits sind aufgebraucht oder ein Aufruf schlägt fehl: abbrechen und melden, nie blind wiederholen.

---

## 5. Der Sprechtext

### 5.1 Länge und Aufbau

- **12 bis 25 Sekunden**, 30 bis 60 Wörter. Kürzer als 12 s wirkt dünn, länger als 25 s verliert Zuschauer. Nie über 60 s.
- **Satz 1: Hook.** Höchstens 7 Wörter.
- **Mitte: 2 bis 4 Sätze.** Je ein Gedanke, je ein Hauptsatz. Keine Nebensatzketten, kein «welches», «wobei», «sodass».
- **Schluss: immer die Marke und der Rechner.** Wortlaut: «Habibi Reinigung! Richtpreis in EINER Minute, auf habibireinigung Punkt C-H!» Varianten sind erlaubt, aber «habibireinigung Punkt C-H» steht genau so da.
- Ansprache: **du und ihr** (Büros: ihr). Nie Sie. Nie «man».

### 5.2 Hook-Muster (eines auswählen)

| Muster | Beispiel |
| --- | --- |
| Frage, die weh tut | «Was kostet eigentlich eine Büroreinigung in Chur?» |
| Mythos umdrehen | «Mehr Putzmittel heisst sauberer? Falsch.» |
| Jahreszeit oder Anlass | «Heizung läuft wieder?» |
| Branchen-Insider | «Darum steht überall «Preis auf Anfrage».» |
| Zahl plus Lücke | «Drei Stellen, die in jedem Büro vergessen gehen.» |
| Direkter Widerspruch | «Euer Büro ist nicht sauber. Es ist nur aufgeräumt.» |

Verboten im Hook: Begrüssung («Hallo zusammen», «Guten Tag»), Firmenname zuerst, «In diesem Video zeige ich dir», «Wusstest du, dass», eine Frage, die man mit Ja beantwortet und weiterwischt.

### 5.3 Inhalt und Säulen

Abwechseln, dasselbe Thema frühestens nach 8 Wochen wieder (letzte Themen in `instagram/reels/index.json` und in der App nachsehen):

- **mythos:** Eine verbreitete Annahme, dann die Korrektur. Stärkste Säule, weil Widerspruch Kommentare auslöst.
- **tipp:** Ein praktischer Reinigungstipp für Büro, Praxis, Studio. Aus der Praxis, sachlich richtig, sofort umsetzbar.
- **transparenz:** Wie Habibi Reinigung arbeitet (fester Monatspreis, keine Mindestlaufzeit, immer dieselben Leute, Besichtigung, Zonen, Einsatzzeiten).
- **lokal:** Chur und Umgebung, Jahreszeit, Wetter, immer mit Bezug zur Reinigung.
- **checkliste:** 3 bis 4 Punkte zum Merken.

Zielgruppe: Inhaber und Office-Verantwortliche von Büros, Praxen, Kanzleien und Studios in Chur und Umgebung, dazu Private aus der Region. Ton: freundlich, konkret, selbstsicher, nie marktschreierisch, nie bittend.

---

## 6. Bild und Grafik

### 6.1 Marke

| | |
| --- | --- |
| Farben | Navy `#152a43`, Navy-Tief `#0a1826`, Stahl `#2c6693`, Eis `#eef3f7`, Hellblau `#9fd3ee`, Weiss, Rot `#e5484d` (nur für Fehler und Durchstreichen) |
| Schrift gross | Poppins 900, Laufweite -0.02em |
| Schrift Betonung | Instrument Serif italic (für das eine hervorgehobene Wort pro Szene) |
| Schrift klein | Poppins 700 und 500 |
| Figur | `assets/maskottchen.png`, das Habibi-Maskottchen. Es gibt Tipps, springt rein, wippt. Es ist die wiedererkennbare Figur der Marke. |
| Wortmarke | `assets/wortmarke.png`, nur in der Abschlussszene |
| Korn | `assets/grain.png`, 7 Prozent, über allem. Nimmt das Digitale weg. |

Hintergrund pro Szene wechseln (Navy, Hellblau, Eis), damit ein Schnitt sichtbar ist.

### 6.2 Text im Bild

- **Kürzer als der Sprechtext.** Das Bild zeigt Stichworte, nicht den Satz. Höchstens 4 bis 5 Wörter pro Zeile, höchstens 3 Zeilen pro Szene.
- Schriftgrösse für die Hauptaussage **100 bis 140 px**, der Knaller-Begriff bis 380 px. Nie unter 54 px, das liest auf dem Handy niemand.
- **Ein Begriff pro Szene in Serif-Kursiv** hervorheben, nicht mehr.
- **Freiräume:** Oben 220 px und unten 380 px bleiben frei von wichtigem Text (dort liegen Instagram-Caption, Profilname und Knöpfe).
- Niemals `<br>` im HTML (HyperFrames verträgt es nicht), stattdessen eigene Zeilen-Elemente.

### 6.3 Szenen-Baukasten (`vorlagen/reel/szenen.py`)

| Szene | Wofür |
| --- | --- |
| `hook` | Riesentext mit steigenden Seifenblasen. Der Einstieg. |
| `punch` | Ein Wort knallt rein, Bildschirm wackelt, Balken schiesst auf. Die Auflösung. |
| `durchstreichen` | Graue Karte fällt rein, roter Strich darüber, sarkastischer Untertitel. Für «so macht es die Branche». |
| `stempel` | Behauptung steht, Stempel FALSCH oder RICHTIG knallt darauf. Für Mythen. |
| `liste` | 2 bis 4 Punkte fliegen von links ein, Häkchen zeichnet sich. Für Checklisten. |
| `preis` | Zahl zählt auf 650 hoch, Stempel «ALLES INBEGRIFFEN». |
| `zone` | 5-km-Ring um Chur, Pin fällt, Abzeichen «ohne Zuschlag». |
| `heizung` | Heizkörper mit Wärmewellen, Staubwirbel oder Bürste von oben nach unten. |
| `maskottchen_tipp` | Figur springt rein, Sprechblase wechselt den Text. Der «Tipp vom Profi». |
| `abschluss` | Wortmarke, «Richtpreis für euer Büro in 1 Minute», Knopf habibireinigung.ch, Figur. **Immer die letzte Szene.** |

Reicht keine Szene, eine neue in `szenen.py` nach demselben Muster bauen (HTML, CSS, GSAP, Soundeffekte) und hier in der Tabelle ergänzen. Nie ausserhalb der Markenfarben und Schriften.

### 6.4 Schnitt und Timing

- **4 bis 7 Szenen** pro Video.
- Jeder Szenenwechsel liegt **auf einer Phrasengrenze** der Stimme, und zwar 0.05 bis 0.10 s **davor**. So wirkt der Schnitt getrieben, nicht hinterher.
- Einblendungen sitzen auf dem betonten Wort, nicht danach.
- Einfahrten kurz und hart: 0.16 bis 0.4 s, `back.out` oder `power4.in`. Nichts blendet langsam ein.

---

## 7. Ton

- **Keine Musik.** Punkt.
- Soundeffekte aus `vorlagen/reel/klang.py`, alle selbst erzeugt und damit lizenzfrei: whoosh, thump, impact, pop, tick, boing, squeak, smear, scratch, chime, glitzer, ding, riser, stamp.
- **Jede sichtbare Bewegung bekommt einen Effekt**, und zwar 0.05 bis 0.1 s vor dem Bild (Whoosh als Anlauf) oder genau auf dem Treffer (Thump, Stempel).
- Effekte liegen **unter** der Stimme: automatisches Ducking um 35 Prozent, sobald gesprochen wird. Die Stimme ist immer das Lauteste.
- Spitze höchstens 0.93, 48 kHz, stereo. Gesamtlautheit um -14 LUFS.
- Kein Effekt-Teppich: höchstens etwa 2 Effekte pro Sekunde, sonst wird es Lärm.

---

## 8. Technische Vorgaben

| | |
| --- | --- |
| Auflösung | 1080 x 1920 (9:16), 30 fps |
| Länge | 12 bis 25 s (Grenze 3 bis 60 s) |
| Video | H.264, High Profile, yuv420p, crf 20, faststart |
| Ton | AAC 192 kbit/s, 48 kHz |
| Dateigrösse | **höchstens 19.5 MB** (die Auslieferung über jsDelivr bricht bei 20 MB ab) |
| Titelbild | JPG aus dem fertigen Video, aus einem Moment mit vollständigem Text, nie aus einem Übergang |
| Dateinamen | `<post_id>.mp4` und `<post_id>_titel.jpg`, post_id im Format `IG-JJJJ-MM-TT-r1` |

---

## 9. Caption

Aufbau, genau in dieser Reihenfolge:

1. **Zeile 1: der Haken**, als Frage oder klare Aussage. Darf dem Sprech-Hook gleichen, muss aber ohne Ton funktionieren.
2. **2 bis 4 kurze Zeilen Nutzen.** Was der Leser davon hat.
3. **Ein Aufruf:** «Richtpreis in 1 Minute: Link in der Bio» oder «Speichern für später».
4. **5 bis 8 Hashtags**, lokal und thematisch: `#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung`.

Höchstens 2200 Zeichen, höchstens 15 Hashtags, höchstens 2 Emojis. Keine Links im Text (Instagram macht sie nicht klickbar). Keine verbotenen Wörter, keine Beträge ausser 650, 15, 35.

---

## 10. Prüfliste vor dem Hochladen (alle Punkte, jedes Mal)

**Stimme**
- [ ] Kein Pausen-Tag im Text, keine Lücke über 0.25 s in der Tonspur
- [ ] 2.6 bis 3.2 Wörter pro Sekunde
- [ ] Pro Satz genau ein betontes Wort, Zahlen und Webadresse ausgeschrieben
- [ ] «habibireinigung Punkt C-H» ist verständlich gesprochen (im Zweifel mit `creative_transcribe_audio` prüfen)

**Bild**
- [ ] `hyperframes check` ohne Fehler
- [ ] Einzelbilder angesehen: kein abgeschnittener Text, nichts überlappt, alles lesbar
- [ ] Oben 220 px und unten 380 px frei von wichtigem Text
- [ ] Figur und Wortmarke vollständig im Bild
- [ ] Keine Szene steht still

**Ton**
- [ ] Keine Musik
- [ ] Stimme deutlich lauter als die Effekte
- [ ] Lautheit um -14 LUFS

**Inhalt**
- [ ] Keine verbotenen Wörter in Sprechtext, Bildtext und Caption
- [ ] Alle Aussagen über die Firma stehen im Faktenregister
- [ ] Beträge nur 650, 15, 35
- [ ] Keine Zahl ohne Quelle
- [ ] Thema in den letzten 8 Wochen nicht verwendet

**Technik**
- [ ] 1080 x 1920, 30 fps, 12 bis 25 s, unter 19.5 MB, Tonspur vorhanden
- [ ] Titelbild zeigt vollständigen Text

Scheitert ein Punkt: beheben und neu rendern, höchstens 3 Runden. Bleibt es schlecht: **nicht hochladen**, Mortaza melden, was nicht geht.

---

## 11. Verbote

**Wörter** (weder gesprochen, noch im Bild, noch in der Caption): haftpflicht, versichert, versicherungsschutz, unsere versicherung, umzugsreinigung, endreinigung, wohnungsreinigung, privatreinigung, fensterreinigung, rabatt, gratis, aktion, 2 personen, zwei personen, newsletter.

**Inhalte:** Versicherungsfragen, Privat-, Umzugs-, End- und Wohnungsreinigung bewerben, Fensterreinigung aktiv bewerben, Rabatte und Aktionen, Teamgrösse nennen, Annahmen über den heutigen Reiniger der Firma, Komplimente ohne Fakt, Kundennamen, Preise ausser 650, 15, 35.

**Formales:** Musik, Gedankenstriche, ß, Gesicht, fremde Logos, geschützte Bilder, Stockmaterial.

**Was es nie wieder geben darf:** die statischen Textkarten-Reels aus `medien.py`. Mortaza hat sie abgelehnt. `medien.py` erzeugt nur noch Karussells und Bilder, Reels entstehen ausschliesslich über den Reel-Baukasten.

---

## 12. Beispiele, die Mortaza angenommen hat

### «Preis auf Anfrage? Nicht bei uns.» (24 s, Säule transparenz)

Sprechtext (Original mit `[short pause]`; dieser Tag ist seit Version 1.0 verboten, Text sonst unverändert gut):

> `[curious]` Was kostet eigentlich eine Büroreinigung in Chur? `[sarcastic]` «Preis auf Anfrage»… super hilfreich. `[excited]` Bei uns steht der Preis DA! Büros ab SECHSHUNDERTFÜNFZIG Franken im Monat. ALLES inbegriffen! `[intense]` Fester Monatspreis. KEINE Mindestlaufzeit. `[warmly]` Und bis fünf Kilometer ab Chur: ohne Zuschlag. `[excited]` Habibi Reinigung! Euren Richtpreis rechnet ihr in EINER Minute aus, auf habibireinigung Punkt C-H!

Szenenfolge: `hook` (Was kostet Büroreinigung in Chur?) → `durchstreichen` («Preis auf Anfrage» mit rotem Strich) → `punch` (DA.) → `preis` (650 zählt hoch, Stempel ALLES INBEGRIFFEN) → `maskottchen_tipp` (Fester Monatspreis / Keine Mindestlaufzeit) → `zone` (5 km ab Chur) → `abschluss`.

### «Heizung läuft wieder?» (15 s, Säule lokal)

> `[excited]` Heizung läuft wieder? `[intense]` Dann wirbelt sie den Staub vom GANZEN Sommer durchs Büro! `[excited]` Also JETZT Heizkörper abstauben, auch ZWISCHEN den Rippen! `[warmly]` Von oben nach unten. `[excited]` Habibi Reinigung! Richtpreis auf habibireinigung Punkt C-H!

Szenenfolge: `heizung` (waerme, «Heizung läuft wieder?») → `heizung` (staub, «Staub vom ganzen Sommer») → `maskottchen_tipp` (Jetzt abstauben / Auch zwischen den Rippen) → `heizung` (buerste, «Von oben nach unten») → `abschluss`.

---

## 13. Ablauf und Dateien

**Ablauf eines Videos** (Einzelheiten in `vorlagen/reel/FABRIK.md`):

1. Thema und Termin wählen (Reel-Termine: Mo 18:00, Mi 18:00, Fr 12:00, So 10:00).
2. Sprechtext nach Abschnitt 5 schreiben.
3. Stimme erzeugen (Abschnitt 4).
4. Audio über die GitHub-Action «Audio holen» in den Arbeitsbereich holen (die Cloud kann die ElevenLabs-Adresse nicht direkt laden).
5. Phrasen bestimmen, Stimme straffen (`fabrik.py phrasen`, `fabrik.py straffen`).
6. Szenen auf die Phrasenzeiten setzen, rendern (`fabrik.py render`).
7. Einzelbilder ansehen, Ton mischen, zusammenführen (`fabrik.py fertig`).
8. Prüfliste Abschnitt 10 abarbeiten.
9. Video, Titelbild und `ig_post.json` ins Repo legen, `instagram/reels/index.json` ergänzen.
10. Der Tageslauf übernimmt es in die App, Mortaza gibt frei, die Aufgabe «Instagram posten» veröffentlicht es.

**Wo was liegt**

| Datei | Inhalt |
| --- | --- |
| `vorlagen/reel/VIDEO-REGELN.md` | diese Datei, die Regeln |
| `vorlagen/reel/FABRIK.md` | technischer Ablauf, Befehle |
| `vorlagen/reel/fabrik.py` | Hilfsbefehle (Umgebung, Phrasen, Straffen, Render, Bilder, Fertig) |
| `vorlagen/reel/szenen.py` | Szenen-Baukasten |
| `vorlagen/reel/klang.py` | Soundeffekte und Endmischung |
| `vorlagen/reel/stimme.py` | Pausen kürzen, Tempo, Lautheit |
| `vorlagen/reel/fakten.json` | Faktenregister (Kopie) |
| `vorlagen/reel/assets/` | Schriften, Maskottchen, Wortmarke, Korn |
| `instagram/reels/index.json` | welche Reels es gibt und welche Themen schon gelaufen sind |

Alles im Repo **HabibiReinigung/Marketing**. Auf dem Laptop liegt diese Datei zusätzlich unter `claude\VIDEO-REGELN.md`.

---

## 14. Änderungen an diesen Regeln

Diese Datei ändert nur Mortaza oder Claude auf seine Anweisung. Wenn er ein Video kritisiert, gehört die Lehre daraus **hier hinein**, nicht nur in die Antwort im Chat. Dann Version und Datum oben hochzählen und unten eine Zeile anfügen.

| Version | Datum | Änderung |
| --- | --- | --- |
| 1.0 | 07.10.2026 | Erste Fassung. Qualitätsmassstab, Pausenverbot, eigene Stimme als Standard, Hook-Muster, Szenen-Baukasten, Prüfliste. |
