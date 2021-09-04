import sys
import os
from genericpath import isdir
from pathlib import Path
import json
import csv

try:
    droppedFolder = sys.argv[1]
    if (not os.path.isdir(droppedFolder)):
        print("Please drag and drop a folder onto main.py.")
        input("Press any key to close.")
        exit()
except IndexError:
    print("Please drag and drop a folder onto main.py.")
    input("Press any key to close.")
    exit()

print('Select reclist')
lists = os.listdir("settings")
for i, reclist in enumerate(lists):
    print(str(i+1) + ". " + reclist[:-5])
list_index = 0
while not (list_index <= len(lists) and list_index > 0):
    list_index = int(input(": "))
selected_list = lists[list_index - 1]

settings = {}
with open("settings\\" + selected_list) as file:
    settings = json.loads(file.read())

print('Specify recording tempo or vowel overlap value?\n1. Tempo\n2. Overlap')
ovl_choice = 0
while (not (ovl_choice == 1) and not (ovl_choice == 2)):
    ovl_choice = int(input(": "))
overlap = 0
if (ovl_choice == 1):
    overlap = int(10000 / int(input('Recording tempo (bpm): ')))
    print(f'Calculated overlap: {overlap}')
elif (ovl_choice == 2):
    overlap = int(input('Preferred vowel overlap (msec): '))

labels = [os.path.join(droppedFolder, file) for file in os.listdir(droppedFolder)]
labels = [file for file in labels if os.path.splitext(file)[1] == ".txt"]

csv.register_dialect('tsv', delimiter='\t')
oto_lines = []
for file in labels:
    filename = Path(file).stem
    print(f'Parsing line: {filename}')
    phonemes = []
    with open(file, mode='r') as csv_file:
        file_data = csv.DictReader(csv_file, dialect='tsv', fieldnames=["start", "end", "text"])
        file_data = list(file_data)

        marker_index = 0
        while marker_index < len(file_data):
            marker = file_data[marker_index]
            if marker['text'] == 'start':
                phonemes.append({"text": "start"})
            elif marker['text'] == 'end':
                phonemes.append({
                    "text": "end",
                    "start": int(float(marker["start"])* 1000)
                })
            elif marker['text'] in settings['vowels'] or marker['text'] in settings['consonants']:
                if marker_index + 1 >= len(file_data):
                    print('Missing end marker.')
                    input('Press any key to close.')
                    exit()

                next = file_data[marker_index + 1]
                if next['text'] == 'stretch':
                    phonemes.append({
                        "text": marker["text"],
                        "start": int(float(marker["start"]) * 1000),
                        "stretch start": int(float(next["start"]) * 1000),
                        "stretch end": int(float(next["end"]) * 1000)
                    })
                    marker_index = marker_index + 1
                else:
                    print(f'Phoneme lacks stretch marker: {marker["text"]}')
                    input('Press any key to close.')
                    exit()
            else:
                print(f'Invalid phoneme: {marker["text"]}')
                input('Press any key to close.')
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
            # -X
            alias = "- " + next['text']
            offset = next['start'] - 10
            fixed = next['stretch start'] - next['start'] + 10
            cutoff = 0 - (next['stretch end'] - next['start'] + 10)
            preutterance = 10
            adjusted_overlap = 0
        elif current['text'] in settings['vowels']:
            if next['start'] - current['stretch start'] < overlap * 2:
                preutterance = next['start'] - current['stretch start']
                adjusted_overlap = int(preutterance/2)
            else:
                preutterance = overlap * 2
                adjusted_overlap = overlap
            
            offset = current['stretch end'] - adjusted_overlap

            if next['text'] == 'end':
                # V-
                alias = current['text'] + " -"
                fixed = preutterance + 10
            else:
                # VV and VC
                alias = current['text'] + " " + next ['text']
                fixed = next['stretch start'] - offset
                cutoff = 0 - (next['stretch end'] - offset)
        elif current['text'] in settings['consonants']:
            offset = current['start']
            preutterance = next['start'] - offset
            if next['text'] == 'end':
                # C-
                alias = current['text'] + " -"
                fixed = next['start'] - offset + 10
            else:
                if next['text'] in settings['vowels']:
                    # CV
                    alias = current['text'] + next['text']
                elif next['text'] in settings['consonants']:
                    # CC
                    alias = current['text'] + " " + next ['text']
                fixed = next['stretch start']
                cutoff = 0 - (next['stretch end'] - offset)
                if current['stretch end'] - offset < int(preutterance/2):
                    # stop cons
                    adjusted_overlap = current['stretch end'] - offset
                else:
                    # stretch cons
                    adjusted_overlap = int(preutterance/2)
        
        oto_lines.append(f'{filename}.wav={alias},{offset},{fixed},{cutoff},{preutterance},{adjusted_overlap}\n')

oto_file = open(os.path.join(droppedFolder, "oto.ini"), "w")
oto_file.writelines(oto_lines)
oto_file.close()
print('Generated OTO has been saved.')
input('Press any key to close.')
exit()