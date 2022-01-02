import discord
from discord.ext import commands

from decouple import config

from cogs import music, suggestions


cogs = [music, suggestions]

intents = discord.Intents().all()
client = commands.Bot(command_prefix=config('PREFIX'), intents=intents)

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print("I'm ready!")


client.run(config('TOKEN'))