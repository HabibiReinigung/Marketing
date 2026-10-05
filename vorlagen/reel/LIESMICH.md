# Reel-Baukasten Habibi Reinigung

Motion-Design-Reels (1080x1920) aus HTML/GSAP, gerendert mit HyperFrames. Keine Musik, nur Stimme + selbst erzeugte Soundeffekte.

## Ablauf
1. Text schreiben (Hook, Auflösung, Tipp der Figur, Abschluss «Habibi Reinigung! Richtpreis … habibireinigung Punkt C-H!»).
2. Stimme bei ElevenLabs erzeugen: Stimme «Lenny – Casual Creator Voice» (voice_id 6IEvIqBOPOMUc5HwR9sQ), Modell eleven_v3, Tags wie [excited], [intense], [warmly], betonte Wörter GROSS.
3. Phrasen bestimmen: `python3 -c "from stimme import energie; print(energie('roh.mp3'))"`, dann `straffen()` (Pausen kürzen, Tempo 1.08, Lautheit).
4. Szenen in einem `reel_<name>.py` zusammenstellen (Beispiele: reel_preis.py, reel_heizung.py). Szenen: hook, punch, durchstreichen, preis, maskottchen_tipp, zone, heizung, abschluss.
5. Projektordner mit `assets/` anlegen, `python3 reel_<name>.py zeiten.json <ordner>`, dann `npx hyperframes check`, `npx hyperframes render -o renders/video.mp4 --fps 30 --quality delivery`.
6. Ton mischen: `klang.mischen(stimme.wav, sfx.json, dauer, 0.15, mix.wav)` und mit ffmpeg zusammenführen.

Technik: `npm i hyperframes@0.8.133 gsap@3`, `HYPERFRAMES_BROWSER_PATH` auf chrome-headless-shell setzen.

Regeln: nur Aussagen aus dem Faktenregister der Marketing-App, keine Versicherung, keine Rabatte, keine Privat-/Umzugs-/Fensterreinigung bewerben, Beträge nur aus dem Faktenregister.
