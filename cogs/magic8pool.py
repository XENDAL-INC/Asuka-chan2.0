import nextcord
import random
from nextcord.ext import commands
from get_from_servers import testServers


class magic8pool(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  global responses
  responses = [
    "It is certain, nya~", "It is decidedly so, senpai~",
    "Without a doubt, desu~", "Yes - definitely, desu~",
    "You may rely on it, onii-chan~", "As I see it, yes, uwu~",
    "Most likely, nyaa~", "Outlook good, baka~", "Yes, sempai notice me~",
    "Signs point to yes, nyan~", "Reply hazy, try again, nya~",
    "Ask again later, desu~", "Better not tell you now, senpai~",
    "Cannot predict now, desu~", "Concentrate and ask again, onii-chan~",
    "Don't count on it, uwu~", "Outlook not so good, nyaa~",
    "My sources say no, baka~", "Very doubtful, sempai notice me~"
  ]

  @commands.command(name='8ball')
  async def magic8ball(self, ctx, *, question: str):
    """Ask a question and receive a magic 8 ball response."""

    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

  @nextcord.slash_command(
    name="8ball",
    description="Ask a question and receive a magic 8 ball response.",
    guild_ids=testServers)
  async def magic8ball_slash(self, interaction, *, question: str):
    await interaction.response.send_message(
      f"Question: {question}\nAnswer: {random.choice(responses)}")


def setup(bot):
  bot.add_cog(magic8pool(bot))
