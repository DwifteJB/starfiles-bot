# Other modules
import json
import os
import asyncio
import random

# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import *

try:
    with open("config.json", "r") as l:
        config = json.load(l)
    token = os.environ['DISCORD_BOT_TOKEN']
    from repl import keep_alive
    prefix = config['prefix']
    repl = True
    #config.pop('token')
except:
    with open("config.json", "r") as l:
        config = json.load(l)
    prefix = config['prefix']
    token = config['token']
    repl = False

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

@bot.event
async def on_connect():
      print(f'Logged in as {bot.user}!\nYour Current Prefix: {prefix}')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'starfiles.co or {prefix}help'))

@bot.event
async def on_command_error(ctx,error):
  embed=discord.Embed(title = f"An Error Occured:", description=f"{str(error)}", color=random.choice(colors))
  await ctx.send(embed=embed)

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'events.{filename[:-3]}')
        except Exception as error:
            print(f"Cog {filename} failed to load\nError: {error}")
            pass

try:
    keep_alive()
    repl = True
except:
    repl = False
    pass
bot.run(token)
