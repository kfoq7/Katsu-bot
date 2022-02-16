import asyncio
import discord
import json
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


class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._dict_message = {}
        self._list_users = []

    @commands.command()
    async def poll(self, ctx, *, args):
        question = args[:args.find(']')].strip('[')
        choices = args[args.find(']') + 2:].replace(' ', '').split(',')

        embed = discord.Embed(
            color=color_rgb(162, 252, 239),
            description=f':bar_chart: **{question}**'
        )
        for choice in choices:
            embed.add_field(name=choice, value='`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`' + '| 0% (0)', inline=False)
        embed.set_footer(text='✅ You may select multiple options in this poll')

        message = await ctx.send(embed=embed)
        self._dict_message[message.id] = message
        # new_embed = discord.Embed(title='embed 2')
        # new_embed.set_footer(text='✅ You may select multiple ')
        # await asyncio.sleep(5)
        # await message.edit(embed=new_embed)

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user, users=[]):
    #     message = self._list_message.get(reaction.message.id)
    #     if message is not None:
    #         users.append(user.id)
    #         print(users)
    #         new_embed = discord.Embed(title='embed 2')
    #         new_embed.set_footer(text='✅ You may select multiple ')
    #         await message.edit(embed=new_embed)


def setup(client):
    client.add_cog(Admin(client))
    client.add_cog(Poll(client))
