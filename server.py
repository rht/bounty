import sqlite3
from flask import Flask, request, render_template
from geopy import distance, Point

app = Flask(__name__)

def nearestbounty(hunterlat,hunterlng):
    hunterlocation = Point(''.join([str(hunterlat),";",str(hunterlng)]))
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''select * from requests''')
    requestslist = c.fetchall()
    distancelist = []
    for row in requestslist:
        #row: id, descript, status, food, request, uid
        #     0      1        2       3     4       5
        if row[2] == 1:
            #foodlat, foodlng = c.execute('''select lat,long from locations where id=? ''',(row[3],))
            c.execute('''select lat,long from locations where id=? ''',(row[3],))
            foodlat, foodlng = c.fetchone()
            foodloc = Point(''.join( [str(foodlat),";",str(foodlng)] ))
            distancelist.append([get_username(int(row[5])),row[1],distance.distance(hunterlocation,foodloc).miles])
    return sorted(distancelist,key=lambda x: x[2])

@app.route('/')
def index():
    uid = 500
    conn = sqlite3.connect('data.db').cursor()
    c.execute('select name from user where id='+uid)
    name =  c.fetchone[0]

    #or simply with json
    #users = json.load(open('user.json'))
    #name = users[str(uid)]

    return render_template('templates/index.html',username=name)


@app.route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return str(result)

@app.route('/get')
def display_forum():
    forum_id = request.args['id']
    page = request.args['page', '1']
    return render_template('templates/hello_template.html', username=forum_id)

@app.route('/dump_requests')
def todo_list():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM requests ")
    result = c.fetchall()
    return str(result)

@app.route('/submit_location')
def submit_location():
    start_lat = request.args['start_lat']
    start_long = request.args['start_long']
    end_lat = request.args['end_lat']
    end_long = request.args['end_long']
    return str(start_lat) + '   ' + str(start_long) +'   '+ str(end_lat) + '   ' + str(end_long) 

@app.route('submit')
def submit():
    start_lat = float(request.args['start_lat'])
    start_long = float(request.args['start_long'])
    end_lat = float(request.args['end_lat'])
    end_long = float(request.args['end_long'])
    description = request.args['description']
    username = request.args['username']

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('insert into user values (null,%s)'%username)
    conn.commit()
    c.execute('select id from "user" where name=%s'%username)
    u_id=c.fetchone()[0]
    c = conn.cursor()
    c.execute('insert into locations values (null,?,?,?)',(end_lat,end_long,""))
    conn.commit()
    c.execute('select id from "locations" where lat=? and long=? ',(end_lat,end_long))
    f_id=c.fetchone()[0]
    c.execute('insert into locations values (null,?,?,?)',(start_lat,start_long,""))
    conn.commit()
    c.execute('select id from "locations" where lat=? and long=? ',(start_lat,start_long))
    e_id=c.fetchone()[0]
    c.execute('insert into requests values (null,?,1,?,?,?)',(description,f_id,e_id,u_id))
    conn.commit()

    return "successfully updated"

@app.route('/hello/:name')
def hello(name):
    return render_template('templates/hello_template.html',username=name)

@app.route('/:name')
def hello(name):
    return render_template(name)

@app.route('tasks')
def tasks():
    string = ''
    lat = request.args['lat']
    lng = request.args['lng']
    data = nearestbounty(20,20)

    for entry in data:
        string += template('task.tpl',username=entry[0],description=entry[1])
    return string
