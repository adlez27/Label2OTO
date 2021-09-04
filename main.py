import os
import json

print('Select reclist')
lists = os.listdir("settings")
for i, reclist in enumerate(lists):
    print(str(i+1) + ". " + reclist[:-5])
selected_list = lists[int(input(": ")) - 1]

settings = {}
with open("settings\\" + selected_list) as file:
    settings = json.loads(file.read())