import nextcord
from nextcord.ext import commands


class Help(nextcord.ext.commands.HelpCommand):

  def __init__(self):
    super().__init__()

  async def send_bot_help(self, mapping):
    embed = nextcord.Embed(title="Help",
                           description="List of available commands:")
    for cog, commands in mapping.items():
      if cog is None:
        continue
      command_list = [
        f"`{cmd.name}` - {cmd.brief}" for cmd in commands if not cmd.hidden
      ]
      if not command_list:
        continue
      cog_name = cog.qualified_name
      if cog_name.lower() == "jishaku":
        continue
      embed.add_field(name=cog_name,
                      value="\n".join(command_list),
                      inline=False)
    await self.context.author.send(embed=embed)
    await self.context.message.delete()


class CustomHelp(commands.Cog):

  def __init__(self, client):
    self._old_help_command = client.help_command
    client.help_command = Help()
    self.client = client

  def cog_unload(self):
    self.client.help_command = self._old_help_command


def setup(client):
  client.add_cog(CustomHelp(client))
