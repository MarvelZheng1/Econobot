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

from requests.exceptions import HTTPError
import krakenex


@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

@bot.command(name="market_depth", description="finds market depth for given pair")
async def market_depth(ctx, pair: str):
    try:
        response = kraken.query_public('Depth', {'pair': pair, 'count': '500'})
        bids = response['result'][list(response["result"].keys())[0]]['bids']
        asks = response['result'][list(response["result"].keys())[0]]['asks']

    except HTTPError as e: 
        await ctx.respond("Oops! An error occurred!")
    await ctx.respond(market_depth.findMarketDepth(asks, bids))

bot.run(TOKEN)
