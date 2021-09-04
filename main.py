from genericpath import isdir
import sys
import os
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
selected_list = lists[int(input(": ")) - 1]

settings = {}
with open("settings\\" + selected_list) as file:
    settings = json.loads(file.read())

overlap = int(input('Preferred vowel overlap (msec): '))

labels = [os.path.join(droppedFolder, file) for file in os.listdir(droppedFolder)]
labels = [file for file in labels if os.path.splitext(file)[1] == ".txt"]

csv.register_dialect('tsv', delimiter='\t')
for file in labels:
    file_data = {}
    with open(file, mode='r') as csv_file:
        file_data = csv.DictReader(csv_file, dialect='tsv', fieldnames=["start", "end", "text"])
        file_data = list(file_data)

    for line in file_data:
        line['start'] = int(float(line['start']) * 1000)
        line['end'] = int(float(line['end']) * 1000)

        text = line['text']
        if text in settings['consonants']:
            line['type'] = 'consonant'
        elif line['text'][:-1] in settings['consonants']:
            if text[-1] == '1':
                line['type'] = 'consonant1'
            elif text[-1] == '2':
                line['type'] = 'consonant2'
            else:
                line['type'] = 'none'
        elif text in settings['vowels']:
            line['type'] = 'vowel'
        else:
            line['type'] = 'none'

    for current, next in zip(file_data, file_data[1:]):
        if current['type'] == 'vowel':
            if next['type'] == 'vowel':
                print('VV', current['text'], next['text'])
            elif next['type'] == 'consonant' or next['type'] == 'consonant1':
                print('VC', current['text'], next['text'])
            elif next['type'] == 'none':
                print('V-', current['text'], next['text'])
            else:
                print('Invalid labels for split consonant:', current['text'], next['text']) # checked
        elif current['type'] == 'consonant':
            if next['type'] == 'vowel':
                print('CV', current['text'], next['text'])
            elif next['type'] == 'consonant' or next['type'] == 'consonant1':
                print('CC', current['text'], next['text'])
            elif next['type'] == 'none':
                print('C-', current['text'], next['text'])
            else:
                print('Invalid labels for split consonant:', current['text'], next['text']) # checked
        elif current['type'] == 'consonant1':
            if next['type'] == 'consonant2':
                print('C', current['text'], next['text'])
            else:
                print('Invalid labels for split consonant:', current['text'], next['text']) # checked
        elif current['type'] == 'consonant2':
            if next['type'] == 'vowel':
                print('CV', current['text'], next['text'])
            elif next['type'] == 'consonant' or next['type'] == 'consonant1':
                print('CC', current['text'], next['text'])
            elif next['type'] == 'none':
                print('C-', current['text'], next['text'])
            else:
                print('Invalid labels for split consonant:', current['text'], next['text']) # checked
        else:
            if next['type'] == 'vowel':
                print('-V', current['text'], next['text'])
            elif next['type'] == 'consonant' or next['type'] == 'consonant1':
                print('-C', current['text'], next['text'])
            elif next['type'] == 'consonant2':
                print('Invalid labels for split consonant:', current['text'], next['text']) # checked
            else:
                print('Invalid labels for silence:', current['text'], next['text']) # checked