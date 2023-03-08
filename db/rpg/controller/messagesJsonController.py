import json


def getAllMessages():
  # Load the JSON file
  with open('db/rpg/db/messages.json', 'r') as f:
    data = json.load(f)
  return data['messages']


def getMessageById(id):
  data = getAllMessages()
  for msg in data:
    if str(msg['id']) == str(id):
      return msg
  return None


def getMessageByName(name):
  data = getAllMessages()
  for msg in data:
    if str(msg['name']) == str(name):
      return msg['msg']
  return None
