# Label2OTO
This script converts embedded wav markers or Audacity label files to oto.ini for UTAU. Drag and drop a prepared voicebank folder onto main.py to run.

## Labels
The script first attempts to read markers embedded in the wav files. These can be created with:
- ocenaudio
- Image-Line Edison
- Reaper
- Adobe Audition (untested)

If invalid markers or no markers are found, it will look for a text file with the same name as the wav file. Correctly formatted label files can be created with:
- Audacity
- DarkAudacity
- Other Audacity forks that use the same label format as Audacity

The required markers are:
- For each phoneme
    - phoneme: Single point, at the start of the phoneme. Used for preutterance when it's the second phoneme in an alias.
    - "-": Region, spanning the stable/stretchable part of the phoneme. For stop/non-continuous consonants, this should span the silent gap before the consonant sound.
- "end": Single point, at the end of the final phoneme

If you want to use "-" or "end" as phonemes, you can specify other text as the stretch and end labels in the reclist settings.

## Settings
JSON files containing the settings for a given reclist. See existing files in `settings` for examples.
- "stretch": (optional) Alternative text for stretch label
- "end": (optional) Alternative text for end label
- "aliases": Which alias formats to include, spacer characters used between phonemes
- "consonants" and vowels: Recognized phonemes, to validate labels and adjust OTO values
- "delete": List of regex strings, to identify aliases that should be deleted from the OTO
- "replace": Dictionary of regex find/replace for modifying aliases

## Preset
You can optionally create a file named `preset.json` in the voicebank folder to preselect options while generating the OTO. You can include as many or as few of these preset options as you want in the file, and will be prompted for any that are missing. See `example-preset.json` for an example.
- "settings": String matching an existing file in the settings folder, or JSON of full settings
- "tempo": Integer recording tempo, used to calculate overlap for when a vowel is the first phoneme. Can be left out if overlap is specified. If both are specified, tempo takes priority.
- "overlap": Integer used for overlap when a vowel is the first phoneme. Can be left out if tempo is specified. If both are specified, tempo takes priority.
- "init_preutt": Integer preutterance for the first phoneme in the wav file. Default value `20`, to compensate for UTAU's default envelope shape.
- "handle_dupes": Boolean, for whether or not to number/delete duplicate aliases. If false, no need to specify max dupes.
- "max_dupes": Integer, maximum amount of duplicate aliases (0 to delete all, -1 to number all)