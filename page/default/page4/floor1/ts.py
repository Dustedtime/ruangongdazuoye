import json

with open('monster.json','r') as f:
    data = json.load(f)

for i in range(2):
    for j in range(16):
        data[i]['images'][j].pop(3)

with open('monster.json','w') as f:
    json.dump(data, f)
