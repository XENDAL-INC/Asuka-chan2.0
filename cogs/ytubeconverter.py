import discord
from discord.ext import commands
from pytube import YouTube
from pytube import Playlist
import shutil
import os

class ytubeconverter(commands.Cog):
  def _init_(self, bot):
    self.bot = bot



  @commands.command()
  async def ytconv(self, ctx):
    """ converts youtube vid to .mp3. """
    def convert(video, title, outPath):
      video=video.streams.filter(only_audio=True)
      try:
        video[4].download(filename=".mp3", filename_prefix=title, output_path=outPath)
      except:
        video[4].download(filename=".mp3", output_path=outPath, filename_prefix="output")
        title="output"
      return title

    if not ctx.message.content.replace("$ytconv", "", -1)=="":
      url=str(ctx.message.content.replace("$ytconv ", "", -1))

    outPath="db/vidConverter/" + str(ctx.author.id)

    if("playlist" in url):
      try:
        p=Playlist(url)
        for video in p.videos:
          await ctx.send("Conversion in progress, pls wait...")
          title=video.title
          title=convert(video, title, outPath)
          await ctx.send(file=discord.File(outPath + "//" + title + ".mp3"))
          await ctx.send('Finished Conversion of "' + title + '"')
      except:
          await ctx.send("An error has occured, make sure that the link is valid and try again")
    else:
      try:
        video=YouTube(url)
        title=video.title
        await ctx.send("Conversion in progress, pls wait...")
        title=convert(video, title, outPath)
        await ctx.send(file=discord.File(outPath + "//" + title + ".mp3"))
        await ctx.send('Finished Conversion of "' + title + '"')
      except:
        await ctx.send("An error has occured, make sure that the link is valid and try again")

    shutil.rmtree(outPath)

def setup(bot):
  bot.add_cog(ytubeconverter(bot))