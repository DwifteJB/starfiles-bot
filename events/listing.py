  
# Other modules
import json
import random
import urllib.request
import requests
import asyncio
import os
import shutil

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
    async def files(self, ctx):
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)
        storage[str(ctx.author.id)]['page'] = 0
        with open("storage.json", "w") as storage2:
            json.dump(storage, storage2, indent=4)
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)

        try:
            key = storage[str(ctx.author.id)]['key']
        except:
            await ctx.send("You did not register a key.")
            return False
        req = requests.get(f"https://api.starfiles.co/user/files?profile={key}")
        filesAPI = req.json()

        fileslen = len(filesAPI)
        print(fileslen)
        actual_page = storage[str(ctx.author.id)]['page']

        package_hash = filesAPI[int(actual_page)]['hash']
        package_id = filesAPI[int(actual_page)]['id']
        package_name = filesAPI[int(actual_page)]['name']
        if filesAPI[int(actual_page)]['star'] == "1":
            package_star = "Yes"
        else:
            package_star = "No"

        while True:
            embed=discord.Embed(title=f'{package_name}', description=f"Starred: {package_star}\nDownload: [File](https://starfiles.co/file/{package_id})", color=random.choice(colors))
            embed.set_footer(text=f"Page {int(actual_page+1)} of {fileslen}")
            message = await ctx.send(embed=embed)
            reactions = ['⬅️', '➡️', '⬇️', '🗑️']
            for react in reactions:
                await message.add_reaction(react)
            
            global user
            def check_react(reaction, user):
                if reaction.message.id != message.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactions:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for('reaction_add', check=check_react)
            except asyncio.TimeoutError:
                print("Time Out")

            if user != ctx.message.author:
                pass
            elif '⬇️' in str(res.emoji):
                await ctx.send(f"Downloading {package_name}")
                try:
                    await message.remove_reaction("⬇️",user)
                except:
                    pass
                try:
                    shutil.rmtree(f"{os.getcwd()}/data/")
                    os.mkdir(f"{os.getcwd()}/data/")
                except:
                    pass
                print(f"Downloading {package_name}")
                req = requests.get(f"https://api.starfiles.co/direct/{package_id}")
                with open(f"{os.getcwd()}/data/{package_name}", "wb") as f:
                    f.write(req.content)
                #opener = urllib.request.build_opener()
                #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                #urllib.request.install_opener(opener)
                #urllib.request.urlretrieve(f'https://api.starfiles.co/direct/{package_id}', f'{os.getcwd()}/data/{package_name}')
                print(f"Done")
                try:
                    upload = discord.File(f"{os.getcwd()}/data/{package_name}")
                    await ctx.send(file=upload)
                except Exception as error:
                    await ctx.send(f"An Error occured while uploadin:\n{error}")
            elif '🗑️' in str(res.emoji):
                await ctx.send(f"Will Delete {package_name}")
                try:
                    await message.remove_reaction("🗑️",user)
                except:
                    pass
                req = requests.get(f"https://api.starfiles.co/file/delete?file={package_id}&profile={key}")
                print(req.text)
                storage[str(ctx.author.id)]['page'] = 0
                with open("storage.json", "w") as storage2:
                    json.dump(storage, storage2, indent=4)
                with open("storage.json", "r") as storage1:
                    storage = json.load(storage1)
                req = requests.get(f"https://api.starfiles.co/user/files?profile={key}")
                filesAPI = req.json()
                actual_page = storage[str(ctx.author.id)]['page']

                package_hash = filesAPI[int(actual_page)]['hash']
                package_id = filesAPI[int(actual_page)]['id']
                package_name = filesAPI[int(actual_page)]['name']
                if filesAPI[int(actual_page)]['star'] == "1":
                    package_star = "Yes"
                else:
                    package_star = "No"
                await ctx.send("Done.")
            elif '➡️' in str(res.emoji):
                storage[str(ctx.author.id)]['page'] += 1
                with open("storage.json", "w") as storage2:
                    json.dump(storage, storage2, indent=4)

                with open("storage.json", "r") as storage1:
                    storage = json.load(storage1)

                try:
                    actual_page = storage[str(ctx.author.id)]['page']
                    package_hash = filesAPI[int(actual_page)]['hash']
                    package_id = filesAPI[int(actual_page)]['id']
                    package_name = filesAPI[int(actual_page)]['name']
                    if filesAPI[int(actual_page)]['star'] == "1":
                        package_star = "Yes"
                    else:
                        package_star = "No"
                    #embed=discord.Embed(title=f'{package_name}', description=f"Starred: {package_star}\nDownload: [File](https://starfiles.co/file/{package_id})", color=random.choice(colors))
                    #embed.set_footer(text=f"Page {str(actual_page)} of {fileslen}")
                except:
                    #await ctx.send("Max Reached.")
                    storage[str(ctx.author.id)]['page'] = 0
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)
                    actual_page = storage[str(ctx.author.id)]['page']
                    package_hash = filesAPI[int(actual_page)]['hash']
                    package_id = filesAPI[int(actual_page)]['id']
                    package_name = filesAPI[int(actual_page)]['name']
                    if filesAPI[int(actual_page)]['star'] == "1":
                        package_star = "Yes"
                    else:
                        package_star = "No"
                try:
                    await message.remove_reaction("➡️",user)
                except:
                    pass
            elif '⬅️' in str(res.emoji):
                storage[str(ctx.author.id)]['page'] -= 1
                with open("storage.json", "w") as storage2:
                    json.dump(storage, storage2, indent=4)

                with open("storage.json", "r") as storage1:
                    storage = json.load(storage1)

                try:
                    actual_page = storage[str(ctx.author.id)]['page']
                    package_hash = filesAPI[int(actual_page)]['hash']
                    package_id = filesAPI[int(actual_page)]['id']
                    package_name = filesAPI[int(actual_page)]['name']
                    if filesAPI[int(actual_page)]['star'] == "1":
                        package_star = "Yes"
                    else:
                        package_star = "No"
                    #embed=discord.Embed(title=f'{package_name}', description=f"Starred: {package_star}\nDownload: [File](https://starfiles.co/file/{package_id})", color=random.choice(colors))
                    #embed.set_footer(text=f"Page {str(actual_page)} of {fileslen}")
                except:
                    #await ctx.send("Max Reached **(Page number's are now fucked up *Congrats*)**.")
                    storage[str(ctx.author.id)]['page'] = 0
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)
                    actual_page = storage[str(ctx.author.id)]['page']
                    package_hash = filesAPI[int(actual_page)]['hash']
                    package_id = filesAPI[int(actual_page)]['id']
                    package_name = filesAPI[int(actual_page)]['name']
                    if filesAPI[int(actual_page)]['star'] == "1":
                        package_star = "Yes"
                    else:
                        package_star = "No"
                try:
                    await message.remove_reaction("⬅️",user)
                except:
                    pass
            else:
                return False

    @commands.command(pass_context=True)
    async def folders(self, ctx):
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)
        storage[str(ctx.author.id)]['page'] = 0
        with open("storage.json", "w") as storage2:
            json.dump(storage, storage2, indent=4)
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)

        try:
            key = storage[str(ctx.author.id)]['key']
        except:
            await ctx.send("You did not register a key.")
            return False
        req = requests.get(f"https://api.starfiles.co/user/folders?profile={key}")
        foldersAPI = req.json()
        folderslen = len(foldersAPI)
        print(folderslen)
        actual_page = storage[str(ctx.author.id)]['page']

        folder_id = foldersAPI[int(actual_page)]['id']
        folder_name = foldersAPI[int(actual_page)]['name']
        if foldersAPI[int(actual_page)]['star'] == "1":
            folder_starred = "Yes"
        else:
            folder_starred = "No"

        while True:
            embed=discord.Embed(title=f'{folder_name}', description=f"Starred: {folder_starred}\nFolder: [Link](https://starfiles.co/folder/{folder_id})", color=random.choice(colors))
            embed.set_footer(text=f"Page {int(actual_page+1)} of {folderslen}")
            message = await ctx.send(embed=embed)
            reactions = ['⬅️', '➡️', '🗑️']
            for react in reactions:
                await message.add_reaction(react)

            global user
            def check_react(reaction, user):
                if reaction.message.id != message.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactions:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
            except asyncio.TimeoutError:
                print("Time Out")

            if user != ctx.message.author:
                pass
            elif '🗑️' in str(res.emoji):
                await ctx.send(f"Will Delete {folder_name}")
                try:
                    await message.remove_reaction("🗑️",user)
                except:
                    pass
                req = requests.get(f"https://api.starfiles.co/folder/delete/{folder_id}&profile={key}")
                print(req.text)
                await ctx.send("Done.")
            elif '➡️' in str(res.emoji):
                storage[str(ctx.author.id)]['page'] += 1
                with open("storage.json", "w") as storage2:
                    json.dump(storage, storage2, indent=4)

                with open("storage.json", "r") as storage1:
                    storage = json.load(storage1)

                try:
                    actual_page = storage[str(ctx.author.id)]['page']
                    folder_id = foldersAPI[int(actual_page)]['id']
                    folder_name = foldersAPI[int(actual_page)]['name']
                    if foldersAPI[int(actual_page)]['star'] == "1":
                        folder_starred = "Yes"
                    else:
                        folder_starred = "No"
                except:
                    #await ctx.send("Max Reached")
                    storage[str(ctx.author.id)]['page'] = 0
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)
                    actual_page = storage[str(ctx.author.id)]['page']
                    folder_id = foldersAPI[int(actual_page)]['id']
                    folder_name = foldersAPI[int(actual_page)]['name']
                    if foldersAPI[int(actual_page)]['star'] == "1":
                        folder_starred = "Yes"
                    else:
                        folder_starred = "No"
                try:
                    await message.remove_reaction("➡️",user)
                except:
                    pass
            elif '⬅️' in str(res.emoji):
                storage[str(ctx.author.id)]['page'] -= 1
                with open("storage.json", "w") as storage2:
                    json.dump(storage, storage2, indent=4)

                with open("storage.json", "r") as storage1:
                    storage = json.load(storage1)

                try:
                    actual_page = storage[str(ctx.author.id)]['page']
                    folder_id = foldersAPI[int(actual_page)]['id']
                    folder_name = foldersAPI[int(actual_page)]['name']
                    if foldersAPI[int(actual_page)]['star'] == "1":
                        folder_starred = "Yes"
                    else:
                        folder_starred = "No"
                except:
                    #await ctx.send("Max Reached")
                    storage[str(ctx.author.id)]['page'] = 0
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)
                    actual_page = storage[str(ctx.author.id)]['page']
                    folder_id = foldersAPI[int(actual_page)]['id']
                    folder_name = foldersAPI[int(actual_page)]['name']
                    if foldersAPI[int(actual_page)]['star'] == "1":
                        folder_starred = "Yes"
                    else:
                        folder_starred = "No"
                try:
                    await message.remove_reaction("⬅️",user)
                except:
                    pass
            else:
                return False

    @commands.command(pass_context=True)
    async def droppers(self, ctx):
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)
        storage[str(ctx.author.id)]['page'] = 0
        with open("storage.json", "w") as storage2:
            json.dump(storage, storage2, indent=4)
        with open("storage.json", "r") as storage1:
            storage = json.load(storage1)

        try:
            key = storage[str(ctx.author.id)]['key']
        except:
            await ctx.send("You did not register a key.")
            return False
        req = requests.get(f"https://api.starfiles.co/user/droppers?profile={key}")
        dropperAPI = req.json()
        dropperslen = len(dropperAPI)
        print(dropperslen)
        actual_page = storage[str(ctx.author.id)]['page']

        dropper_id = dropperAPI[int(actual_page)]['id']

        while True:
            embed=discord.Embed(title=f'{dropper_id}', description=f"Dropper: [Link](https://starfiles.co/dropper/{dropper_id})", color=random.choice(colors))
            embed.set_footer(text=f"Page {int(actual_page+1)} of {dropperslen}")
            message = await ctx.send(embed=embed)
            reactions = ['⬅️', '➡️', '🗑️']
            for react in reactions:
                await message.add_reaction(react)

            global user
            def check_react(reaction, user):
                if reaction.message.id != message.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactions:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for('reaction_add', check=check_react)
            except asyncio.TimeoutError:
                print("Time Out")

            if user != ctx.message.author:
                pass
            elif '🗑️' in str(res.emoji):
                await ctx.send(f"Will Delete {dropper_id}")
                try:
                    await message.remove_reaction("🗑️",user)
                except:
                    pass
                req = requests.get(f"https://api.starfiles.co/dropper/delete/{dropper_id}&profile={key}")
                print(req.text)
                await ctx.send("Done.")
            elif '➡️' in str(res.emoji):
                try:
                    storage[str(ctx.author.id)]['page'] += 1
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)

                    with open("storage.json", "r") as storage1:
                        storage = json.load(storage1)
                    actual_page = storage[str(ctx.author.id)]['page']
                    dropper_id = dropperAPI[int(actual_page)]['id']
                except:
                    #await ctx.send("Max Reached")
                    storage[str(ctx.author.id)]['page'] = 0
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)
                    actual_page = storage[str(ctx.author.id)]['page']
                    dropper_id = dropperAPI[int(actual_page)]['id']
                try:
                    await message.remove_reaction("➡️",user)
                except:
                    pass
            elif '⬅️' in str(res.emoji):
                try:
                    storage[str(ctx.author.id)]['page'] -= 1
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)

                    with open("storage.json", "r") as storage1:
                        storage = json.load(storage1)
                    actual_page = storage[str(ctx.author.id)]['page']
                    dropper_id = dropperAPI[int(actual_page)]['id']
                except:
                    #await ctx.send("Max Reached")
                    storage[str(ctx.author.id)]['page'] = 0
                    with open("storage.json", "w") as storage2:
                        json.dump(storage, storage2, indent=4)
                    actual_page = storage[str(ctx.author.id)]['page']
                    dropper_id = dropperAPI[int(actual_page)]['id']
                try:
                    await message.remove_reaction("⬅️",user)
                except:
                    pass
            else:
                return False

    @commands.command(pass_context=True)
    async def status(self, ctx):
        req = requests.get("https://starfiles.co/cronjobs/uptime")
        state = req.json()
        embed=discord.Embed(title=f'Status', description=f"Database: ``{state['database']}``\nWebsite: ``{state['starfiles.co']}``\nCDN: ``{state['cdn.starfiles.co']}``\nAPI: ``{state['api.starfiles.co']}``\nFile Download: ``{state['starfiles.co file download']}``", color=random.choice(colors))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def fileinfo(self, ctx, arg1):
        req = requests.get(f"https://api.starfiles.co/file/fileinfo?file={arg1}")
        info = req.json()

        while True:
            embed=discord.Embed(title="File Info", description=f"Filename: ``{info['name']}``\nExtension: ``.{info['extension']}``\nMime_type: ``{info['mime_type']}``\nSize: ``{info['tidy_size']}``\nUpload Date: ``{info['time_ago']}``\nDownload Count: ``{info['download_count']}``")
            embed.set_footer(text="React to ⬇️ to download the File.")
            message = await ctx.send(embed=embed)
            reactions = ['⬇️']
            for react in reactions:
                await message.add_reaction(react)

            global user
            def check_react(reaction, user):
                if reaction.message.id != message.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactions:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for('reaction_add', check=check_react)
            except asyncio.TimeoutError:
                print("Time Out")

            if user != ctx.message.author:
                pass
            elif '⬇️' in str(res.emoji):
                await ctx.send(f"Downloading...")
                try:
                    await message.remove_reaction("⬇️",user)
                except:
                    pass
                try:
                    shutil.rmtree(f"{os.getcwd()}/data/")
                    os.mkdir(f"{os.getcwd()}/data/")
                except:
                    pass
                print(f"Downloading..")
                req = requests.get(f"https://api.starfiles.co/direct/{arg1}")
                with open(f"{os.getcwd()}/data/{info['name']}", "wb") as f:
                    f.write(req.content)
                #opener = urllib.request.build_opener()
                #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                #urllib.request.install_opener(opener)
                #urllib.request.urlretrieve(f'https://api.starfiles.co/direct/{arg1}', f"{os.getcwd()}/data/{info['name']}")
                print(f"Done")
                try:
                    upload = discord.File(f"{os.getcwd()}/data/{info['name']}")
                    await ctx.send(file=upload)
                except Exception as error:
                    await ctx.send(f"An Error occured while uploadin:\n{error}")
            else:
                print("a")



def setup(bot: commands.Bot):
    bot.add_cog(listing_cog(bot))
