from nextcord.ext import commands
import json

class serverevents(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    with open('db/servers.json', 'r') as f:
      servers = json.load(f)
    
    servers[guild.id]= {}
    servers[guild.id]['name']= guild.name
    servers[guild.id]['prefix'] = "$"

    with open('db/servers.json', 'w') as f:
      json.dump(servers,f)
  
  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    with open('db/servers.json', 'r') as f:
      servers = json.load(f)
    
    try:
      servers.pop(str(guild.id))
    except:
      print("lmao")

    with open('db/servers.json', 'w') as f:
      json.dump(servers,f)

def setup(bot):
  bot.add_cog(serverevents(bot))