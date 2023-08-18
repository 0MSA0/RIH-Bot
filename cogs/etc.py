import json
import requests
from typing import Optional
from discord.ext import commands


def get_joke(typ: Optional[str]) -> str:
    """
    Gets a random joke from a API
    """
    if (typ is None):
        response = requests.get("https://jokes-and-quotes-api.herokuapp.com/jokes/random")
    elif (typ == "general"):
        response = requests.get("https://jokes-and-quotes-api.herokuapp.com/jokes/general/random")
    elif (typ == "programming"):
        response = requests.get("https://jokes-and-quotes-api.herokuapp.com/jokes/programming/random")
    elif (typ == "knock-knock"):
        response = requests.get("https://jokes-and-quotes-api.herokuapp.com/jokes/knock-knock/random")
    else:
        response = requests.get("https://jokes-and-quotes-api.herokuapp.com/jokes/random")

    json_data = json.loads(response.text)
    joke = json_data['setup'] + '\n' + json_data['punchline']
    return joke


class ETC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")

    @commands.command(aliases=["sh"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        print("Bot shutting down...")
        await self.bot.close()

    @commands.command()
    async def hello(self, ctx):
        """
        Says hello there
        """
        await ctx.send('Hello there.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Schlong")

    @commands.command()
    async def joke(self, ctx, typ: Optional[str]):
        """
        Prints a random joke from https://jokes-and-quotes-api.herokuapp.com.
        There are three types of jokes:
        1. general (g)
        2. programming (p)
        3. knock knock (k)
        """
        """if type(typ) is str:
            if (typ == "general" or typ == "g"):
                joke = get_joke("general")
            elif (typ == "programming" or typ == "p"):
                joke = get_joke("programming")
            elif (typ == "knock knock" or typ == "k"):
                joke = get_joke("knock-knock")
            else:
                joke = get_joke(None)
        else:
            joke = get_joke(None)
        """
        await ctx.send("Cullently no workin sowwy UwU")


async def setup(bot: commands.Bot):
    await bot.add_cog(ETC(bot))
