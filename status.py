import discord
from itertools import cycle

activity_1 = discord.Activity(type=discord.ActivityType.watching, name='que pend*jada haces')
activity_2 = discord.Activity(type=discord.ActivityType.listening, name='?help | ?play')

status = cycle([activity_1, activity_2])
