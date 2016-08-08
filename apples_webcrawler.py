# coding=utf-8
import requests, bs4
import pprint
import sqlite3
import time

res = requests.get('http://www.sadbiznes.pl/notowania-jablek/7')
text = bs4.BeautifulSoup(res.text, "html.parser")

def get_column_data(data_selector, class_value_selector):
    results=[]
    for i in text.find_all(data_selector, class_=class_value_selector):
        results.append(i.string.strip())
    return results


def pivot_data(col_dict, timestamp=time.time()):
  output = []

  first_key_name = col_dict.keys()[0]
  values_column_len = len(col_dict[first_key_name])
  print("values_column_len: " + str(values_column_len))

  for value_no in range(values_column_len):
    row_data = {}
    for key in col_dict.keys():
      row_data[key] = col_dict[key][value_no]
    row_data['timestamp'] = int(timestamp)
    output.append(row_data)

  # print(str(output))

  return output

selector_info = {
    "for_day":["td", "views-field views-field-changed"],
    "name": ["td", "views-field views-field-tid-3"],
    "note_day": ["span", "date-display-single"],
    "city": ["td", "views-field views-field-tid"],
    "price_min": ["td", "views-field views-field-field-cena-min-value"],
    "price_max": ["td", "views-field views-field-field-cena-max-value"]
}

col_dict = {}

for key_name, (selector_first, selector_second) in selector_info.iteritems():
    col_dict[key_name] = get_column_data(selector_first, selector_second)

# pprint.pprint(col_dict)

assert len(col_dict['for_day']) == len(col_dict['name']) == len(col_dict['note_day']) \
       == len(col_dict['city']) == len(col_dict['price_min']) == len(col_dict['price_max'])


conn = sqlite3.connect('apples_webcrawler.db')
cursor = conn.cursor()

# cursor.execute("drop table note")
# cursor.execute("create table note (for_day, name, note_day, city, price_min, price_max, timestamp)")

pivoted_data = pivot_data(col_dict)

for values in pivoted_data:
  # pprint.pprint(values)
  res = cursor.execute('INSERT INTO note (for_day, name, note_day, city, price_min, price_max, timestamp) ' +
                       'VALUES (:for_day, :name, :note_day, :city, :price_min, :price_max, :timestamp)', values)
  conn.commit()


results = cursor.execute("select for_day, name, note_day, city, price_min, price_max, timestamp from note")
print(str(results.fetchall()))

conn.close()