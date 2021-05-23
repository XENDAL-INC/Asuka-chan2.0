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
	client.load_extension('cogs.interactions')
	client.load_extension('cogs.tictactoe')
	print('We have logged in as {0.user}'.format(client))
	await client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Activity(type=discord.ActivityType.listening,name="XENDAL-Sama"))


#commands only possible for XENDAL_INC

@client.command(hidden=True)
async def updatepfp(ctx):
  if ctx.author.name=="XENDAL_INC":
    pfp_path = "update/pfp.png"
    fp = open(pfp_path, 'rb')
    pfp = fp.read()
    await client.user.edit(avatar=pfp)
    await ctx.channel.purge(limit=1)
    user = await client.fetch_user(ctx.author.id)
    await DMChannel.send(user, "My pfp has been updated successfully thx MASTER!:heart:\nhttps://tenor.com/05fP.gif")


keep_alive()
client.run(os.getenv('TOKEN'))
