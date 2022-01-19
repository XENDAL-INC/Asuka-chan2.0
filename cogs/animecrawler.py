import discord
from discord.utils import get
from discord.ext import commands
from discord import Embed
import requests
from bs4 import BeautifulSoup


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


def printAnimeInfo(index, obj):
  animeTest="\n\n##########################################\n"
  animeTest+="Title: " + obj[index].title
  animeTest+="\nType: " + obj[index].type
  animeTest+="\nEpisodes: " + obj[index].episodes
  animeTest+="\nStatus: " + obj[index].status
  animeTest+="\nAired: " + obj[index].aired
  animeTest+="\nPremiered: " + obj[index].premiered
  animeTest+="\nBroadcast: " + obj[index].broadcast
  animeTest+="\nStudios: " + obj[index].studios
  animeTest+="\nSource: " + obj[index].source
  animeTest+="\nGenres: " + obj[index].genres
  animeTest+="\nDuration: " + obj[index].duration
  animeTest+="\nRating: " + obj[index].rating
  animeTest+="\nScore: " + obj[index].score
  animeTest+="\nSynopsis: " + obj[index].synopsis
  animeTest+="\n##########################################"
  return animeTest

def searchAnime(url, obj):
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

class animecrawler(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.command()
  async def searchAnime(self, ctx):
    obj=[]
    print("what do u want to do?\n1)Top 10 Most Popular Anime\n2)Current Season Anime\n3)Search for a specific Anime")
    choice = int(input())
    if choice == 1:
      await ctx.send(searchTopAnime("https://myanimelist.net/topanime.php?type=bypopularity", obj))
      print("\n\nChoose one of the results above for more info.")
      choice=int(input())
      choice-=1
      getInfo(choice, obj)
      await ctx.send(printAnimeInfo(choice, obj))
    elif choice == 3:
      print("pls input the anime u r interested in:")
      temp=input()
      search="https://myanimelist.net/search/all?cat=all&q=" + temp.replace(" ", "%20", -1)
      await ctx.send(searchAnime(search, obj))
      print("\n\nChoose one of the results above.")
      choice=int(input())
      choice-=1
      getInfo(choice, obj)
      await ctx.send(printAnimeInfo(choice, obj))

    else:
      await ctx.send(searchSeasonAnime("https://myanimelist.net/anime/season", obj))
      print("\n\nChoose one of the results above for more info.")
      choice=int(input())
      choice-=1
      getInfo(choice, obj)
      await ctx.send(printAnimeInfo(choice, obj))
    


def setup(bot):
  bot.add_cog(animecrawler(bot))