import json

with open('monster_data.json', 'r') as f:
    data = json.load(f)

for i in range(len(data)):
    for j in range(len(data[i]['images'])):
        data[i]['images'][j][3] = "2"

with open('monster_data.json', 'w') as f:
    json.dump(data, f)
