import nextcord
from nextcord.ext import commands
from nextcord import Embed
#from nextcord import Button, ButtonStyle
import requests
from bs4 import BeautifulSoup
import asyncio

class Manga:
  type=""
  volumes=""
  chapters=""
  status=""
  published=""
  genres=""
  demographic=""
  serialization=""
  authors=""
  score=""
  title=""
  link=""
  synopsis=""
  background=""
  thumbnail=""

def searchMangaInfo(url, obj):
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct=0 
  tstring=""
  for link in soup.findAll('a', {'class': 'hoverinfo_trigger fw-b'}):
    if ct<5:
      
      temp=Manga()
      temp.title = str(link.contents).replace("[<strong>", "", -1)
      temp.title = temp.title.replace("</strong>]", "", -1)
      temp.link = link.get('href')
      tstring+="\n**" + str(ct+1) + ")** " + temp.title
      obj.append(temp)
      ct+=1
    else:
      break
  return tstring

def searchTopManga(url, obj):
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct=0   
  tstring=""
  for link in soup.findAll('a', {'class': 'hoverinfo_trigger fs14 fw-b'}):
    if ct<10:
      temp=Manga()
      temp.title = str(link.next_element)
      temp.link = link.get('href')
      tstring+="\n**" + str(ct+1) + ")** " + temp.title
      obj.append(temp)
      ct+=1
    else:
      break
  return tstring

def getTextInfo(soup, text):
  content="N\\A"
  for manga in soup.findAll('span', {'class': 'dark_text'}):
    if text in str(manga):
      if text == "Type":
        temp= manga.parent.find('a')
        content=str(temp.next_element)
        return content

      if text != "Score":            
        content=str(manga.nextSibling)
        
      else:
        temp=manga.parent.find('span', {'itemprop': 'ratingValue'})
        try:
          content=str(temp.next_element)
        except:
          content="N/A"
      content=content.replace("\n ", "", -1)
      content=content.lstrip(' ')
      
      if content=="\n":
        content=""
        ct=0
        for temp in manga.parent.findAll('a'):
          if ct >= 1:
            content+=", "
          content += str(temp.next_element)
          ct+=1
      content=content.replace("\n", "", -1)
      break
  return content

def getInfo(index, obj):
  source_code = requests.get(obj[index].link)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")

  obj[index].type=getTextInfo(soup, "Type")
  obj[index].volumes=getTextInfo(soup, "Volumes")
  obj[index].chapters=getTextInfo(soup, "Chapters")
  obj[index].status=getTextInfo(soup, "Status")
  obj[index].published=getTextInfo(soup, "Published")
  obj[index].genres=getTextInfo(soup, "Genres")
  obj[index].demographic=getTextInfo(soup, "Demographic")
  obj[index].serialization=getTextInfo(soup, "Serialization")
  obj[index].authors=getTextInfo(soup, "Authors")
  obj[index].score=getTextInfo(soup, "Score")
  #for thumbnail
  ctThumb=0
  for images in soup.findAll('img'):
    if ctThumb==1:
      thumbnail=images
      break
    ctThumb+=1
  obj[index].thumbnail = thumbnail.get('data-src')

  #for synopsis
  temp=soup.find('span', {'itemprop': 'description'})
  for content in temp.contents:
    if "<br>" and "<br/>" not in str(content):
      obj[index].synopsis+=str(content)
  obj[index].synopsis=str(obj[index].synopsis.replace("<i>", "***", -1))
  obj[index].synopsis=str(obj[index].synopsis.replace("</i>", "***", -1))
  obj[index].synopsis=str(obj[index].synopsis.replace("<br>", "", -1))
  obj[index].synopsis=str(obj[index].synopsis.replace("</br>", "", -1))

def printMangaInfo(index, obj):
  mangaTest=""
  mangaTest+="**Title: **" + obj[index].title
  mangaTest+="\n**Type: **" + obj[index].type
  mangaTest+="\n**Volumes: **" + obj[index].volumes
  mangaTest+="\n**Chapters: **" + obj[index].chapters
  mangaTest+="\n**Status: **" + obj[index].status
  mangaTest+="\n**Published: **" + obj[index].published
  mangaTest+="\n**Genres: **" + obj[index].genres
  mangaTest+="\n**Demographic: **" + obj[index].demographic
  mangaTest+="\n**Serialization: **" + obj[index].serialization
  mangaTest+="\n**Authors: **" + obj[index].authors
  mangaTest+="\n**Score: **" + obj[index].score
  mangaTest+="\n" + obj[index].link
  return mangaTest

class mangacrawler(commands.Cog):
  def __init__(self, bot):
        self.bot = bot
 

  @commands.command()
  async def searchManga(self, ctx, *, args):
    """ Search Manga info. """
    
    currentp=ctx.author.id
    obj=[]
    temp=""

    def check(m):
        return m.author.id == currentp and m.channel == ctx.channel

    try:
      temp=args
    except:
      await ctx.send("pls don't waste my time, next time remember to write what manga you want to search b-baka")
      return
    search="https://myanimelist.net/manga.php?cat=manga&q=" + temp.replace(" ", "%20", -1)
    await ctx.send(searchMangaInfo(search, obj))
    
    await ctx.send("Choose one of the results above.")
    try:
      response = await self.bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
      return
    try:
      choice=int(response.content)
      choice-=1
      try:
        getInfo(choice, obj)
      except Exception as e:
        print(e)
        return
      embed = Embed()
      embed.color = 0xf8562d
      embed.title = obj[choice].title
      embed.set_image(url=obj[choice].thumbnail)
      embed.description=printMangaInfo(choice, obj)
      embed.set_footer(text='Page 1/2')
      synopsisEmbed = Embed()
      synopsisEmbed.set_footer(text='Page 2/2')
      synopsisEmbed.color = 0xf8562d
      synopsisEmbed.title = obj[choice].title
      synopsisEmbed.description = "**Synopsis: **" + obj[choice].synopsis
      #embed.set_thumbnail(url=obj[choice].thumbnail)
      embedMessage = await ctx.send(embed=embed)
      asuka=embedMessage.author
      await embedMessage.add_reaction("▶️")
      embedCt=-1

      def checkReaction(reaction, user):
        global userReact
        if reaction.message == embedMessage and reaction.emoji=="▶️":
          if user == asuka:
            userReact = ctx.author
          else:
            userReact=user
            return True
      try:
        emoji="▶️"
        while await self.bot.wait_for('reaction_add', check=checkReaction, timeout=60):
          embedCt*=-1
          await embedMessage.remove_reaction(emoji, userReact)
          if embedCt==1:
            await embedMessage.edit(embed=synopsisEmbed)
          else:
            await embedMessage.edit(embed=embed)
          
      except asyncio.TimeoutError:
        await embedMessage.remove_reaction(emoji, asuka)
        return
      
      
    except Exception as e:
      print(e)
      await ctx.send("Invalid response b-baka!")
            
  @commands.command()
  async def topManga(self, ctx):
    """ Search Top 10 Manga. """
    
    currentp=ctx.author.id
    obj=[]

    def check(m):
        return m.author.id == currentp and m.channel == ctx.channel
    
    try:
      await ctx.send(searchTopManga("https://myanimelist.net/topmanga.php?type=bypopularity", obj))
    except Exception as e:
      print(e)
      return
    await ctx.send("Choose one of the results above for more info.")
    try:
      response = await self.bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
      return
    try:
      choice=int(response.content)
      choice-=1
      getInfo(choice, obj)
      embed = Embed()
      embed.color = 0xf8562d
      embed.title = obj[choice].title
      embed.set_image(url=obj[choice].thumbnail)
      embed.description=printMangaInfo(choice, obj)
      embed.set_footer(text='Page 1/2')
      synopsisEmbed = Embed()
      synopsisEmbed.set_footer(text='Page 2/2')
      synopsisEmbed.color = 0xf8562d
      synopsisEmbed.title = obj[choice].title
      synopsisEmbed.description = "**Synopsis: **" + obj[choice].synopsis
      #embed.set_thumbnail(url=obj[choice].thumbnail)
      embedMessage = await ctx.send(embed=embed)
      asuka=embedMessage.author
      await embedMessage.add_reaction("▶️")
      embedCt=-1

      def checkReaction(reaction, user):
        global userReact
        if reaction.message == embedMessage and reaction.emoji=="▶️":
          if user == asuka:
            userReact = ctx.author
          else:
            userReact=user
            return True
      try:
        emoji="▶️"
        while await self.bot.wait_for('reaction_add', check=checkReaction, timeout=60):
          embedCt*=-1
          await embedMessage.remove_reaction(emoji, userReact)
          if embedCt==1:
            await embedMessage.edit(embed=synopsisEmbed)
          else:
            await embedMessage.edit(embed=embed)
          
      except asyncio.TimeoutError:
        await embedMessage.remove_reaction(emoji, asuka)
        return
    except Exception as e:
      print(e)
      await ctx.send("Invalid response b-baka!")


def setup(bot):
  bot.add_cog(mangacrawler(bot))