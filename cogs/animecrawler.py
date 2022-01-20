import discord
from discord.ext import commands
from discord import Embed
import requests
from bs4 import BeautifulSoup
import asyncio

class Anime:
  type=""
  episodes=""
  status=""
  aired=""
  premiered=""
  broadcast=""
  studios=""
  source=""
  genres=""
  duration=""
  rating=""
  score=""
  title=""
  link=""
  synopsis=""
  thumbnail=""

def searchAnimeInfo(url, obj):
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct=0 
  tstring=""  
  for link in soup.findAll('a', {'class': 'hoverinfo_trigger fw-b fl-l'}):
    if ct<5:
      temp=Anime()
      temp.title = str(link.contents).replace("['", "", -1)
      temp.title = temp.title.replace("']", "", -1)
      temp.link = link.get('href')
      tstring+="\n**" + str(ct+1) + ")** " + temp.title
      #thumbnail = soup.findAll('img', {'class': 'lazyloaded'})
      #temp.thumbnail = thumbnail.get('src')
      obj.append(temp)
      ct+=1
    else:
      break
  return tstring

def searchTopAnime(url, obj):
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct=0   
  tstring=""
  for link in soup.findAll('h3', {'class': 'hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3'}):
    if ct<10:
      temp=Anime()
      tlink=link.find('a')
      temp.title = str(tlink.next_element)
      temp.link = tlink.get('href')
      tstring+="\n**" + str(ct+1) + ")** " + temp.title
      obj.append(temp)
      ct+=1
    else:
      break
  return tstring

def searchSeasonAnime(url, obj):
  source_code = requests.get(url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  ct=0
  tstring="" 
  for link in soup.findAll('h2', {'class': 'h2_anime_title'}):
    if ct<20:
      temp=Anime()
      tlink=link.find('a')
      temp.title = str(tlink.next_element)
      temp.link = tlink.get('href')
      tstring+="\n**" + str(ct+1) + ")** " + temp.title
      obj.append(temp)
      ct+=1
    else:
      break
  return tstring

def getTextInfo(soup, text):
  content="N\\A"
  for anime in soup.findAll('span', {'class': 'dark_text'}):
    if text in str(anime):
      if text != "Score":            
        content=str(anime.nextSibling)
      else:
        temp=anime.parent.find('span', {'itemprop': 'ratingValue'})
        content=str(temp.next_element)
      content=content.replace("\n ", "", -1)
      content=content.lstrip(' ')
      if content=="\n":
        content=""
        ct=0
        for temp in anime.parent.findAll('a'):
          if ct >= 1:
            content+=", "
          content += str(temp.next_element)
          ct+=1
      break
  return content

def getInfo(index, obj):
  source_code = requests.get(obj[index].link)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")
  
  
  obj[index].type=getTextInfo(soup, "Type")
  obj[index].episodes=getTextInfo(soup, "Episodes")
  obj[index].status=getTextInfo(soup, "Status")
  obj[index].aired=getTextInfo(soup, "Aired")
  obj[index].premiered=getTextInfo(soup, "Premiered")
  obj[index].broadcast=getTextInfo(soup, "Broadcast")
  obj[index].studios=getTextInfo(soup, "Studios")
  obj[index].source=getTextInfo(soup, "Source")
  obj[index].genres=getTextInfo(soup, "Genres")
  obj[index].duration=getTextInfo(soup, "Duration")
  obj[index].rating=getTextInfo(soup, "Rating")
  obj[index].score=getTextInfo(soup, "Score")
  #for synopsis
  temp=soup.find('p', {'itemprop': 'description'})
  for content in temp.contents:
    if "<br>" and "<br/>" not in str(content):
        obj[index].synopsis+=str(content)
  obj[index].synopsis=str(obj[index].synopsis.replace("<i>", "***", -1))
  obj[index].synopsis=str(obj[index].synopsis.replace("</i>", "***", -1))

def printAnimeInfo(index, obj):
  #animeTest="\n\n##########################################\n"
  animeTest=""
  animeTest+="**Title: **" + obj[index].title
  animeTest+="\n**Type: **" + obj[index].type
  animeTest+="\n**Episodes: **" + obj[index].episodes
  animeTest+="\n**Status: **" + obj[index].status
  animeTest+="\n**Aired: **" + obj[index].aired
  animeTest+="\n**Premiered: **" + obj[index].premiered
  animeTest+="\n**Broadcast: **" + obj[index].broadcast
  animeTest+="\n**Studios: **" + obj[index].studios
  animeTest+="\n**Source: **" + obj[index].source
  animeTest+="\n**Genres: **" + obj[index].genres
  animeTest+="\n**Duration: **" + obj[index].duration
  animeTest+="\n**Rating: **" + obj[index].rating
  animeTest+="\n**Score: **" + obj[index].score
  #animeTest+="\n**Synopsis: **" + obj[index].synopsis
  #animeTest+="\n##########################################"
  return animeTest

class animecrawler(commands.Cog):
  def __init__(self, bot):
        self.bot = bot
 

  @commands.command()
  async def searchAnime(self, ctx):
    """ Search Anime info. """
    
    currentp=ctx.author.id
    obj=[]
    temp=""

    def check(m):
        return m.author.id == currentp and m.channel == ctx.channel

    if not ctx.message.content.replace("$searchAnime", "", -1)=="":
      temp=str(ctx.message.content.replace("$searchAnime ", "", -1))
    if temp=="":
      await ctx.send("pls don't waste my time, next time remember to write what anime you want to search b-baka")
      return
    search="https://myanimelist.net/search/all?cat=all&q=" + temp.replace(" ", "%20", -1)
    await ctx.send(searchAnimeInfo(search, obj))
    
    await ctx.send("Choose one of the results above.")
    try:
      response = await self.bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
      await ctx.send("Timed Out, you took too much to reply b-baka!")
      return
    try:
      choice=int(response.content)
      choice-=1
      getInfo(choice, obj)
      embed = Embed()
      embed.color = 10181046
      embed.title = obj[choice].title
      embed.description=printAnimeInfo(choice, obj)
      #embed.set_thumbnail(url=obj[choice].thumbnail)
      #await ctx.send(printAnimeInfo(choice, obj))
      await ctx.send(embed=embed)
    except:
      await ctx.send("Invalid response b-baka!")
            
  @commands.command()
  async def topAnime(self, ctx):
    """ Search Top 10 Anime. """
    
    currentp=ctx.author.id
    obj=[]

    def check(m):
        return m.author.id == currentp and m.channel == ctx.channel
    
    await ctx.send(searchTopAnime("https://myanimelist.net/topanime.php?type=bypopularity", obj))
    await ctx.send("Choose one of the results above.")
    try:
      response = await self.bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
      await ctx.send("Timed Out, you took too much to reply b-baka!")
      return
    try:
      choice=int(response.content)
      choice-=1
      getInfo(choice, obj)
      embed = Embed()
      embed.color = 10181046
      embed.title = obj[choice].title
      embed.description=printAnimeInfo(choice, obj)
      #embed.set_thumbnail(url=obj[choice].thumbnail)
      #await ctx.send(printAnimeInfo(choice, obj))
      await ctx.send(embed=embed)
    except:
      await ctx.send("Invalid response b-baka!")

  @commands.command()
  async def seasonAnime(self, ctx):
    """ Search current Season Anime. """
    
    currentp=ctx.author.id
    obj=[]

    def check(m):
        return m.author.id == currentp and m.channel == ctx.channel

    await ctx.send(searchSeasonAnime("https://myanimelist.net/anime/season", obj))
    await ctx.send("Choose one of the results above.")
    try:
      response = await self.bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
      await ctx.send("Timed Out, you took too much to reply b-baka!")
      return
    try:
      choice=int(response.content)
      choice-=1
      getInfo(choice, obj)
      embed = Embed()
      embed.color = 10181046
      embed.title = obj[choice].title
      embed.description=printAnimeInfo(choice, obj)
      #embed.set_thumbnail(url=obj[choice].thumbnail)
      #await ctx.send(printAnimeInfo(choice, obj))
      await ctx.send(embed=embed)
    except:
      await ctx.send("Invalid response b-baka!")

def setup(bot):
  bot.add_cog(animecrawler(bot))