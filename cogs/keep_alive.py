import nextcord
from nextcord.ext import commands
from asyncio import sleep


class keep_alive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def keep_bot_alive(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.bot.change_presence(
                status=nextcord.Status.do_not_disturb,
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.listening, name="XENDAL-Sama"))
            await sleep(300)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')
        self.bot.loop.create_task(self.keep_bot_alive())


def setup(bot):
    bot.add_cog(keep_alive(bot))
