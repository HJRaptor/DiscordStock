import discord
from discord import Member

msft = yf.Ticker("MSFT")

print(msft.info)


#intents
intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = discord.Bot(intents=intents)

#@bot.slash_command(guild_ids=[903618670700417065])
#async def start(ctx):
    



