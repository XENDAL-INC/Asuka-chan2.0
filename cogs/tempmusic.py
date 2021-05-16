"""from discord.ext import commands

class music(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.command(pass_context=True, aliases=['p'])
  async def play(self, ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


  @commands.command()
  async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


  @commands.command(aliases=['die'])
  async def leave(ctx):
    await ctx.voice_client.disconnect()


def setup(bot):
  bot.add_cog(music(bot))"""