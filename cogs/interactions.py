import discord
from discord.utils import get
from discord.ext import commands

class interactions(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.command(aliases=['hi'])
  async def hello(self, ctx):
    author=ctx.message.author.name
    if(author=='XENDAL_INC'):
      honorifics='-Sama'
    else:
      honorifics=' Sempai'
    if(author=='Waleed-Kun'):
      await ctx.send('**HENTAI! LOLICON!**')
    elif(author=="Gentleman N'WAH"):
      await ctx.send('**SHUT THE FUCK UP MONKEY**')
    else:
      await ctx.send('Ohayo ' + ctx.message.author.mention +honorifics+' :heart:')
  

  @commands.command()
  async def name(self, ctx):
    #await ctx.message.add_reaction("❤️")
    await ctx.send("Yo! My name is Asuka-chan")


def setup(bot):
  bot.add_cog(interactions(bot))