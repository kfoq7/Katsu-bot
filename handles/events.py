import discord
from discord.ext import commands

from cogs.music import check_queue, clear_server_queue
from handles.tasks import Tasks


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tk = Tasks(self.client)

    @commands.Cog.listener()
    async def on_ready(self):
        # self.tk.change_status.start()
        print("I'm ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(838620697878069278)
        await channel.send(f'Welcome <@{member.id}> to our server! Make sure to check the normas channel')

    @commands.Cog.listener()
    async def on_voice_state_update(self, *args, **kwargs):
        voice_client = discord.utils.get(self.client.voice_clients)
        if voice_client is not None:
            members = [
                member.id for member in voice_client.channel.members
                if member.bot is not True
            ]
            if len(members) == 0:
                if check_queue(voice_client.guild) is True:
                    clear_server_queue(voice_client.guild)
                await voice_client.disconnect()

def setup(client):
    client.add_cog(Events(client))
