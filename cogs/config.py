import discord
from discord.ext import commands

from media.gif import *


class config(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def embed(self, ctx, *key):
        query = ' '.join(key)

        @commands.Cog.listener()
        async def on_message(ctx):
            await ctx.message.delete()

        if query == '':
            await on_message(ctx)
            await ctx.send('you need to send a second argument!', delete_after=5)

        if query == 'minecraft':
            await on_message(ctx)
            embed = discord.Embed(
                title=minecraft['title'],
                description=minecraft['description'],
                color=minecraft['color']
            )
            embed.set_thumbnail(url=minecraft['thumbnail_url'])
            embed.add_field(name=minecraft['name'], value=minecraft['value'])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(config(client))
