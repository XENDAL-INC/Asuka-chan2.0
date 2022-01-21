import discord
from discord.ext import commands
from pytube import YouTube
from pytube import Playlist
from discord import FFmpegPCMAudio
from discord import Embed
import urllib.request
import re
import shutil



queues={}

def convert(video, title, outPath):
  illegalChar=["#","%","&","{","}","<",">","*","/","?","\\"]
  for char in illegalChar:
    title=title.replace(char,"",-2)
  video=video.streams.filter(only_audio=True)
  try:
    video[int(len(video)-2)].download(filename=".mp3", filename_prefix=title, output_path=outPath)
  except Exception as e:
    print(e)
  return title

def check_queue(ctx, id, voice):
  try:
    if queues[id] != []:
      queues[id].pop(0)
      if queues[id] != []:
        source=queues[id][0]
        
        print("Next Song: " + str(source))
        try:
          player = voice.play(source, after=lambda x=None: check_queue(ctx, id, voice))
        except Exception as e:
          print(e)
      else:
        voice.stop()
        queues.pop(int(id))
        outPath="db/music/" + str(id)
        shutil.rmtree(outPath)
        return
    else:
      voice.stop()
      queues.pop(int(id))
      outPath="db/music/" + str(id)
      shutil.rmtree(outPath)
  except:
    return


class music(commands.Cog):
  def __init__(self, bot):
        self.bot = bot
 

  @commands.command(aliases=['p'])
  async def play(self, ctx, *, args):
    """" Searches and plays a song or playlist from YouTube. """
    if ctx.author.voice:
      guild_id=ctx.message.guild.id

      try:
        channel = ctx.message.author.voice.channel
        voice=ctx.guild.voice_client
        try:
          voice = await channel.connect()
        except:
          print("")
        
        ###############################################
        #strip command from message content#
        try:
          url=args
        except:
          await ctx.send("pls don't waste my time, next time remember to write the vide you want to play b-baka!")
          return
        outPath="db/music/" + str(ctx.guild.id)
        
        ################################################
        #return results from youtube if not url
        if not "https://" in url:
          search="https://www.youtube.com/results?search_query=" + str(url.replace(" ", "+", -1))
          html = urllib.request.urlopen(search)
          video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
          url="https://www.youtube.com/watch?v=" + video_ids[0]

        #################################################
        #download video and setup embed
        try:
          video=YouTube(url)
          title=video.title
          embed=Embed()
          embed.color=0x8218ce
          embed.title="Track Enqueued"
          trackMin=str(int(video.length/60))
          trackSec=str(int(video.length%60))
          if int(trackSec) < 10:
            trackSec="0"+trackSec
          embed.set_thumbnail(url=video.thumbnail_url)
          description="["+title+"]("+video.embed_url+")\n\nLength: "+trackMin+":"+trackSec+"\n\nRequested by: ["+ctx.author.mention+"]"
          embed.description=description
          title=convert(video, title, outPath)
          
        except Exception as e:
          print(e)
          await ctx.send("An error has occured, make sure that the link is valid and try again")

        ###############################################
        
        source=FFmpegPCMAudio(outPath + "//" + title + ".mp3")
        
        
        if guild_id in queues:
          queues[guild_id].append(source)
        else:
          queues[guild_id] = [source]
          try:
            player=voice.play(source, after=lambda x=None: check_queue(ctx, guild_id, voice))
          except Exception as e:
            print(e)
            return
          
        
        await ctx.send(embed=embed)
        
      except Exception as e:
        print(e)
        return
    else:
      await ctx.send("pls enter a vc first b-baka!")
  
  @commands.command()
  async def pause(self, ctx):
    """ Pauses Player. """
    try:
      global msg
      msg=ctx.message
      #await msg.add_reaction("⏸️")
      player=discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
      
      if player.is_playing():
        await msg.add_reaction("⏸️")
        await player.pause()
      else:
        await ctx.send('The player is already paused b-Baka!')
    except Exception as e:
      print(e)
      return

  @commands.command()
  async def resume(self, ctx):
    """ Resumes Player. """
    try:
      global msg
      msg=ctx.message
      player=discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
      
      if player.is_paused():
        await msg.add_reaction("▶️")
        await player.resume()
      else:
        await ctx.send('The player is already playing b-Baka!')
    except Exception as e:
      print(e)
      return
  
  @commands.command(aliases=['die'])
  async def leave(self, ctx):
    """ Disconnects the player from the voice channel. """
    try:
      msg=ctx.message
      if ctx.voice_client:
        
        try:
          queues.pop(int(ctx.guild.id))
          outPath="db/music/" + str(ctx.guild.id)
          shutil.rmtree(outPath)
        except:
          print("")
        await msg.add_reaction("👋")
        await ctx.send('Sorry ' + msg.author.mention + ' Sempai, I hope i was being usefull :cry:')
        await ctx.guild.voice_client.disconnect()
      else:
        await ctx.send('Im not in a voice channel...')
    except Exception as e:
      print(e)
      return
  
  @commands.command()
  async def isplaying(self, ctx, *, args):
    """ Pauses Player. """
    try:
      await ctx.send(args)
    except:
      await ctx.send("there was no text after command")
    #query = args.strip('<>')
    #await ctx.send(str(query))
    return
    try:
      global msg
      msg=ctx.message
      #await msg.add_reaction("⏸️")
      player=discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
      
      if not player.is_playing():
        await ctx.send("The player stopped playing!")
      else:
        await ctx.send('The player is still playing a song')
    except Exception as e:
      print(e)
      return

  @commands.command()
  async def queue(self, ctx):
    """ Print Queue """
    guild_id=ctx.message.guild.id
    await ctx.send(str(queues))

  @commands.command()
  async def skip(self, ctx):
    """ skip """
    guild_id=ctx.message.guild.id
    if guild_id in queues:
      try:
        if queues[guild_id]!=[]:
          voice=ctx.guild.voice_client
          try:
            source=queues[guild_id][1]
          except:
            voice.stop()
            queues.pop(int(guild_id))
            outPath="db/music/" + str(guild_id)
            shutil.rmtree(outPath)

          voice.stop()
          player=voice.play(source, after=lambda x=None: check_queue(ctx, guild_id, voice))
        else:
          queues.pop(int(guild_id))
          voice.stop()
      except Exception as e:
        print(e)
        return



def setup(bot):
  bot.add_cog(music(bot))