import discord
import os
import krakenex
import crypto_data
from dotenv import load_dotenv
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt

kraken = krakenex.API()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')


@bot.command(name="market_depth", description="finds market depth for given pair")
async def market_depth(ctx, pair: str):
    if crypto_data.checkValidity(pair):
        await ctx.respond(f'{pair} market depth: {crypto_data.findMarketDepth(pair)}')
    else:
        await ctx.respond(f'{pair} is an invalid pair.')


@bot.command(name="price", description="finds asking price of given pair")
async def price(ctx, pair):
    if crypto_data.checkValidity(pair):
        await ctx.respond(f'{pair} ask price: {crypto_data.findAveragePrice(pair)}')
    else:
        await ctx.respond(f'{pair} is an invalid pair.')

@bot.command(name = "graph_depth", description = "displays the market depth graph for a currency pair")
async def graph_depth(ctx, pair):
    if crypto_data.checkValidity(pair):
        await ctx.respond(file = discord.File(crypto_data.graph(pair)))
        os.remove("graph.png")
        plt.close()
    else:
        await ctx.respond(f'{pair} is an invalid pair.')

bot.run(TOKEN)
