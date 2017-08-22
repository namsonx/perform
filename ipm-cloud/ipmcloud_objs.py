# Defined the objects for ipm cloud

class parking_place(object):
    
    def __init__(self, placeName, unicode, **kwargs):
        self.id = None
        self.name = placeName
        self.unicode = unicode
        self.long = kwargs.get('longitude', 77.66297310590744)
        self.lat = kwargs.get('latitude', 12.851636423171994)
        self.availability = kwargs.get('availability', 0)
        self.parkType = kwargs.get('parkType', 0)
        self.passRuleName = kwargs.get('passRuleName', '24hr')
        self.createdBy = kwargs.get('createdBy', 'Auto')
        self.autoExit = kwargs.get('autoExit', 'Y')
        
class parking_block(object):
    
    def __init__(self, placeId, blockName, unicode, **kwargs):
        self.id = None
        self.placeId = placeId
        self.name = blockName
        self.unicode = unicode
        self.availability = kwargs.get('availability', 0)
        self.createdBy = kwargs.get('createdBy', 'Auto')
        self.parkGuidanceURL = kwargs.get('parkGuidanceURL', ' ')
        self.parkFor = kwargs.get('parkFor', 4)
        self.solutionType = kwargs.get('solutionType', 1)
        
class parking_slot(object):
    
    def __init__(self, placeId, blockId, slotName, tagId, unicode, **kwargs):
        self.id = None
        self.placeId = placeId
        self.blockId = blockId
        self.slotName = slotName
        self.tagId = tagId
        self.unicode = unicode
        self.availability = kwargs.get('availability', 1)
        self.createdBy = kwargs.get('createdBy', 'Auto')
        
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