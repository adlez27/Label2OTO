import sys
import os
from genericpath import isdir
from pathlib import Path
import json
import csv
import re

try:
    dropped_folder = sys.argv[1]
    if (not os.path.isdir(dropped_folder)):
        print("Please drag and drop a folder onto main.py.")
        input("Press enter to close.")
        exit()
except IndexError:
    print("Please drag and drop a folder onto main.py.")
    input("Press enter to close.")
    exit()

preset = {
    "load_preset": False,
    "settings": -1,
    "tempo": -1,
    "overlap": False,
    "init_preutt": 20
}

def set_settings():
    print('Select reclist')
    lists = os.listdir("settings")
    for i, reclist in enumerate(lists):
        print(str(i+1) + ". " + reclist[:-5])
    list_index = 0
    while not (list_index <= len(lists) and list_index > 0):
        list_index = int(input(": "))
    selected_list = lists[list_index - 1]

    with open("settings\\" + selected_list, encoding='utf-8') as file:
        preset['settings'] = json.loads(file.read())
    preset['load_preset'] = False

def set_overlap():
    print('Specify recording tempo or vowel overlap value?\n1. Tempo\n2. Overlap')
    ovl_choice = 0
    while (not (ovl_choice == 1) and not (ovl_choice == 2)):
        ovl_choice = int(input(": "))
    if (ovl_choice == 1):
        preset["overlap"] = int(10000 / int(input('Recording tempo (bpm): ')))
        print(f'Calculated overlap: {preset["overlap"]}')
    elif (ovl_choice == 2):
        preset["overlap"] = int(input('Preferred vowel overlap (msec): '))
    preset['load_preset'] = False

def set_handle_dupes(handle):
    if not handle:
        print('Handle duplicate aliases? (y/n)')
        num_dupes_choice = 0
        while (not (num_dupes_choice == 'y') and not (num_dupes_choice == 'n')):
            num_dupes_choice = input(": ")
        handle = True if num_dupes_choice == 'y' else False

    if handle:
        preset['handle_dupes'] = True
        print('Maximum number of duplicates (0 to delete all, -1 to keep all)')
        preset['max_dupes'] = int(input(': '))
    else:
        preset['handle_dupes'] = False

    preset['load_preset'] = False

try:
    with open(os.path.join(dropped_folder, "preset.json")) as file:
        file_preset = json.loads(file.read())
        for key, value in file_preset.items():
            preset[key] = value

    preset['load_preset'] = True

    if type(preset['settings']) is str:
        lists = os.listdir("settings")
        lists = [x[:-5] for x in lists]
        if preset['settings'] in lists:
            print('Loading from settings for', preset['settings'] + ".")
            with open("settings\\" + preset['settings'] + ".json", encoding='utf-8') as file:
                preset['settings'] = json.loads(file.read())
        else:
            print('Could not find settings for', preset['settings'] + ".")
            set_settings()
    elif type(preset['settings']) is dict:
        print('Loading settings from preset file.')
    else:
        set_settings()

    if preset['tempo'] > 0:
        preset['overlap'] = int(10000 / preset['tempo'])
        print(f'Calculated overlap from tempo: {preset["overlap"]}')
    elif type(preset['overlap']) is bool:
        set_overlap()

    if 'max_dupes' not in preset:
        if ('handle_dupes' not in preset) or preset['handle_dupes']:
            set_handle_dupes(True)
except IOError:
    set_settings()
    set_overlap()
    set_handle_dupes()

labels = [os.path.join(dropped_folder, file) for file in os.listdir(dropped_folder)]
labels = [file for file in labels if os.path.splitext(file)[1] == ".txt"]

csv.register_dialect('tsv', delimiter='\t')
oto_lines = []
for file in labels:
    filename = Path(file).stem
    print(f'Parsing line: {filename}')
    phonemes = [{"text": "start"}]
    with open(file, mode='r', encoding="utf-8") as csv_file:
        file_data = csv.DictReader(csv_file, dialect='tsv', fieldnames=["start", "end", "text"])
        file_data = list(file_data)

        marker_index = 0
        while marker_index < len(file_data):
            marker = file_data[marker_index]
            if marker['text'] in preset['settings']['vowels'] or marker['text'] in preset['settings']['consonants']:
                if marker_index + 1 >= len(file_data):
                    print('Missing end marker.')
                    input('Press enter to close.')
                    exit()

                next = file_data[marker_index + 1]
                if next['text'] == '-':
                    phonemes.append({
                        "text": marker["text"],
                        "start": int(float(marker["start"]) * 1000),
                        "stretch start": int(float(next["start"]) * 1000),
                        "stretch end": int(float(next["end"]) * 1000)
                    })
                    marker_index = marker_index + 1
                else:
                    print(f'Phoneme lacks stretch marker: {marker["text"]}')
                    input('Press enter to close.')
                    exit()
            elif marker['text'] == 'end':
                phonemes.append({
                    "text": "end",
                    "start": int(float(marker["start"])* 1000)
                })
            else:
                print(f'Invalid phoneme: {marker["text"]}')
                input('Press enter to close.')
                exit()
            marker_index = marker_index + 1

    for current, next in zip(phonemes, phonemes[1:]):
        alias = ""
        offset = 0
        fixed = 0
        cutoff = 0
        preutterance = 0
        adjusted_overlap = 0
        if current['text'] == 'start':
            if next['text'] in preset['settings']['vowels']:
                # -V
                alias = "-" + preset['settings']['aliases']['-v']['spacer'] + next['text']
                if not preset['settings']['aliases']['-v']['include']:
                    continue
            elif next['text'] in preset['settings']['consonants']:
                # -C
                alias = "-" + preset['settings']['aliases']['-c']['spacer'] + next['text']                
                if not preset['settings']['aliases']['-c']['include']:
                    continue
            offset = next['start'] - preset['init_preutt']
            fixed = next['stretch start'] - next['start'] + preset['init_preutt']
            cutoff = 0 - (next['stretch end'] - next['start'] + preset['init_preutt'])
            preutterance = preset['init_preutt']
            adjusted_overlap = int(preset['init_preutt'] / 2)
        elif current['text'] in preset['settings']['vowels']:
            if next['start'] - current['stretch start'] < preset['overlap'] * 2:
                preutterance = next['start'] - current['stretch start']
                adjusted_overlap = int(preutterance/2)
                offset = current['stretch start']
            elif next['start'] - current['stretch end'] > preset['overlap']:
                preutterance = (next['start'] - current['stretch end']) + preset['overlap']
                adjusted_overlap = preset['overlap']
                offset = current['stretch end'] - preset['overlap']
            else:
                preutterance = preset['overlap'] * 2
                adjusted_overlap = preset['overlap']
                offset = next['start'] - preutterance

            if next['text'] == 'end':
                # V-
                alias = current['text'] + preset['settings']['aliases']['v-']['spacer'] +  "-"
                fixed = preutterance + 10
                if not preset['settings']['aliases']['v-']['include']:
                    continue
            else:
                if next['text'] in preset['settings']['vowels']:
                    # VV
                    alias = current['text'] + preset['settings']['aliases']['vv']['spacer'] + next ['text']
                    if not preset['settings']['aliases']['vv']['include']:
                        continue
                elif next['text'] in preset['settings']['consonants']:
                    # VC
                    alias = current['text'] + preset['settings']['aliases']['vc']['spacer'] + next['text']
                    if not preset['settings']['aliases']['vc']['include']:
                        continue
                fixed = next['stretch start'] - offset
                cutoff = 0 - (next['stretch end'] - offset)
        elif current['text'] in preset['settings']['consonants']:
            offset = current['start']
            preutterance = next['start'] - offset
            if next['text'] == 'end':
                # C-
                alias = current['text'] + preset['settings']['aliases']['c-']['spacer'] + "-"
                fixed = next['start'] - offset + int(preset['init_preutt'] / 2)                
                if not preset['settings']['aliases']['c-']['include']:
                    continue
            else:
                if next['text'] in preset['settings']['vowels']:
                    # CV
                    alias = current['text'] + preset['settings']['aliases']['cv']['spacer'] + next['text']
                    if not preset['settings']['aliases']['cv']['include']:
                        continue
                elif next['text'] in preset['settings']['consonants']:
                    # CC
                    alias = current['text'] + preset['settings']['aliases']['cc']['spacer'] + next ['text']
                    if not preset['settings']['aliases']['cc']['include']:
                        continue
                fixed = next['stretch start'] - offset
                cutoff = 0 - (next['stretch end'] - offset)
            if current['stretch end'] - offset < int(preutterance/2):
                # stop cons
                adjusted_overlap = current['stretch end'] - offset
            else:
                # stretch cons
                adjusted_overlap = int(preutterance/2)
        
        oto_lines.append({
            "filename": filename,
            "alias": alias,
            "offset": offset,
            "fixed": fixed,
            "cutoff": cutoff,
            "preutterance": preutterance,
            "overlap": adjusted_overlap
        })

new_oto_lines = []
for line in oto_lines:
    keep = True
    for find in preset['settings']['delete']:
        if re.search(find, line['alias']):
            keep = False
            break
    if keep:
        new_oto_lines.append(line)

for line in new_oto_lines:
    for find, replace in preset['settings']['replace'].items():
        line['alias'] = re.sub(find,replace,line['alias'])

oto_lines = new_oto_lines

if preset['handle_dupes']:
    alias_count = {}
    new_oto_lines = []
    for line in oto_lines:
        if line['alias'] not in alias_count:
            alias_count[f'{line["alias"]}'] = 0
            new_oto_lines.append(line)
        elif line['alias'] in alias_count and (preset['max_dupes'] == -1 or alias_count[f'{line["alias"]}'] < preset['max_dupes']):
            alias_count[f'{line["alias"]}'] += 1
            line['alias'] += str(alias_count[f'{line["alias"]}'])
            new_oto_lines.append(line)
    oto_lines = new_oto_lines

oto_file = open(os.path.join(dropped_folder, "oto.ini"), "w")
oto_lines = [f'{line["filename"]}.wav={line["alias"]},{line["offset"]},{line["fixed"]},{line["cutoff"]},{line["preutterance"]},{line["overlap"]}\n' for line in oto_lines]
oto_file.writelines(oto_lines)
oto_file.close()

if not (preset['load_preset']):
    print('Generated OTO has been saved.')
    input('Press enter to close.')