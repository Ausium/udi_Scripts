#! /usr/bin/python3

import flask
import sqlite3
from datetime import datetime

server = flask.Flask(__name__)

@server.route("/", methods=['GET', 'POST'])
def location():
    with sqlite3.connect('./udi.db') as conn:
        cursor = conn.cursor()
        arg = flask.request.args.get('type')
        if flask.request.method == 'POST':
            data = flask.request.json.get("IP")
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if arg == 'udi01':
                SQL = 'insert into udi01(DATE, IP) values("%s", "%s")' %(today, data)
                cursor.execute(SQL)
                conn.commit()
            elif arg == 'udi02':
                SQL = 'insert into udi02(DATE, IP) values("%s", "%s")' %(today, data)
                cursor.execute(SQL)
                conn.commit()
            else:
                try:
                    data = flask.request.headers['X-Real-Ip']
                except KeyError:
                    date = flask.request.remote_addr
            print(data, arg)
            return data
        if arg == 'udi01':
            SQL = 'select IP from udi01 order by id desc limit 1'
            cursor.execute(SQL)
            res = cursor.fetchone()
            ip = res[0]
        elif arg == 'udi02':
            SQL = 'select IP from udi02 order by id desc limit 1'
            cursor.execute(SQL)
            res = cursor.fetchone()
            ip = res[0]
        else:
            try:
                ip = flask.request.headers['X-Real-Ip']
            except KeyError:
                ip = flask.request.remote_addr
    print(ip)
    return ip

server.config['JSON_AS_ASCII'] = False
server.run(host='0.0.0.0', port=8888, debug=True, threaded=True)
