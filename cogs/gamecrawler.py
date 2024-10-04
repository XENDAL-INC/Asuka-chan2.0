import nextcord
from nextcord import Embed
from nextcord.ext import commands
from nextcord.ui import StringSelect, View
from bs4 import BeautifulSoup
import asyncio
import requests
import get_from_servers as asukaDB


class Game:
  appid = ""
  title = ""
  link = ""
  thumbnail = ""
  price = ""
  developer = ""
  publisher = ""
  release_date = ""
  synopsis = ""


#########################################################################


def searchGameInfo(args):
  obj = []
  args = args.replace(" ", "%20", -1)
  url = f"https://store.steampowered.com/search/?term={args}"

  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct = 0
  for link in soup.findAll('a', attrs={'data-ds-appid': True}):
    if ct < 5:
      temp = Game()
      temp.appid = link.get('data-ds-appid')

      temp.title = link.find('span', {'class': 'title'}).text
      temp.link = f"https://store.steampowered.com/app/{temp.appid}"
      obj.append(temp)
      ct += 1
    else:
      break
  tstring = "Choose one of the Games below for more info."
  return tstring, obj


#########################################################################
'''def searchTopManga():
  obj = []
  url = "https://myanimelist.net/topmanga.php?type=bypopularity"

  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct = 0
  tstring = ""
  for link in soup.findAll('a', {'class': 'hoverinfo_trigger fs14 fw-b'}):
    if ct < 10:
      temp = Manga()
      temp.title = str(link.next_element)
      temp.link = link.get('href')
      obj.append(temp)
      ct += 1
    else:
      break
    tstring = "Choose one of the Mangas below for more info."
  return tstring, obj'''

#########################################################################


def getInfo(index, obj):
  source_code = requests.get(obj[index].link)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")

  for developer in soup.findAll('div', attrs={'id': 'developers_list'}):
    obj[index].developer += f", {developer.find('a').text}"
  obj[index].developer = obj[index].developer[2:]

  isBreak = False
  for div in soup.findAll('div', attrs={'class': 'summary column'}):
    if not isBreak:
      if div.get('id') == 'developers_list':
        isBreak = True
    else:
      for publisher in div.findAll('a'):
        obj[index].publisher += f", {publisher.text}"
      obj[index].publisher = obj[index].publisher[2:]
      break

  obj[index].release_date = soup.find('div', attrs={'class': 'date'}).text
  obj[index].price = soup.find('div',
                               attrs={
                                 'class': 'game_purchase_price price'
                               }).text.strip()

  #for thumbnail
  obj[index].thumbnail = soup.find('link', attrs={
    'rel': "image_src"
  }).get('href')

  #for synopsis
  obj[index].synopsis = soup.find('div', attrs={
    'id': 'aboutThisGame'
  }).find('div', attrs={
    'class': 'game_area_description'
  }).text

  embed = Embed()
  embed.color = 0xf8562d
  embed.title = obj[index].title
  embed.set_image(url=obj[index].thumbnail)
  embed.description = printGameInfo(index, obj)
  embed.set_footer(text='Page 1/2')
  synopsisEmbed = Embed()
  synopsisEmbed.set_footer(text='Page 2/2')
  synopsisEmbed.color = 0xf8562d
  synopsisEmbed.title = obj[index].title
  synopsisEmbed.description = obj[index].synopsis

  return embed, synopsisEmbed


#########################################################################


def printGameInfo(index, obj):
  gameString = f"**AppID: ** {obj[index].appid}"
  gameString += f"\n**Title:** {obj[index].title}"
  gameString += f"\n**Release Date:** {obj[index].release_date}"
  gameString += f"\n**Developer:** {obj[index].developer}"
  gameString += f"\n**Publisher:** {obj[index].publisher}"
  gameString += f"\n**Price:** {obj[index].price}"
  gameString += f"\n{obj[index].link}"

  return gameString


#########################################################################


async def controllerFunc(self, msgController, cmd, msg, obj):
  choice = None
  if (cmd == "interaction"):
    author = msgController.user
  else:
    author = msgController.author

  view = View()
  selectOptions = StringSelect(custom_id='selction0',
                               placeholder='-- choose game --',
                               min_values=1,
                               max_values=1)

  for i in range(len(obj)):
    if i >= 25:
      break
    title = obj[i].title
    shortened_title = title[:50] if len(title) > 50 else title
    selectOptions.add_option(label=str(i + 1) + " - " + shortened_title,
                             value=str(i))

  async def handle_select(interaction):
    nonlocal choice
    selected_value = interaction.data['values'][0]
    choice = int(selected_value)
    view.stop()

  selectOptions.callback = handle_select
  view.add_item(selectOptions)

  if cmd == "interaction":
    chooseMsg = await msgController.send(content=msg,
                                         view=view,
                                         ephemeral=True)
  else:
    chooseMsg = await msgController.send(content=msg, view=view)
  await view.wait()

  try:
    await chooseMsg.delete()
    embed, synopsisEmbed = getInfo(choice, obj)
    embedMessage = await msgController.channel.send(embed=embed)
    await embedMessage.add_reaction("▶️")
    embedCt = -1

    def checkReaction(reaction, user):
      global userReact
      if reaction.message == embedMessage and reaction.emoji == "▶️":
        if user.id == asukaDB.asuka:
          userReact = author
        else:
          userReact = user
          return True

    try:
      emoji = "▶️"
      while await self.bot.wait_for('reaction_add',
                                    check=checkReaction,
                                    timeout=60):
        embedCt *= -1
        await embedMessage.remove_reaction(emoji, userReact)
        if embedCt == 1:
          await embedMessage.edit(embed=synopsisEmbed)
        else:
          await embedMessage.edit(embed=embed)

    except asyncio.TimeoutError:
      if embedMessage != None:
        await embedMessage.remove_reaction(emoji, asukaDB.asuka)
      return
  except Exception as e:
    print(e)


#########################################################################


class gamecrawler(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def searchGame(self, ctx, *, game: str):
    """ Search given Game on Steam db. """

    msg, obj = searchGameInfo(game)
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(name='searchgame',
                          description="Search given Game on Steam db",
                          guild_ids=asukaDB.testServers)
  async def searchGameSlash(self, interaction, *, game: str):
    await interaction.response.defer(ephemeral=True, with_message=True)
    msg, obj = searchGameInfo(game)
    await controllerFunc(self, interaction, "interaction", msg, obj)

  #########################################################################
  '''@commands.command()
  async def topGame(self, ctx):
    """ Search Top 10 Manga on myanimelist db. """

    msg, obj = searchTopManga()
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(name='topmanga',
                          description="Search Top 10 Manga on myanimelist db",
                          guild_ids=asukaDB.testServers)
  async def topMangaSlash(self, interaction):
    await interaction.response.defer(ephemeral=True, with_message=True)
    msg, obj = searchTopManga()
    await controllerFunc(self, interaction, "interaction", msg, obj)'''


def setup(bot):
  bot.add_cog(gamecrawler(bot))
