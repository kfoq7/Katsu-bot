import discord
from discord.ext import commands
from pymongo import MongoClient

from env import MONGO_DB

cluster = MongoClient(MONGO_DB)
records = cluster['discord']['heroes']


class Growth(commands.Cog):

    def __init__(self, client):
        self.client = client

    def embed_pickup(self, hero):
        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title='**>>>Pickup Hero Summon**',
            description="```xl\n**%s!**\n'Summon Chance UP!'```" % (hero['name']))
        embed.set_thumbnail(url=hero['thumbnail'])
        embed.set_image(url=hero['image'])
        return embed

    @commands.command()
    async def banner(self, ctx):
        emoji_right = '➡️'
        emoji_left = '⬅️'

        heros = list(records.find())
        hero_selected = heros[0]
        embed = self.embed_pickup(hero_selected)

        message = await ctx.send(embed=embed)

        await message.add_reaction(emoji_left)
        await message.add_reaction(emoji_right)

        def on_reaction_check(reaction, user):
            return user == ctx.author \
                and str(reaction.emoji) in [emoji_right, emoji_left]

        while True:
            try:
                reaction, user = await self.client.wait_for(
                    'reaction_add', check=on_reaction_check, timeout=60)

                if emoji_right == str(reaction):
                    index_hero = heros.index(hero_selected)
                    hero_selected = heros[index_hero + 1]

                    embed = self.embed_pickup(hero_selected)

                    await message.remove_reaction(str(emoji_right), user)
                    await message.edit(embed=embed)

                if emoji_left == str(reaction):
                    index_hero = heros.index(hero_selected)
                    hero_selected = heros[index_hero - 1]

                    embed = self.embed_pickup(hero_selected)

                    await message.remove_reaction(str(emoji_left), user)
                    await message.edit(embed=embed)
            except IndexError:
                hero_selected = heros[0]

                embed = self.embed_pickup(hero_selected)

                await message.remove_reaction(str(emoji_right), user)
                await message.edit(embed=embed)
            except Exception:
                break

    @commands.group(invoke_without_command=True)
    async def summon(self, ctx):
        await ctx.send('`-summon <type> <ount>`')

    @summon.command(name='hero')
    async def summon_hero(self, ctx, count: int=None, *target):
        if count is None:
            print(count)


def setup(client):
    client.add_cog(Growth(client))
