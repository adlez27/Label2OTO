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
                phonemes.append({"text": "end"})
            else:
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
            marker_index = marker_index + 1

    for current, next in zip(phonemes, phonemes[1:]):
        print(f'{current["text"]} {next["text"]}')