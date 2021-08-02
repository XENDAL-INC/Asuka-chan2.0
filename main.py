import discord
from discord import DMChannel
from discord.ext import commands
import os
from keep_alive import keep_alive
#import subprocess

#subprocess.run('java -jar Lavalink.jar', shell=True)
client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
	client.load_extension('cogs.music')
	client.load_extension('cogs.interactions')
	client.load_extension('cogs.tictactoe')
	print('We have logged in as {0.user}'.format(client))
	await client.change_presence(status=discord.Status.do_not_disturb,
	                             activity=discord.Activity(
	                                 type=discord.ActivityType.listening,
	                                 name="XENDAL-Sama"))


#commands only possible for XENDAL_INC


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
    user = await client.fetch_user(ctx.author.id)
    if not ctx.message.mentions:
      await DMChannel.send(user, "pls mention someone MASTER!")
    else:
      await ctx.channel.purge(limit=1)
      msg=""
      #await DMChannel.send(user, "pls procede and type the message u want to send MASTER!")
      def check(m):
        return m.author.name == "XENDAL_INC"
      response = await client.wait_for('message', check=check)
      msg=response.content
      response.channel.purge(limit=1)
      
      for i in ctx.message.mentions:
        mentioned = await client.fetch_user(i.id)
        await DMChannel.send(mentioned, msg)


keep_alive()
client.run(os.getenv('TOKEN'))
