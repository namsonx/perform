import requests
import json
import random
from ipmcloud_objs import parking_place, parking_block, parking_slot, sensor_tagId, vehicleTenant
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

def get_parking_place_info(serverIp, placeName):
    sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
    x = sqlConn.cursor()
    query = 'SELECT id, lang, lat, unicode, pass_rule, auto_exit FROM sm_ipm_park_place WHERE place_name =\'%s\'' %placeName
    x.execute(query)
    info = x.fetchone()
    sqlConn.close()
    print 'place info: ', info
    parkingPlace = parking_place(placeName=placeName, unicode=info[3], placeId=info[0], longitude=info[1], latitude=info[2], passRuleName=info[4], autoExit=info[5])
    return parkingPlace

def update_parking_place(serverIp, port, placeName, **kwargs):
    
    parkingPlace = get_parking_place_info(serverIp, placeName)
    if kwargs.get('autoExit'):
        print 'Updating for autoExit'
        parkingPlace.autoExit = kwargs.get('autoExit')
    if kwargs.get('availability'):
        print 'Updating for availability'
        parkingPlace.availability = kwargs.get('availability')
    if kwargs.get('longitude'):
        print 'Updating for longitude'
        parkingPlace.long = kwargs.get('longitude')
    if kwargs.get('latitude'):
        print 'Updating for latitude'
        parkingPlace.lat = kwargs.get('latitude')
    if kwargs.get('placeName'):
        print 'Updating for placeName'
        parkingPlace.name = kwargs.get('placeName')
    if kwargs.get('ruleName'):
        print 'Updating for ruleName'
        parkingPlace.passRuleName = kwargs.get('ruleName')
    if kwargs.get('unicode'):
        print 'Updating for unicode'
        parkingPlace.unicode = kwargs.get('unicode')
    
    headers = {"content-type": "application/json"}
    data = {"placeName": parkingPlace.name, "unicode": parkingPlace.unicode, "autoExit": parkingPlace.autoExit, "availability": parkingPlace.availability,
             "updatedBy": 'Auto', "lang": parkingPlace.long, "lat": parkingPlace.lat, "ruleName": parkingPlace.passRuleName, "placeId": parkingPlace.id}
    
    print 'data: ', data
    print 'json data: ', json.dumps(data)
    updateParkingPlaceURL = 'http://' + serverIp + ':' + port + '/admin/updateParkingPlace'
    try:
        r = requests.put(updateParkingPlaceURL, data=json.dumps(data), headers=headers)
    except ValueError:
        raise ValueError('Cannot update parking place via api. Status code is: ', r.status_code)
        
    if r.status_code!=200:
        raise ValueError('Cannot update parking place via api. Status code is: ', r.status_code)
    else:
        print 'One parking place is updated successful'
          
        

def delete_parking_place(serverIp, placeName):
    
    sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
    x = sqlConn.cursor()
    deleteQuery = 'DELETE FROM sm_ipm_park_place WHERE place_name = \'%s\'' %placeName
    x.execute(deleteQuery)
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

def create_parking_slot(serverIp, port, slotType ,number, placeId, blockId, slotName, tagId, unicode, **kwargs):
    
    slotList = []
    if slotType=='sensor':
        sensor = sensor_tagId()
        numberSensor = len(sensor.tagList)
        if number>numberSensor:
            print 'Will create %s slots instead of %s due to just %s sensor tagId in the sensor object', numberSensor, number, numberSensor
            number = numberSensor    
    
    headers = {"content-type": "application/json"}    
    createParkingSlotkURL = 'http://' + serverIp + ':' + port + '/admin/createParkingSlot'
    count = 0
    while count<number:
        
        if slotType=='sensor':
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

def create_vehicle_list_for_tenant(number):
    vehList = []
    vehTypes = [2,3,4,6]
    i = 0
    while i<number:
        vehType = random.choice(vehTypes)
        vehNo = 'KA' + str(random.randint(0, 99)) + 'MH' + str(random.randint(1000, 9999)) 
        veh = vehicleTenant(vehNo, vehType)
        vehList.append(veh)
        i=i+1
        
    return vehList

def get_tenant_id(serverIp, placeName, tenantName):
    parkingPlace = get_parking_place_info(serverIp, placeName)
    sqlConn = connect_db(host=serverIp, user='root', password='SmartCity@123', db='ipmtest')
    x = sqlConn.cursor()
    queryCmd = 'SELECT id FROM sm_ipm_place_tenant WHERE place_id = %s AND tenant_name = \'%s\'' %(parkingPlace.id, tenantName)
    x.execute(queryCmd)
    tenantId = x.fetchone()[0]
    return tenantId

def get_tenant_info(serverIp, port, tenantId):
    tenantUrl = 'http://' + serverIp + ':' + port + '/tenantManagment/tenant/' + str(tenantId)
    header = {'Content-Type': 'application/json'}
    try:
        r = requests.get(tenantUrl, headers=header)
    except ValueError:
        print 'Cannot get tenant info via api: %s.\n Status code is: %s' %(tenantUrl, r.status_code)
        
    if r.status_code!=200:
        errMessage = 'Cannot get tenant info via api: %s.\n Status code is: %s' %(tenantUrl, r.status_code)
        raise ValueError(errMessage)
    return r.json()['data']

def get_reserved_slot_of_tenant(serverIp, port, placeName, tenantName):
    tenantId = get_tenant_id(serverIp, placeName, tenantName)
    tenantInfo = get_tenant_info(serverIp, port, tenantId)
    return tenantInfo['reservedSlots']

def get_all_tenant_of_place(serverIp, port, placeName):
    parkingPlace = get_parking_place_info(serverIp, placeName)
    tenantUrl = 'http://' + serverIp + ':' + port + '/tenantManagment/tenants/' + str(parkingPlace.id)
    header = {'Content-Type': 'application/json'}
    try:
        r = requests.get(tenantUrl, headers=header)
    except ValueError:
        print 'Cannot get tenants of place via api: %s. Status code is: %s' %(tenantUrl, r.status_code)
        
    if r.status_code!=200:
        errMessage = 'Cannot get tenants of place via api: %s. Status code is: %s' %(tenantUrl, r.status_code)
        raise ValueError(errMessage)
    tenantList = r.json()['data']
    print 'Tenant list is: ', tenantList
    return tenantList
    

def get_all_vehicle_of_tenant(serverIp, port, tenantId):

    vehTenantUrl = 'http://' + serverIp + ':' + port + '/tenantManagment/vehicles/' + str(tenantId)
    header = {'Content-Type': 'application/json'}
    try:
        r = requests.get(vehTenantUrl, headers=header)
    except ValueError:
        print 'Cannot get vehicles of tenant via api: %s. Status code is: %s' %(vehTenantUrl, r.status_code)
        
    if r.status_code!=200:
        errMessage = 'Cannot get vehicles of tenant via api: %s. Status code is: %s' %(vehTenantUrl, r.status_code)
        raise ValueError(errMessage)
    
    vehsTenant = r.json()['data']
    for veh in vehsTenant:
        print 'Vehicle: ', veh    
    return vehsTenant

