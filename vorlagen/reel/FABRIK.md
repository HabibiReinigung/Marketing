# Reel-Fabrik Habibi Reinigung (Anleitung für den geplanten Cloud-Lauf)

> **Zuerst `VIDEO-REGELN.md` im selben Ordner lesen.** Dort stehen die verbindlichen Regeln zu Hook, Stimme, Emotion, Bild, Ton und Schnitt (inklusive Pausenverbot; Stimme ist Lenny). Diese Datei hier beschreibt nur den technischen Ablauf.

Ziel: 4 Reels pro Woche, vollautomatisch erstellt, in der Qualität der bisherigen Reels (Motion Design, KI-Stimme mit Energie, Soundeffekte, KEINE Musik). Mortaza gibt jedes Reel in seiner App frei, erst dann wird es gepostet.

## 0. Ablauf auf einen Blick

```
Reel-Fabrik (Cloud, täglich)        -> instagram/<post_id>/ + instagram/reels/index.json (GitHub)
Tageslauf 22:10 (Laptop)            -> holt neue Reels in die App, schreibt instagram/reels/status.json
Mortaza gibt in der App frei        -> Instagram vorbereiten 23:50 trägt in instagram/plan.json ein
Instagram posten (Cloud)            -> veröffentlicht zur geplanten Zeit über Windsor
```

## 1. Reel-Termine (fest)

| Tag | Zeit |
| --- | --- |
| Montag | 18:00 |
| Mittwoch | 18:00 |
| Freitag | 12:00 |
| Sonntag | 10:00 |

Die übrigen Tage (Di, Do, Sa) gehören den Karussells und Bildern des Tageslaufs.

`post_id` der Fabrik: `IG-JJJJ-MM-TT-r1` (Datum = Termin). Bei einem zweiten Versuch für denselben Termin `-r2`, `-r3`.

## 2. Was ist zu tun? (Reihenfolge)

1. `instagram/reels/index.json` (eigene Liste der Fabrik) und `instagram/reels/status.json` (Stand der App, vom Tageslauf) lesen.
2. **Änderungswunsch zuerst:** Steht in status.json ein Reel der Fabrik mit `status: "aenderung"` und Termin mindestens 2 Tage in der Zukunft: dasselbe Reel mit derselben `post_id` neu bauen und den Wunsch (`aenderung`) umsetzen. In index.json `version` erhöhen, `import_noetig: true`.
3. **Sonst den nächsten freien Termin:** Reel-Termine von übermorgen bis in 8 Tagen. Frei ist ein Termin, wenn
   - in index.json kein Reel für dieses Datum steht, das nicht `abgelehnt` ist (Status aus status.json, falls dort vorhanden), und
   - in status.json kein anderer Beitrag mit genau diesem Datum und dieser Zeit steht (ausser `abgelehnt`).
   Abgelehnt heisst: Mortaza wollte es nicht. Für diesen Termin ein neues Reel mit anderem Thema und neuer post_id (`-r2`).
4. Pro Lauf höchstens **1 Reel**. Kein freier Termin: nur «Nichts zu tun» melden, keine Credits verbrauchen.

## 3. Thema und Text

**Säulen** abwechseln (letzte Säule in index.json ansehen): `mythos` (Mythos oder Fakt), `tipp` (Reinigungstipp für Büro, Praxis, Studio), `transparenz` (wie Habibi Reinigung arbeitet), `lokal` (Chur, Jahreszeit, Wetter, mit Bezug zur Reinigung), `checkliste` (3 Stellen, die oft vergessen gehen).

- Kein Thema wiederholen, das in index.json oder status.json in den letzten 8 Wochen vorkam.
- Zielgruppe: Inhaber und Office-Verantwortliche von Büros, Praxen, Kanzleien, Studios in Chur. Du-/Ihr-Form.
- Nur Aussagen aus `fakten.json` (Faktenregister) über Habibi Reinigung. Keine erfundenen Zahlen oder Studien. Tipps aus der Praxis, sachlich richtig.
- **Nie:** Versicherung/Haftpflicht, Umzugs-, End-, Wohnungs-, Privat- oder Fensterreinigung, Rabatte, Gratis, Aktionen, Teamgrösse, Kundennamen, Vorher-Nachher, Gedankenstriche. Beträge nur 650, 15, 35 (CHF).

**Sprechtext** (für die Stimme), keine Längenvorgabe:
- Satz 1 = Haken (Frage oder steile These), sofort Spannung.
- Mitte: 2 bis 4 kurze Sätze, je ein Gedanke.
- Schluss immer: «[excited] Habibi Reinigung! Richtpreis in EINER Minute, auf habibireinigung Punkt C-H!» (Varianten erlaubt, aber «habibireinigung Punkt C-H» genau so).
- ElevenLabs v3 Tags für Emotion: `[excited]`, `[intense]`, `[curious]`, `[sarcastic]`, `[warmly]`. **Pausen-Tags sind verboten** (VIDEO-REGELN Abschnitt 3). Betonte Wörter in GROSSBUCHSTABEN (sparsam, 1 pro Satz). Zahlen ausschreiben («SECHSHUNDERTFÜNFZIG»). Keine Abkürzungen.
- Beispiele: `vorlagen/reel/reel_preis.py` und `reel_heizung.py` (Texte in FABRIK.md Abschnitt 9).

**Wort-Zeitstempel:** nach dem Erzeugen `creative_transcribe_audio` auf den Sprach-Knoten (`connect_from`, kostet nichts). Die Wortzeiten mit `karte.json` umrechnen und die Szenen daran haengen. Siehe VIDEO-REGELN Abschnitt 18.3.

## 4. Stimme (ElevenLabs)

- Stimme «Lenny» `voice_id 6IEvIqBOPOMUc5HwR9sQ`, Modell `eleven_v3`, Sprache Deutsch.
- `creative_generate_speech` mit dem Sprechtext. Falls nötig Parameter mit `creative_get_model_schema` prüfen. `generations_count: 1` (Credits sparen). Danach `creative_get_flow_run_status` abfragen, bis fertig. Nie denselben Aufruf blind wiederholen.
- Optional (empfohlen): `creative_transcribe_audio` auf den Sprach-Knoten. Stimmt der Text nicht (v.a. «habibireinigung Punkt C-H», Zahlen): genau einmal neu erzeugen, Text leicht anpassen (z.B. Bindestriche, Schreibweise).
- Credits fehlen / Fehler: abbrechen und melden («ElevenLabs: keine Credits»).

## 5. Audio holen (Brücke über GitHub)

Die Cloud darf storage.googleapis.com nicht direkt laden. Deshalb:

```bash
cd /home/claude/marketing
echo '{"url": "<audio-URL aus ElevenLabs>"}' > werkstatt/audio/<post_id>.json
git add werkstatt/audio/<post_id>.json && git commit -m "Audio anfordern <post_id>" && git push
# warten, bis die GitHub Action «Audio holen» die Datei bringt (meist unter 2 Minuten):
for i in $(seq 1 40); do git pull -q --rebase; ls werkstatt/audio/<post_id>.* | grep -v json && break; sleep 15; done
```

Ergebnis `werkstatt/audio/<post_id>.mp3` (oder .wav). Bei `<post_id>.fehler` oder nach 10 Minuten nichts: abbrechen und melden.
Danach `werkstatt/audio/<post_id>.json` stehen lassen (nicht löschen).

## 6. Bauen

```bash
R=/home/claude/marketing/vorlagen/reel; W=/tmp/reel/<post_id>; mkdir -p $W
python3 $R/fabrik.py umgebung
python3 $R/fabrik.py phrasen werkstatt/audio/<post_id>.mp3          # Phrasen + Lautstärke-Karte
#  -> Phrasen den Sätzen zuordnen, Namen P1..Pn, als [[name, start, ende], ...] in $W/phrasen.json
python3 $R/fabrik.py straffen werkstatt/audio/<post_id>.mp3 $W/phrasen.json $W   # stimme.wav, zeiten.json, karte.json
python3 $R/fabrik.py projekt $W
#  -> $W/reel.py schreiben (Vorlage: reel_preis.py / reel_heizung.py), Szenen an die Phrasen-Zeiten hängen
python3 $W/reel.py $W/zeiten.json $W
python3 $R/fabrik.py render $W
python3 $R/fabrik.py bilder $W 0.6 2.0 4.0 6.0 9.0 12.0 <Ende-1>     # Einzelbilder, jedes mit Read ansehen
python3 $R/fabrik.py fertig $W <post_id> /home/claude/marketing/instagram/<post_id> <titelbild_s>
```

In `reel.py` gilt `T = json.load(open(sys.argv[1]))` (direkt das Objekt aus zeiten.json, ohne Schlüssel wie 'preis').

**Szenen** (alle in `szenen.py`, Zeiten in Sekunden, A('P3', .2) = 0.2 s nach Beginn von P3):
- `hook` Riesentext mit Blasen (Haken), `punch` ein Wort knallt rein, `durchstreichen` Karte + roter Strich,
- `stempel` Behauptung + Stempel FALSCH/RICHTIG (Mythos), `liste` Checkliste mit Häkchen (2 bis 4 Punkte, kurz),
- `preis` Zähler bis 650, `zone` 5-km-Ring Chur, `heizung` Heizkörper (waerme/staub/buerste),
- `maskottchen_tipp` Figur mit Sprechblase (der «Tipp vom Profi»), `abschluss` Wortmarke + «Richtpreis in 1 Minute» + Knopf habibireinigung.ch (immer am Schluss).
- Jede Szene beginnt kurz (0.05 bis 0.1 s) vor ihrer Phrase. Texte auf dem Bild sind KÜRZER als der Sprechtext (Stichworte). Szenenwechsel genau auf Phrasengrenzen.
- Neue Szene nötig? In `szenen.py` nach dem Muster der vorhandenen bauen (HTML + CSS + GSAP + Soundeffekte), Markenfarben (var(--navy), --steel, --ice, --blue), Schriften Poppins/Instrument Serif.

**Technikregeln HyperFrames:** ein pausierter GSAP-Timeline `tl` (macht `szenen.py`), keine `<br>`, kein Math.random (nur `rnd()`), jede Szene ist ein `.clip` mit data-start/data-duration (macht `szenen.py`).

## 7. Qualitätsprüfung (Pflicht, vor dem Hochladen)

- `hyperframes check` ohne Fehler (macht `fabrik.py render`).
- Einzelbilder ansehen: kein Text abgeschnitten oder ausserhalb des Bildes, nichts überlappt unschön, Text gut lesbar (Kontrast), oben 220 px und unten 380 px frei von wichtigem Text (Instagram-Bedienelemente), Figur und Wortmarke vollständig.
- Ton: Stimme klar und laut (fabrik.py zeigt die Lautheit, Ziel um -14 LUFS), Effekte leiser als die Stimme, keine Musik.
- `fabrik.py fertig` meldet «Prüfungen OK» (höchstens 19.5 MB, 1080x1920, Ton vorhanden).
- Probleme beheben und neu rendern (höchstens 3 Runden). Bleibt es schlecht: nicht hochladen, melden.

## 8. Ablegen und melden

1. `instagram/<post_id>/<post_id>.mp4` und `<post_id>_titel.jpg` (macht `fabrik.py fertig`).
2. `instagram/<post_id>/ig_post.json`: genau das `daten`-Objekt für die App:
```json
{"post_id": "IG-2026-10-12-r1", "datum": "2026-10-12", "zeit": "18:00", "format": "reel",
 "thema": "…", "saeule": "tipp", "caption": "…",
 "spec": {"szenen": [{"text": "…"}], "schluss": {"text": "Richtpreis für euer Büro in 1 Minute", "knopf": "habibireinigung.ch"}, "sprechtext": "…"},
 "medien": [{"datei": "IG-2026-10-12-r1.mp4", "typ": "video"}, {"datei": "IG-2026-10-12-r1_titel.jpg", "typ": "titelbild"}],
 "ordner": "instagram/IG-2026-10-12-r1", "warnungen": []}
```
   `spec.szenen[].text` = die Texte auf dem Bild (die App prüft sie auf verbotene Wörter).
3. **Caption:** erste Zeile ein Haken, dann 2 bis 4 kurze Zeilen Nutzen, dann «Richtpreis in 1 Minute: Link in der Bio», dann 5 bis 8 Hashtags (#chur #graubünden #büroreinigung #reinigungchur #unterhaltsreinigung #praxisreinigung #habibireinigung). Keine Links, höchstens 2 Emojis, Schweizer Schreibweise (ss), keine Gedankenstriche, höchstens 2200 Zeichen.
4. `instagram/reels/index.json` ergänzen: `{"post_id", "datum", "zeit", "thema", "saeule", "sprechtext", "erstellt_am", "version": 1, "import_noetig": true}`.
5. Commit «Reel <post_id>» und push (bei Konflikt `git pull --rebase` und nochmals).
6. Bericht (eine bis drei Zeilen): post_id, Termin, Thema, Dauer, Credits ungefähr.

## 9. Beispieltexte (gut bewertet)

Preis (24 s): «[curious] Was kostet eigentlich eine Büroreinigung in Chur? [sarcastic] «Preis auf Anfrage»… super hilfreich. [excited] Bei uns steht der Preis DA! Büros ab SECHSHUNDERTFÜNFZIG Franken im Monat. ALLES inbegriffen! [intense] Fester Monatspreis. KEINE Mindestlaufzeit. [warmly] Und bis fünf Kilometer ab Chur: ohne Zuschlag. [excited] Habibi Reinigung! Euren Richtpreis rechnet ihr in EINER Minute aus, auf habibireinigung Punkt C-H!»

Heizung (15 s): «[excited] Heizung läuft wieder? [intense] Dann wirbelt sie den Staub vom GANZEN Sommer durchs Büro! [excited] Also JETZT Heizkörper abstauben, auch ZWISCHEN den Rippen! [warmly] Von oben nach unten. [excited] Habibi Reinigung! Richtpreis auf habibireinigung Punkt C-H!»

## 10. Verboten

Selbst auf Instagram posten, plan.json ändern (das macht nur «Instagram vorbereiten»), Kundendaten ins Repo, Musik, Stockvideos, KI-Bilder von Menschen oder angeblicher echter Arbeit, Gesicht oder Stimme von Mortaza, mehr als 1 Reel pro Lauf.
