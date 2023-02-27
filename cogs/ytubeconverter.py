import nextcord
from nextcord.ext import commands
from pytube import YouTube
from pytube import Playlist
from nextcord import FFmpegPCMAudio
import shutil

class ytubeconverter(commands.Cog):
  def _init_(self, bot):
    self.bot = bot


  @commands.command()
  async def ytconv(self, ctx, *, args):
    """ converts youtube vid to .mp3. """
    illegalChar=["#","%","&","{","}","<",">","*","/","?","\\"]
    def convert(video, title, outPath):
      for char in illegalChar:
        title=title.replace(char,"",-1)
      video=video.streams.filter(only_audio=True)
      try:
        video[int(len(video))-1].download(filename=".mp3", filename_prefix=title, output_path=outPath)
      except Exception as e:
        print(e)
        video[int(len(video))-1].download(filename=".mp3", output_path=outPath, filename_prefix="output")
        title="output"
      return title

    url=args

    outPath="db/vidConverter/" + str(ctx.author.id)

    if("playlist" in url):
      try:
        p=Playlist(url)
        for video in p.videos:
          await ctx.send("Conversion in progress, pls wait...")
          title=video.title
          title=convert(video, title, outPath)
          await ctx.send("lmao")
          await ctx.send(file=nextcord.File(outPath + "//" + title + ".mp3"))
          await ctx.send('Finished Conversion of "' + title + '"')
      except:
          await ctx.send("An error has occured, make sure that the link is valid and try again")
    else:
      try:
        video=YouTube(url)
        title=video.title
        await ctx.send("Conversion in progress, pls wait...")
        title=convert(video, title, outPath)
        
        await ctx.send(file=nextcord.File(outPath + "//" + title + ".mp3"))
        await ctx.send('Finished Conversion of "' + title + '"')
      except Exception as e:
        print(e)
        await ctx.send("An error has occured, make sure that the link is valid and try again")

    shutil.rmtree(outPath)

def setup(bot):
  bot.add_cog(ytubeconverter(bot))