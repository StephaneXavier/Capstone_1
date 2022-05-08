from models import User, Submitted_Data, Bus, Stop
from app import app, db


def get_busNo_from_gtfs_routes_text(routes_text):
    """Returns an array of buses from the gtfs "routes.txt" file"""
    file = open(routes_text)
    lines = file.readlines()[1:]
    bus_arr = []

    for line in lines:
        route_id=''
        route_short_name = ''
        count = 0
        
        for char in line:
            if char == ',':
                count += 1

            if count <1:
                route_id += char

            if count == 1:
                route_short_name+=char
            
        
        bus_arr.append((route_id, route_short_name[1:]))
        
    file.close()  
    return bus_arr
            
def get_stopNo_from_gtfs_stops_text(stops_text):
    """Returns an array of stop_id from the gtfs "routes.txt" file"""
    file = open(stops_text)
    lines = file.readlines()[1:]
    stop_id_arr = []

    for line in lines:
        stop_name = ''
        stop_code = ''

        count = 0
        for char in line:
            
            if 2 <= count < 3:
                if char =='"':
                    continue
                stop_name+=char

            if 2 > count >= 1:
                stop_code+=char

            if char == ',':
                count += 1
            
        
        stop_id_arr.append((stop_code[:-1],stop_name[:-1]))
        
    file.close()  
    return stop_id_arr



"""Need to change the file paths for buses and stops whenever new text files come out"""
buses = get_busNo_from_gtfs_routes_text('/mnt/c/Users/steph/Desktop/gtfs/routes.txt')
stops = get_stopNo_from_gtfs_stops_text('/mnt/c/Users/steph/Desktop/gtfs/stops.txt')

db.drop_all()
db.create_all()

bm = []
sm = []

for route_id,route_short_name in buses:
    b = Bus(route_id=route_id,route_short_name=route_short_name)
    bm.append(b)

for stop_code, stop_name in stops:
    s = Stop(stop_code=stop_code,stop_name=stop_name)
    sm.append(s)

db.session.add_all(bm)
db.session.add_all(sm)
db.session.commit()