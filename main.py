import discord
from discord.ext import commands

from cogs import music, suggestions, config

cogs = [music, suggestions, config]

from decouple import config

intents = discord.Intents().all()
client = commands.Bot(command_prefix=config('PREFIX'), intents=intents)

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print("I'm ready!")

client.run(config('TOKEN'))