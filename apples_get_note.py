# -*- coding: utf-8 -*-

import json
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, _app_ctx_stack, Response


app = Flask(__name__)


def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('apples_webcrawler.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db



@app.route('/')
def data():
    db = get_db()
    cur = db.execute("select name, city, round(avg(price_min),2) as price_min, round(avg(price_max),2) as price_max "
                     "from note where timestamp in (select timestamp from note group by timestamp "
                     "order by timestamp desc limit 50) group by name, city")
    result1 = cur.fetchall()
    return render_template('table_all.html', rows1=result1)


@app.route('/api/apples')
def data_api():
    db = get_db()
    cur = db.execute("select name, city, round(avg(price_min),2) as price_min, round(avg(price_max),2) as price_max "
                     "from note where timestamp in (select timestamp from note group by timestamp "
                     "order by timestamp desc limit 50) group by name, city")
    result1 = cur.fetchall()

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
    resp = Response(response=dat,
                    status=200, \
                    mimetype="application/json")
    return resp
