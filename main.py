import discord
from discord import DMChannel
from discord.ext import commands
import os
from keep_alive import keep_alive
import time
#import subprocess

#subprocess.run('java -jar Lavalink.jar', shell=True)
intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('$'), intents=intents)
#client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
  #client.load_extension('cogs.music')
	client.load_extension('cogs.interactions')
	client.load_extension('cogs.tictactoe')
	print('We have logged in as {0.user}'.format(client))
	await client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Activity(type=discord.ActivityType.listening, name="XENDAL-Sama"))
  

#commands only possible for XENDAL_INC

@client.event
async def on_voice_state_update(member, before, after):
  inVC=False
  for roles in member.guild.roles:
    if roles.name=="inVC":
      inVC=True
      role=roles
      break

  if inVC:
    if not member.voice:
      await member.remove_roles(role)
    else:
      await member.add_roles(role)

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
