#Define the booking object

class vehicle(object):
    
    def __init__(self, vehicleNo=' ', vehicleImage=' ', cameraId=' ', time=' ', direction='ENTRY', **kwargs):
        self.vehicleNo = vehicleNo
        self.vehicleImage = vehicleImage
        self.cameraId = cameraId
        self.time = time
        self.direction = direction
        if not kwargs.get('type', None):
            self.type = ' '
            
class parking_location(object):
    def __init__(self, locationId, **kwargs):
        self.locationId = locationId
        self.name = kwargs.get('name', None)
        self.capacity = kwargs.get('capacity', 0)
        self.avai = kwargs.get('avai', 0)
        self.entry_cam = kwargs.get('entry_cam', None)
        self.exit_cam = kwargs.get('exit_cam', None)
        self.super_loc_id = kwargs.get('super_loc_id', None)
        self.cloud_id = kwargs.get('cloud_id', None)
        
class camera_obj(object):
    def __init__(self, cam_id, **kwargs):
        self.cameraId = cam_id
        self.mac_address = kwargs.get('mac_address', None)
        self.locationId = kwargs.get('locationId', None)
        
class cam_moxa_cfg():
    def __init__(self, cfg_id, **kwargs):
        self.cfg_id = cfg_id
        self.cam_id = kwargs.get('cameraId', None)
        self.buttonPin = kwargs.get('buttonPin', None)
        self.barrierPin = kwargs.get('barrier', None)
        self.vehicleType = kwargs.get('vehicleType', 4)
        