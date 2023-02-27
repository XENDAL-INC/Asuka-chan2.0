import random
import nextcord
from nextcord.ext import commands


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


def setup(client):
    client.add_cog(dndroll(client))
