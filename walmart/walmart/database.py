import sqlite3

conn = sqlite3.connect('something.db')
curr = conn.cursor()

curr.execute("""insert into """)