import asyncio
import discord
import functools
from discord.ext import commands

import youtube_dl

from utils import *


queue = Map()
server_queue = {}
voted_skip = []

class YoutubeDL(youtube_dl.YoutubeDL):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

    def validate_url_is_playlist(self, query):
        if '&' in query:
            _format = query[:query.find('&')]
            return _format
        return query

    def search_yt(self, query, author):
        query = self.validate_url_is_playlist(query)

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                song = {
                    'url': info['formats'][0]['url'],
                    'id': info['id'],
                    'title': info['title'],
                    'thumbnail': info['thumbnail'],
                    'duration': info['duration'],
                    'author': author.name
                }
            except Exception:
                return {'detail': 'There was an error finding video.'}
        return song


class Queue(YoutubeDL):
    """
    This class is created to mapping and handle of the songs.
    """

    def _server_queue(self, song, ctx):
        server_queue = self.get_server_queue(ctx.guild)
        song = self.search_yt(song, ctx.author).copy()
        if not server_queue:
            queue_object = {
                'voice_channel': self.voice_channel,
                'text_channel': self.text_channel,
                'connection': self.connection,
                'songs': []
            }
            queue.set(ctx.guild.id, queue_object)
            queue_object['songs'].append(song)
            return self.get_server_queue(ctx.guild), None
        else:
            server_queue['songs'].append(song)
            return server_queue, str

    def get_server_queue(self, guild=None):
        server_queue = queue.get(guild.id)
        return server_queue

    def get_next_song(self):
        return self.get_queue()['songs'][0]

    def song_player(self, ctx, query):
        server_queue, message = self._server_queue(query, ctx)
        return server_queue, message

    def add_embed_queue(self, song, ctx):
        embed = discord.Embed(title=song[-1]['title'], color=000, url='https://www.youtube.com/watch?v=%s' % song[-1]['id'])
        embed.set_author(name='Added to queue', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=song[-1]['thumbnail'])
        embed.add_field(name='Requested by:', value='`%s`' %  song[-1]['author'])
        embed.add_field(name='Song Duration', value='`%s`' % format_seconds(song[-1]['duration']))
        embed.add_field(name='Position in queue', value='`%s.`' % str(song.index(song[-1])))
        embed.set_footer(text='✅ | Use `?queue` to see the queue.')
        return embed


class music(Queue, commands.Cog):
    """
    This class contains all commands to play music into whichever server on Discord.
    """

    def __init__(self, client):
        self.client = client

        self.guild = None
        self.voice_channel = None
        self.text_channel = None
        self.connection = None

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __handle_bot_queue_status(coro):
        @functools.wraps(coro)
        async def decorator(self, ctx, *args, **kwargs):
            if ctx.author.voice is None:
                return await ctx.send('You are not in a voice channel!')
            elif (' '.join(args) != '' or not '') and ctx.author.voice is not None:
                if coro.__name__ not in ['play', 'join', 'leave'] and self.get_server_queue(ctx.guild) is None:
                    return await ctx.send('There are not songs in queue!')
                return await coro(self, ctx, *args, **kwargs)
        return decorator

    @commands.command()
    @__handle_bot_queue_status
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send(f'**Joined `{voice_channel.name}` and requested into <#{ctx.channel.id}>**')
        else:
            await ctx.voice_client.move_to(voice_channel)

    async def play_next(self, ctx):
        # When there are songs in queue it is need to repeat the process to play
        # the next song, so this function gotten next song and play it.
        songs = self.get_server_queue(ctx.guild)['songs']
        songs.pop(0) # delete the last song played.

        if len(songs) == 0:
            queue.delete(ctx.guild.id)
        if len(songs) > 0:
            source = await discord.FFmpegOpusAudio.from_probe(songs[0]['url'], **self.FFMPEG_OPTIONS)
            try:
                ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.client.loop))
            except:
                pass # ignored error: `discord.errors.ClientException: Already playing audio.`

    @commands.command(aliases=['p'])
    @__handle_bot_queue_status
    async def play(self, ctx, *args):
        query = " ".join(args)

        if query == "":
            await ctx.send('You need to send the second argument!')
        else:
            self.guild = ctx.guild
            self.text_channel = ctx.channel
            self.voice_channel = ctx.author.voice.channel

            server_queue, message = self.song_player(ctx, query)
            song = server_queue['songs'][0]

            try:
                if ctx.voice_client is None:
                    self.connection = await self.voice_channel.connect()
                    await ctx.guild.change_voice_state(channel=self.voice_channel, self_mute=False, self_deaf=True)
                    await ctx.send(f'**Joined `{self.voice_channel.name}` and requested into <#{self.text_channel.id}>**')

                if message is not None:
                    await ctx.send(embed=self.add_embed_queue(server_queue['songs'], ctx))
                else:
                    await ctx.send(':mag_right: Searching on **YouTube**')

                source = discord.FFmpegPCMAudio(song['url'], **self.FFMPEG_OPTIONS)
            except:
                await ctx.send('There was an error connecting')
            else:
                try:
                    ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.client.loop))
                except:
                    pass # ignored error: `discord.errors.ClientException: Already playing audio.`
                else:
                    await ctx.send(f':notes: Now playing ~ **%s**' % song['title'])

    @commands.command(aliases=['s'])
    @__handle_bot_queue_status
    async def skip(self, ctx, *args):
        global voted_skip

        channel = self.client.get_channel(self.voice_channel.id)

        # before counts members in voice channel, it is needs to check
        # if either of the all members is a bot or not.
        length_members = [member.id for member in channel.members if member.bot is not True]
        voted_skip.append(ctx.author.id) if ctx.author.id not in voted_skip else await ctx.send('You already voted!', delete_after=5)

        require = len(length_members) * 0.8

        if len(voted_skip) > round(require):
            voted_skip.clear()
            voted_skip.append(ctx.author.id)
            await ctx.send('Restarting vote, due to either of the members has left.', delete_after=5)
            await asyncio.sleep(5)

        if len(voted_skip) == round(require):
            ctx.voice_client.stop()
            await ctx.send('**Skkiped** :thumbsup:')
            song = self.get_server_queue(ctx.guild)
            if song is not None:
                await self.play_next(ctx)
            voted_skip.clear()
        else:
            await ctx.send('**Skipping?** (%s/%s peolple)' % (len(voted_skip), round(require)))

    @commands.command(aliases=['fs'])
    @commands.has_role('ADMIN')
    @__handle_bot_queue_status
    async def forceskip(self, ctx):
        ctx.voice_client.stop()
        voted_skip.clear()
        await self.play_next(ctx)
        await ctx.send('**Skkiped** :thumbsup:')

    @forceskip.error
    async def is_not_admin(self, ctx, error):
        await ctx.send('Missing permissions, sorry')

    @commands.command(aliases=['np'])
    @__handle_bot_queue_status
    async def nowplaying(self, ctx):
        now_playing = self.get_server_queue(ctx)['songs'][0]
        embed = discord.Embed(
            color=000,
            title='▶️ | Now playing',
            description='[**%s**](https://www.youtube.com/watch?v=%s) | Duration %s\n`Requested by: %s`\nㅤ' %
            (now_playing['title'], now_playing['id'], format_seconds(now_playing['duration']), now_playing['author']))
        embed.set_thumbnail(url=now_playing['thumbnail'])
        embed.add_field(name='Add Songs.', value='✅ | Use command `?play`.')
        await ctx.send(embed=embed)

    @commands.command(aliases=[])
    @__handle_bot_queue_status
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send('Stopped')

    @commands.command()
    @__handle_bot_queue_status
    async def leave(self, ctx):
        global server_queue

        _server_queue = server_queue.get(ctx.guild.id, None)
        if _server_queue is not None:
            server_queue.pop(ctx.guild.id)
            ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send('Leaving channel, see you :v:')

    @commands.command()
    @__handle_bot_queue_status
    async def queue(self, ctx):
        songs = self.get_server_queue(ctx.guild)['songs']
        now_playing = songs[0]
        embed_list_songs = discord.Embed(
            color=000,
            title='📄 | Queue List',
            description='__Now Playing__:\n[**%s**](https://www.youtube.com/watch?v=%s) | `%s Requested by: %s`\nㅤ' %
            (now_playing['title'], now_playing['id'], format_seconds(now_playing['duration']), now_playing['author']),)
        embed_list_songs.set_thumbnail(url=now_playing['thumbnail'])

        cont = 0
        if len(songs) > 0:
            for song in songs[1:]:
                cont += 1
                embed_list_songs.add_field(
                    name='%s' % song['title'],
                    value='`%s.` Duration %s | `Requested by: %s`' %
                    (cont, format_seconds(song['duration']), song['author']),
                    inline=False)
            embed_list_songs.set_footer(text='✅ | Use command `?play` to add songs.')
        else:
            embed_list_songs.add_field(
                name='There are no songs in queue.', value='✅ | No songs? use command `?play` to add songs')

        await ctx.send(embed=embed_list_songs)

def check_queue():
    status = False if queue == {} else True
    return status

def clear_server_queue(voice_client):
    queue.get(voice_client.guild.id)['songs'].clear()
    queue.delete(voice_client.guild.id)
    voted_skip.clear()

def setup(client):
    client.add_cog(music(client))
