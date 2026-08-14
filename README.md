# Bref — On a fait une crémaillère

Montage vidéo style "Bref" pour une crémaillère, avec voix off générée automatiquement.

## Structure du projet

- `script.md` — script minuté complet fourni par l'utilisateur
- `photos/` — photos de l'appartement (à fournir, groupées par moment du script si possible)
- `audio/` — voix off générée (échantillons de voix + narration finale)
- `work/` — fichiers de travail intermédiaires (segments, sous-titres, etc.)
- `output/` — vidéo finale

## Pipeline technique

- **ffmpeg** pour le montage (Ken Burns, transitions, texte incrusté, synchro audio)
- **edge-tts** (voix neuronale Microsoft, gratuite) pour la voix off en français
