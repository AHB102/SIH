import sqlite3

def getScript_sql(key):
    with sqlite3.connect("Script_sql.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT script FROM scripts WHERE key = :key", {"key": key})
        row = cursor.fetchone()
        if row:
            script = str(row[0])
            return str(script)
        else:
            # Handle the case where no row is found
            print("No script found for key", key)