import discord
import datetime
import json
import sqlite3
from sqlite3 import Error

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


def get_birthday_kid() -> list[str]:
    conn: sqlite3.Connection = create_connection(DATABASE_FILE)
    cur: sqlite3.Cursor = conn.cursor()
    date = "12-31"
    query: str = "SELECT discord_name, birthday FROM person WHERE birthday LIKE '____-%s'" % date
    cur.execute(query)
    rows: list[str] = cur.fetchall()
    if date == "03-05":
        query = "SELECT discord_name, birthday FROM person ORDER BY random() LIMIT 1;"
        cur.execute(query)
        rows += [cur.fetchone()]
    return rows


def get_current_day() -> str:
    date: datetime.date = datetime.date.today()
    return date.strftime("%m-%d")


def read_json() -> dict:
    """
    Reads JSON file and saves everything into a dictionary
    """
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        calendar = json.load(f)
    print("Succesfully copied JSON into dict.")
    return calendar


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


def bd_check_task():
    # Get channel & server

    # Get current date

    bdkinder: list[str] = get_birthday_kid()
    if bdkinder != []:
        bdtext = ""
        for person, birthday in bdkinder:
            age = calc_age(datetime.date.fromisoformat(birthday))

            if person == "doribumi":
                for i in range(int(age[:-2])):
                    bdtext += "%s lemao congrats lelul\n" % person
            else:

                bdtext += "Happy %s Birthday  %s. @everyone" % (age, person)
                bdtext += ":partying_face: :partying_face: \n"
        print(bdtext)


def listbd():
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
    print(output)


if __name__ == '__main__':
    listbd()
