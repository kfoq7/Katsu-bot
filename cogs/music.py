import discord
from discord.ext import commands

import youtube_dl


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    def search_yt(self, query):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            except Exception:
                return False
        return {'url': info['formats'][0]['url'], 'title': info['title']}

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        query = " ".join(args)
        if query == "": await ctx.send('You need to send the second argument')
        if ctx.author.voice is None: await ctx.send("You're not in a voice channel")

        voice_channel = ctx.author.voice.channel

        if query != '':
            if ctx.voice_client is None:
                await voice_channel.connect()
            vc = ctx.voice_client
            video = self.search_yt(query)['url']
            source = await discord.FFmpegOpusAudio.from_probe(video, **self.FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command(aliases=[])
    async def stop(self, ctx):
        await ctx.voice_client.stop()
        await ctx.send("Stopped")

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("resume")


def setup(client):
    client.add_cog(music(client))
