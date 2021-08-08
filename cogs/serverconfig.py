import discord
from discord import DMChannel
from discord.utils import get
from discord.ext import commands
import json
import re

class serverconfig(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.command(hidden=True)
  async def prefix(self, ctx):
    msg = await ctx.fetch_message(ctx.message.id)
    with open('db/servers.json', 'r') as f:
      servers = json.load(f)
    
    try:
      t = servers[str(ctx.guild.id)]
    except:
      servers[ctx.guild.id]= {}
      servers[ctx.guild.id]['name']= ctx.guild.name
      servers[ctx.guild.id]['prefix'] = "$"
      with open('db/servers.json', 'w') as f:
        json.dump(servers,f)
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

def setup(bot):
  bot.add_cog(serverconfig(bot))