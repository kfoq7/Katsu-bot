import asyncio
import discord
import random

from discord.ext import commands

from media.gif import eightBall

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *args):
        question = ' '.join(args)

        if not question:
            complain = 'Please ask me a question to me to answer it!'
            await ctx.send(complain)
            return

        randomizedAnswers = random.choice(eightBall)
        answer = f'**{ctx.author.name}** - {randomizedAnswers}'
        await ctx.send(answer)

    @commands.command()
    async def ticket(self, ctx, *args):
        emoji_lock = '🔒'
        emoji_delete = '⛔'

        category = self.client.get_channel(789656899318448138)
        channel = await ctx.message.guild.create_text_channel(f'ticket: {ctx.author.name}', category=category)

        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = True
        await channel.set_permissions(ctx.author, overwrite=overwrite)
        await channel.set_permissions(ctx.author, send_message=True)

        message = await channel.send('Thank you for contacting support!')

        await message.add_reaction(emoji_lock)
        await message.add_reaction(emoji_delete)

        await ctx.message.delete()
        await ctx.send(f'We will be right to you! {channel}', delete_after=7)

        def on_reaction_check(reaction, user):
            return user == ctx.author and str(reaction) in [emoji_delete, emoji_lock]

        while True:
            try:
                reaction, user = await self.client.wait_for(
                    'reaction_add', check=on_reaction_check)
                print(reaction)
                if reaction == str(emoji_lock):
                    print(1)
                    await channel.set_permissions(ctx.author, send_message=False)
                    break

                if reaction == str(emoji_delete):
                    print(1)
                    await channel.send('Deleting this channel in 5 second')
                    await asyncio.sleep(5)
                    # await channel.delete()
                    break
            except:
                raise

def setup(client):
    client.add_cog(Fun(client))
