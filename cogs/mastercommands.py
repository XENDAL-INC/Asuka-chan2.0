from discord import DMChannel
from discord.ext import commands
import time

class mastercommands(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.command(hidden=True)
  async def updatepfp(self, ctx):
    if ctx.author.name == "XENDAL_INC":
      pfp_path = "update/pfp.png"
      fp = open(pfp_path, 'rb')
      pfp = fp.read()
      await self.bot.user.edit(avatar=pfp)
      await ctx.channel.purge(limit=1)
      user = await self.bot.fetch_user(ctx.author.id)
      await DMChannel.send(
          user,
          "My pfp has been updated successfully thx MASTER!:heart:\nhttps://tenor.com/05fP.gif"
      )
  
  @commands.command(hidden=True)
  async def sendDM(self, ctx):
    if ctx.author.name == "XENDAL_INC":
      temp = ctx.author.id;
      user = await self.bot.fetch_user(ctx.author.id)
      if not ctx.message.mentions:
        await DMChannel.send(user, "pls mention someone MASTER!")
      else:
        await ctx.channel.purge(limit=1)
        msg=""
        dmfeedback = await DMChannel.send(user, "pls procede and type the message u want to send MASTER!")
        time.sleep(2)
        await dmfeedback.delete()
        def check(m):
          return m.author.name == "XENDAL_INC"
        response = await self.bot.wait_for('message', check=check)
        msg=response.content
        #response.channel.purge(limit=1)
        response.delete()
        
        for i in ctx.message.mentions:
          mentioned = await ctx.fetch_user(i.id)
          await DMChannel.send(mentioned, msg + temp)

  @commands.command(hidden=True)
  async def sendDMbyID(self, ctx):
    if ctx.author.name == "XENDAL_INC":
      #temp = ctx.author.id;
      user = self.bot.fetch_user(ctx.author.id)
      if not ctx.message.content.replace("$sendDMbyID", "",-1)=="" or ctx.message.content.replace("$sendDMbyID", "",-1)==" ":
        dmID = ctx.message.content.replace("$sendDMbyID", "",-1)
        dmID = dmID.replace(" ", "",-1)
        #await ctx.message.delete
        msg=""
        dmfeedback = await DMChannel.send(user, "pls procede and type the message u want to send MASTER!")
        time.sleep(2)
        await dmfeedback.delete()
        def check(m):
          return m.author.name == "XENDAL_INC"
        response = await self.bot.wait_for('message', check=check)
        msg=response.content
        #response.channel.purge(limit=1)
        target = await ctx.message.fetch_user(dmID)
        await DMChannel.send(target, msg)
      else:
        dmfeedback = await DMChannel.send(user, "pls mention someone MASTER!")
        time.sleep(2)
        await dmfeedback.delete()

def setup(bot):
  bot.add_cog(mastercommands(bot))