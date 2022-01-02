import discord
from discord.ext import commands

import youtube_dl


class Queue:
    """
    This class is created to mapping and a control of the song;
    """

    def __init__(self):
        pass

    def server_queue(self, song, songs=[]):
        songs.append(self.search_yt(song).copy())
        queue_constructor = {
            'voice_channel': self.voice_channel,
            'text_channel': self.text_channel,
            'connection': self.connection,
            'songs': songs
        }
        return queue_constructor

    def get_queue(self):
        queue = self.server_queue()

        if queue is None:
            msg = 'There are no songs in queue'
            return msg
        return queue

    def song_player(self, query):
        song_queue = self.server_queue(query)
        return song_queue, True

    def search_yt(self, query):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                song = {'url': info['formats'][0]['url'], 'title': info['title']}
            except Exception:
                return {'detail': 'There was an error finding video.'}
        return song


class music(Queue, commands.Cog):
    """
    This class contains all commands to play music into whichever server on Discord.
    """

    def __init__(self, client):
        self.client = client
        self.voice_channel = None
        self.text_channel = None
        self.connection = None

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channnel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        query = " ".join(args)

        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        else:
            if query == "":
                await ctx.send('You need to send the second argument!')
            else:
                self.voice_channel = ctx.author.voice.channel
                self.text_channel = ctx.channel

                try:
                    if ctx.voice_client is None:
                        self.connection = await self.voice_channel.connect()
                    song, found = self.song_player(query)
                    if found:
                        song_title = song['songs'][0]['title']
                        song_url = song['songs'][0]['url']
                        await ctx.send(':mag_right: Searching on `YouTube`')
                        source = await discord.FFmpegOpusAudio.from_probe(
                            song_url, **self.FFMPEG_OPTIONS)
                        ctx.voice_client.play(source)
                        await ctx.send(f':notes: Now playing **{song_title}**')
                except:
                    await ctx.send('There was a error connecting')

    @commands.command(aliases=[])
    async def stop(self, ctx):
        await ctx.voice_client.stop()
        await ctx.send('Stopped')

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send('Paused')

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send('resume')


def setup(client):
    client.add_cog(music(client))