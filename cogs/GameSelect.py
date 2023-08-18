
import discord
import json
from discord.ext import commands, tasks

JSON_FILE = "gamelist.json"


def read_json() -> dict:
    """
        Reads JSON file and saves everything into a dictionary
    """
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
    print("Succesfully copied JSON into dict.")
    return json_dict


class GameSelect(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.gamelist = read_json()
