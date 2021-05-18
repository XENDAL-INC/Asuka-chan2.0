from discord.ext import commands
import os

nQueue = "-1"

class queue_storage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def queue(self, ctx):
    isempty = 1
    queueName = ctx.message.content
    if not queueName == "$queue":
      queueName = queueName.replace("$queue ", "", -1)
      if (queueName == ""):
        await ctx.send(
            'Sorry ' + ctx.message.author.mention +
            ' Sempai, but you have not specified the queue you want to view. Pls write **$queue (name of the queue)**, in order for the command to work :pensive:'
        )

      else:
        if os.path.exists(queueName + '.txt'):
          f = open(queueName + '.txt', "r")
          for x in f:
            isempty = 0
            await ctx.send(x)
          f.close
          global nQueue
          nQueue = queueName
          if isempty == 1:
            await ctx.send(
                ctx.message.author.mention +
                ' Sempai, the queue you requested is currently empty, if u want to add items u should use the command **$add (name of item)** :grin:'
            )
        else:
          await ctx.send(
              'Sorry ' + ctx.message.author.mention +
              ' Sempai, but I cannot find the queue you requested in the storage, maybe you wrote the wrong name. Try Again :pensive: '
          )
    else:
      await ctx.send(
          'Sorry ' + ctx.message.author.mention +
          ' Sempai, but you have not specified the queue you want to view. Pls write **$queue (name of the queue)**, in order for the command to work :pensive:'
      )

  @commands.command()
  async def cqueue(self, ctx):
    queueName = ctx.message.content

    if (queueName == "$squeue"):
      await ctx.send('You have to give a name to the queue b-Baka!')
    elif (queueName == ""):
      await ctx.send('You have to give a name to the queue b-Baka!')
    else:
      queueName = queueName.replace("$squeue ", "", -1)
      f = open(queueName + '.txt' , "w")
      temp=""
      #queueList = player.queue
      queueList=[]
      count=0
      for x in queueList:
        if count!=0:
          temp +=("\n")
        temp += x
        count+=1
      f.write(temp)
      f.close
      
      await ctx.send('**NICEU ' + ctx.message.author.mention + 'SEMPAI!** You have created the a new queue called ' + queueName + ' :heart:')


  @commands.command()
  async def add(self, ctx):
    if nQueue == "-1":
      await ctx.send(
          'Sorry ' + ctx.message.author.mention +
          ' Sempai, but you have not opened any queue yet try the command **$queue (queue name)** first before trying this again :pensive:'
      )

    msg = ctx.message.content
    if not msg == "$add":
      msg = msg.replace("$add ", "", -1)
      if (msg == ""):
        await ctx.send(
            'Sorry ' + ctx.message.author.mention +
            ' Sempai, but you have not specified the new item u want to add to the queue. Pls write **$add (name of the item)**, in order for the command to work :pensive:'
        )

      else:
        isempty = 1
        f = open(nQueue + ".txt", "r")
        tlist = []
        for x in f:
          isempty = 0
          tlist.append(x)
        f.close

        if isempty == 0:
          tlist.append("\n" + msg)
        else:
          tlist.append(msg)

        f = open(nQueue + ".txt", "w")
        for element in tlist:
          f.write(element)
        f.close()
        await ctx.send(
            '**WOW' + ctx.message.author.mention +
            ' Sempai**, u have successfully added a new item to you queue :heart:'
        )


  @commands.command()
  async def clear(self, ctx):
    if nQueue == "-1":
      await ctx.send(
          'Sorry ' + ctx.message.author.mention +
          ' Sempai, but you have not opened any queue yet try the command **$queue (queue name)** first before trying this again :pensive:'
      )
    else:
      await ctx.message.add_reaction(":wastebasket:")
      f = open(nQueue + ".txt", "w")
      f.truncate(0)
      f.close

def setup(bot):
  bot.add_cog(queue_storage(bot))