import json


def loadAttacksJSON():
  with open('db/rpg/db/attacks.json', 'r') as f:
    data = json.load(f)
  return data["attacks"]


def getAllAttacks():
  attacks = loadAttacksJSON()
  return attacks


def getAllAttacksByType(type):
  allAttacks = getAllAttacks()
  typeAttacks = {}
  for attack in allAttacks:
    if attack['type'].lower() == type.lower():
      typeAttacks[str(attack['id'])] = attack
  return typeAttacks


def getAllAttacksByTypeAndLevel(type, lvl):
  allAttacks = getAllAttacks()
  targetAttacks = {}
  for attack in allAttacks:
    if attack['type'].lower() == type.lower() and attack['lvl'] == lvl:
      targetAttacks[str(attack['id'])] = attack
  #print(targetAttacks[str(0)]['description'])
  return targetAttacks


def getAttacksByName(name):
  attacks = getAllAttacks()
  for attack in attacks:
    if attack["name"] == name:
      return attack
  return None


def getAttacksById(id):
  attacks = getAllAttacks()
  for attack in attacks:
    if attack["id"] == id:
      return attack
  return None


def getAttributeFromAttack(name, attribute):
  attack = getAttacksByName(name)
  return attack[attribute]
