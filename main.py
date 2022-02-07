import discord
from discord.ext import commands

from cogs import music, suggestions, admin, reactions, fun
from env import TOKEN, PREFIX
from handles import events

activity_1 = discord.Activity(type=discord.ActivityType.watching, name='que pend*jada haces')
cogs = [music, suggestions, admin, reactions, fun, events]

intents = discord.Intents().all()
client = commands.Bot(command_prefix=PREFIX, activity=activity_1, intents=intents)

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(TOKEN)
