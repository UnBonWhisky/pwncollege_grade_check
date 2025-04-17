import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os


import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from lib.pwncollege_user import pwncollegeUser, read_info, compare_progress
from lib.maxime import maxime_quote
from lib.debug import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
DELAY=6


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} !")
    send_message.start()

@bot.command(name="subscribe")
async def subscribe(ctx, username: str):
    """Commande : !subscribe <pseudo>"""
    user = pwncollegeUser(username)  
    user.init() 
    
    message = (
        f"✅ {ctx.author.mention} inscrit avec le pseudo **{username}**\n"
        f"_{maxime_quote()}_"
    )
    debug(f"commande subscribe effectué par {ctx.author.mention} : {username}")
    await ctx.send(message)


@bot.command(name="get")
async def get_info(ctx, username: str):
    """Commande : !get <pseudo>"""
    debug(f"commande GET effectué par {ctx.author.mention}")
    info = read_info(username)
    base_message = (
        f"{info}\n"
        f"_{maxime_quote()}_"
    )
    #debug(f"Message a envoyer : {base_message}")
    
    max_chars = 1900
    
    if len(base_message) > max_chars:
        message_chunks = [base_message[i:i+max_chars] for i in range(0, len(base_message), max_chars)]
        
        for i, chunk in enumerate(message_chunks):
            if i == 0:
                await ctx.send(f"```\n{chunk}\n``` (1/{len(message_chunks)})")
            else:
                await ctx.send(f"```\n{chunk}\n``` ({i+1}/{len(message_chunks)})")
    else:
        await ctx.send(f"```\n{base_message}\n```")



#automation
@tasks.loop(minutes=DELAY)
async def send_message():
    debug(f"Update DB - check solve")

    channel = await bot.fetch_channel(CHANNEL_ID)
    
    for user in os.listdir("users"):
        u = pwncollegeUser(user)  
        u.init() 

        info = compare_progress(user, DELAY)
        debug(f" info : {info}")
        if info:
            await channel.send(info)



@send_message.before_loop
async def before_send_message():
    await bot.wait_until_ready()





@subscribe.error
@get_info.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Format: !{ctx.command.name} <pseudo>\n_{maxime_quote()}_")






@bot.command()
async def hello(ctx):
    await ctx.send("Hello !")





# Permet la coexistence entre on_message et les commandes
@bot.event
async def on_message(message):
    await bot.process_commands(message)




bot.run(TOKEN)

