import nextcord
from nextcord.ext import commands


class RockPaperScissors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self, ctx):
        player1 = ctx.author
        await ctx.send(
            f"{player1.mention}, please choose rock, paper, or scissors.")
        msg1 = await self.client.wait_for(
            'message',
            check=lambda m: m.author == player1 and m.content.lower(
            ) in ['rock', 'paper', 'scissors'])
        player1_choice = msg1.content.lower()

        player2_mentions = list(
            filter(lambda x: x != player1, ctx.message.mentions))
        if len(player2_mentions) != 1:
            await ctx.send(
                f"{player1.mention}, you need to mention one other player to play with!"
            )
            return

        player2 = player2_mentions[0]
        await ctx.send(
            f"{player2.mention}, please choose rock, paper, or scissors.")
        msg2 = await self.client.wait_for(
            'message',
            check=lambda m: m.author == player2 and m.content.lower(
            ) in ['rock', 'paper', 'scissors'])
        player2_choice = msg2.content.lower()

        winner = None
        if player1_choice == player2_choice:
            result = "It's a tie!"
        elif player1_choice == 'rock' and player2_choice == 'scissors':
            winner = player1
        elif player1_choice == 'paper' and player2_choice == 'rock':
            winner = player1
        elif player1_choice == 'scissors' and player2_choice == 'paper':
            winner = player1
        else:
            winner = player2

        if winner is not None:
            result = f"{winner.mention} wins!"
        await ctx.send(
            f"{player1.mention} chose {player1_choice}, {player2.mention} chose {player2_choice}. {result}"
        )


def setup(client):
    client.add_cog(RockPaperScissors(client))
