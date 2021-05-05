#other modules
import random
import json

# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import *

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        with open("config.json", "r") as l:
            config = json.load(l)
        prefix = config['prefix']
        embed=discord.Embed(title="Help", description=f"**Help:**\n**{prefix}help** (Show all Commands)\n\n**Private Key:**\n**{prefix}register** [private key] (adds your private key)\n**{prefix}logout** (removes your private key)\n\n**Info:**\n**{prefix}profileinfo** (DMs you about your Profile Info)\n**{prefix}status** (shows status of starfiles)\n\n**Files/Upload/Download:**\n**{prefix}upload** [folder ID (optional)] (attach a file and it upload it)\n**{prefix}files** (list files)\n**{prefix}folders** (list folders)\n**{prefix}droppers** (list droppers)\n**{prefix}fileinfo** [file ID] (Shows information about a file)\n\n**Bot Invite/About:**\n**{prefix}invite** (get bot invite)\n**{prefix}credits**", color=random.choice(colors))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/739435448203608134/794846055988199424/starfiles.png")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        embed=discord.Embed(title="Invite", description=f"Invite me: [link](https://discord.com/api/oauth2/authorize?client_id=788373372429664277&permissions=0&scope=bot%20applications.commands)", color=random.choice(colors))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def prefix(self, ctx):
        with open("config.json", "r") as l:
            config = json.load(l)
        prefix = config['prefix']
        await ctx.send(f"My prefix is **{prefix}**")

    @commands.command(pass_context=True)
    async def credits(self, ctx):
        embed=discord.Embed(title="Credits", description="Quix for creating [starfiles](https://starfiles.co)\nUnna000 for [Hastebin API](https://raw.githubusercontent.com/Unna000/Hastebin-API/master/hastebin.py) information", color=random.choice(colors))
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(help_cog(bot))
