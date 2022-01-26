import asyncio
import discord
from discord.ext import commands

from media.gif import *
from utils import *


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role('ADMIN')
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
            embed.add_field(name=minecraft['force']['name'], value=minecraft['force']['value'], inline=False)
            embed.add_field(name=minecraft['resource_pack']['name'], value=minecraft['resource_pack']['value'])
            await ctx.send(embed=embed)

    @commands.command()
    async def clean(self, ctx, amount=None, user=None, message=[]):

        async def on_delete_message():
            await asyncio.sleep(3)
            await ctx.message.delete()

        if amount is None:
            await ctx.send('please entre the amount of message that you want to clear!', delete_after=7)
            await on_delete_message()
            return

        if is_number(amount) is not True:
            await ctx.send('please entre a real number!', delete_after=7)
            return await on_delete_message()

        if int(amount) > 100:
            await ctx.send('please entre a real number!', delete_after=7)
            return await ctx.message.delete()
        elif int(amount) < 1:
            await ctx.send('please entre a real number!', delete_after=7)
            return await ctx.message.delete()

        if amount is not None and user is None:
            await ctx.channel.purge(limit=int(amount))
            await ctx.send(f'**{ctx.author.name}**, msg has been deleted! ♻️', delete_after=5)
            await ctx.message.delete()
        elif user is not None:
            await ctx.message.delete()
            async for msg in ctx.message.channel.history(limit=200):
                if msg.author.name == user:
                    if len(message) == int(amount):
                        break
                    message.append(msg)
            for i in range(len(message)):
                await message[i].delete()
            message.clear()
            await ctx.send(f'**{ctx.author.name}**, msg has been deleted! ♻️', delete_after=5)

def setup(client):
    client.add_cog(Admin(client))
