import requests
import json
from ipmcloud_objs import parking_place, parking_block


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
        
    print 'One parking place is created successful'
    

def create_parking_block(serverIp, port, placeId, blockName, unicode, **kwargs):
    
    parkingBlock = parking_block(placeId, blockName, unicode, **kwargs)
    headers = {"content-type": "application/json"}
    data = {'palceid': parkingBlock.placeId, 'block_name': parkingBlock.name, 'unicode': parkingBlock.unicode, 'availability': parkingBlock.availability, 
            'created_by': parkingBlock.createdBy, 'parkGuidanceURL': parkingBlock.parkGuidanceURL, 'park_for': parkingBlock.parkFor, 'solution_type': parkingBlock.solutionType}
    
    createParkingBlockURL = 'http://' + serverIp + ':' + port + '/admin/createParkingBlock'
    try:
        r = requests.post(createParkingBlockURL, data=json.dumps(data), headers=headers)
    except ValueError:
        print 'Cannot create parking place via api. Status code is: ', r.status_code
        
    print 'One parking block is created successful'