import nextcord
from nextcord import Embed
from nextcord.ext import commands
from nextcord.ui import StringSelect, View
from bs4 import BeautifulSoup
import asyncio
import requests
import get_from_servers as asukaDB


class Anime:
  type = ""
  episodes = ""
  status = ""
  aired = ""
  premiered = ""
  broadcast = ""
  studios = ""
  source = ""
  genres = ""
  duration = ""
  rating = ""
  score = ""
  title = ""
  link = ""
  synopsis = ""
  thumbnail = ""


#########################################################################


def searchAnimeInfo(args):
  obj = []
  url = "https://myanimelist.net/search/all?cat=all&q=" + args.replace(
    " ", "%20", -1)

  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct = 0
  for link in soup.findAll('a', {'class': 'hoverinfo_trigger fw-b fl-l'}):
    if ct < 5:
      temp = Anime()
      temp.title = str(link.contents).replace("['", "", -1)
      temp.title = temp.title.replace("']", "", -1)
      temp.link = link.get('href')
      obj.append(temp)
      ct += 1
    else:
      break
  tstring = "Choose one of the animes below for more info."
  return tstring, obj


#########################################################################


def searchTopAnime():
  obj = []
  url = "https://myanimelist.net/topanime.php?type=bypopularity"
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct = 0
  for link in soup.findAll('h3', {'class': 'fl-l fs14 fw-b anime_ranking_h3'}):
    if ct < 10:
      temp = Anime()
      tlink = link.find('a')
      temp.title = str(tlink.next_element)
      temp.link = tlink.get('href')
      obj.append(temp)
      ct += 1
    else:
      break

  tstring = "Choose one of the animes below for more info."
  return tstring, obj


#########################################################################


def searchSeasonAnime():
  obj = []
  url = "https://myanimelist.net/anime/season"
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct = 0
  for link in soup.findAll('h2', {'class': 'h2_anime_title'}):
    if ct < 20:
      temp = Anime()
      tlink = link.find('a')
      temp.title = str(tlink.next_element)
      temp.link = tlink.get('href')
      obj.append(temp)
      ct += 1
    else:
      break

  tstring = "Choose one of the animes below for more info."
  return tstring, obj


#########################################################################


def getTextInfo(soup, text):
  content = "N\\A"
  for anime in soup.findAll('span', {'class': 'dark_text'}):
    if text in str(anime):
      if text != "Score":
        content = str(anime.nextSibling)
      else:
        temp = anime.parent.find('span', {'itemprop': 'ratingValue'})
        try:
          content = str(temp.next_element)
        except:
          content = "N/A"
      content = content.replace("\n ", "", -1)
      content = content.lstrip(' ')
      if content == "\n":
        content = ""
        ct = 0
        for temp in anime.parent.findAll('a'):
          if ct >= 1:
            content += ", "
          content += str(temp.next_element)
          ct += 1
      break
  return content


#########################################################################


def getInfo(index, obj):
  source_code = requests.get(obj[index].link)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")

  obj[index].type = getTextInfo(soup, "Type")
  obj[index].episodes = getTextInfo(soup, "Episodes")
  obj[index].status = getTextInfo(soup, "Status")
  obj[index].aired = getTextInfo(soup, "Aired")
  obj[index].premiered = getTextInfo(soup, "Premiered")
  obj[index].broadcast = getTextInfo(soup, "Broadcast")
  obj[index].studios = getTextInfo(soup, "Studios")
  obj[index].source = getTextInfo(soup, "Source")
  obj[index].genres = getTextInfo(soup, "Genres")
  obj[index].duration = getTextInfo(soup, "Duration")
  obj[index].rating = getTextInfo(soup, "Rating")
  obj[index].score = getTextInfo(soup, "Score")
  #for thumbnail
  ctThumb = 0
  for images in soup.findAll('img'):
    if ctThumb == 1:
      thumbnail = images
      break
    ctThumb += 1
  obj[index].thumbnail = thumbnail.get('data-src')

  #for synopsis
  temp = soup.find('p', {'itemprop': 'description'})
  for content in temp.contents:
    if "<br>" and "<br/>" not in str(content):
      obj[index].synopsis += str(content)
  obj[index].synopsis = str(obj[index].synopsis.replace("<i>", "***", -1))
  obj[index].synopsis = str(obj[index].synopsis.replace("</i>", "***", -1))

  embed = Embed()
  embed.color = 0x1a59ce  #10181046
  embed.title = obj[index].title
  embed.set_image(url=obj[index].thumbnail)
  embed.description = printAnimeInfo(index, obj)
  embed.set_footer(text='Page 1/2')

  synopsisEmbed = Embed()
  synopsisEmbed.set_footer(text='Page 2/2')
  synopsisEmbed.color = 0x1a59ce  #10181046
  synopsisEmbed.title = obj[index].title
  synopsisEmbed.description = "**Synopsis: **" + obj[index].synopsis

  return embed, synopsisEmbed


#########################################################################


def printAnimeInfo(index, obj):
  animeTest = ""
  animeTest += "**Title: **" + obj[index].title
  animeTest += "\n**Type: **" + obj[index].type
  animeTest += "\n**Episodes: **" + obj[index].episodes
  animeTest += "\n**Status: **" + obj[index].status
  animeTest += "\n**Aired: **" + obj[index].aired
  animeTest += "\n**Premiered: **" + obj[index].premiered
  animeTest += "\n**Broadcast: **" + obj[index].broadcast
  animeTest += "\n**Studios: **" + obj[index].studios
  animeTest += "\n**Source: **" + obj[index].source
  animeTest += "\n**Genres: **" + obj[index].genres
  animeTest += "\n**Duration: **" + obj[index].duration
  animeTest += "\n**Rating: **" + obj[index].rating
  animeTest += "\n**Score: **" + obj[index].score
  animeTest += "\n" + obj[index].link

  return animeTest


#########################################################################


async def controllerFunc(self, msgController, cmd, msg, obj):
  choice = None
  if (cmd == "interaction"):
    author = msgController.user
  else:
    author = msgController.author

  view = View()
  selectOptions = StringSelect(custom_id='selction0',
                               placeholder='-- choose anime --',
                               min_values=1,
                               max_values=1)

  for i in range(len(obj)):
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


class animecrawler(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def searchAnime(self, ctx, *, args):
    """ Search given Anime on myanimelist db. """

    msg, obj = searchAnimeInfo(args)
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(name='searchanime',
                          description="Search given Anime on myanimelist db",
                          guild_ids=asukaDB.testServers)
  async def searchAnimeSlash(self, interaction, *, anime: str):
    await interaction.response.defer(ephemeral=True, with_message=True)

    msg, obj = searchAnimeInfo(anime)
    await controllerFunc(self, interaction, "interaction", msg, obj)

  #########################################################################

  @commands.command()
  async def topAnime(self, ctx):
    """ Search Top 10 Anime on myanimelist db. """

    msg, obj = searchTopAnime()
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(name='topanime',
                          description="Search Top 10 Anime on myanimelist db",
                          guild_ids=asukaDB.testServers)
  async def topAnimeSlash(self, interaction):
    await interaction.response.defer(ephemeral=True, with_message=True)
    msg, obj = searchTopAnime()
    await controllerFunc(self, interaction, "interaction", msg, obj)

  #########################################################################

  @commands.command()
  async def seasonAnime(self, ctx):
    """ Search current season Anime on myanimelist db. """

    msg, obj = searchSeasonAnime()
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(
    name='seasonanime',
    description="Search current season Anime on myanimelist db",
    guild_ids=asukaDB.testServers)
  async def seasonAnimeSlash(self, interaction):
    await interaction.response.defer(ephemeral=True, with_message=True)
    msg, obj = searchSeasonAnime()
    await controllerFunc(self, interaction, "interaction", msg, obj)


def setup(bot):
  bot.add_cog(animecrawler(bot))
