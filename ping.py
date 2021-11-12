import json

with open('events.json') as f:
    obj = json.load(f)

for i in obj:
    print(obj[i]['name'])
    print(obj[i]['date'])
    print(obj[i]['time'])