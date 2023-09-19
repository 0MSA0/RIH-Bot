import asyncio
import os
import discord
import logging

from config import TOKEN
from discord import app_commands
from discord.ext import commands

# Logger setup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot setup

description = '"Bot straight outa hell"'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                   description=description,
                   intents=intents)
#tree = app_commands.CommandTree(bot)


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load_cogs()
    await bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
