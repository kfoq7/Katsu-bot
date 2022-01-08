import discord
from discord.ext import commands

from cogs import music, suggestions, admin

from decouple import config

cogs = [music, suggestions, admin]

intents = discord.Intents().all()
activity = discord.Activity(type=discord.ActivityType.watching, name='que pend*jada haces')
client = commands.Bot(command_prefix=config('PREFIX'), activity=activity, intents=intents)

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print("I'm ready!")

client.run(config('TOKEN'))