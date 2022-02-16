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


class Map:
    def __init__(self): self._dict = {}

    def __str__(self): return '%s' % self._dict

    def set(self, key, value):
        new__dict = self._dict[key] = value
        return new__dict

    def has(self, key):
        obj = self._dict.get(key, None)
        if obj is not None:
            return True
        return False

    def get(self, key): return self._dict.get(key, None)
    def delete(self, key): return self._dict.pop(key)
    def clear(self): return self._dict.clear()
