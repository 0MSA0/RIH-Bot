from typing import Optional

import discord
import datetime
import json
from discord.ext import commands, tasks
from random import choice
from config import BD_CHANNEL_ID, GUILD_ID

JSON_FILE = "calendar.json"


def get_position_of_sharp(text: str) -> int:
    for i, x in enumerate(text):
        if x == '#':
            return i
    return -1


def read_json() -> dict:
    """
        Reads JSON file and saves everything into a dictionary
    """
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        calendar = json.load(f)
    print("Succesfully copied JSON into dict.")
    return calendar


class Birthday(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot:commands.Bot = bot
        self.bd_channel_id:int = BD_CHANNEL_ID
        self.calendar:dict = read_json()
        self.bd_check_task.start()

    def add_to_json(self):
        """
        Writes all changes in calendar-dictionary to JSON file
        """
        with open(JSON_FILE, 'w', encoding='UTF8') as jf:
            json.dump(self.calendar, jf, indent=2)


    @tasks.loop(time=datetime.time.min)
    async def bd_check_task(self):
        await self.bot.wait_until_ready()
        # Get channel & server
        message_channel = self.bot.get_channel(self.bd_channel_id)
        server = self.bot.get_guild(GUILD_ID)
        # Get current date
        current_date = datetime.datetime.now()
        day = current_date.strftime("%d").strip("0")
        month = current_date.strftime("%m")
        if month != "10":
            month = month.strip("0")
        current_date = day + "." + month
        # query the dict
        bdkinder = self.calendar[current_date]
        if current_date == "1.4":
            # Aprils fool
            ncal = [self.calendar[bdkind] for bdkind in self.calendar if (self.calendar[bdkind] != [])]
            rdm_kid = choice(ncal)
            bdkinder += rdm_kid
        if bdkinder != []:
            bdtext = ""
            for person in bdkinder:
                sharp = get_position_of_sharp(person)
                if sharp != -1:
                    # Old naming system compatability
                    personname = person[:sharp]
                    persondiscriminator = person[sharp + 1:]
                    user_id = discord.utils.get(self.bot.get_all_members(),
                                                                name=personname,
                                                                discriminator=persondiscriminator)
                else:
                    # new naming system
                    user_id = server.get_member_named(person)
                if (person == "doribumi"):
                    bdtext += "%s lemao congrats lelul\n" % (user_id.mention)
                else:
                    bdtext += "Happy Birthday %s. @everyone" % (user_id.mention)
                    bdtext += ":partying_face: :partying_face: \n"
            await message_channel.send(bdtext)

    @commands.command()
    async def add(self, ctx, username: Optional[str], date: Optional[str]):
        """
        Adds a Birthday and Person to database.
        Usage: !add Muster 01.01
        Zeroes must be written out!
        """
        if (username is None or date is None):
            output_str = "Failed to add person. Usage: `!add Muster 01.01`"
        else:
            if (len(date) != 5 or len(username) == 0 or date[2] != '.'):
                output_str = "Failed to add person. Usage: `!add Muster 01.01`"
            else:
                try:
                    int(date[0:2])
                    int(date[3:5])
                except ValueError:
                    output_str = "Please enter a valid date!"
                else:
                    # formatting date-string so it fits the dict
                    month = str(int(date[3:5]))
                    day = str(int(date[:2]))
                    date = day + "."
                    date += month
                    # add user to dict

                    sharp = get_position_of_sharp(username)
                    if sharp != -1:

                        personname = username[:sharp]
                        persondiscriminator = username[sharp + 1:]

                        user_id = discord.utils.get(self.bot.get_all_members(),
                                                    name=personname,
                                                    discriminator=persondiscriminator)
                    else:
                        user_id = discord.utils.get(self.bot.get_all_members(),
                                                    global_name=username)
                    if user_id is not None:

                        if len(self.calendar[date]) > 0:
                            self.calendar[date] += [username]
                        else:
                            self.calendar[date] = [username]
                        self.add_to_json()
                        output_str = "%s successfully added to database." % (username)
                    else:
                        output_str = "User not found. Check for typos."
        await ctx.send(output_str)

    @commands.command()
    async def listbd(self, ctx):
        """
            Lists and prints out all birthdays stored in the database
            """
        output = ""
        for pair in self.calendar.items():
            if pair[1] != ['']:
                for value in pair[1]:
                    output += "%s: %s\n" % (pair[0], value)
            else:
                continue
        await ctx.send(output)


async def setup(bot):
    await bot.add_cog(Birthday(bot))
