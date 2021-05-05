# modules
import os
import sys
import shutil
import json
import stat
from os import path

# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import *


class upload_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def update(self, ctx):
        if ctx.author.id == 526470337295024148:
            with open(f"{os.getcwd()}/config.json") as f:
                config = json.load(f)

            try:
                GIT_USRNM = os.environ['GITURSNM']
                GIT_PASS = os.environ['GITPASS']
            except:
                GIT_USRNM = config['git']['username']
                GIT_PASS = config['git']['pass']

        
            message = await ctx.send("Updating...")
            os.system(f"git clone https://{GIT_USRNM}:{GIT_PASS}@github.com/repo/repo.git temp")

            # remove all files
            os.remove(f"{os.getcwd()}/main.py")
            os.remove(f"{os.getcwd()}/config.json")
            os.remove(f"{os.getcwd()}/config.py")
            for filename in os.listdir(f'{os.getcwd()}/events'):
                if filename.endswith('.py'):
                    os.remove(f"{os.getcwd()}/events/{filename}")
                    print(f"Removed old {filename}")

            # move all new files
            for filename in os.listdir(f'{os.getcwd()}/temp/events'):
                if filename.endswith('.py'):
                    shutil.copy(f"{os.getcwd()}/temp/events/{filename}", f"{os.getcwd()}/events/{filename}")
                    print(f"Copied new {filename}")
            shutil.move(f"{os.getcwd()}/temp/config.py", f"{os.getcwd()}/config.py")
            shutil.move(f"{os.getcwd()}/temp/main.py", f"{os.getcwd()}/main.py")
            shutil.move(f"{os.getcwd()}/temp/config.json", f"{os.getcwd()}/config.json")

            #remove temp folder
            for root, dirs, files in os.walk(f"{os.getcwd()}/temp/"):
                for dir in dirs:
                    os.chmod(path.join(root, dir), stat.S_IRWXU)
                for file in files:
                    os.chmod(path.join(root, file), stat.S_IRWXU)
            shutil.rmtree(f"{os.getcwd()}/temp/")
            with open(f"{os.getcwd()}/config.json", "r") as f:
                changelog1 = json.load(f)
            await message.edit(content=f"Update Finished\n\n**Changelog:**\n{changelog1['changelog']}")
            os.system(f"py -3 {os.getcwd()}/main.py")
            os.system(f"python3 {os.getcwd()}/main.py")
            sys.exit(1)
        else:
            await ctx.send("You're still not the bot owner.")

def setup(bot: commands.Bot):
    bot.add_cog(upload_cog(bot))