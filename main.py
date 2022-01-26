import discord
from discord.ext import commands

from cogs import music, suggestions, admin, reactions, fun

from tasks import Tasks
from decouple import config

cogs = [music, suggestions, admin, reactions, fun]

intents = discord.Intents().all()
client = commands.Bot(command_prefix=config('PREFIX'), intents=intents)
tk = Tasks(client)

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    tk.change_status.start()
    tk.check_voice_channel.start()
    print("I'm ready!")

client.run(config('TOKEN'))
