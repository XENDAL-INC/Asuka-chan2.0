import discord
from discord.utils import get
from discord.ext import commands
from discord import Embed
import time
import random

class interactions(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.command(aliases=['purge'])
  async def clear(self, ctx, amount=6):
    """ clears a default number of 5 messages if not declared after command. """
    if not ctx.message.content.replace("$clear", "", -1)=="":
      amount=int(ctx.message.content.replace("$clear ", "", -1))
      amount+=1
    await ctx.channel.purge(limit=amount)
  
  @commands.command()
  async def usrinfo(self, ctx, *,  target : discord.Member=None):
    """ Display mentioned user's info. """
    if not ctx.message.mentions:
      target = ctx.author
    
    embed = discord.Embed()
    embed.title = "User Info"
    embed.set_thumbnail(url=target.avatar_url)
    fields=[("ID", target.id, False),
            ("Name", str(target), True),
            ("Bot?", target.bot, True),
            ("Top Role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            #("Activity", f"{target.activity.name} {str(getattr(target.activity, 'type')).title()}", True),
            ("Created At", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Joined At", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)

  @commands.command()
  async def avatar(self, ctx, *,  target : discord.Member=None):
    """ Display mentioned user's avatar. """
    if not ctx.message.mentions:
      target = ctx.author
      
    await ctx.send(target.avatar_url)
  
  @commands.command(aliases=['hi'])
  async def hello(self, ctx):
    author=ctx.message.author.name
    if(author=='XENDAL_INC'):
      honorifics='-Sama'
    else:
      honorifics=' Sempai'
    if(author=='Waleed-Kun'):
      await ctx.send('**HENTAI! LOLICON!**')
    elif(author=="Gentleman N'WAH"):
      await ctx.send('**SHUT THE FUCK UP MONKEY**')
    else:
      await ctx.send('Ohayo ' + ctx.message.author.mention +honorifics+' :heart:')
  
  @commands.command()
  async def daisuki(self, ctx):
    """ Return affection to my owner only. """
    master="<@380016239310929931>"
    if ctx.message.author.name == "XENDAL_INC":
      await ctx.send("Watashi mo! "+ctx.message.author.mention+"-Sama!:heart:\nhttps://tenor.com/ZOap.gif")
    else:
      await ctx.send("hehe, do u really think I could accept those mere feelings when I have "+master+"-Sama???\nhttps://tenor.com/buIuA.gif")
  
  @commands.command()
  async def name(self, ctx):
    #await ctx.message.add_reaction("❤️")
    await ctx.send("Yo! My name is Asuka-chan")

  
  #helps if u want to delete a message
  """@commands.command()
  async def delete(self, ctx):
    await ctx.message.delete()
    msg = await ctx.send("Deleted. and going to delete this in 2 sec")
    time.sleep(2)
    await msg.delete()"""

  #helps if u want to call events or message manipulation
  """@commands.Cog.listener()
  async def on_message(self, message):
    if message.content.startswith('slap'):
        if message.mentions:
          mention = '<@'
          mention += str(message.mentions[0].id) + '>'
          await message.channel.send(message.author.mention + ' starts slapping ' + mention)
        else:
          await message.channel.send(message.author.mention + ' starts slapping himself')"""

  @commands.command(aliases=['slaps','bitchslap','bitchslaps'])
  async def slap(self, ctx):
    author=ctx.message.author.name
    if(author=='XENDAL_INC'):
      honorifics='-Sama'
    else:
      honorifics=' Sempai'
    if ctx.message.mentions and ctx.message.author.id!=ctx.message.mentions[0].id:
      if ctx.message.author.name=="XENDAL_INC" and str(ctx.message.mentions[0].id) == '842228270400536586':
        await ctx.send('HIDOI ' + ctx.author.mention + honorifics + ' :broken_heart:\nhttps://tenor.com/xNYJ.gif')
      
      else:
        f = open("gifs/slap.txt", "r")
        gif=[]
        for x in f:
          gif.append(x.replace("\n", "", -1))
        if not str(ctx.message.mentions[0].id) == '842228270400536586':
          mention = '<@'
          mention += str(ctx.message.mentions[0].id) + '>'
          await ctx.send('YOOO, ' + ctx.message.author.mention + honorifics + ' started slapping the shit out of ' + mention + '\n' + random.choice(gif))
        else:
          await ctx.send('Heh, nice try' + ctx.message.author.mention + honorifics + '~\nhttps://tenor.com/bBKj0.gif')
        
    else:
      await ctx.send(ctx.message.author.mention + honorifics + ' started slapping themselves\nhttps://tenor.com/biv57.gif')
  
  @commands.command(aliases=['hit', 'hits', 'jab', 'jabs', 'fight', 'fights', 'punches'])
  async def punch(self, ctx):
    author=ctx.message.author.name
    if(author=='XENDAL_INC'):
      honorifics='-Sama'
    else:
      honorifics=' Sempai'
    if ctx.message.mentions and ctx.message.author.id!=ctx.message.mentions[0].id:
      if ctx.message.author.name=="XENDAL_INC" and str(ctx.message.mentions[0].id) == '842228270400536586':
        await ctx.send('HIDOI ' + ctx.author.mention + honorifics + ' :broken_heart:\nhttps://tenor.com/xNYJ.gif')
      
      else:
        f = open("gifs/punch.txt", "r")
        gif=[]
        for x in f:
          gif.append(x.replace("\n", "", -1))
        if not str(ctx.message.mentions[0].id) == '842228270400536586':
          mention = '<@'
          mention += str(ctx.message.mentions[0].id) + '>'
          await ctx.send('SUGOI!!!, ' + ctx.message.author.mention + honorifics + ' started punching ' + mention + '\n' + random.choice(gif))
        else:
          await ctx.send('Heh, nice try' + ctx.message.author.mention + honorifics + '~\nhttps://tenor.com/bBKj0.gif')
        
    else:
      await ctx.send(ctx.message.author.mention + honorifics + ' started punching themselves\nhttps://tenor.com/bnBiy.gif')
  
  @commands.command(aliases=['hugs','cuddle','cuddling'])
  async def hug(self, ctx):
    author=ctx.message.author.name
    if(author=='XENDAL_INC'):
      honorifics='-Sama'
    else:
      honorifics=' Sempai'
    if ctx.message.mentions and ctx.message.author.id!=ctx.message.mentions[0].id:
      if ctx.message.author.name=="XENDAL_INC" and str(ctx.message.mentions[0].id) == '842228270400536586':
        await ctx.send(ctx.author.mention + honorifics + ' b-Baka! s-stop... pls :heart:\nhttps://tenor.com/blkN3.gif')
      
      else:
        f = open("gifs/hug.txt", "r")
        gif=[]
        for x in f:
          gif.append(x.replace("\n", "", -1))
        if not str(ctx.message.mentions[0].id) == '842228270400536586':
          mention = '<@'
          mention += str(ctx.message.mentions[0].id) + '>'
          await ctx.send(ctx.message.author.mention + honorifics + ' started hugging ' + mention + '\n' + random.choice(gif))
        else:
          await ctx.send('Heh, that is so creepy that u are ridiculing yourself' + ctx.message.author.mention + honorifics + '~\nhttps://tenor.com/blITm.gif')
        
    else:
      await ctx.send(ctx.message.author.mention + honorifics + ' started hugging themselves :smirk:\nhttps://tenor.com/bCzqL.gif')
  
  @commands.command()
  async def tadaima(self, ctx):
    author=ctx.message.author.name
    if(author=='XENDAL_INC'):
      honorifics='-Sama!'
    else:
      honorifics=' Sempai!'
    await ctx.send('Welcome back '+ctx.message.author.mention+honorifics+' :heart:')
    time.sleep(2)
    await ctx.send('Would u like your dinner?')
    time.sleep(2)
    await ctx.send('Or bath?')
    time.sleep(2)
    await ctx.send('Or...')
    time.sleep(3)
    await ctx.send('Asuka-chan?')
    
  @commands.command()
  async def explosion(self,ctx):
    await ctx.send('Darkness blacker than black \nand darker than dark,')
    time.sleep(3)
    await ctx.send('I beseech thee, combine with my deep crimson.')
    time.sleep(3)
    await ctx.send('The time of awakening cometh.')
    time.sleep(3)
    await ctx.send('Justice, fallen upon the infallible boundary,')
    time.sleep(3)
    await ctx.send('appear now as an intangible distortion!')
    time.sleep(3)
    await ctx.send('This is the mightiest means of attack known to man,')
    time.sleep(3)
    await ctx.send('the ultimate attack magic!')
    time.sleep(3)
    await ctx.send('**EXPLOSION!!**')
    time.sleep(3)
    await ctx.send('https://media1.tenor.com/images/a5200ff8939402e4e2bbda3a8107d2b1/tenor.gif?itemid=7559840')


def setup(bot):
  bot.add_cog(interactions(bot))