# Label2OTO
This script converts Audacity label files to oto.ini for UTAU. Drag and drop a prepared voicebank folder onto main.py to run.

## Labels
Each wav file in the voicebank has one corresponding label file, with the same name as the wav file.

- For each phoneme
    - phoneme: Single point, at the start of the phoneme. Used for preuttetrance when it's the second phoneme in an alias.
    - "-": Region, spanning the stable/stretchable part of the phoneme. For stop/non-continuous consonants, this should span the silent gap before the consonant sound.
- "end": Single point, at the end of the final phoneme

## Settings
JSON files containing the settings for a given reclist. See existing files in `settings` for examples.
- Spacers: Character used between phonemes for each alias format
- Consonants and vowels: Recognized phonemes, to validate labels and adjust OTO values
- Delete: List of regex strings, to identify aliases that should be deleted from the OTO
- Replace: Dictionary of regex find/replace for modifying aliases

## Preset
You can optionally create a file named `preset.json` in the voicebank folder to preselect options while generating the OTO. You can include as many or as few of these preset options as you want in the file, and will be prompted for any that are missing. See `example-preset.json` for an example.
- "settings": String matching an existing file in the settings folder, or JSON of full settings
- "tempo": Integer recording tempo, used to calculate overlap for when a vowel is the first phoneme. Takes priority over explicit overlap value.
- "overlap": Integer used for overlap when a vowel is the first phoneme.
- "init_preutt": Integer preutterance for the first phoneme in the wav file. Default value `20`, to compensate for UTAU's default envelope shape.
- "handle_dupes": Boolean, for whether or not to number/delete duplicate aliases
- "max_dupes": Integer, maximum amount of duplicate aliases (0 to delete all, -1 to number all)