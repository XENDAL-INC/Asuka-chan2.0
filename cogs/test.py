import nextcord
from nextcord.ext import commands
from nextcord_slash_command import cog_ext, SlashContext


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash()
    async def my_command(self, ctx: SlashContext):
        await ctx.send("Hello, world!")


def setup(bot):
    bot.add_cog(test(bot))
