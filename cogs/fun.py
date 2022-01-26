from msilib.schema import Error
import random
import asyncio

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
        category = self.client.get_channel(789656899318448138)
        channel = await ctx.message.guild.create_text_channel(f'ticket: {ctx.author.name}', category=category)

        reactionMessage = await channel.send('Thank you for contacting support!')
        try:
            await reactionMessage.add_reaction('🔒')
            await reactionMessage.add_reaction('⛔')
        except:
            await ctx.send('Error sending emojis')

        collector = await reactionMessage.channel.fetch_message(reactionMessage.id)
        print(collector)

        await ctx.send(f'We will be right to you! {channel}', delete_after=7)
        await asyncio.sleep(3)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Fun(client))
