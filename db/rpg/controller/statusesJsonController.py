import json


def getAllStatuses():
  # Load the JSON file
  with open('db/rpg/db/statuses.json', 'r') as f:
    data = json.load(f)
  return data


def getStatusByName(name):
  data = getAllStatuses()
  for status in data['statuses']:
    if status['name'].lower() == name.lower():
      return status
  return None


def getStatusById(id):
  data = getAllStatuses()
  for status in data['statuses']:
    if status['id'] == id:
      return status
  return None


def getDmgFromStatus(name):
  status = getStatusByName(name)
  return status['dmg']


def checkIfInhibit(name):
  status = getStatusByName(name)
  return status['inhibit']
