import discord
from discord import member
import yfinance
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import date, timedelta
from matplotlib import pyplot as plt
import sqlite3


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

async def updatestockprices(userid):
    mydb = sqlite3.connect("data.db")
    cursor = mydb.cursor()


async def purchase(userid,ticker,quantity):
    mydb = sqlite3.connect("data.db")
    cursor = mydb.cursor()
    stock = yfinance.Ticker(ticker)
    stockvalue = stock.info['regularMarketOpen']
    
    existing = await stockexists(user_id=userid,symbol=ticker)
    if existing:
        
        cursor.execute('''SELECT Balance FROM Portfolio WHERE userid=?''', (userid,))
        currentbalance = cursor.fetchall()
        currentbalance = currentbalance[0][0]


        cursor.execute('''SELECT quantity FROM Stocks WHERE userid=? AND ticker=?''', (userid,ticker,))
        currentquantity = cursor.fetchall()
        currentquantity = currentquantity[0][0]
        newquantity = quantity + currentquantity
        cursor.execute('''UPDATE Stocks SET quantity=? ,price=? WHERE userid=? AND ticker=?''',(newquantity,stockvalue,userid,ticker,))

        remainingbalance = currentbalance-(stockvalue*quantity)
        cursor.execute('''UPDATE Portfolio SET Balance=? WHERE userid=?''',(remainingbalance,userid,))
        mydb.commit()
        mydb.close()
        print("done")

    else:
        
        cursor.execute('''SELECT Balance FROM Portfolio WHERE userid=?''', (userid,))
        currentbalance = cursor.fetchall()
        currentbalance = currentbalance[0][0]

        remainingbalance = currentbalance-(stockvalue*quantity)
        cursor.execute('''INSERT INTO Stocks VALUES(?,?,?,?)''',(userid,ticker,quantity,stockvalue,))
        cursor.execute('''UPDATE Portfolio SET Balance=? WHERE userid=?''',(remainingbalance,userid,))
        mydb.commit()
        mydb.close()
        print("dones")


async def stockexists(user_id, symbol):
    mydb = sqlite3.connect("data.db")
    cursor = mydb.cursor()
    cursor.execute('''SELECT * FROM Stocks WHERE userid=? AND ticker=?''', (user_id, symbol))
    existing_stock = cursor.fetchone()
    cursor.close()
    return existing_stock


@bot.slash_command(guild_ids=[903618670700417065])
async def info(ctx, symbol: str):
    selectedStock = yfinance.Ticker(symbol)

    #values
    name = selectedStock.info['shortName']
    regular_market_open = selectedStock.info['regularMarketOpen']
    daylow = selectedStock.info['dayLow']
    dayhigh = selectedStock.info['dayHigh']
    divYield = selectedStock.info.get('dividendYield',None)
    newsFinance = selectedStock.news
    #graphing
    result = pd.DataFrame(yfinance.download(symbol, start=start,end=end)['Open'])     
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
    stockembed.add_field(name="Day High", value=dayhigh)
    if divYield != None:
        divYield = float(divYield)*100
        divYield = round(divYield,2)
        stockembed.add_field(name="Annual Dividend Yield", value=str(divYield)+"%")
    stockembed.set_image(url="attachment://graph.png")
    stockembed.set_footer(text="HJRaptor - 2024")

    for news in newsFinance[:2]:
        title = news['title']
        publisher = news['publisher']
        link = news['link']
        stockembed.add_field(name=title, value=f"Publisher: {publisher}\n[Read More]({link})", inline=False)


    await ctx.respond(embed=stockembed, file=image)
    

@bot.slash_command(guild_ids=[903618670700417065])
async def portfolio(ctx):
    userid = str(ctx.author.id)
    print(userid)
    mydb = sqlite3.connect("data.db")
    cursor = mydb.cursor()
    cursor.execute('''SELECT Balance FROM Portfolio WHERE userid=?''', (userid,))
    balance = cursor.fetchall()
    balance = balance[0][0]
    mydb.close()
    

    
    await ctx.respond("$" + str(round(balance,2)))

@bot.slash_command(guild_ids=[903618670700417065])
async def buy(ctx, symbol: str, quantity: str):
    locuserid = str(ctx.author.id)
    

    

    await purchase(locuserid,symbol,int(quantity))
    await ctx.respond("Purchase complete")
    

@bot.slash_command(guild_ids=[903618670700417065])
async def login(ctx):
    userid = ctx.author.id
    print(userid)
    mydb = sqlite3.connect("data.db")
    cursor = mydb.cursor()
    cursor.execute('''INSERT INTO Portfolio VALUES(?)''',(userid))


    

    
    await ctx.respond("Logged in")




@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.run(os.environ.get('token'))

