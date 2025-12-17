import discord
from discord.ext import commands
import os
import dotenv

## Load DotENV
dotenv.load_dotenv()

intents=discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="dab!",intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")


if __name__ == "__main__":
    for cog in os.listdir("./cogs"):
        if cog != "__pycache__":
            bot.load_extension(f'cogs.{cog[:-3]}')
            print("Loaded " + cog)
    
    bot.run(os.getenv("TOKEN"))