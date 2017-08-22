import requests
import json
from ipmcloud_objs import parking_place, parking_block
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
            print 'Cannot create parking place via api. Status code is: ', r.status_code
            
        if r.status_code!=200:
            print 'Cannot create parking place via api. Status code is: ', r.status_code
        else:
            print 'One parking block is created successful'
        blockList.append(parkingBlock)
        count = count + 1
        
    return blockList

def create_parking_slot(serverIp, port, number, placeId, blockId, slotName, tagId, unicode, **kwargs):
    
    slotList = []
    headers = {"content-type": "application/json"}    
    createParkingBlockURL = 'http://' + serverIp + ':' + port + '/admin/createParkingSlot'
    count = 0
    while count<number:
        name = slotName
        tag = tagId
        uni = unicode
        name = name + str(count)
        tag = tag + str(count)
        uni = uni + str(count)
        
        