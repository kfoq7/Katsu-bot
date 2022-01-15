from discord import channel
from discord.ext import commands


class Reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def here(self, ctx, *args):

        @commands.Cog.listener()
        async def on_reaction_add():
            # chanmel = reaciton.message.channel
            # user = user.name
            await ctx.send('Hola')
            # await ctx.send('Hola')

        @commands.Cog.listener()
        async def on_message(message):
            print(message)

        await on_message()

def setup(client):
    client.add_cog(Reactions(client))