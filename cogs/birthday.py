import discord
import datetime
import json
import sqlite3
from sqlite3 import Error
from typing import Optional
from discord.ext import commands, tasks
from config import BD_CHANNEL_ID, GUILD_ID

DATABASE_FILE = "./data/RIH-SQLiteDB/RIH-SQLiteDB"


def get_position_of_sharp(text: str) -> int:
    for i, x in enumerate(text):
        if x == '#':
            return i
    return -1


def create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def get_birthday_kids() -> list[str]:
    conn: sqlite3.Connection = create_connection(DATABASE_FILE)
    cur: sqlite3.Cursor = conn.cursor()
    date: str = get_current_day()

    query: str = "SELECT discord_name, birthday FROM person WHERE birthday LIKE '____-%s'" % date
    cur.execute(query)
    rows: list[str] = cur.fetchall()
    if date == "04-01":
        query = "SELECT discord_name FROM person ORDER BY random() LIMIT 1;"
        cur.execute(query)
        rows += cur.fetchone()
    return rows


def get_current_day() -> str:
    date: datetime.date = datetime.date.today()
    return date.strftime("%m-%d")


def calc_age(birthday: datetime.date) -> str:
    age = datetime.date.today().year - birthday.year
    match (age % 10):
        case 1:
            return "%dst" % age
        case 2:
            return "%dnd" % age
        case 3:
            return "%drd" % age
        case _:
            return "%dth" % age


class Birthday(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.bd_channel_id: int = BD_CHANNEL_ID
        self.bd_check_task.start()

    @tasks.loop(hours=24)
    async def bd_check_task(self):
        await self.bot.wait_until_ready()
        # Get channel & server
        message_channel = self.bot.get_channel(self.bd_channel_id)
        server = self.bot.get_guild(GUILD_ID)
        # Get birthday kiddos
        bdkinder: list[str] = get_birthday_kids()
        if bdkinder != []:
            bdtext = ""
            for person, birthday in bdkinder:
                sharp = get_position_of_sharp(person)
                age = calc_age(datetime.date.fromisoformat(birthday))
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
                if person == "doribumi":
                    for i in range(int(age[:-2])):
                        bdtext += "%s lemao congrats lelul\n" % user_id.mention
                else:
                    bdtext += "Happy %s Birthday %s. @everyone" % (age, user_id.mention)
                    bdtext += ":partying_face: :partying_face: \n"
            await message_channel.send(bdtext)

    @commands.command()
    async def listbd(self, ctx: discord.ext.commands.Context):
        """
        Lists and prints out all birthdays stored in the database
        """
        special_format_months = ["March", "June", "April", "July", "August", "May"]
        output = ""
        conn = create_connection(DATABASE_FILE)
        cursor = conn.cursor()
        query = "SELECT person_name, birthday FROM person ORDER BY substr(birthday, 6, 5)"
        cursor.execute(query)
        rows = cursor.fetchall()
        for person, date in rows:
            if date != "YYYY-MM-DD":
                date = datetime.date.fromisoformat(date)
                day = date.strftime("%d")
                day = day.lstrip('0').rjust(len(day))
                month = date.strftime("%B")
                output += "%s. %s " % (day, month)
                if month in special_format_months:
                    output += "\t"
                output += "\t %s\n" % person
        await ctx.send(output)


async def setup(bot: commands.Bot):
    await bot.add_cog(Birthday(bot))
