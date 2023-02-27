import nextcord
from nextcord.ext import commands


class ServerStatus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def status(self, ctx):
        """
        Display the status of the server.
        """
        # Get the server information
        guild = ctx.guild
        server_name = guild.name
        server_region = guild.region
        server_members = guild.member_count

        # Create the status message
        status_message = f"Server Name: {server_name}\nServer Region: {server_region}\nServer Members: {server_members}"

        # Send the status message to the channel
        await ctx.send(status_message)


def setup(client):
    client.add_cog(ServerStatus(client))
