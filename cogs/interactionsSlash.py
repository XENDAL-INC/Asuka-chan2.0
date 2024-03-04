import nextcord
from nextcord.ext import commands
from nextcord import Embed
import time
#import random
import get_from_servers as asukaDB


class interactionsSlash(commands.Cog):

  def _init_(self, bot):
    self.bot = bot

  @nextcord.slash_command(name="hi",
                          description="Say hi to Asuka-chan!",
                          guild_ids=asukaDB.testServers)
  async def hi(self, interaction):
    author = interaction.user
    honorifics = asukaDB.get_honorifics(author.id)

    if author.id == 319617215391465472:
      await interaction.response.send_message("# **HENTAI! LOLICON!**")
    elif author.id == 265181840288120833:
      await interaction.response.send_message("# **SHUT THE FUCK UP MONKEY**")
    else:
      await interaction.response.send_message("Ohayo" + author.mention +
                                              honorifics + " :heart:")

  @nextcord.slash_command(
    name='purge',
    description=
    "clears a default number of 5 messages if not declared after command.",
    guild_ids=asukaDB.testServers)
  async def clear(self, interaction, *, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message("Messages purged successfully!",
                                            ephemeral=True)

  @nextcord.slash_command(name='usrinfo',
                          description="Display mentioned user's info.",
                          guild_ids=asukaDB.testServers)
  async def usrinfo(self, interaction, *, target: nextcord.Member):
    if target == None:
      target = interaction.user

    embed = nextcord.Embed()
    embed.title = "User Info"
    embed.set_thumbnail(url=target.avatar.url)
    fields = [
      ("ID", target.id, False),
      ("Name", str(target), True),
      ("Bot?", target.bot, True),
      ("Top Role", target.top_role.mention, True),
      ("Status", str(target.status).title(), True),
      #("Activity", f"{target.activity.name} {str(getattr(target.activity, 'type')).title()}", True),
      ("Created At", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
      ("Joined At", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True)
    ]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.response.send_message(embed=embed)

  @nextcord.slash_command(name='avatar',
                          description="Display mentioned user's avatar.",
                          guild_ids=asukaDB.testServers)
  async def avatar(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    if target == None:
      target = interaction.user

    embed = Embed()
    embed.set_image(url=target.display_avatar)
    embed.color = 0x4887c6
    embed.title = target.name + "'s Avatar"
    embed.set_footer(text="Requested by " + author.name)
    await interaction.response.send_message(embed=embed)

  @nextcord.slash_command(name='daisuki',
                          description="Return affection to my owner only.",
                          guild_ids=asukaDB.testServers)
  async def daisuki(self, interaction):
    master = "<@380016239310929931>"
    if interaction.user.id == 380016239310929931:
      await interaction.response.send_message(
        "Watashi mo! " + interaction.user.mention +
        "-Sama!:heart:\nhttps://tenor.com/ZOap.gif")
    else:
      await interaction.response.send_message(
        "hehe, do u really think I could accept those mere feelings when I have "
        + master + "-Sama???\nhttps://tenor.com/buIuA.gif")

  @nextcord.slash_command(name='tadaima',
                          description="soothing waifu",
                          guild_ids=asukaDB.testServers)
  async def tadaima(self, interaction):
    tadaima_msg = [
      "Would u like your dinner?", "Or bath?", "Or...", "A", "su", "ka",
      "chan!?"
    ]
    async with interaction.channel.typing():
      time.sleep(2)
      honorifics = asukaDB.get_honorifics(interaction.user.id)
      await interaction.response.send_message('Welcome back ' +
                                              interaction.user.mention +
                                              honorifics + ' :heart:')

      for string in tadaima_msg:
        async with interaction.channel.typing():
          time.sleep(2)
          await interaction.channel.send(content=string)

  @nextcord.slash_command(name='explosion',
                          description="unleash strongest magic",
                          guild_ids=asukaDB.testServers)
  async def explosion(self, interaction):
    explosion_msg = [
      "I beseech thee, combine with my deep crimson.",
      "The time of awakening cometh.",
      "Justice, fallen upon the infallible boundary,",
      "appear now as an intangible distortion!",
      "This is the mightiest means of attack known to man,",
      "the ultimate attack magic!", "# **EXPLOSION!!**",
      "https://media1.tenor.com/images/a5200ff8939402e4e2bbda3a8107d2b1/tenor.gif?itemid=7559840"
    ]
    async with interaction.channel.typing():
      time.sleep(2)
      await interaction.response.send_message(
        'Darkness blacker than black and darker than dark,')

    for string in explosion_msg:
      async with interaction.channel.typing():
        time.sleep(3)
      await interaction.channel.send(content=string)


def setup(bot):
  bot.add_cog(interactionsSlash(bot))
