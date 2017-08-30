# Defined the objects for ipm cloud
from libs import connect_db

class parking_place(object):
    
    def __init__(self, placeName, unicode, **kwargs):
        if kwargs.get('placeId'):
            self.id = kwargs.get('placeId')
        else:
            self.id = None
        self.name = placeName
        self.unicode = unicode
        self.long = kwargs.get('longitude', 77.66297310590744)
        self.lat = kwargs.get('latitude', 12.851636423171994)
        self.availability = kwargs.get('availability', 0)
        self.parkType = kwargs.get('parkType', 1)
        self.passRuleName = kwargs.get('passRuleName', '24hr')
        self.createdBy = kwargs.get('createdBy', 'Auto')
        self.autoExit = kwargs.get('autoExit', 'Y')
        
    def get_place_id(self, serverIp):
        sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
        x = sqlConn.cursor()
        x.execute('''SELECT id FROM sm_ipm_park_place WHERE place_name = %s AND unicode = %s''', (self.name, self.unicode))
        placeId = x.fetchone()
        self.id = placeId[0]
        sqlConn.close()
        return self.id
    
class parking_block(object):
    
    def __init__(self, placeId, blockName, unicode, **kwargs):
        self.id = None
        self.placeId = placeId
        self.name = blockName
        self.unicode = unicode
        self.availability = kwargs.get('availability', 0)
        self.createdBy = kwargs.get('createdBy', 'Auto')
        self.parkGuidanceURL = kwargs.get('parkGuidanceURL', '')
        self.parkFor = kwargs.get('parkFor', 4)
        self.solutionType = kwargs.get('solutionType', 2)
        
    def get_block_id(self, serverIp):
        sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
        x = sqlConn.cursor()
        x.execute('''SELECT id FROM sm_ipm_park_block WHERE block_name = %s AND unicode = %s''', (self.name, self.unicode))
        blockId = x.fetchone()
        self.id = blockId[0]
        sqlConn.close()
        return self.id
        
class parking_slot(object):
    
    def __init__(self, placeId, blockId, slotName, tagId, unicode, **kwargs):
        self.id = None
        self.placeId = placeId
        self.blockId = blockId
        self.name = slotName
        self.tagId = tagId
        self.unicode = unicode
        self.availability = kwargs.get('availability', 0)
        self.createdBy = kwargs.get('createdBy', 'Auto')
        
    def get_slot_id(self, serverIp):
        sqlConn = connect_db(serverIp, 'root', 'SmartCity@123', 'ipmtest')
        x = sqlConn.cursor()
        x.execute('''SELECT id FROM sm_ipm_park_slot WHERE slot_name = %s AND unicode = %s''', (self.name, self.unicode))
        slotId = x.fetchone()
        self.id = slotId[0]
        sqlConn.close()
        return self.id
        
class tenant(object):
    
    def __init__(self, placeId, tenantName, **kwargs):
        self.id = None
        self.placeId = placeId
        self.name = tenantName
        
class vehicleTenant(object):
    
    def __init__(self, tenantId, vehicleNo, vehicleType):
        self.id = None
        self.tenantId = tenantId
        self.vehicleNo = vehicleNo
        self.vehicleType = vehicleType
        
class sensor_tagId(object):
    
    def __init__(self):
        self.tagList = ['1070', '1016', '1042', '1082', '1007', '1079', '1076', '1010', '1021', '1033', '1013', '1002', '1035', '1017', '1034', '1001',
                        '1080', '1003', '1078', '1023', '1011', '1008', '1059', '1085', '1081', '1006', '1075', '1012', '1053', '1064', '1030', '1074',
                        '1014', '4299', '1065', '1061', '1060', '1057', '1056', '1029', '1027', '1025', '1067', '1080', '1044', '1043', '1040', '1084',
                        '1083', '1039', '1038', '1037', '1055', '1052', '1049', '1005', '1048', '1047', '1046', '1045', '1009', '4213', '4228']        