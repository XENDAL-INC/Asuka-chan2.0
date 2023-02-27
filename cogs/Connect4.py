import nextcord
from nextcord.ext import commands


class Connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.board = [[0 for i in range(7)] for j in range(6)]
        self.players = [None, None]
        self.turn = 0

    def print_board(self):
        output = ""
        for i in range(6):
            for j in range(7):
                output += ":red_circle:" if self.board[i][
                    j] == 1 else ":blue_circle:" if self.board[i][
                        j] == 2 else ":white_circle:"
                output += " "
            output += "\n"
        output += "1 2 3 4 5 6 7"
        return output

    def play(self, col):
        for i in range(5, -1, -1):
            if self.board[i][col] == 0:
                self.board[i][col] = self.turn + 1
                return True
        return False

    def check_win(self):
        # Check rows
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.turn + 1 and self.board[i][
                        j + 1] == self.turn + 1 and self.board[i][
                            j + 2] == self.turn + 1 and self.board[i][
                                j + 3] == self.turn + 1:
                    return True
        # Check columns
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.turn + 1 and self.board[
                        i + 1][j] == self.turn + 1 and self.board[
                            i + 2][j] == self.turn + 1 and self.board[
                                i + 3][j] == self.turn + 1:
                    return True
        # Check diagonals
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.turn + 1 and self.board[i + 1][
                        j + 1] == self.turn + 1 and self.board[i + 2][
                            j + 2] == self.turn + 1 and self.board[i + 3][
                                j + 3] == self.turn + 1:
                    return True
                if self.board[i][j + 3] == self.turn + 1 and self.board[i + 1][
                        j + 2] == self.turn + 1 and self.board[i + 2][
                            j + 1] == self.turn + 1 and self.board[
                                i + 3][j] == self.turn + 1:
                    return True
        return False

    @commands.command()
    async def connect4(self, ctx):
        if self.players[0] == None:
            self.players[0] = ctx.author
            await ctx.send("Player 1 joined the game.")
        elif self.players[1] == None:
            self.players[1] = ctx.author
            await ctx.send("Player 2 joined the game.")
            await ctx.send(self.print_board())
            self.turn = 0
        else:
            await ctx.send("The game is already full.")

    def is_board_full(self):
        for col in range(7):
            if self.board[0][col] == ':white_circle:':
                return False
        return True

    @commands.command()
    async def playConnect4(self, ctx, col: int):
        if ctx.author == self.players[self.turn]:
            if self.play(col - 1):
                await ctx.send(self.print_board())
                if self.check_win():
                    await ctx.send(
                        f"{self.players[self.turn].mention} won the game!")
                    # Game is over, reset
                    self.players = [None, None]
                    self.board = [[' ' for _ in range(7)] for _ in range(6)]
                    self.turn = 0
                else:
                    if self.turn == 0:
                        self.turn = 1
                    else:
                        self.turn = 0


def setup(bot):
    bot.add_cog(Connect4(bot))
