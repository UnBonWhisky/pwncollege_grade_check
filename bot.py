from pwncollege_user import *
import discord
from dotenv import load_dotenv
import os
from maxime import maxime_quote


load_dotenv()

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("PWN THE WORLDDD!!")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith("!subscribe"):
        parts = message.content.split()
        
        if len(parts) < 2:
            await message.channel.send("❌ Format: !subscribe <pseudo>")
            return
            
        username = parts[1].strip()
        
        user = pwncollegeUser(username)
        user.subscribe()

       
        await message.channel.send(f"✅ {message.author.mention} inscrit avec le pseudo **{username}** \n {maxime_quote()}")
            




bot.run(os.getenv("TOKEN"))

