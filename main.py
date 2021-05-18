import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
#import subprocess

#subprocess.run('java -jar Lavalink.jar', shell=True)
client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
	client.load_extension('cogs.interactions')
	#client.load_extension('cogs.queue_storage')
	#client.load_extension('cogs.music')
	print('We have logged in as {0.user}'.format(client))
	await client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Activity(type=discord.ActivityType.listening,name="XENDAL-Sama"))


keep_alive()
client.run(os.getenv('TOKEN'))
