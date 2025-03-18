from pwncollege_user import pwncollegeUser, read_info
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os
from maxime import maxime_quote

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  


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
    await ctx.send(message)

@bot.command(name="get")
async def get_info(ctx, username: str):
    """Commande : !get <pseudo>"""
    info = read_info(username)
    message = (
        f"==> {ctx.author.mention}\n"
        f"{info}\n"
        f"_{maxime_quote()}_"
    )
    await ctx.send(message)



#automation
@tasks.loop(minutes=10)
async def send_message():
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        await channel.send(f"Automatic Maxime : _{maxime_quote()}_ ⏰")

    except (discord.NotFound, discord.Forbidden) as e:
        print(f"Erreur de salon : {e}")





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

