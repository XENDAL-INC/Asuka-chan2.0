import discord
from discord import DMChannel
from discord.ext import commands
import os
from keep_alive import keep_alive
import time
import json
import re
#import subprocess

#subprocess.run('java -jar Lavalink.jar', shell=True)
def get_prefix(client, message):
  try:
    with open('db/servers.json', 'r') as f:
      servers = json.load(f)
    return servers[str(message.guild.id)]['prefix']
  except:
    return "$"


intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents=intents)
#client = commands.Bot(command_prefix='$')



@client.event
async def on_ready():
  #client.load_extension('cogs.music')
  client.load_extension('cogs.levelsystem')
  client.load_extension('cogs.serverevents')
  client.load_extension('cogs.interactions')
  client.load_extension('cogs.tictactoe')
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Activity(type=discord.ActivityType.listening, name="XENDAL-Sama"))
  

#commands only possible for XENDAL_INC



"""@client.event
async def on_message(message):
    print(message.content)"""


@client.command(hidden=True)
async def prefix(ctx):
  msg = await ctx.fetch_message(ctx.message.id)
  with open('db/servers.json', 'r') as f:
    servers = json.load(f)
  
  current_prefix=servers[str(ctx.guild.id)]['prefix']
  prefix = msg.content.replace(current_prefix + "prefix ", "", -1)
  prefix = prefix.replace(" ", "", -1)
  check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
  if "prefix" not in prefix:
    if(check.search(prefix) == None):
      await ctx.send("sry " + ctx.author.mention + ", but you have typed an invalid prefix, pls try using these symbols:\n[@_!#$%^&*()<>?/\|}{~:]")
    else:
      await ctx.send(ctx.author.mention + "the server's prefix have been updated!")
      servers[str(ctx.guild.id)]['prefix']=str(prefix[0])

  with open('db/servers.json', 'w') as f:
    json.dump(servers,f)
      
@client.command(hidden=True)
async def updatepfp(ctx):
	if ctx.author.name == "XENDAL_INC":
		pfp_path = "update/pfp.png"
		fp = open(pfp_path, 'rb')
		pfp = fp.read()
		await client.user.edit(avatar=pfp)
		await ctx.channel.purge(limit=1)
		user = await client.fetch_user(ctx.author.id)
		await DMChannel.send(
		    user,
		    "My pfp has been updated successfully thx MASTER!:heart:\nhttps://tenor.com/05fP.gif"
		)

@client.command(hidden=True)
async def sendDM(ctx):
  if ctx.author.name == "XENDAL_INC":
    temp = ctx.author.id;
    user = await client.fetch_user(ctx.author.id)
    if not ctx.message.mentions:
      await DMChannel.send(user, "pls mention someone MASTER!")
    else:
      await ctx.channel.purge(limit=1)
      msg=""
      dmfeedback = await DMChannel.send(user, "pls procede and type the message u want to send MASTER!")
      time.sleep(2)
      await dmfeedback.delete()
      def check(m):
        return m.author.name == "XENDAL_INC"
      response = await client.wait_for('message', check=check)
      msg=response.content
      #response.channel.purge(limit=1)
      response.delete()
      
      for i in ctx.message.mentions:
        mentioned = await client.fetch_user(i.id)
        await DMChannel.send(mentioned, msg + temp)

@client.command(hidden=True)
async def sendDMbyID(ctx):
  if ctx.author.name == "XENDAL_INC":
    #temp = ctx.author.id;
    user = await client.fetch_user(ctx.author.id)
    if not ctx.message.content.replace("$sendDMbyID", "",-1)=="" or ctx.message.content.replace("$sendDMbyID", "",-1)==" ":
      dmID = ctx.message.content.replace("$sendDMbyID", "",-1)
      dmID = dmID.replace(" ", "",-1)
      #await ctx.message.delete
      msg=""
      dmfeedback = await DMChannel.send(user, "pls procede and type the message u want to send MASTER!")
      time.sleep(2)
      await dmfeedback.delete()
      def check(m):
        return m.author.name == "XENDAL_INC"
      response = await client.wait_for('message', check=check)
      msg=response.content
      #response.channel.purge(limit=1)
      target = await client.fetch_user(dmID)
      await DMChannel.send(target, msg)
    else:
      dmfeedback = await DMChannel.send(user, "pls mention someone MASTER!")
      time.sleep(2)
      await dmfeedback.delete()

keep_alive()
client.run(os.getenv('TOKEN'))
