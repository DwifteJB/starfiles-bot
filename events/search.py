# Other modules
import json
import random
import requests
import asyncio
import os
import re

# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import *

class listing_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def search(self, ctx, *, arg1):
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)
        try:
            key = storage[str(ctx.author.id)]['key']
        except:
            await ctx.send("No key registered")
            return False
        req = requests.get(f"https://api.starfiles.co/user/files?profile={key}")
        print(req.text)

        res = re.search(f"{arg1}", req.text)
        try:
            results = res.group(0)
            print(results)
            await ctx.send(f"Found {results} results")
        except:
            await ctx.send("No Results found")

def setup(bot: commands.Bot):
    bot.add_cog(listing_cog(bot))