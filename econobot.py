import discord
import os
import krakenex
import market_depth
from dotenv import load_dotenv
from requests.exceptions import HTTPError

kraken = krakenex.API()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

@bot.command(name="market_depth", description="finds market depth for given pair")
async def market_depth(ctx, pair):
    await ctx.respond(market_depth.findMarketDepth(pair))

bot.run(TOKEN)