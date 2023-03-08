import json


def getAllMessages():
  # Load the JSON file
  with open('db/rpg/db/messages.json', 'r') as f:
    data = json.load(f)
  return data


def getAllMessagesByType(type):
  data = getAllMessages()
  if str(type) in data and data[str(type)] is not None:
    return data[str(type)]
  return None


def getMessageById(type, id):
  data = getAllMessagesByType(type)
  for msg in data:
    if str(msg['id']) == str(id):
      return msg
  return None


def getMessageByName(type, name):
  data = getAllMessagesByType(type)
  for msg in data:
    if str(msg['name']) == str(name):
      return msg
  return None
