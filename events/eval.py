#other modules
import ast
import io
from contextlib import redirect_stdout
import random
import requests
import json
import subprocess


# Discord Modules
import discord
#from discord import *
from discord.ext import commands
from discord.ext.commands import Bot
from config import colors

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


#cog
class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Old No Longer used Eval command OwO.
    #Have an Better one which can run discord functions.

    #@commands.command(pass_context=True)
    #async def eval(self, ctx, *, arg1):
        #if ctx.author.id == 526470337295024148:
            #try:
                #code = f"{arg1}"
                #f = io.StringIO()
                #with redirect_stdout(f):
                   #x = exec(code)
                #out = f.getvalue()
                #print(out)
                #embed=discord.Embed(title=f'**Eval (Successful)**', description=f"**Code:**\n```py\n{arg1}```\n\n**Output:**\n```{out}```", color=random.choice(colors))
                #await ctx.send(embed=embed)
            #except Exception as bruh:
                #embed=discord.Embed(title=f'**Eval (Error)**', description=f"**Code:**\n```py\n{arg1}```\n\n**Output:**\n```Error: {bruh}```", color=random.choice(colors))
                #await ctx.send(embed=embed)
        #else:
            #await ctx.send("Kiddie who you think you are??")
            #return False

    @commands.command(pass_context=True)
    async def eval(self, ctx, *, cmd):
        if ctx.author.id == 526470337295024148:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)

            env = {
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            try:
                exec(compile(parsed, filename="<ast>", mode="exec"), env)
                result = (await eval(f"{fn_name}()", env))
                try:
                    embed=discord.Embed(title=f'**Eval (Successful)**', description=f"**Code:**\n```py\n{cmd}```\n\n**Output:**\n```{result}```", color=random.choice(colors))
                    await ctx.send(embed=embed)
                except:
                    data = f"Input:\n{cmd}\n\nOutput:\n{result}"
                    req = requests.post('https://hastebin.com/documents', data=data)
                    print(req.text)
                    key = req.json()
                    await ctx.send(f"Result was to big! https://hastebin.com/{key['key']}")
            except Exception as bruh:
                try:
                    embed=discord.Embed(title=f'**Eval (Error)**', description=f"**Code:**\n```py\n{cmd}```\n\n**Output:**\n```Error: {bruh}```", color=random.choice(colors))
                    await ctx.send(embed=embed)
                except:
                    data = f"Input:\n{cmd}\n\nOutput:\n{bruh}"
                    req = requests.post('https://hastebin.com/documents', data=data)
                    print(req.text)
                    key = req.json()
                    await ctx.send(f"Result was to big! https://hastebin.com/{key['key']}")
        else:
            await ctx.send("Since wen are you the bot owner <:kekDisco:796013186033778708>")
            return False

    @commands.command(pass_context=True)
    async def shell(self, ctx, *, cmd):
        if ctx.author.id == 526470337295024148:
            shell = subprocess.check_output(f"{cmd}", shell=True).decode()
            try:
                embed=discord.Embed(title=f'**Shell**', description=f"**Code:**\n```bash\n{cmd}```\n\n**Output:**\n```{shell}```", color=random.choice(colors))
                await ctx.send(embed=embed)
            except:
                data = f"Input:\n{cmd}\n\nOutput:\n{shell}"
                req = requests.post('https://hastebin.com/documents', data=data)
                print(req.text)
                key = req.json()
                await ctx.send(f"Result was to big! https://hastebin.com/{key['key']}")
        else:
            await ctx.send("Since wen are you the bot owner <:kekDisco:796013186033778708>")
            return False

def setup(bot: commands.Bot):
    bot.add_cog(help_cog(bot))