import sqlite3
from geopy import distance, Point


def get_username(id):
    conn = sqlite3.connect('hack.db')
    c = conn.cursor()
    c.execute("""select name from user where id=?""",(id,))
    a=c.fetchone()
    name = a[0]
    return name
    

def insert_table(f_lat, f_long, e_lat, e_long,description,username):
    conn = sqlite3.connect('hack.db')
    c = conn.cursor()
    c.execute("""insert into user values (null,?)""",(username,))
    conn.commit()
    c.execute("""select id from 'user' where name=? """,(username,))
    a=c.fetchone()
    u_id = a[0]
    c = conn.cursor()
    c.execute("""insert into locations values (null,?,?,?)""",(f_lat,f_long,""))
    conn.commit()
    c.execute("""select id from 'locations' where lat=? and long=? """,(f_lat,f_long))
    a=c.fetchone()
    f_id = a[0]
    c.execute("""insert into locations values (null,?,?,?)""",(e_lat,e_long,""))
    conn.commit()
    c.execute("""select id from 'locations' where lat=? and long=? """,(e_lat,e_long))
    a=c.fetchone()
    e_id = a[0]
    c.execute("""insert into requests values (null,?,1,?,?,?)""",(description,f_id,e_id,u_id))
    conn.commit()

def nearestbounty(hunterlat,hunterlng):
    hunterlocation = Point(''.join([str(hunterlat),";",str(hunterlng)]))
    conn = sqlite3.connect('hack.db')
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
            a = c.fetchone()
            foodlat=a[0]
            foodlng = a[1]
            foodloc = Point(''.join( [str(foodlat),";",str(foodlng)] ))
            distancelist.append([get_username(int(row[5])),row[1],distance.distance(hunterlocation,foodloc).miles])
    return sorted(distancelist,key=lambda x: x[2])


if __name__=='__main__':
    print nearestbounty(20,20)

