# Label2OTO
This script converts Audacity label files to oto.ini for UTAU. Drag and drop a prepared voicebank folder onto main.py to run.

## Settings
JSON files containing lists of phonemes and alias spacers used an a given reclist. Used to validate phonemes in labels and to adjust OTO parameters. See existing files for format.

## Labels
Each wav file in the voicebank has one corresponding label file, with the same name as the wav file.

Required labels:
- "start": Single point, at 0 sec
- "end": Single point, at the end of the final phoneme
- For each phoneme
    - phoneme: Single point, at the start of the phoneme. Used for preuttetrance when it's the second phoneme in an alias.
    - "-": Region, spanning the stable/stretchable part of the phoneme. For stop/non-continuous consonants, this should span the silent gap before the consonant sound.