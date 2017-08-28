import requests
import json
from ipmcloud_objs import parking_place, parking_block, parking_slot, sensor_tagId
from libs import connect_db


def create_parking_place(serverIp, port, placeName, unicode, **kwargs):
    
    parkingPlace = parking_place(placeName, unicode, **kwargs)
    headers = {"content-type": "application/json"}
    data = {"placeName": parkingPlace.name, "unicode": parkingPlace.unicode, "autoExit": parkingPlace.autoExit, "availability": parkingPlace.availability,
             "createdBy": parkingPlace.createdBy, "lang": parkingPlace.long, "lat": parkingPlace.lat, "park_type": parkingPlace.parkType, "passRuleName": parkingPlace.passRuleName}
     
    createParkingPlaceURL = 'http://' + serverIp + ':' + port + '/admin/createParkingPlace'
    try:
        r = requests.post(createParkingPlaceURL, data=json.dumps(data), headers=headers)
    except ValueError:
        print 'Cannot create parking place via api. Status code is: ', r.status_code
        
    if r.status_code!=200:
        print 'Cannot create parking place via api. Status code is: ', r.status_code
    else:
        print 'One parking place is created successful'
        parkingPlace.id = parkingPlace.get_place_id(serverIp = serverIp)
        print 'parking place ID is: %s', parkingPlace.id
    
    return parkingPlace

def get_parking_place_info(serverIp, placeName, **kwargs):
    sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
    x = sqlConn.cursor()
    query = 'SELECT id, lang, lat, unicode, pass_rule, auto_exit FROM sm_ipm_park_place WHERE place_name =\' %s\'' %placeName
    x.execute(query)
    info = x.fetchone()
    sqlConn.close()
    print 'place infor: ', info
    parkingPlace = parking_place(placeName=placeName, unicode=info[3], )
        

def delete_parking_place(serverIp, placeId):
    
    sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
    x = sqlConn.cursor()
    x.execute("""DELETE FROM sm_ipm_park_place WHERE id = %s""", placeId)
    sqlConn.commit()
    sqlConn.close()        
    print 'Deleted parking successul'    

def create_parking_block(serverIp, port, number, placeId, blockName, unicode, **kwargs):
    
    blockList = []
    headers = {"content-type": "application/json"}    
    createParkingBlockURL = 'http://' + serverIp + ':' + port + '/admin/createParkingBlock'
    count = 0
    while count<number:
        name = blockName
        uni = unicode
        name = name + str(count)
        uni = uni + str(count)
        parkingBlock = parking_block(placeId, name, uni, **kwargs)
        data = {'availability': parkingBlock.availability, 'block_name': parkingBlock.name, 'created_by': parkingBlock.createdBy, 'parkGuidanceURL': parkingBlock.parkGuidanceURL, 
                'park_for': parkingBlock.parkFor, 'placeid': parkingBlock.placeId, 'solution_type': parkingBlock.solutionType, 'unicode': parkingBlock.unicode}

        try:
            r = requests.post(createParkingBlockURL, data=json.dumps(data), headers=headers)
        except ValueError:
            print 'Cannot create parking block via api. Status code is: ', r.status_code
            
        if r.status_code!=200:
            print 'Cannot create parking block via api. Status code is: ', r.status_code
        else:
            print 'One parking block is created successful'
        blockList.append(parkingBlock)
        count = count + 1
        
    return blockList

def create_parking_slot(serverIp, port,type ,number, placeId, blockId, slotName, tagId, unicode, **kwargs):
    
    slotList = []
    if type=='sensor':
        sensor = sensor_tagId()
        numberSensor = len(sensor.tagList)
        if number>numberSensor:
            print 'Will create %s slots instead of %s due to just %s sensor tagId in the sensor object', numberSensor, number, numberSensor
            number = numberSensor    
    
    headers = {"content-type": "application/json"}    
    createParkingSlotkURL = 'http://' + serverIp + ':' + port + '/admin/createParkingSlot'
    count = 0
    while count<number:
        
        if type=='sensor':
            tag = sensor.tagList[count]
            name = 'S' + tag
        else:
            tag = tagId
            tag = tag + str(count)
            name = slotName
            name = name + str(count)
        uni = unicode
        uni = uni + str(count)
        parkingSlot = parking_slot(placeId, blockId, name, tag, uni, **kwargs)
        data = {'placeId': parkingSlot.placeId, 'blockId': parkingSlot.blockId, 'slotName': parkingSlot.name, 'tagId': parkingSlot.tagId, 'unicode': parkingSlot.unicode,
                'availability': parkingSlot.availability, 'createdBy': parkingSlot.createdBy}
        
        try:
            r = requests.post(createParkingSlotkURL, data=json.dumps(data), headers=headers)
        except ValueError:
            print 'Cannot create parking slot via api. Status code is: ', r.status_code
            
        if r.status_code!=200:
            print 'Cannot create parking slot via api. Status code is: ', r.status_code
        else:
            print 'One parking slot is created successful'
        
        slotList.append(parkingSlot)    
        count = count+1
    return slotList

def get_number_of_parking_place(serverIp):
    
    sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
    x = sqlConn.cursor()
    x.execute('''SELECT COUNT(*) FROM sm_ipm_park_place''')
    numOfPlace = x.fetchone()[0]
    return numOfPlace
        