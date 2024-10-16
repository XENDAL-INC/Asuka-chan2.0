import nextcord
from nextcord import Embed
from nextcord.ext import commands
from nextcord.ui import StringSelect, View
from bs4 import BeautifulSoup
import asyncio
import requests
import get_from_servers as asukaDB


class Manga:
  type = ""
  volumes = ""
  chapters = ""
  status = ""
  published = ""
  genres = ""
  demographic = ""
  serialization = ""
  authors = ""
  score = ""
  title = ""
  link = ""
  synopsis = ""
  background = ""
  thumbnail = ""


#########################################################################


def searchMangaInfo(args):
  obj = []
  url = "https://myanimelist.net/manga.php?cat=manga&q=" + args.replace(
    " ", "%20", -1)

  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct = 0
  tstring = ""
  for link in soup.findAll('a', {'class': 'hoverinfo_trigger fw-b'}):
    if ct < 5:

      temp = Manga()
      temp.title = str(link.contents).replace("[<strong>", "", -1)
      temp.title = temp.title.replace("</strong>]", "", -1)
      temp.link = link.get('href')
      obj.append(temp)
      ct += 1
    else:
      break
    tstring = "Choose one of the Mangas below for more info."
  return tstring, obj


#########################################################################


def searchTopManga():
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
  return tstring, obj


#########################################################################


def getTextInfo(soup, text):
  content = "N\\A"
  for manga in soup.findAll('span', {'class': 'dark_text'}):
    if text in str(manga):
      if text == "Type":
        temp = manga.parent.find('a')
        content = str(temp.next_element)
        return content

      if text != "Score":
        content = str(manga.nextSibling)

      else:
        temp = manga.parent.find('span', {'itemprop': 'ratingValue'})
        try:
          content = str(temp.next_element)
        except:
          content = "N/A"
      content = content.replace("\n ", "", -1)
      content = content.lstrip(' ')

      if content == "\n":
        content = ""
        ct = 0
        for temp in manga.parent.findAll('a'):
          if ct >= 1:
            content += ", "
          content += str(temp.next_element)
          ct += 1
      content = content.replace("\n", "", -1)
      break
  return content


def getInfo(index, obj):
  source_code = requests.get(obj[index].link)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")

  obj[index].type = getTextInfo(soup, "Type")
  obj[index].volumes = getTextInfo(soup, "Volumes")
  obj[index].chapters = getTextInfo(soup, "Chapters")
  obj[index].status = getTextInfo(soup, "Status")
  obj[index].published = getTextInfo(soup, "Published")
  obj[index].genres = getTextInfo(soup, "Genres")
  obj[index].demographic = getTextInfo(soup, "Demographic")
  obj[index].serialization = getTextInfo(soup, "Serialization")
  obj[index].authors = getTextInfo(soup, "Authors")
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
  temp = soup.find('span', {'itemprop': 'description'})
  for content in temp.contents:
    if "<br>" and "<br/>" not in str(content):
      obj[index].synopsis += str(content)
  obj[index].synopsis = str(obj[index].synopsis.replace("<i>", "***", -1))
  obj[index].synopsis = str(obj[index].synopsis.replace("</i>", "***", -1))
  obj[index].synopsis = str(obj[index].synopsis.replace("<br>", "", -1))
  obj[index].synopsis = str(obj[index].synopsis.replace("</br>", "", -1))

  embed = Embed()
  embed.color = 0xf8562d
  embed.title = obj[index].title
  embed.set_image(url=obj[index].thumbnail)
  embed.description = printMangaInfo(index, obj)
  embed.set_footer(text='Page 1/2')
  synopsisEmbed = Embed()
  synopsisEmbed.set_footer(text='Page 2/2')
  synopsisEmbed.color = 0xf8562d
  synopsisEmbed.title = obj[index].title
  synopsisEmbed.description = "**Synopsis: **" + obj[index].synopsis

  return embed, synopsisEmbed


#########################################################################


def printMangaInfo(index, obj):
  mangaTest = ""
  mangaTest += "**Title: **" + obj[index].title
  mangaTest += "\n**Type: **" + obj[index].type
  mangaTest += "\n**Volumes: **" + obj[index].volumes
  mangaTest += "\n**Chapters: **" + obj[index].chapters
  mangaTest += "\n**Status: **" + obj[index].status
  mangaTest += "\n**Published: **" + obj[index].published
  mangaTest += "\n**Genres: **" + obj[index].genres
  mangaTest += "\n**Demographic: **" + obj[index].demographic
  mangaTest += "\n**Serialization: **" + obj[index].serialization
  mangaTest += "\n**Authors: **" + obj[index].authors
  mangaTest += "\n**Score: **" + obj[index].score
  mangaTest += "\n" + obj[index].link
  return mangaTest


#########################################################################


async def controllerFunc(self, msgController, cmd, msg, obj):
  choice = None
  if (cmd == "interaction"):
    author = msgController.user
  else:
    author = msgController.author

  view = View()
  selectOptions = StringSelect(custom_id='selction0',
                               placeholder='-- choose manga --',
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


class mangacrawler(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def searchManga(self, ctx, *, args):
    """ Search given Manga on myanimelist db. """

    msg, obj = searchMangaInfo(args)
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(name='searchmanga',
                          description="Search given Manga on myanimelist db",
                          guild_ids=asukaDB.testServers)
  async def searchMangaSlash(self, interaction, *, args):
    await interaction.response.defer(ephemeral=True, with_message=True)
    msg, obj = searchMangaInfo(args)
    await controllerFunc(self, interaction, "interaction", msg, obj)

  #########################################################################

  @commands.command()
  async def topManga(self, ctx):
    """ Search Top 10 Manga on myanimelist db. """

    msg, obj = searchTopManga()
    await controllerFunc(self, ctx, "ctx", msg, obj)

  @nextcord.slash_command(name='topmanga',
                          description="Search Top 10 Manga on myanimelist db",
                          guild_ids=asukaDB.testServers)
  async def topMangaSlash(self, interaction):
    await interaction.response.defer(ephemeral=True, with_message=True)
    msg, obj = searchTopManga()
    await controllerFunc(self, interaction, "interaction", msg, obj)


def setup(bot):
  bot.add_cog(mangacrawler(bot))
