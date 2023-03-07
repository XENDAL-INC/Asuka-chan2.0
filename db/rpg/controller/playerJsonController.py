import json


def loadPlayersJSON():
  with open('db/rpg/db/players.json', 'r') as f:
    data = json.load(f)
  return data


def getAllPlayers():
  # Load the JSON file
  data = loadPlayersJSON()
  # Extract the "statuses" array
  players = data
  return players


def getPlayersById(id):
  player = getAllPlayers()
  if str(id) not in player:
    return None
  return player[str(id)]


def getAttributeFromPlayer(id, attribute):
  player = getPlayersById(id)
  return player[attribute]


def updatePlayersDB(players):
  with open('db/rpg/db/players.json', 'w') as f:
    json.dump(players, f)


def updateSinglePlayerInfo(player, id):
  players = getAllPlayers()
  players[str(id)]['user_name'] = player['user_name']
  players[str(id)]['lvl'] = player['lvl']
  players[str(id)]['exp'] = player['exp']
  players[str(id)]['MaxHp'] = player['MaxHp']
  players[str(id)]['CurrentHp'] = player['CurrentHp']
  players[str(id)]['atk'] = player['atk']
  players[str(id)]['defense'] = player['defense']
  players[str(id)]['speed'] = player['speed']
  players[str(id)]['evasion'] = player['evasion']
  players[str(id)]['accuracy'] = player['accuracy']
  players[str(id)]['attacks'] = player['attacks']
  updatePlayersDB(players)


def createNewPlayerDB(id,
                      user_name,
                      clss="Fire",
                      name="test",
                      hp=60,
                      atk=54,
                      defense=54,
                      speed=54,
                      evasion=0,
                      accuracy=0,
                      attacks=None):
  players = loadPlayersJSON()

  if str(id) not in players:
    players[str(id)] = {}

  players[str(id)]['user_name'] = str(user_name)
  players[str(id)]['name'] = str(name)
  players[str(id)]['class'] = clss
  players[str(id)]['lvl'] = 1
  players[str(id)]['exp'] = 0
  players[str(id)]['MaxHp'] = hp
  players[str(id)]['CurrentHp'] = hp
  players[str(id)]['atk'] = atk
  players[str(id)]['defense'] = defense
  players[str(id)]['speed'] = speed
  players[str(id)]['evasion'] = evasion
  players[str(id)]['accuracy'] = accuracy
  players[str(id)]['attacks'] = attacks
  players[str(id)]['status'] = None

  updatePlayersDB(players)
