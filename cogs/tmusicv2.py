"""from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed

class MusicCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.music = lavalink.Client(self.bot.user.id)
    self.bot.music.add_node('0.0.0.0', 6969, 'yourpass', 'na', 'music-node')
    self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
    self.bot.music.add_event_hook(self.track_hook)

  @commands.command()
  async def join(self, ctx):
    vc = ctx.author.voice.channel
    player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
    player.store('channel', ctx.channel.id)
    await self.connect_to(ctx.guild.id, str(vc.id))

  @commands.command()
  async def search(self, ctx, *, query):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    query = f'ytsearch:{query}'
    results = await player.node.get_tracks(query)
    tracks = results['tracks'][0:10]
    track = tracks[0]
    trackSeconds = (track["info"]["length"]) / 1000
    trackMinutes = int((trackSeconds) /60)
    trackSeconds = int(trackSeconds - (trackMinutes*60))
    embed = Embed()
    embed.title = 'Results'
    embed.description = '['+track["info"]["title"]+']('+track["info"]["uri"]+')\n\nLength: '+str(trackMinutes) + ':' + str(trackSeconds) + '\n\nRequested by: [' + ctx.message.author.mention + ']'
    await ctx.send(embed=embed)


  @commands.command()
  async def pause(self,ctx,player):
    print("pause")
  
  @commands.command(aliases=["p"])
  async def play(self, ctx, *, query):
    try:
      vc = ctx.author.voice.channel
      player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
      player.store('channel', ctx.channel.id)
      await self.connect_to(ctx.guild.id, str(vc.id))
      if player.is_playing:
        ctx.send("There is already a song playing b-Baka!")
      query = f'ytsearch:{query}'
      results = await player.node.get_tracks(query)
      tracks = results['tracks'][0:10]
      track = tracks[0]

      player.add(requester=ctx.author.id, track=track)
      if not player.is_playing:
        trackSeconds = (track["info"]["length"]) / 1000
        trackMinutes = int((trackSeconds) /60)
        trackSeconds = int(trackSeconds - (trackMinutes*60))
        embed = Embed()
        embed.title = 'Now Playing'
        embed.description = '['+track["info"]["title"]+']('+track["info"]["uri"]+')\n\nLength: '+str(trackMinutes) + ':' + str(trackSeconds) + '\n\nRequested by: [' + ctx.message.author.mention + ']'
        await ctx.send(embed=embed)
        
        await player.play()

    except Exception as error:
      print(error)
  
  
  
  @commands.command()
  async def resume(self,ctx):
    print("resume")

  @commands.command(pass_context = True)
  async def leave(self,ctx):
    self.
    for x in self.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()

    return await ctx.send("I am not connected to any voice channel on this server!")
  
  @commands.command()
  async def die(self,ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)

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
  
  async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await self.connect_to(guild_id, None)
      
  async def connect_to(self, guild_id: int, channel_id: str):
    ws = self.bot._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)


def setup(bot):
  bot.add_cog(MusicCog(bot))"""