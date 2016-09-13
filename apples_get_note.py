# -*- coding: utf-8 -*-
import json
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, _app_ctx_stack, Response
# from flasgger import Swagger



app = Flask(__name__)
# Swagger(app)

QUERY = 'select name, city, round(avg(price_min),2) as price_min, round(avg(price_max),2) as price_max ' \
        'from note where timestamp in (select timestamp from note group by timestamp ' \
        'order by timestamp desc limit 50) group by name, city'


@app.route('/')
def data():
    return _get_all_data(False)


@app.route('/api/apples')
def data_api():
    return _get_all_data(True)


def _get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('apples_webcrawler.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db


def _get_all_data(as_json=False, tpl='table_all.html'):
    db = _get_db()
    cur = db.execute(QUERY)
    result1 = cur.fetchall()
    if not as_json:
        res = render_template(tpl, rows1=result1)
    else:
        try:
            keys = result1[0].keys()
        except KeyError:
            keys = []

        rows_as_dicts = []
        for r in result1:
            d = {}
            for key in keys:
                d[key] = r[key]
            rows_as_dicts.append(d)

        dat = json.dumps(rows_as_dicts)
        res = Response(response=dat, status=200,
                       mimetype="application/json")
    return res

if __name__ == "__main__":
    app.run(debug=True)


