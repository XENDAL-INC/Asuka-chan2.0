import json


def loadMonstersJSON():
    with open('db/rpg/db/monsters.json', 'r') as f:
        data = json.load(f)
    return data


def getAllMonsters():
    # Load the JSON file
    data = loadMonstersJSON()
    # Extract the "monsters" array
    #print(data)
    return data


def getMonsterById(id):
    monsters = loadMonstersJSON()
    try:
        return monsters[str(id)]
    except:
        return None


def getAttributeFromMonster(id, attribute):
    monster = getMonsterById(id)
    return monster[attribute]


def createNewMonster(id,
                     hp=None,
                     atk=None,
                     defense=None,
                     speed=None,
                     evasion=1,
                     accuracy=1,
                     attacks=None):
    newMonster = getMonsterById(id)

    #newMonster[str(id)]['MaxHp'] = hp
    #newMonster[str(id)]['CurrentHp'] = hp
    #newMonster[str(id)]['atk'] = atk
    #newMonster[str(id)]['defense'] = defense
    #newMonster[str(id)]['speed'] = speed
    #newMonster[str(id)]['evasion'] = evasion
    #newMonster[str(id)]['accuracy'] = accuracy
    #newMonster[str(id)]['attacks'] = attacks
    return newMonster
