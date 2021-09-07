# Label2OTO
This script converts Audacity label files to oto.ini for UTAU. Drag and drop a prepared voicebank folder onto main.py to run.

## Settings
JSON files containing the settings for a given reclist. See existing files for samples.
- Spacers: Character used between phonemes for each alias format
- Consonants and vowels: Recognized phonemes, to validate labels and adjust OTO values
- Delete: List of regex strings, to identify aliases that should be deleted from the OTO
- Replace: Dictionary of regex find/replace for modifying aliases

## Labels
Each wav file in the voicebank has one corresponding label file, with the same name as the wav file.

Required labels:
- For each phoneme
    - phoneme: Single point, at the start of the phoneme. Used for preuttetrance when it's the second phoneme in an alias.
    - "-": Region, spanning the stable/stretchable part of the phoneme. For stop/non-continuous consonants, this should span the silent gap before the consonant sound.
- "end": Single point, at the end of the final phoneme