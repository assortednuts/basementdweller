import discord
from discord.ext import commands
from discord.commands import default_permissions

from mcrcon import MCRcon

from dotenv import load_dotenv
import os

# My imports
import userbase

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True  # This may be useless but i'll leave it for now

bot = commands.Bot(command_prefix='/', intents=intents)

# Minecraft connect settings
rcon_ip = '127.0.0.1'
rcon_pass = os.getenv('RCON_PASS')

def run_mc_command(command):
    with MCRcon(rcon_ip, rcon_pass) as mcr:
        resp = mcr.command("/"+command)
        print('Minecraft server replied:', resp)
        return resp

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.before_invoke
async def ensure_user_in_database(ctx):
    # Ensure user exists in database
    if not userbase.user_exists(ctx.author.id):
        userbase.user_create(ctx.author.id, ctx.author.name)
        print(f"Created new user {ctx.author.name} with ID {ctx.author.id}")

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    # Add user to list if not already added
    if not userbase.user_exists(ctx.author.id):
        userbase.user_create(ctx.author.id, ctx.author.name)

    await bot.process_commands(ctx)

@bot.slash_command()
async def linkmc(ctx, minecraft_username: str, version='auto'):
    whitelist_add = userbase.add_minecraft_user(ctx.author.id, minecraft_username, version)

    if whitelist_add == minecraft_username:
        whitelist_resp = run_mc_command("whitelist add " + minecraft_username)
        if whitelist_resp == f'Added {minecraft_username} to the whitelist':
            await ctx.respond(f'Added Java user {minecraft_username}')
        elif whitelist_resp == 'Player is already whitelisted':
            await ctx.respond(whitelist_resp)
        else:
            await ctx.respond('Sorry something went wrong')
    elif whitelist_add == "." + minecraft_username:
        run_mc_command(f"fwhitelist add {minecraft_username}")
        await ctx.respond(f"Added Bedrock user {minecraft_username}")
    elif whitelist_add == 404:
        await ctx.respond("User not found")
    elif whitelist_add == 405:
        await ctx.respond("Account already linked, use /unlinkmc to link a new account")

@bot.slash_command()
async def unlinkmc(ctx):
    whitelist_remove = userbase.remove_minecraft_user(ctx.author.id)
    if whitelist_remove != None and "." not in whitelist_remove:
        whitelist_remove_response = run_mc_command("whitelist remove " + whitelist_remove)
        if whitelist_remove_response == f'Removed {whitelist_remove} from the whitelist':
            await ctx.respond(f'Removed {whitelist_remove} from the whitelist')
    elif whitelist_remove != None and "." in whitelist_remove:
        run_mc_command(f"fwhitelist remove {whitelist_remove}")
        await ctx.respond('Unlinked Bedrock Account')
    else:
        await ctx.respond('No account linked')

@bot.slash_command()
async def mcrun(ctx, command: str):
    resp = run_mc_command(command)
    if resp != "":
        await ctx.respond(resp)
    else:
        await ctx.respond("Server did not reply")
bot.run(os.getenv('DISCORD_TOKEN'))
