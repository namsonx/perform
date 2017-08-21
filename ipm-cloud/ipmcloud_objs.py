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
        self.passRuleName = kwargs.get('passRuleName', 'Cash')
        self.createdBy = kwargs.get('createdBy', 'Auto')
        self.autoExit = kwargs.get('autoExit', 'Yes')
        
        