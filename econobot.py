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


def findAveragePrice(asks):
    sum = 0
    for i in asks:
        sum += float(i[0])
    return sum / 500


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


@bot.command(name="price", description="finds asking price of given pair")
async def price(ctx, pair):
    try:
        response = kraken.query_public('Depth', {'pair': pair, 'count': '500'})
        asks = response['result'][list(response["result"].keys())[0]]['asks']
    except HTTPError as e:
        print(str(e))

    await ctx.respond(findAveragePrice(asks))


bot.run(TOKEN)
