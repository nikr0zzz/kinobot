import sqlite3
#cursor.execute("""CREATE TABLE favour_films(id integer, film text)""")
conn = sqlite3.connect("kinobot.db")
cursor = conn.cursor()
