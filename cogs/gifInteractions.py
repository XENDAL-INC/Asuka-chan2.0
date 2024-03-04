import nextcord
from nextcord.ext import commands
from nextcord import Embed
import get_from_servers as asukaDB


async def send_message(cmd,
                       msgController,
                       content=None,
                       embed=None,
                       ephemeral=False):
  if cmd == "ctx":
    await msgController.send(content, embed=embed)
  elif cmd == "interaction":
    if embed == None:
      await msgController.response.send_message(content,
                                                embed=embed,
                                                ephemeral=ephemeral)


def no_event_gifs(gifType, author, target):
  honorifics = asukaDB.get_honorifics(author.id)
  mention = target.mention
  embed = Embed()
  embed.color = 0xdf2020
  gif = asukaDB.get_random_gif(gifType)
  embed.set_image(url=gif)
  return honorifics, mention, embed


###############################################################################


async def slap_func(cmd, msgController, author, target):
  honorifics, mention, embed = no_event_gifs("slap", author, target)
  if target.id != author.id:  #while not mentioning yourself
    mention = target.mention
    if target.id == 842228270400536586:  #if XENDAL mention asuka
      if honorifics == '-sama':
        embed.title = "HIDOI! :broken_heart:"
        embed.description = f'*{author.mention}{honorifics} made {mention} cry!*'
        embed.set_image(url="https://c.tenor.com/otSAwjPqcJsAAAAC/sad-cry.gif")

      else:
        embed.title = "Heh. nice try!"  #if user mention asuka
        embed.description = f'{author.mention}{honorifics} failed miserably to punch {mention}!'
        embed.set_image(
          url="https://c.tenor.com/XN4eaRmwtkQAAAAC/nobara-kugisaki-nobara.gif"
        )

    else:
      embed.title = "You gave a slap!"  #if user mention another user
      embed.description = f'*YOOO, {author.mention}{honorifics} started slapping the shit out of {mention}!*'

  else:
    embed.title = "Are you... ok?!"
    embed.description = f'*{author.mention}{honorifics} started slapping themselves!*'
    embed.set_image(
      url="https://c.tenor.com/IVA2Go3aoAkAAAAC/pichu-pickachu.gif")

  if cmd == "ctx":
    await send_message(cmd=cmd, msgController=msgController, embed=embed)
  else:
    return embed


###############################################################################


async def punch_func(cmd, msgController, author, target):
  honorifics, mention, embed = no_event_gifs("punch", author, target)
  if target.id != author.id:  #while not mentioning yourself
    mention = target.mention
    if target.id == 842228270400536586:  #if XENDAL mention asuka
      if honorifics == '-sama':
        embed.title = "HIDOI! :broken_heart:"
        embed.description = f'*{author.mention}{honorifics} made {mention} cry!*'
        embed.set_image(url="https://c.tenor.com/otSAwjPqcJsAAAAC/sad-cry.gif")

      else:
        embed.title = "Heh. nice try!"  #if user mention asuka
        embed.description = f'{author.mention}{honorifics} failed miserably to punch {mention}!'
        embed.set_image(
          url="https://c.tenor.com/XN4eaRmwtkQAAAAC/nobara-kugisaki-nobara.gif"
        )

    else:
      embed.title = "You gave a punch!"  #if user mention another user
      embed.description = f'*SUGOI!!!, {author.mention}{honorifics} started punching {mention}!*'

  else:
    embed.title = "Are you... ok?!"
    embed.description = f'*{author.mention}{honorifics} started punching themselves!*'
    embed.set_image(
      url=
      'https://tenor.com/it/view/bonerdelete-anime-punch-penis-gif-17978908.gif'
    )

  if cmd == "ctx":
    await send_message(cmd=cmd, msgController=msgController, embed=embed)
  else:
    return embed


###############################################################################


async def kick_func(cmd, msgController, author, target):
  honorifics, mention, embed = no_event_gifs("kick", author, target)
  embed.title = "You gave a kick!"
  embed.description = f'*YOOO, {author.mention}{honorifics} started kicking the shit out of {mention}!*'
  if cmd == "ctx":
    await send_message(cmd=cmd, msgController=msgController, embed=embed)
  else:
    return embed


@nextcord.slash_command(name='kiss',
                        description="Kiss another user.",
                        guild_ids=asukaDB.testServers)
async def kiss_func(cmd, msgController, author, target):
  honorifics, mention, embed = no_event_gifs("kiss", author, target)
  embed.title = "You gave a kiss!"
  embed.description = f'*Awww, {author.mention}{honorifics} blew a kiss to {mention}!*'
  if cmd == "ctx":
    await send_message(cmd=cmd, msgController=msgController, embed=embed)
  else:
    return embed


###############################################################################


async def lick_func(cmd, msgController, author, target):
  honorifics, mention, embed = no_event_gifs("lick", author, target)
  embed.title = "You gave a lick!"
  embed.description = f'*Ewww,{ author.mention}{honorifics} licked {mention} like a puppy!*'
  if cmd == "ctx":
    await send_message(cmd=cmd, msgController=msgController, embed=embed)
  else:
    return embed


###############################################################################


async def hug_func(cmd, msgController, author, target):
  honorifics, mention, embed = no_event_gifs("hug", author, target)
  if target.id != author.id:  #while not mentioning yourself
    mention = target.mention
    if target.id == 842228270400536586:  #if XENDAL mention asuka
      if honorifics == '-sama':
        embed.title = "b-Baka! s-stop... pls :heart:"
        embed.description = f'*{author.mention}{honorifics} made {mention} blush!*'
        embed.set_image(
          url=
          "https://tenor.com/it/view/anime-cute-girl-kotori-itsuka-date-a-live-gif-17438857.gif"
        )

      else:
        embed.title = "Huh, that is so creepy.."  #if user mention asuka
        embed.description = f'*{author.mention}{honorifics} started ridiculing themselves!*'
        embed.set_image(
          url=
          "https://tenor.com/it/view/ram-re-zero-mad-death-stare-anime-gif-17531442.gif"
        )

    else:
      embed.title = "You gave a hug!"  #if user mention another user
      embed.description = f'*Aww, {author.mention}{honorifics} started hugging {mention}!*'

  else:
    embed.title = "Are you... ok?!"
    embed.description = f'*{author.mention}{honorifics} started hugging themselves <:Harold1:605069232249765899>!*'
    embed.set_image(
      url=
      'https://tenor.com/it/view/natsume-hidamari-sketch-pillow-hug-anime-roll-gif-21546649.gif'
    )

  if cmd == "ctx":
    await send_message(cmd=cmd, msgController=msgController, embed=embed)
  else:
    return embed


###############################################################################


class gifInteractions(commands.Cog):

  def _init_(self, bot):
    self.bot = bot

  ###############################################################################

  @commands.command(aliases=['slaps', 'bitchslap', 'bitchslaps'])
  async def slap(self, ctx):
    author = ctx.message.author
    await slap_func("ctx", ctx, author, ctx.message.mentions[0])

  @nextcord.slash_command(name='slap',
                          description="Slap another user.",
                          guild_ids=asukaDB.testServers)
  async def slap_slash(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    embed = await slap_func("interaction", interaction, author, target)
    await interaction.response.send_message(embed=embed)

  ###############################################################################

  @commands.command(aliases=['hit', 'hits', 'jab', 'jabs', 'punches'])
  async def punch(self, ctx):
    author = ctx.message.author
    await punch_func("ctx", ctx, author, ctx.message.mentions[0])

  @nextcord.slash_command(name='punch',
                          description="Punch another user.",
                          guild_ids=asukaDB.testServers)
  async def punch_slash(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    embed = await punch_func("interaction", interaction, author, target)
    await interaction.response.send_message(embed=embed)

  ###############################################################################

  @commands.command()
  async def kick(self, ctx):
    author = ctx.message.author
    await kick_func("ctx", ctx, author, ctx.message.mentions[0])

  @nextcord.slash_command(name='kick',
                          description="Kick another user.",
                          guild_ids=asukaDB.testServers)
  async def kick_slash(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    embed = await kick_func("interaction", interaction, author, target)
    await interaction.response.send_message(embed=embed)

  ###############################################################################

  @commands.command()
  async def lick(self, ctx):
    author = ctx.message.author
    await lick_func("ctx", ctx, author, ctx.message.mentions[0])

  @nextcord.slash_command(name='lick',
                          description="Lick another user.",
                          guild_ids=asukaDB.testServers)
  async def lick_slash(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    embed = await lick_func("interaction", interaction, author, target)
    await interaction.response.send_message(embed=embed)

  ###############################################################################

  @commands.command()
  async def kiss(self, ctx):
    author = ctx.message.author
    await kiss_func("ctx", ctx, author, ctx.message.mentions[0])

  @nextcord.slash_command(name='kiss',
                          description="Kiss another user.",
                          guild_ids=asukaDB.testServers)
  async def kiss_slash(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    embed = await kiss_func("interaction", interaction, author, target)
    await interaction.response.send_message(embed=embed)

  ###############################################################################

  @commands.command(aliases=['hugs', 'cuddle', 'cuddling'])
  async def hug(self, ctx):
    author = ctx.message.author
    await hug_func("ctx", ctx, author, ctx.message.mentions[0])

  @nextcord.slash_command(name='hug',
                          description="Hug another user.",
                          guild_ids=asukaDB.testServers)
  async def hug_slash(self, interaction, *, target: nextcord.Member):
    author = interaction.user
    embed = await hug_func("interaction", interaction, author, target)
    await interaction.response.send_message(embed=embed)


###############################################################################


def setup(bot):
  bot.add_cog(gifInteractions(bot))
