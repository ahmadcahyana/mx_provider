import sqlite3


con = sqlite3.connect("providers.db")
con.execute("CREATE TABLE IF NOT EXISTS providers (domain TEXT, mx TEXT, provider TEXT)")
