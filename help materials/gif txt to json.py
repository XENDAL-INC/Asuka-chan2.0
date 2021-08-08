import json
import os

with open('template.json', 'r') as f:
    y = json.load(f)

temp=str(y)
gifclass="punch"
temp=temp.replace("class", gifclass, -1)
temp=temp.replace("'", "\"", -1)

k = open(gifclass + ".txt", 'r')
for x in k:
    link=x.replace("\n", "", -1)
    temp=temp.replace("giflink", link, 1)

print(temp)
gif = json.loads(temp)
with open(gifclass + ".json", 'w') as z:
    json.dump(gif, z)