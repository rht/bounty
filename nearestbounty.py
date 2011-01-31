from geopy import distance, Point
import sqlite3

def nearestbounty(hunterlat,hunterlng):
    hunterlocation = Point(''.join([str(hunterlat),";",str(hunterlng)]))
    conn = sqlite3.connect('hack.db')
    c = conn.cursor()
    requestslist = c.execute('''select * from requests''')
    distancelist = []
    for row in requestslist:
        #row: id, descript, status, food, request, uid
        #     0      1        2       3     4       5
        print row
        if row[2] == 1:
            print row
            #foodlat, foodlng = c.execute('''select lat,long from locations where id=? ''',(row[3],))
            aaaa = c.execute('''select * from locations where id=? ''',(row[3],))
            shit = 
            print aaaa[1] , "jfasofjasofaosdf"
            foodloc = Point(''.join( [str(foodlat),";",str(foodlng)] ))
            distancelist.append([row[5],distance.distance(hunterlocation,foodloc).miles])
    return sorted(distancelist,key=lambda x: x[1])

nearestbounty(20,20)


