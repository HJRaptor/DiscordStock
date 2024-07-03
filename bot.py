import discord
from discord import member
import yfinance

#intents
intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[903618670700417065])
async def info(ctx, symbol: str):
    selectedStock = yfinance.Ticker(symbol)
    regular_market_open = selectedStock.info['regularMarketOpen']
    await ctx.respond(regular_market_open)
    

bot.run()

