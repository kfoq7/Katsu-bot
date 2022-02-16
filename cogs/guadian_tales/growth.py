import discord
from discord.ext import commands
from pymongo import MongoClient

class Growth(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Growth(client))
