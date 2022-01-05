import discord
from discord.ext import commands


class suggestions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def suggestion(self, ctx, *args):
        channel = self.client.get_channel(837143240476983307)
        msg = ' '.join(args)

        @commands.Cog.listener()
        async def on_message(ctx):
            await ctx.message.delete()

        if msg != "":
            author = ctx.author

            embedVar = discord.Embed(
                description='%s' % msg,
                color=10928526)
            embedVar.set_author(name=author.name, icon_url=author.avatar_url)
            await on_message(ctx)
            await channel.send(embed=embedVar)
        else:
            await on_message(ctx)
            await ctx.send('You need to send an argument', delete_after=5)


def setup(client):
    client.add_cog(suggestions(client))
