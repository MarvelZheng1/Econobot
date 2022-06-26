import discord
import os
import krakenex
from dotenv import load_dotenv
from requests.exceptions import HTTPError

kraken = krakenex.API()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Bot()

from requests.exceptions import HTTPError
import krakenex

def findSubtotals(results):
    orders = {}
    for i in results:
        orders[float(i[0])] = float(i[1])

    sum = 0
    for value in orders.keys():
        sum += value
    marketPrice = sum/50

    total = 0
    for value in orders.keys():
        weighted = 1/((abs((value-marketPrice)/marketPrice))+1)*orders[value]
        total += weighted
    return total

def findMarketDepth(asks, bids):
    return findSubtotals(asks) + findSubtotals(bids)

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
    await ctx.respond(findMarketDepth(asks, bids))

bot.run(TOKEN)