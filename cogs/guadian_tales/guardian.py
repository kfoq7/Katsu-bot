import asyncio
import discord
import functools
from discord.ext import commands
from pymongo import MongoClient


cluster = MongoClient(
    'mongodb+srv://kfoq7:admin@cluster0.petxl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
#  cluster.get_database('discord')
records = cluster['discord']['guardian']

# new_guardian = {
#     'name': 'kfoqiu7',
#     'roll': 'admin'
# }

# records.insert_one(new_guardian)
# records.count_documents({})

# print(records.find_one({'name': 'kfoqiu7'}))


class Guardian(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def initialize(self, ctx):
        if records.find_one({'id': ctx.author.id}) is None:
            new_guardian = {
                'id': ctx.author.id,
                'username': None,
            }
            records.insert_one(new_guardian)
            return await ctx.send('You can now use the other commands <@%s>. Have fun!' % (ctx.author.id))

        return await ctx.send('You are already intialized, <@%s>. Has fun!' % (ctx.author.id))

    def __handle_is_initialized(coro):
        @functools.wraps(coro)
        async def wrapper(self, ctx, *args, **kwargs):
            if records.find_one({'id': ctx.author.id}) is None:
                return await ctx.send('You need to intialize first!')
            return await coro(self, ctx, *args, **kwargs)
        return wrapper

    @commands.command()
    async def profile(self, ctx, mention: discord.Member=None):
        guardian = records.find_one({'id': ctx.author.id})
        if guardian is None:
            return await ctx.send('You need to intialize first!')

        embed = discord.Embed(color=000)
        embed.add_field(name='Username', value=guardian['username'], inline=False)
        embed.add_field(name='User EXP', value=None, inline=False)
        # embed.add_field(name='Username', value=guardian['name'], inline=False)

        return await ctx.send(embed=embed)

    @commands.command()
    @__handle_is_initialized
    async def username(self, ctx, username=None):
        if username is None:
            embed = discord.Embed(color=000, description='-username <usernamer>')
            return await ctx.send(embed=embed)

        # guardian = {'id': ctx.author.id}
        records.update_one({'id': ctx.author.id}, {"$set": {'username': username}})
        return await ctx.send(f'Your username is now, **{username}**. Enjoy, <@{ctx.author.id}>')

    @commands.group(invoke_without_command=True)
    @__handle_is_initialized
    async def team(self, ctx):
        message = await ctx.send(
            f'Time to explain.., Hey, <@{ctx.author.id}>, you better read properly. tsk')

        await asyncio.sleep(1)
        await message.reply(
            'Issue `-team`'
        )

    @team.command(name='set')
    async def team_set(self, ctx, key=None, *heroes):
        if not key:
            return await ctx.send("You forgot to specify the key. Put `main` as the key "
                + "if you want to be able to use commands like `arena` "
                + "without having to specify `key`.")

        if not heroes:
            return await ctx.send("Specify the heroes you want in the team. "
                + "One team consists of one to four heroes. "
                + "Make sure to separate the heroes with `;` "
                + "For example, "
                + "`Alef;Idol Captain Eva;Gabriel;Princess` "
                + "or just `Alef` if you want only one hero "
                + "in your team.")

        # exist = 
def setup(client):
    client.add_cog(Guardian(client))
