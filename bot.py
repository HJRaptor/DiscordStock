import discord
from discord import member
import yfinance
from dotenv import load_dotenv
import os

load_dotenv()

#intents
intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = discord.Bot(intents=intents)




@bot.slash_command(guild_ids=[903618670700417065])
async def info(ctx, symbol: str):
    selectedStock = yfinance.Ticker(symbol)

    name = selectedStock.info['shortName']
    regular_market_open = selectedStock.info['regularMarketOpen']
    daylow = selectedStock.info['dayLow']
    dayhigh = selectedStock.info['dayHigh']
    divYield = float(selectedStock.info['dividendYield'])*100
    divYield = round(divYield, 2)

    stockembed = discord.Embed(title=name,color=discord.Colour.blurple())
    stockembed.add_field(name="Market Open",value=regular_market_open)
    stockembed.add_field(name="Day Low", value=daylow)
    stockembed.add_field(name="Day Low", value=dayhigh)
    stockembed.add_field(name="Annual Dividend Yield", value=divYield+"%")
    stockembed.set_footer(text="HJRaptor - 2024")
    

    
    await ctx.respond(embed=stockembed)
    

@bot.slash_command(guild_ids=[903618670700417065])
async def portfolio(ctx, symbol: str):
    
    

    
    await ctx.respond()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.run(os.environ.get('token'))

