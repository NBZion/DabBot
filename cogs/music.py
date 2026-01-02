import discord
import os
from discord.ext import commands
from discord.ext.pages import Paginator, Page 
from discord.commands import Option
import requests
import json
import dotenv


dotenv.load_dotenv()

endpoint = "https://dab.yeet.su/api"
fileHostEndpoint = "https://0x0.st"

class DabSessionHandler():
    def __init__(self):
        self.session = requests.Session()
        self.logged = False


    def login(self, email, password):
        loginResponse = None
        if self.logged == False:
            try:
                loginResponse = self.session.post(endpoint+"/auth/login",json={"email": email, "password":password})
            except Exception as e:
                return "An Error Has Occured: {e}"
            
            if loginResponse.status_code != 200:
                print("Failed To Login - Error " + str(loginResponse.status_code))
                return loginResponse.status_code
            else:
                self.logged = True
                return 200
        else: 
            print("Already Logged In!")
            return
        
    
    def search(self, name: str, album: bool):
        searchResponse = None
        
        if album:
            # Album
            searchResponse = self.session.get(endpoint + f"/search?q={name}&offset=0&type=album")
        else:
            # Regular Song/Track
            searchResponse = self.session.get(endpoint + f"/search?q={name}&offset=0&type=track")
        
        if searchResponse.status_code == 200:
            if album:   return json.loads(searchResponse.content)['albums'] 
            else:   return json.loads(searchResponse.content)['tracks']
        else:
            return searchResponse.status_code
        
    def getStreamLink(self, id: str):
        streamResponse = self.session.get(endpoint + f"/stream?trackId={id}")

        if streamResponse.status_code == 200:
            return json.loads(streamResponse.content)['url']
        else:
            return f"Error: {streamResponse.status_code}"
        


## Temp Variable for Whitelisted Servers

whitelistedServers = os.getenv("WHITELISTED_SERVER")

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot      
        self.session_handler = DabSessionHandler()
        self.logged = False

    @commands.slash_command(guild_ids={whitelistedServers}, description="Searches DAB Servers For The Song You Want")
    async def search_song(self, ctx, songname: str):
       
        # Login
        if self.logged == False:
            self.session_handler.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
       
        tracks = self.session_handler.search(songname, False)
        trackPages = []
        
        for track in tracks:
            trackEmbed = discord.Embed(
                title=track["artist"] +  " - "  + track["title"],
            )
            trackEmbed.add_field(name="Album", value=track["albumTitle"])
            trackEmbed.add_field(name="ID", value=track["id"])
            trackEmbed.set_image(url=track["albumCover"])
            
            trackPages.append(Page(
                embeds=[trackEmbed]
            ))
    
        paginator = Paginator(trackPages)
        await paginator.respond(ctx.interaction, ephemeral=False)
    
    @commands.slash_command(guild_ids={whitelistedServers}, description="Provides a Download Link to A Song")
    async def download_song(self, ctx, id: str):
        # Login
        if self.logged == False:
            self.session_handler.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))

        streamLink = self.session_handler.getStreamLink(id)

        if "Error" in streamLink:
            print(streamLink)
            await ctx.respond(streamLink)
            return

        await ctx.respond(f"[Here]({streamLink}) is your requested song!")

        # Due to the Nature of The Project, Put Here to Test an API :)
        #fileUrl = requests.post(fileHostEndpoint, data={'url':streamLink, 'expires':1},headers={"User-Agent": "DabBot/1.0" })
        #print(fileUrl.content)
        


        




       
        


def setup(bot):
    bot.add_cog(music(bot))