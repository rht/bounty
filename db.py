import sqlite3


def insert_table(f_lat, f_long, e_lat, e_long,description,u_id):
    conn = sqlite3.connect('hack.db')
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


#if __name__ == '__main__':
#    insert_table(0,0,0,0,"Test1",0)
