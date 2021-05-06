# Other modules
import random
import re
import requests
import json
import os
import shutil

# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import *

header={
    'User-Agent': 'starfiles-bot/crafterpika (requests/2.25.1)'
}

class upload_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def upload(self, ctx, folder = None):
        if not ctx.message.attachments:
            await ctx.send("You need to attach a file.")
            return False
        else:
            with open("storage.json", "r") as storage1:
                storage = json.load(storage1)
            try:
                key = storage[str(ctx.author.id)]['key']
            except:
                await ctx.send("You need to register your private key.")
            print(ctx.message.attachments)
            attachment = ctx.message.attachments[0]
            print(attachment.url)
            await attachment.save(attachment.filename)
            try:
                shutil.rmtree(f"{os.getcwd()}/data/")
                os.mkdir(f"{os.getcwd()}/data/")
            except:
                os.mkdir(f"{os.getcwd()}/data/")
            shutil.move(f"{os.getcwd()}/{attachment.filename}", f"{os.getcwd()}/data/{attachment.filename}")

            files1 = {
                'upload': (f'{os.getcwd()}/data/{attachment.filename}', open(f'{os.getcwd()}/data/{attachment.filename}', 'rb'))
            }
            if folder == f"{folder}":
                response = requests.post(f'https://api.starfiles.co/upload/upload_file?folder={folder}&profile={key}', files=files1, headers=header)
            else:
                response = requests.post(f'https://api.starfiles.co/upload/upload_file?profile={key}', files=files1, headers=header)
            print(response.text)
            upload_done = response.json()
            embed=discord.Embed(title=f'File Uploaded', description=f"Your file ``{attachment.filename}`` to starfiles\nFile: [Page](https://starfiles.co/file/{upload_done['file']})\nDownload: [File](https://api.starfiles.co/direct/{upload_done['file']})", color=random.choice(colors))
            await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(upload_cog(bot))
