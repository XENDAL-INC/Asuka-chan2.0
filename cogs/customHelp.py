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

    # Split fields into pages
    fields = embed.fields
    max_fields = 5  # Maximum number of fields per page
    pages = [
      fields[i:i + max_fields] for i in range(0, len(fields), max_fields)
    ]

    # Send pages as separate messages
    for i, page in enumerate(pages):
      page_embed = nextcord.Embed(title=f"Help ({i+1}/{len(pages)})",
                                  description="List of available commands:")
      for field in page:
        page_embed.add_field(name=field.name,
                             value=field.value,
                             inline=field.inline)
      await self.context.author.send(embed=page_embed)

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
