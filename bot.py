import discord
from discord import member
import yfinance
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import date, timedelta
from matplotlib import pyplot as plt


load_dotenv()

#intents
intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = discord.Bot(intents=intents)


#time period for graphs
start = date.today() - timedelta(365)
start.strftime('%Y-%m-%d')

end = date.today() + timedelta(2)
end.strftime('%Y-%m-%d')


@bot.slash_command(guild_ids=[903618670700417065])
async def info(ctx, symbol: str):
    selectedStock = yfinance.Ticker(symbol)

    #values
    name = selectedStock.info['shortName']
    regular_market_open = selectedStock.info['regularMarketOpen']
    daylow = selectedStock.info['dayLow']
    dayhigh = selectedStock.info['dayHigh']

    if selectedStock.info['dividendYield'] in selectedStock.info:
        divYield = float(selectedStock.info['dividendYield'])*100
    else:
        divYield = None

    #graphing
    result = pd.DataFrame(yfinance.download(symbol, start=start,end=end)['Adj Close'])     
    plt.plot(result)
    plt.ylabel('Price ($)')
    plt.xlabel('Date')
    
    graphImage = "graph.png"
    plt.savefig(graphImage)
    image = discord.File(graphImage)

    
    #constructing the embed
    stockembed = discord.Embed(title=name,color=discord.Colour.blurple())
    stockembed.add_field(name="Market Open",value=regular_market_open)
    stockembed.add_field(name="Day Low", value=daylow)
    stockembed.add_field(name="Day Low", value=dayhigh)
    if divYield != None:
        stockembed.add_field(name="Annual Dividend Yield", value=str(divYield)+"%")
    stockembed.set_image(url="attachment://graph.png")
    stockembed.set_footer(text="HJRaptor - 2024")
    
    
    await ctx.respond(embed=stockembed, file=image)
    

@bot.slash_command(guild_ids=[903618670700417065])
async def portfolio(ctx, symbol: str):
    
    

    
    await ctx.respond()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.run(os.environ.get('token'))

