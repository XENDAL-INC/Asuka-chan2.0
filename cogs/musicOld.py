import re
import discord
import lavalink
import os
from discord.ext import commands
from discord import Embed

url_rx = re.compile(r'https?://(?:www\.)?.+')


class music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
      bot.lavalink = lavalink.Client(bot.user.id)
      bot.lavalink.add_node('0.0.0.0', 6969, 'yourpass', 'eu', 'default-node')  # Host, Port, Password, Region, Name
      bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

    lavalink.add_event_hook(self.track_hook)

  def cog_unload(self):
    """ Cog unload handler. This removes any event hooks that were registered. """
    self.bot.lavalink._event_hooks.clear()

  async def cog_before_invoke(self, ctx):
    """ Command before-invoke handler. """
    guild_check = ctx.guild is not None
    #  This is essentially the same as `@commands.guild_only()`
    #  except it saves us repeating ourselves (and also a few lines).

    if guild_check:
        await self.ensure_voice(ctx)
        #  Ensure that the bot and command author share a mutual voicechannel.

    return guild_check

  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(error.original)
        # The above handles errors thrown in this cog and shows them to the user.
        # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
        # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
        # if you want to do things differently.

  async def ensure_voice(self, ctx):
    """ This check ensures that the bot and command author are in the same voicechannel. """
    player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
    # Create returns a player if one exists, otherwise creates.
    # This line is important because it ensures that a player always exists for a guild.

    # Most people might consider this a waste of resources for guilds that aren't playing, but this is
    # the easiest and simplest way of ensuring players are created.

    # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
    # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
    should_connect = ctx.command.name in ('play',)

    if not ctx.author.voice or not ctx.author.voice.channel:
        # Our cog_command_error handler catches this and sends it to the voicechannel.
        # Exceptions allow us to "short-circuit" command invocation via checks so the
        # execution state of the command goes no further.
        raise commands.CommandInvokeError('Join a voicechannel first.')

    if not player.is_connected:
        if not should_connect:
            raise commands.CommandInvokeError('Not connected.')

        permissions = ctx.author.voice.channel.permissions_for(ctx.me)

        if not permissions.connect or not permissions.speak:  # Check user limit too?
            raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

        player.store('channel', ctx.channel.id)
        await ctx.guild.change_voice_state(channel=ctx.author.voice.channel)
    else:
        if int(player.channel_id) != ctx.author.voice.channel.id:
            raise commands.CommandInvokeError('You need to be in my voicechannel.')

  async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
        # When this track_hook receives a "QueueEndEvent" from lavalink.py
        # it indicates that there are no tracks left in the player's queue.
        # To save on resources, we can tell the bot to disconnect from the voicechannel.
        #guild_id = int(event.player.guild_id)
        #guild = self.bot.get_guild(guild_id)
        #await guild.change_voice_state(channel=None)
        print('end of tracks')

  @commands.command(aliases=['p'])
  async def play(self, ctx, *, query: str):
      """ Searches and plays a song from a given query. """
      # Get the player for this guild from cache.
      player = self.bot.lavalink.player_manager.get(ctx.guild.id)
      # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
      query = query.strip('<>')

      # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
      # SoundCloud searching is possible by prefixing "scsearch:" instead.
      if not url_rx.match(query):
          query = f'ytsearch:{query}'

      # Get the results for the query from Lavalink.
      results = await player.node.get_tracks(query)

      # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
      # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
      if not results or not results['tracks']:
          return await ctx.send('Nothing found!')

      embed = discord.Embed(color=discord.Color.blurple())

      # Valid loadTypes are:
      #   TRACK_LOADED    - single video/direct URL)
      #   PLAYLIST_LOADED - direct URL to playlist)
      #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
      #   NO_MATCHES      - query yielded no results
      #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
      if results['loadType'] == 'PLAYLIST_LOADED':
          tracks = results['tracks']

          for track in tracks:
              # Add all of the tracks from the playlist to the queue.
              player.add(requester=ctx.author.id, track=track)

          embed.title = 'Playlist Enqueued!'
          embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
      else:
          track = results['tracks'][0]

          trackSeconds = (track["info"]["length"]) / 1000
          trackMinutes = int((trackSeconds) /60)
          trackSeconds = int(trackSeconds - (trackMinutes*60))
          embed = Embed()
          embed.color = 10181046
          embed.title = 'Track Enqueued'
          embed.description = '['+track["info"]["title"]+']('+track["info"]["uri"]+')\n\nLength: '+str(trackMinutes) + ':' + str(trackSeconds) + '\n\nRequested by: [' + ctx.message.author.mention + ']'

          # You can attach additional information to audiotracks through kwargs, however this involves
          # constructing the AudioTrack class yourself.
          track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
          player.add(requester=ctx.author.id, track=track)

      await ctx.send(embed=embed)

      # We don't want to call .play() if the player is playing as that will effectively skip
      # the current track.
      if not player.is_playing:
          await player.play()


  @commands.command()
  async def queue(self,ctx):
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)
    currentTrack = str(player.current['title'])
    queueList = player.queue
    count=2
    queuestr = "```css\n" + str(count-1) + ") " + currentTrack
    for element in queueList: 
        queuestr += '\n' + str(count) + ') '
        queuestr += str(element['title'])
        count += 1

    queuestr += "\n\nThis is the end of the queue!\n```"
    await ctx.send(queuestr)

  @commands.command()
  async def shuffle(self,ctx):
    """ Shuffles Queue. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)
    if not player.shuffle:
      player.shuffle = True
      await ctx.message.add_reaction("🔀")
    else:
      player.shuffle = False
      

  @commands.command()
  async def loop(self,ctx):
    """ Loops Queue. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)
    if not player.repeat:
      player.repeat = True
      await ctx.message.add_reaction("🔁")
    else:
      player.repeat = False
  
  @commands.command()
  async def skip(self, ctx):
    """ Skip to next track if exists. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
        return await ctx.send('Not connected.')

    if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        return await ctx.send('You\'re not in my voicechannel!')

    await player.skip()
    await ctx.message.add_reaction("⏭️")

  @commands.command()
  async def pause(self, ctx):
    """ Pauses Player. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
        return await ctx.send('Not connected.')

    if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        return await ctx.send('You\'re not in my voicechannel!')

    if not player.paused:
      await player.set_pause(pause = True)
      await ctx.message.add_reaction("⏸️")
    else:
      await ctx.send('The player is already paused b-Baka!')
  
  @commands.command()
  async def resume(self, ctx):
    """ Resumes Player. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
        return await ctx.send('Not connected.')

    if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        return await ctx.send('You\'re not in my voicechannel!')

    if player.paused:
      await player.set_pause(pause = False)
      await ctx.message.add_reaction("▶️")
    else:
      await ctx.send('The player is already playing b-Baka!')
  
  @commands.command()
  async def stop(self,ctx):
    """ Clears the current queue and stop the player. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
        return await ctx.send('Not connected.')

    if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        return await ctx.send('You\'re not in my voicechannel!')

    player.queue.clear()
    await player.stop()
    await ctx.message.add_reaction("⛔")
  
  @commands.command(aliases=['die'])
  async def leave(self, ctx):
    """ Disconnects the player from the voice channel and clears its queue. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
        # We can't disconnect, if we're not connected.
        return await ctx.send('Not connected.')

    if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
        # may not disconnect the bot.
        return await ctx.send('You\'re not in my voicechannel!')

    # Clear the queue to ensure old tracks don't start playing
    # when someone else queues something.
    player.queue.clear()
    # Stop the current track so Lavalink consumes less resources.
    await player.stop()
    # Disconnect from the voice channel.
    await ctx.guild.change_voice_state(channel=None)
    await ctx.message.add_reaction("👋")
    await ctx.send('Sorry ' + ctx.message.author.mention + ' Sempai, I hope i was being usefull :cry:')

  @commands.command()
  async def remove(self, ctx):
    """ Removes track from queue at position given after command. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
      return await ctx.send('Not connected.')
    else:
      if player.queue:
        queueLength = len(player.queue)
        index = int(ctx.message.content.replace("$remove ","",-1))
        index-=2

        if (queueLength-1)>=index:
          await ctx.send("```\nThe Track: " + str(player.queue[index]['title']) + " has been removed\n```")
          player.queue.pop(index)
        else:
          await ctx.send("Invalid Track Number or There is only 1 song in queue")
      else:
        await ctx.send("There is no queue currently playing")

  
  @commands.command()
  async def squeue(self, ctx):
    """ Saves the current playing queue. """
    player = self.bot.lavalink.player_manager.get(ctx.guild.id)

    if not player.is_connected:
        return await ctx.send('Not connected.')
    
    else:
      author=ctx.message.author.name
      if(author=='XENDAL_INC'):
        honorifics='-Sama!'
      else:
        honorifics=' Sempai!'
      
      queueName = ctx.message.content
      currentTrack = str(player.current['title'])

      if (queueName == "$squeue"):
        await ctx.send('You have to give a name to the queue b-Baka!')
      elif (queueName == ""):
        await ctx.send('You have to give a name to the queue b-Baka!')
      else:
        queueName = queueName.replace("$squeue ", "", -1)
        f = open(queueName + '.txt' , "w")
        temp=currentTrack
        queueList = player.queue
        for x in queueList:
          temp += "\n" + str(x['title'])
        f.write(temp)
        f.close
        
        await ctx.send('**NICEU ' + ctx.message.author.mention + honorifics + ',** You have created a new queue called ' + queueName + ' :heart:')

  @commands.command()
  async def lqueue(self, ctx):
      """ Loads a queue already saved. """
      queueName = ctx.message.content

      if (queueName == "$lqueue" or queueName == ""):
        await ctx.send('You have to give the name of the queue u want to load b-Baka!')
      else:
        queueName = queueName.replace("$lqueue ", "", -1)
        if os.path.exists(queueName + '.txt'):
          f = open(queueName + '.txt' , "r")
          player = self.bot.lavalink.player_manager.get(ctx.guild.id)
          embed = Embed()
          embed.color = 10181046
          embed.title = 'Track Enqueued'
          
          counter=0
            
          for x in f:
            query = x.replace("\n", "", -1)
            query = f'ytsearch:{query}'
            results = await player.node.get_tracks(query)
            track = results['tracks'][0]
            trackSeconds = (track["info"]["length"]) / 1000
            trackMinutes = int((trackSeconds) /60)
            trackSeconds = int(trackSeconds - (trackMinutes*60))
            embed.description = '['+track["info"]["title"]+']('+track["info"]["uri"]+')\n\nLength: '+str(trackMinutes) + ':' + str(trackSeconds) + '\n\nRequested by: [' + ctx.message.author.mention + ']'

            track = lavalink.models.AudioTrack(track, ctx.author.id,recommended=True)
            player.add(requester=ctx.author.id, track=track)
            await ctx.send(embed=embed)
            if counter==0:
              counter+=1
              if not player.is_playing:
                await player.play()
          

def setup(bot):
    bot.add_cog(music(bot))