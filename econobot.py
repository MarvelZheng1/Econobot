import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')


bot.run(TOKEN)
