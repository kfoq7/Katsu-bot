"""
This archive contain all message will be include into the embeds.
"""

import discord

minecraft = {
    # default init for Minecraft Embed message
    'title': 'Minecraft Server',
    'description': 'Well guys, here is the list of the all resource we will use in the server',
    'color': discord.Color.from_rgb(117, 253, 104),

    # thumbnail field
    'thumbnail_url': 'https://media.discordapp.net/attachments/751240067158376508/861694154061250630/210674225_1552880831712602_7405473157188067689_n.png?width=648&height=648',

    # fields
    'resource_pack': {
        'name': 'Download resource pack here',
        'value': '[click here!](https://www.youtube.com/)'
    },

    'force': {
        'name': 'Downlad force version 1.12.2',
        'value': '[click here!]()'
    },

    # image
    'image': 'https://media.tenor.co/videos/bd7d811746b561653e60575e5e24998f/mp4',
}