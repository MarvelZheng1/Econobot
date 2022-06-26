import discord
import os
import krakenex
import crypto_data
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
async def market_depth(ctx, pair: str):
    await ctx.respond(crypto_data.findMarketDepth(pair))


@bot.command(name="price", description="finds asking price of given pair")
async def price(ctx, pair):
    await ctx.respond(crypto_data.findAveragePrice(pair))


bot.run(TOKEN)
