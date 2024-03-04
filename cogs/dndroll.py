import random
import nextcord
from nextcord.ext import commands
from get_from_servers import testServers


class dndroll(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def roll(self, ctx, dice: str):
    """
        Roll a dice in NdN format.
        """
    try:
      rolls, limit = map(int, dice.split('d'))
    except Exception:
      await ctx.send('Invalid format. Please use NdN format.')
      return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

  @nextcord.slash_command(
    name="dndroll",
    description="Roll a dice in dice_count X dice_sides format.",
    guild_ids=testServers)
  async def roll_slash(self, interaction, *, dice_count: int, dice_sides: int):
    result = ', '.join(
      str(random.randint(1, dice_sides)) for r in range(dice_count))
    await interaction.response.send_message(result, ephemeral=True)


def setup(client):
  client.add_cog(dndroll(client))
