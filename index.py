import sqlite3
import os,sys
from bottle import route, run
from bottle import request, response

@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return str(result)

@route('/get')
def display_forum():
    forum_id = request.GET.get('id')
    page = request.GET.get('page', '1')
    return 'Forum ID: %s (page %s)' % (forum_id, page)

@route('/dump_requests')
def todo_list():
    conn = sqlite3.connect('hack.db')
    c = conn.cursor()
    c.execute("SELECT * FROM requests ")
    result = c.fetchall()
    return str(result)


@route('ls')
def ls():
    f = os.popen("ls")
    return f.read()


@route('php')
def ls():
    f = os.popen("php test.php")
    return f.read()


@route('phpdb')
def ls():
    f = os.popen("php db.php")
    return f.read()





run()
