import discord
from discord.ext import commands

import youtube_dl


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

    @commands.Cog.listener()
    async def on_ready(self):
        print("I'm ready")

    @commands.command()
    async def join(self, message):
        if message.author.voice is None:
            await message.send("You're not in a voice channnel")
        voice_channel = message.author.voice.channel
        if message.voice_client is None:
            await voice_channel.connect()
        else:
            await message.voice.client.move_to(voice_channel)

    def search_yt(self, query):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            except Exception:
                return False
        return {'url': info['formats'][0]['url'], 'title': info['title']}

    @commands.command(aliases=['p'])
    async def play(self, message, *args):
        query = " ".join(args)

        vc = message.voice_client
        video = self.search_yt(query)['url']
        source = await discord.FFmpegOpusAudio.from_probe(video, **self.FFMPEG_OPTIONS)
        vc.play(source)

    @commands.command(aliases=[])
    async def stop(self, message):
        await message.voice_client.stop()

    @commands.command()
    async def leave(self, message):
        await message.voice_client.disconnect()

    @commands.command()
    async def pause(self, message):
        await message.voice_client.pause()
        await message.send("Paused")

    @commands.command()
    async def resume(self, message):
        await message.voice_client.resume()
        await message.send("resume")


def setup(client):
    client.add_cog(music(client))
