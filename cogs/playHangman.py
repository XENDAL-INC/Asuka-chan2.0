import random
#import json
import nextcord
from nextcord.ext import commands


class playHangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = [
            "dog", "cat", "house", "car", "tree", "book", "chair", "phone",
            "table", "pizza", "banana", "computer", "desk", "flower", "hat",
            "jacket", "lamp", "mirror", "pen", "shirt", "shoe", "socks",
            "spoon", "toothbrush", "towel", "umbrella", "wallet", "watch",
            "window", "yoyo"
        ]
        self.current_word = ""
        self.current_guesses = []
        self.max_guesses = 6

    @commands.command()
    async def hangman(self, ctx):
        """Starts a game of hangman"""
        # Choose a random word
        self.current_word = random.choice(self.words)
        # Initialize the list of guesses
        self.current_guesses = ["_"] * len(self.current_word)
        # Initialize the number of incorrect guesses
        incorrect_guesses = 0
        # Loop until the game is won or lost
        while "_" in self.current_guesses and incorrect_guesses < self.max_guesses:
            # Display the current state of the game
            await self.display_game(ctx, incorrect_guesses)
            # Get the user's guess
            guess = await self.get_guess(ctx)
            # Check if the guess is correct
            if guess in self.current_word:
                # Update the list of guesses
                for i in range(len(self.current_word)):
                    if self.current_word[i] == guess:
                        self.current_guesses[i] = guess
            else:
                # Increment the number of incorrect guesses
                incorrect_guesses += 1
        # Display the final state of the game
        await self.display_game(ctx, incorrect_guesses)
        # Check if the game was won or lost
        if "_" not in self.current_guesses:
            await ctx.send(
                f"Congratulations, you guessed the word {self.current_word}!")
        else:
            await ctx.send(
                f"Sorry, you ran out of guesses. The word was {self.current_word}."
            )

    async def display_game(self, ctx, incorrect_guesses):
        """Displays the current state of the game"""
        # Create the hangman ASCII art
        hangman = [
            "   ____", "  |    |",
            f"  |    {'' if incorrect_guesses < 1 else 'O'}",
            f"  |   {'' if incorrect_guesses < 2 else '/' }{'' if incorrect_guesses < 1 else '|' }{'' if incorrect_guesses < 2 else 'L' }",
            f"  |    {'' if incorrect_guesses < 3 else '|'}",
            f"  |   {'' if incorrect_guesses < 4 else '/'} {'' if incorrect_guesses < 5 else 'L'}",
            " _|_"
        ]
        # Add the current state of the word
        hangman.append(" ".join(self.current_guesses))
        # Send the message to the channel
        await ctx.send("```" + "\n".join(hangman) + "```")

    async def get_guess(self, ctx):
        """Gets the user's guess"""
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and len(
                message.content) == 1

        # Wait for the user's response
        message = await self.bot.wait_for("message", check=check)
        # Return the lowercase version of the user's guess
        return message.content.lower()


def setup(bot):
    bot.add_cog(playHangman(bot))
