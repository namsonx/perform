

import random
import requests
#import json
from libs import connect_db
#from datetime import datetime
from time import sleep
from objects import vehicle



def recorded_vehicle(serverIp, veh_no, veh_img, camera, direction):
    sql_conn = connect_db(host=serverIp)
    x = sql_conn.cursor()
    
    try:
        x.execute("""INSERT INTO anpr(vehicle_number, vehicle_image, camera_mac_address, date_time, direction)
                            VALUE(%s,%s,%s,NOW(),%s)""", (veh_no, veh_img, camera, direction) )
        sql_conn.commit()
        print 'New vehicle is recorded \n'
    except:
        print 'Could not insert the data\n'
        sql_conn.rollback()
    sql_conn.close()

def data_generate(workspace, num, direction='ENTRY'):
    print 'Simulating %s number of booking' %num
    veh_list = []

    data_recorded = workspace + '\logs\data_recorded.txt'
    f = open(data_recorded, 'w')
    count = 0
    while(count<num):
        veh = vehicle()
        veh.direction = direction
            
        veh.vehicleNo = 'KA99MS'
        veh.vehicleNo = veh.vehicleNo + str(random.randint(1000, 9999))
        data = {"cameraId": veh.cameraId, "image": veh.vehicleImage, "vehicleNo": veh.vehicleNo, "time": veh.time, "status": veh.direction, "vehicleType": veh.type}
        f.write(str(data))
        f.write('\n')
        veh_list.append(veh)
        count = count + 1
    
    f.close()
    for veh in veh_list:
        print veh.vehicleNo
        print veh.vehicleImage
        print veh.direction
        print veh.time
    return veh_list

def booking_and_reconcile_simulate(veh_list, number, serverIp, port, mode, location_id=None):
    i=0
    print 'Start booking simulation: \n'
    #hardcode location id = 4
    if location_id==2:
        entry_camera = 'entry-camera-01'
        exit_camera = 'exit-camera-01'
        di_pin = 'DI0'
    if location_id==3:
        entry_camera = 'entry-camera-02'
        exit_camera = 'exit-camera-02'
        di_pin = 'DI1'
    #headers = {"content-type": "application/json"}
    button_header = {"content-type": "*/*"}
    #reconcile_url = 'http://' + serverIp + ':' + port + '/booking/reconcile'
    button_url = 'http://' + serverIp + ':' + port + '/test/pushButton/' + di_pin
    
    if mode=='entry':
        for veh in veh_list:
            print 'Starting entry booking simulation for %s\n' %veh.vehicleNo
            veh.cameraId = entry_camera
            recorded_vehicle(serverIp, veh.vehicleNo, veh.vehicleImage, veh.cameraId, veh.direction)
            #sleep(1)
            try:
                print button_url
                r = requests.post(button_url, headers=button_header)
            except:
                print 'Post request %s failed with status code: %s', (button_url, r.status_code)
            sleep(10)
            i = i+1
            if i==number:
                break
            
    if mode=='exit':
        for veh in veh_list:
            print 'Start exit reconcile simulation for %s \n' %veh.vehicleNo
            cameraId = exit_camera
            vehicleNo = veh.vehicleNo
            recorded_vehicle(serverIp, vehicleNo, ' ', cameraId, 'EXIT')
            try:
                r = requests.post(button_url, headers=button_header)
            except:
                print 'Post request %s failed with status code: %s', (button_url, r.status_code)

            sleep(10)
            i = i+1
            if i==number:
                break
        
def get_vehicle_not_reconcile(serverIp):
    sql_conn = connect_db(host=serverIp)
    veh_list = []
    x = sql_conn.cursor()
    x.execute("""SELECT id, vehicleno, location_id FROM sim.booking WHERE exittime IS NULL""")
    vehicles = x.fetchall()
    for veh in vehicles:
        vehi = vehicle()
        vehi.vehicleNo = veh[1]
        print 'test print veh No: ', veh[1]
        veh_list.append(vehi)
        
    sql_conn.close()    
    return veh_list

def setup():
    print 'Initialize suite setup. Will implement if needed'
                 
        