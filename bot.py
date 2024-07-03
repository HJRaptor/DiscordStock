import discord
from discord import member
import yfinance

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

    stockembed = discord.Embed(title=name,color=discord.Colour.blurple())
    stockembed.add_field(name="Market Open",value=regular_market_open)
    stockembed.add_field(name="Day Low", value=daylow)
    stockembed.add_field(name="Day Low", value=dayhigh)
    stockembed.set_footer(text="HJRaptor - 2024")
    stockembed.ad

    
    await ctx.respond(embed=stockembed)
    

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.run("MTI1ODE2MjcxNzY3MjYwNzg5Ng.GERP2P.Ul9xs7hwQ62nsokNt0DMBWdjEWRHVyc0GIL6yo")

