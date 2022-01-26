import datetime
import discord


def format_seconds(duration):
    timer = str(datetime.timedelta(seconds=duration))
    time = timer if int(timer[0:1]) > 0 else timer[2:7]
    return time

def color_rgb(r, g, b):
    color = discord.Color.from_rgb(r, g, b)
    return color

def is_number(arg):
    elem = True if arg >= '0' and arg <= '9' else False
    return elem