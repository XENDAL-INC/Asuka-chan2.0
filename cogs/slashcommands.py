import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from get_from_servers import testServers


class slashcommands(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @nextcord.slash_command(name="testanother", description="testing slash commands from other instance", guild_ids=testServers)
  async def testanother(interaction:Interaction):
    print("lol")

  @nextcord.slash_command(name="hi", description="Say hi to Asuka-chan", guild_ids=testServers)
  async def hey(interaction:Interaction):
    print("lol")

  @nextcord.slash_command(name="repeat", description="repeat what u just said", guild_ids=testServers)
  async def repeat(interaction:Interaction, *, args):
    print("lol")

###############################################################
#---------------------------MUSIC-----------------------------#

  @nextcord.slash_command(name="play", description="Searches and plays a song from YouTube.", guild_ids=testServers)
  async def play(interaction:Interaction, *, args):
    print("lol")
  
  @nextcord.slash_command(name="pause", description="Pauses Player", guild_ids=testServers)
  async def pause(interaction:Interaction):
    print("lol")

  @nextcord.slash_command(name="resume", description="Resumes Player", guild_ids=testServers)
  async def resume(interaction:Interaction):
    print("lol")
  
  @nextcord.slash_command(name="leave", description="Leaves Voice", guild_ids=testServers)
  async def leave(interaction:Interaction):
    print("lol")

  @nextcord.slash_command(name="skip", description="Skips current song", guild_ids=testServers)
  async def skip(interaction:Interaction):
    print("lol")
  

  @commands.command()
  async def getList(self, ctx):
    await ctx.send(testServers)



def setup(bot):
  bot.add_cog(slashcommands(bot))