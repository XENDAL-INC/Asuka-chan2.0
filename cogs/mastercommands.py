import nextcord
from nextcord.ext import commands


class mastercommands(commands.Cog):

  def _init_(self, bot):
    self.bot = bot

  @nextcord.slash_command(name='updatepfp',
                          description="update pfp for asuka-chan.",
                          guild_ids=[720672074070360064])
  async def updatepfp(self, interaction):
    if interaction.user.id == 380016239310929931:
      pfp_path = "update/pfp.png"
      fp = open(pfp_path, 'rb')
      pfp = fp.read()
      await interaction.client.user.edit(avatar=pfp)
      await interaction.response.send_message(
        "My pfp has been updated successfully thx MASTER!:heart:\nhttps://tenor.com/05fP.gif",
        ephemeral=True)

  @nextcord.slash_command(name='dmsend',
                          description="send DM by user ID thorugh asuka-chan.",
                          guild_ids=[720672074070360064])
  async def sendDMbyID(self, interaction, *, target_id, message: str):
    if interaction.user.id == 380016239310929931:
      target = await interaction.client.fetch_user(target_id)
      target_dm = await target.create_dm()
      await target_dm.send(content=message)
      await interaction.response.send_message(
        "Message was sent successfully to " + target.name + "!",
        ephemeral=True)


def setup(bot):
  bot.add_cog(mastercommands(bot))
