import random
import time
import nextcord
import asyncio
from nextcord.ext import commands


class SpeedTyping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def typing(self, ctx):
        """
        Start a speedtyping challenge.
        """
        # Define a list of words
        word_list = [
            "python", "nextcord", "discord", "bot", "coding", "challenge",
            "programming", "server", "message", "channel"
        ]

        # Choose a random word
        chosen_word = random.choice(word_list)

        # Send the chosen word to the user
        await ctx.send(
            f"Type the following word as fast as you can: **{chosen_word}**")

        # Get the start time
        start_time = time.time()

        # Wait for the user's response
        def check(msg):
            return msg.author == ctx.author and msg.content.lower(
            ) == chosen_word

        try:
            await self.client.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, time's up!")
            return

        # Get the end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time

        # Send the results to the user
        await ctx.send(
            f"Congratulations, you completed the challenge in {duration:.2f} seconds!"
        )


def setup(client):
    client.add_cog(SpeedTyping(client))