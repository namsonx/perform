import os
import argparse
from libs import get_parking_locations, get_camera_list, get_cam_moxa_cfg
#from perform import data_generate, booking_and_reconcile_simulate, get_vehicle_not_reconcile
from datetime import datetime
import robot



def runtests_and_collectlogs(args, runtestlog, workspace):
    runtestlog.write('======================Starting robot running======================\n')
    logdir = args.outputdir + '\\logs'
    testsuite = args.testsuite
    
    try:
        '''
        for _f in glob.glob(args.outputdir + '\\*'):
            autotestlog.write('\n Clean up file %s \n' % _f)
            os.remove(_f)
        '''
        runtestlog.write('\n Clean up old log files \n')
        os.remove(logdir + '\\output.xml')
        os.remove(logdir + '\\report.html')
        os.remove(logdir + '\\log.html')
    except os.error:
        pass
    variable = []
    variable.append('server_ip:' + args.server_ip)
    variable.append('port:' + args.port)
    variable.append('workspace:' + workspace)
    
    status = robot.run(testsuite, variable=variable, outputdir=logdir)
    print 'Runing status is: ', status
    log = str(('Runing status is: ', status))
    runtestlog.write((log + '\n'))

def main():
    """
    if len(sys.argv)<2:
        print'The server and port should be provide \n'
        sys.exit(0)
    """   
    global workspace
    workspace = os.getcwd()
    workspace = workspace.strip(' \n\t')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-ts', '--testsuite', help='Path to testsuite file', default='C:\\Users\\mas2hc\\Desktop\\workspace\\performance\\testsuites\\booking_simulation.txt')
    parser.add_argument('-s', '--server_ip', help='Input server ip address', default='localhost')
    parser.add_argument('-p', '--port', help='Input port number', default='50211')
    parser.add_argument('-d', '--outputdir', help='variable', default=workspace)
    
    args = parser.parse_args()
    
    server_ip = args.server_ip   

    time = str(datetime.now())
    tmp = time.split(' ')
    time = tmp[0]+ '-' + tmp[1].split('.')[0]
    time = time.replace(':', '-')
    
    runtestlogfile = args.outputdir + '\\logs\\runtest' + time +'.log'
    runtestlog = open(runtestlogfile, 'w')
    runtestlog.write('==============================Started running test==============================\n')
    
    print 'List out all location:\n'
    runtestlog.write('List out all location:\n')
    location_list = get_parking_locations(server_ip)
    for location in location_list:
        print 'Location: ', location.locationId, location.name, location.avai, location.capacity
        log = str(('location: ', location.locationId, location.name, location.avai, location.capacity))
        runtestlog.write((log + '\n'))
    
    print 'List out all camera:\n'
    runtestlog.write('List out all camera:\n')
    camera_list = get_camera_list(server_ip)
    for cam in camera_list:
        print 'Camera is: ', cam.cameraId, cam.mac_address, cam.locationId
        log = str(('Camera is: ', cam.cameraId, cam.mac_address, cam.locationId))
        runtestlog.write((log + '\n'))
        
    print 'List out all camera config:\n'
    runtestlog.write('List out all camera config:\n')
    cfg_list = get_cam_moxa_cfg(server_ip)
    for cfg in cfg_list:
        print 'Camera config is: ', cfg.cfg_id, cfg.cam_id, cfg.buttonPin, cfg.barrierPin, cfg.vehicleType
        log = str(('Camera config is: ', cfg.cfg_id, cfg.cam_id, cfg.buttonPin, cfg.barrierPin, cfg.vehicleType))
        runtestlog.write((log + '\n'))
        
    runtests_and_collectlogs(args, runtestlog, workspace)
    
    runtestlog.close()
    exit(0)
if __name__ == '__main__':
    main()
    pass