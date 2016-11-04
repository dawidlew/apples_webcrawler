# coding=utf-8
import time
import sqlite3

conn = sqlite3.connect('apples_webcrawler.db')
cursor = conn.cursor()
timestamp = int(time.time())
print timestamp

# cursor.execute("drop table note_agg")
# cursor.execute("create table note_agg (name, city, avg_price_min, avg_price_max, timestamp)")

avg_price = cursor.execute("select DISTINCT name, city, round(avg(replace(price_min, ',', '.')),2), "
                           "round(avg(replace(price_max, ',', '.')),2), strftime('%s','now') from note "
                           "where for_day in (select DISTINCT for_day from note order by for_day desc limit 10) "
                           "group by name, city")
avg_price_data = avg_price.fetchall()

# print avg_price_data[1]
# print avg_price_data[1][0]

stmt = "insert into note_agg(name, city, avg_price_min, avg_price_max, timestamp) VALUES(?, ?, ?, ?, ?)"
cursor.executemany(stmt, avg_price_data)
conn.commit()


results = cursor.execute("select name, city, avg_price_min, avg_price_max, timestamp from note_agg")
print(str(results.fetchall()))

cursor.close()
