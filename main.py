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

labels = [os.path.join(droppedFolder, file) for file in os.listdir(droppedFolder)]
labels = [file for file in labels if os.path.splitext(file)[1] == ".txt"]

csv.register_dialect('tsv', delimiter='\t')
for file in labels:
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, dialect='tsv', fieldnames=["start", "end", "text"])
        for row in csv_reader:
            print(f'Start time: {row["start"]}\nEnd time: {row["end"]}\nLabel text: {row["text"]}')