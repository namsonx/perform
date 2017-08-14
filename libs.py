import MySQLdb
from objects import parking_location, camera_obj, cam_moxa_cfg


def connect_db(host='localhost', user='root', password='SmartCity@123', db='sim'):
    try:
        sql_connect = MySQLdb.connect(host=host,
                                      user=user,
                                      passwd=password,
                                      db=db)
    except ValueError:
        print 'Cannot connect to mySQL db. Please check!!!'
        
    return sql_connect

def get_parking_locations(serverIp):
    loc_list = []
    conn_sql = connect_db(serverIp)
    x = conn_sql.cursor()
    x.execute("""SELECT * FROM location""")  
    locations = x.fetchall()
    for location in locations:
        loc = parking_location(location[0], name=location[1], avai=location[2], capacity=location[3], super_loc_id=location[4], cloud_id=location[5])
        loc_list.append(loc)
        
    conn_sql.close()
    return loc_list

def get_camera_list(serverIp):
    cam_list = []
    conn_sql = connect_db(serverIp)
    x = conn_sql.cursor()
    x.execute("""SELECT * FROM camera""")
    cameras = x.fetchall()
    for camera in cameras:
        cam = camera_obj(camera[0], mac_address=camera[1], locationId=camera[2])
        cam_list.append(cam)
    
    conn_sql.close()
    return cam_list

def get_cam_moxa_cfg(serverIp):
    cfg_list = []
    conn_sql = connect_db(serverIp)
    x = conn_sql.cursor()
    x.execute("""SELECT * FROM camera_config""")
    cfgs = x.fetchall()
    for cfg in cfgs:
        config = cam_moxa_cfg(cfg[0], cameraId=cfg[1], buttonPin=cfg[2], barrierPin=cfg[3], vehicleType=cfg[4])
        cfg_list.append(config)
        
    conn_sql.close()
    return cfg_list

def get_location_availability(serverIp, locationId):
    sql_conn = connect_db(serverIp)
    x = sql_conn.cursor()
    x.execute("""SELECT availability FROM location where id = %s""", locationId)
    avai = x.fetchall()
    sql_conn.close()
    return avai[0]

def set_location_availability(serverIp, locationId, avai):
    sql_conn = connect_db(serverIp)
    x = sql_conn.cursor()
    try:
        x.execute("""INSERT INTO location(availability) VALUE(%s) WHERE id = %s""", (avai, locationId))
        sql_conn.commit()
    except ValueError:
        print 'Can not insert availability into location table'
    
    sql_conn.close()
    
def delete_all_booking(serverIp, locationId):
    sql_conn = connect_db(serverIp)
    x = sql_conn.cursor()
    x.execute("""DELETE FROM booking WHERE location_id = %s""", locationId)
    sql_conn.commit()
    sql_conn.close()
    
def get_num_current_booking(serverIp, locationId):
    sql_conn = connect_db(serverIp)
    x = sql_conn.cursor()
    x.execute("""SELECT count(*) FROM booking WHERE location_id = %s AND exittime is Null""", locationId)
    numBooking = x.fetchone()
    sql_conn.close()
    return numBooking[0]

def get_num_reconciliation(serverIp, locationId):
    sql_conn = connect_db(serverIp)
    x = sql_conn.cursor()
    x.execute("""SELECT count(*) FROM booking WHERE location_id = %s AND exittime is not Null""", locationId)
    numReconcile = x.fetchone()
    sql_conn.close()
    return numReconcile[0]