
import discord
import json
from discord.ext import commands

# TODO: Use a database
JSON_FILE = "gamelist.json"


def read_json() -> list[str]:
    """
        Reads JSON file and saves everything into a list
    """
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
    print("Succesfully copied JSON into a list.")
    return json_dict


class GameSelect(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.gamelist: list[str] = read_json()


async def setup(bot: commands.Bot):
    await bot.add_cog(GameSelect(bot))
