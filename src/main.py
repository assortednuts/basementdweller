import discord
from discord.ext import commands

from mcrcon import MCRcon

from dotenv import load_dotenv
import os

# My imports
import userbase

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True  # This may be useless but i'll leave it for now

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    # Add user to list if not already added
    if not userbase.user_exists(ctx.author.id):
        userbase.user_create(ctx.author.id, ctx.author.name)

    await bot.process_commands(ctx)

@bot.command()
async def linkmc(ctx, minecraft_username):
    whitelist_add = userbase.add_minecraft_user(ctx.author.id, minecraft_username)

    if whitelist_add == minecraft_username:
        with MCRcon("127.0.0.1", os.getenv('RCON_PASS')) as mcr:
            resp = mcr.command("/whitelist add " + minecraft_username)
            print(resp)
    elif whitelist_add == 404:
        await ctx.reply("Java user not found")
    elif whitelist_add == 405:
        await ctx.reply("Account already linked, use /unlinkmc to link a new account")

@bot.command()
async def unlinkmc(ctx):
    whitelist_remove = userbase.remove_minecraft_user(ctx.author.id)
    if whitelist_remove != None:
        with MCRcon("127.0.0.1", os.getenv('RCON_PASS')) as mcr:
            resp = mcr.command("/whitelist remove " + whitelist_remove)
            print(resp)

bot.run(os.getenv('DISCORD_TOKEN'))
