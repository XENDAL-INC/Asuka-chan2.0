import nextcord
from nextcord.ext import commands
import os
#from keep_alive import keep_alive
import json

#import subprocess
from get_from_servers import testServers

#since pytube sucks lol
"""subprocess.run('python -m pip uninstall discord.py', shell=True)
subprocess.run('y', shell=True)
subprocess.run('python -m pip uninstall discord', shell=True)
subprocess.run('y', shell=True)"""


def get_prefix(client, message):
  try:
    with open('db/servers.json', 'r') as f:
      servers = json.load(f)
    return servers[str(message.guild.id)]['prefix']
  except:
    return "$"


#intents = nextcord.Intents.all()
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=get_prefix, intents=intents)


@client.event
async def on_ready():
  client.load_extension('cogs.music')
  client.load_extension('cogs.levelsystem')
  client.load_extension('cogs.serverevents')
  client.load_extension('cogs.interactions')
  client.load_extension('cogs.interactionsSlash')
  client.load_extension('cogs.gifInteractions')
  client.load_extension('cogs.tictactoe')
  client.load_extension('cogs.Connect4')
  client.load_extension('cogs.Connect4Slash')
  client.load_extension('cogs.magic8pool')
  client.load_extension('cogs.playHangman')
  client.load_extension('cogs.SpeedTyping')
  #client.load_extension('cogs.RockPaperScissors')
  client.load_extension('cogs.dndroll')
  client.load_extension('cogs.serverconfig')
  client.load_extension('cogs.ServerStatus')
  client.load_extension('cogs.animecrawler')
  client.load_extension('cogs.mangacrawler')
  client.load_extension('cogs.gamecrawler')
  #client.load_extension('cogs.ytubeconverter')
  client.load_extension('cogs.RPGCommands')
  client.load_extension('cogs.chatgpt')
  client.load_extension('cogs.mastercommands')
  client.load_extension('cogs.customHelp')
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(status=nextcord.Status.do_not_disturb,
                               activity=nextcord.Activity(
                                 type=nextcord.ActivityType.listening,
                                 name="XENDAL-Sama"))

  for server in testServers:
    await client.sync_application_commands(data=None,
                                           guild_id=server,
                                           associate_known=True,
                                           delete_unknown=True,
                                           update_known=True,
                                           register_new=True)
  '''commands = client.get_all_application_commands()
  for command in commands:
    print(f'{command.name} - {str(command.guild_ids)}')'''
  print("commands sync done!")


#keep_alive()
client.run(os.getenv('TOKEN'))
