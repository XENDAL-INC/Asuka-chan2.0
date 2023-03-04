import json


def loadAttacksJSON():
    with open('db/rpg/db/attacks.json', 'r') as f:
        data = json.load(f)
    return data["types"]


def getAllAttackTypes(type):

    attacks = loadAttacksJSON()
    for atk_type in attacks:
        if atk_type["name"] == type:
            return atk_type["attacks"]
    return None


def getAttacksByName(type, name):
    attacks = getAllAttackTypes(type)
    for attack in attacks:
        if attack["name"] == name:
            return attack
    return None


def getAttacksById(type, id):
    attacks = getAllAttackTypes(type)
    for attack in attacks:
        if attack["id"] == id:
            return attack
    return None


def getAttributeFromAttack(name, attribute):
    attack = getAttacksByName(type, name)
    return attack[attribute]
