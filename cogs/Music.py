import nextcord
from nextcord.ext import commands
import yt_dlp

import nextcord
from nextcord.ext import commands
import yt_dlp


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.playlist = []

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a song"""
        # Get the voice channel of the user who typed the command
        voice_channel = ctx.author.voice.channel
        # Connect to the voice channel if not already connected
        if self.vc is None:
            self.vc = await voice_channel.connect()
        elif self.vc.is_connected() and voice_channel.id != self.vc.channel.id:
            await self.vc.move_to(voice_channel)

        # Create a YTDL options object
        ytdl_format_options = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

        try:
            # Try to extract information about the video using the query as a search term
            info = ytdl.extract_info(f"ytsearch:{query}",
                                     download=False)['entries'][0]
        except yt_dlp.DownloadError:
            await ctx.send(
                "Failed to find any videos matching your search query.")
            return

        # Add the song to the playlist
        self.playlist.append(info)

        # Play the song if it's the first song in the playlist
        if len(self.playlist) == 1:
            await self.play_music()

    async def play_music(self):
        """Plays the next song in the playlist"""
        # If there are no songs in the playlist, return
        if not self.playlist:
            return

        # If the voice client is already playing audio, stop it
        if self.vc.is_playing():
            self.vc.stop()

        # Get the next song in the playlist
        song_info = self.playlist[0]
        self.playlist = self.playlist[1:]

        # Create a source from the song URL
        source = await nextcord.FFmpegOpusAudio.from_probe(song_info['url'])

        # Play the source
        self.vc.play(
            source,
            after=lambda _: self.bot.loop.create_task(self.play_music()))

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song"""
        if self.vc is not None and self.vc.is_playing():
            self.vc.stop()

    @commands.command()
    async def disconnect(self, ctx):
        """Disconnects the bot from the voice channel"""
        if self.vc is not None:
            await self.vc.disconnect()
            self.vc = None
            self.playlist = []

    @play.before_invoke
    async def ensure_voice(self, ctx):
        """Ensure the user is in a voice channel"""
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")


def setup(bot):
    bot.add_cog(Music(bot))
