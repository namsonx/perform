

import random
import requests
from threading import Thread
#import json
from libs import connect_db, get_camera_list, get_cam_moxa_cfg, get_parking_locations
#from datetime import datetime
from time import sleep
from objects import vehicle, parking_location



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

def booking_and_reconcile_simulate(veh_list, number, serverIp, port, mode, location_id):
    location_objs = []
    locationId_list = []
    dests = ['ENTRY', 'EXIT']
    cam_list = get_camera_list(serverIp)
    moxa_cfgs = get_cam_moxa_cfg(serverIp)

    for cam in cam_list:
        for moxacfg in moxa_cfgs:
            if cam.cameraId==moxacfg.cam_id:
                if moxacfg.buttonPin!=None:
                    cam.buttonPin = moxacfg.buttonPin
                if moxacfg.barrierPin!=None:
                    cam.barrierPin = moxacfg.barrierPin
                               
        if cam.locationId not in locationId_list:
            location = parking_location(cam.locationId)
            location.entry_cam = cam.mac_address
            locationId_list.append(cam.locationId)
            location_objs.append(location)
        else:
            for loc_obj in location_objs:
                if cam.locationId==loc_obj.locationId:
                    loc_obj.exit_cam = cam.mac_address
                
                    
    print 'List location id is: %s\n' %locationId_list
    i=0
    print 'Start booking simulation: \n'
    di_pin = 'none'
    dio_pin = 'none'
    for location in location_objs:
    #hardcode location id = 4
        if location_id==location.locationId:
            entry_camera = location.entry_cam
            exit_camera = location.exit_cam
            for cam in cam_list:        
                if cam.mac_address==entry_camera and cam.buttonPin!=None:
                    print 'button pin: ', cam.buttonPin
                    di_pin = cam.buttonPin
                if cam.mac_address==exit_camera and cam.barrierPin!=None:
                    dio_pin = cam.barrierPin

                 
    #headers = {"content-type": "application/json"}
    button_header = {"content-type": "*/*"}
    #reconcile_url = 'http://' + serverIp + ':' + port + '/booking/reconcile'
    button_url = 'http://' + serverIp + ':' + port + '/test/pushButton/' + di_pin
    barrie_url = 'http://' + serverIp + ':' + port + '/test/pushButton/' + dio_pin
    
    if mode=='entry':
        cameraId = entry_camera
        direction = dests[0]
        
    if mode=='exit':
        cameraId = exit_camera
        direction = dests[1]
        
    for veh in veh_list:
        print 'Starting %s booking simulation for %s\n', direction, veh.vehicleNo
        veh.direction = direction 
        recorded_vehicle(serverIp, veh.vehicleNo, veh.vehicleImage, cameraId, veh.direction)
        #sleep(1)
        print button_url
        if di_pin!='none':
            try:
                print button_url
                r = requests.post(button_url, headers=button_header)
            except:
                print 'Post request %s failed with status code: %s', (button_url, r.status_code)
        sleep(random.randint(10,20))
        i = i+1
        if i==number:
            break
               
def random_booking_and_reconcile(workspace, serverIp, port):
    print 'Start performance test for multi-location\n'
    #dests = ['ENTRY', 'EXIT']
    loc_list = get_parking_locations(serverIp)
    cam_list = get_camera_list(serverIp)
    
    for location in loc_list:
        check = 0
        for cam in cam_list:
            if location.locationId==cam.locationId:
                check = check+1
                break
        if check==0:
            loc_list.remove(location)
    
    for loc in loc_list:
        print 'location is: ', loc

    count = 0
    while count<20:
        '''
        location = random.choice(loc_list)
        dest = random.choice(dests)
        if dest=='ENTRY':
            mode = 'entry'
        if dest=='EXIT':
            mode = 'exit'
        '''
        t1_list = []
        t2_list = []
        for location in loc_list:       
            veh = data_generate(workspace, 1, 'ENTRY')
            t1 = Thread(target=booking_and_reconcile_simulate, args=(veh, 1, serverIp, port, 'entry', location.locationId))
            t1.start()
            t1_list.append(t1)
            veh = data_generate(workspace, 1, 'EXIT')
            t2 = Thread(target=booking_and_reconcile_simulate, args=(veh, 1, serverIp, port, 'exit', location.locationId))
            t2.start()
            t2_list.append(t2)
        while True:
            t1_status = []
            t2_status =[]
            for t1 in t1_list:
                t1_status.append(t1.isAlive())                
            for t2 in t2_list:
                t2_status.append(t2.isAlive())
            print 'Debug: ', t1_status
            
            if (True in t1_status) or (True in t2_status):
                continue
            break
        
        count = count + 1
         
def get_vehicle_not_reconcile(serverIp):
    sql_conn = connect_db(host=serverIp)
    veh_list = []
    x = sql_conn.cursor()
    x.execute("""SELECT id, vehicleno, location_id FROM sim.booking WHERE exittime IS NULL""")
    vehicles = x.fetchall()
    for veh in vehicles:
        vehi = vehicle()
        vehi.vehicleNo = veh[1]
        vehi.vehicleImage = ' '
        print 'test print veh No: ', veh[1]
        veh_list.append(vehi)
        
    sql_conn.close()    
    return veh_list

def setup():
    print 'Initialize suite setup. Will implement if needed'
                 
        