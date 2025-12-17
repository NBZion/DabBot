import discord
import os
from discord.ext import commands, pages
from discord.commands import Option
import requests
from requests.auth import HTTPBasicAuth
import dotenv


dotenv.load_dotenv()

## Temp Variable for Whitelisted Servers
endpoint = "https://dab.yeet.su/api"
whitelistedServers = os.getenv("WHITELISTED_SERVER")

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=whitelistedServers, description="Searches DAB Servers For The Song You Want")
    async def search_song(self, ctx, songname: str):
        # Initialize Session
        session = requests.Session()
        # Login
        payload = {"email": os.getenv("EMAIL"), "password": os.getenv("PASSWORD")}
        try:
            loginResponse = session.post(endpoint+"/auth/login",json=payload)
        except Exception as e:
            await ctx.respond(f"Connection Failed: {e}")
            return 
        
        if loginResponse.status_code != 200:
            await ctx.respond("Login Failed: Error " + loginResponse.status_code)
            return

        


        # Search File
        searchResponse = session.get(endpoint + f"/search?q={songname}&offset=0&type=track")
        if searchResponse.status_code == 200:
            await ctx.respond(searchResponse.content)
        else:
            await ctx.respond(searchResponse.status_code)
        


def setup(bot):
    bot.add_cog(music(bot))