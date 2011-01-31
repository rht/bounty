import sqlite3
import os,sys
from bottle import route, run, view, template
from bottle import request, response
from db import insert_table

@route('/')
def index():
    return template('index.tpl')


@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return str(result)

@route('/get')
@view('hello_template')
def display_forum():
    forum_id = request.GET.get('id')
    page = request.GET.get('page', '1')
    #return 'Forum ID: %s (page %s)' % (forum_id, page)
    return dict(username=forum_id)

@route('/dump_requests')
def todo_list():
    conn = sqlite3.connect('hack.db')
    c = conn.cursor()
    c.execute("SELECT * FROM requests ")
    result = c.fetchall()
    return str(result)

@route('/submit_location')
def submit_location():
    start_lat = request.GET.get('start_lat')
    start_long = request.GET.get('start_long')
    end_lat = request.GET.get('end_lat')
    end_long = request.GET.get('end_long')
    return str(start_lat) + '   ' + str(start_long) +'   '+ str(end_lat) + '   ' + str(end_long) 

@route('submit')
def submit():
    uid = 500
    start_lat = request.GET.get('start_lat')
    start_long = request.GET.get('start_long')
    end_lat = request.GET.get('end_lat')
    end_long = request.GET.get('end_long')
    description = request.GET.get('description')
    insert_table(float(end_lat),float(end_long),float(start_lat),float(start_long),description,uid)
    return "successfully updated"



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

@route('/hello/:name')
@view('hello_template')
def hello(name):
    return dict(username=name)

@route('/:name')
def hello(name):
    return template(name)

    



run()
