# Other modules
import json
import random
import requests
from datetime import datetime

# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import *

class register_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def register(self, ctx, arg1):
        try:
            await ctx.message.delete()
        except:
            pass

        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)

            storage[str(ctx.author.id)] = {}
        with open("storage.json", "w") as storage2:

            storage[str(ctx.author.id)]['key'] = f"{arg1}"
        with open("storage.json", "w") as storage2:
            json.dump(storage, storage2, indent=4)

            storage[str(ctx.author.id)]['page'] = 0
        with open("storage.json", "w") as storage2:
            json.dump(storage, storage2, indent=4)

        await ctx.send(f"Registered your Private Key {ctx.author.mention}.")

    @commands.command(pass_context=True)
    async def logout(self, ctx):
        #try:
            #await ctx.message.delete()
        #except:
            #pass

        try:
            with open("storage.json", "r") as storage1:
                storage = json.load(storage1)
        
                storage.pop(str(ctx.author.id))

            with open("storage.json", "w") as storage2:
                json.dump(storage, storage2, indent=4)

            await ctx.send(f"You've been logged out {ctx.author.mention}")
        except:
            await ctx.send("Are you registered?")

    @commands.command(pass_context=True)
    async def profileinfo(self, ctx):
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)
        try:
            key = storage[str(ctx.author.id)]['key']
        except:
            await ctx.send("You did not register a key.")
            return False
        req = requests.get(f"https://api.starfiles.co/2.0/users/get_details.php?profile={key}")
        info = req.json()

        tier1 = info['tier']
        if tier1 == "":
            tier = "None."
        else:
            tier = info['tier']

        try:
            avatar1 = info['avatar'][0]
            print(avatar1)
        except:
            avatar1 = f"{ctx.author.avatar_url}"

        tier_expire1 = info['tier_expires']
        if tier_expire1 == "0":
            tier_expire = "There is no tier to expire."
        else:
            tier_expire = datetime.utcfromtimestamp(int(tier_expire1)).strftime('%Y-%m-%d %H:%M:%S')


        header_image1 = info['header_image']
        if header_image1 == "0":
            header_image = "``No Header image set``"
        else:
            header_image = f"[Image URL]({header_image1})"


        embed=discord.Embed(title=f'Your Profile Info', description=f"Username: ``{info['username']}``\nTier: ``{tier}``\nTier Expiry: ``{tier_expire}``\nKey: ``{key}``\nHeader Image: {header_image}", color=random.choice(colors))
        try:
            embed.set_thumbnail(url=avatar1)
        except:
            pass
        try:
            await ctx.author.send(embed=embed)
        except:
            await ctx.send("Hey it seems like your DMs are closed please open them.")
        


def setup(bot: commands.Bot):
    bot.add_cog(register_cog(bot))
