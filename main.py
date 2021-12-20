import discord
from discord.ext import commands

from decouple import config

from cogs import music


cogs = [music]

intents = discord.Intents().all()
client = commands.Bot(command_prefix=config('PREFIX'), intents=intents)

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(config('TOKEN'))