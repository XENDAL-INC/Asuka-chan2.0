import json
import random


def get_servers():
  try:
    with open('db/servers.json', 'r') as f:
      servers = json.load(f)
      test = []
      for server in servers:
        test.append(int(server))
      return test
  except:
    return [720672074070360064]


testServers = get_servers()


def get_honorifics(id):
  if id == 380016239310929931:
    return "-sama"
  else:
    return " Sempai"


#############################################################

global gifsPath
gifsPath = "db/gifs.asdb"


def open_gifs(gifDB=None):
  if gifDB == None:
    gifDB = gifsPath
  with open(gifDB, 'r') as f:
    gifs = json.load(f)
  f.close()
  return gifs


def edit_gifs(gifs, gifDB=None):
  if gifDB == None:
    gifDB = gifsPath
  #backup
  backGifs = open_gifs(gifDB)
  with open(gifDB + ".back", 'w') as f:
    json.dump(backGifs, f)
  f.close()
  #edit
  with open(gifDB, 'w') as f:
    json.dump(gifs, f)
  f.close()


def create_gif_from_text(txtPath, gifType, gifDB=None):
  if gifDB == None:
    gifDB = gifsPath
  gifs = open_gifs(gifDB)
  gifs[gifType] = {}
  with open(txtPath, 'r') as f:
    lines = f.readlines()
  f.close()
  ct = 0
  for line in lines:
    line = line.replace("\n", "")
    gifs[gifType][ct] = line
    ct += 1
  edit_gifs(gifs, gifDB)


def get_random_gif(gifType, gifDB=None):
  if gifDB == None:
    gifs = open_gifs()
  else:
    gifs = open_gifs(gifDB)
  index = random.randint(0, len(gifs[gifType]) - 1)
  return gifs[gifType][str(index)]