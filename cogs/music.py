import asyncio
import discord
from discord.ext import commands

import youtube_dl


class Queue:
    """
    This class is created to mapping and a control of the song;
    """
    server_queue = {}

    def __init__(self):
        pass

    def _server_queue(self, song, songs=[]):
        queue = self.server_queue.get(self.guild_id)
        if not queue:
            songs.append(self.search_yt(song).copy())
            self.server_queue[self.guild_id] = {
                'voice_channel': self.voice_channel,
                'text_channel': self.text_channel,
                'connection': self.connection,
                'songs': songs
            }
            return self.server_queue, None
        else:
            song = self.search_yt(song).copy()
            queue['songs'].append(song)
            return self.server_queue, ':thumbsup: **%s** added to queue!' % song['title']

    def get_queue(self):
        queue = self.server_queue.get(self.guild_id)
        if queue is not None:
            return queue
        return None

    def get_next_song(self):
        _queue = self.get_queue()
        # del _queue['songs'][0]
        return _queue

    def song_player(self, ctx, query):
        server_queue, message = self._server_queue(query)
        song_queue = server_queue.get(ctx.guild.id)
        return song_queue, message

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

        self.guild_id = None

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
                self.guild_id = ctx.guild.id
                self.voice_channel = ctx.author.voice.channel
                self.text_channel = ctx.channel

                song, message = self.song_player(ctx, query)
                song_url = song['songs'][0]['url']
                song_title = song['songs'][0]['title']

                async def play_next(ctx):
                    # When there are songs in queue we need to repeat the process to play
                    # the next song, so this function gotten next song and play it.
                    songs = len(self.get_queue()['songs'])
                    if songs == 0:
                        self.server_queue.pop(ctx.guild.id)
                    if songs > 0:
                        song = self.get_next_song()['songs']
                        source = await discord.FFmpegOpusAudio.from_probe(song[0]['url'], **self.FFMPEG_OPTIONS)
                        ctx.voice_client.play(
                            source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), self.client.loop))
                        await ctx.send(':notes: Now playing ~ **%s**' % song[0]['title'])
                        song.pop(0) # delete the last song played.

                try:
                    if ctx.voice_client is None:
                        self.connection = await self.voice_channel.connect()
                        await ctx.send(f'**Joined `{self.voice_channel.name}` and requested into <#{self.text_channel.id}>**')

                    if message is not None:
                        await ctx.send(message, delete_after=5)
                    else:
                        await ctx.send(':mag_right: Searching on `YouTube`')

                    source = await discord.FFmpegOpusAudio.from_probe(song_url, **self.FFMPEG_OPTIONS)
                except:
                    await ctx.send('There was an error connecting')
                else:
                    try:
                        ctx.voice_client.play(
                            source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), self.client.loop))
                        song['songs'].pop(0) # delete the last song played.
                    except:
                        pass # ignored error: `discord.errors.ClientException: Already playing audio.`
                    else:
                        await ctx.send(f':notes: Now playing ~ **{song_title}**')

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
