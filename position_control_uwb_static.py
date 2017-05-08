# import dronekit_sitl
import time
import serial
import re
import threading
import socket
import sys
from dronekit import connect, VehicleMode
from pymavlink import mavutil
from velocity_fns import send_body_ned_velocity, send_body_ned_velocity_logging
from uwb import uwb
from serversocket import serversocket

# print "Start simulator (SITL)"
# sitl = dronekit_sitl.start_default()
# connection_string = sitl.connection_string()


def control(goal):
    while True:
        myPos = radio.getRange()
        print "My current position:" + str(myPos)
        gain = 0.0005
        print "Desired position: " + str(desiredPos)
        if (abs(goal - myPos) > 20):
            speed = (goal - myPos)*gain
            send_body_ned_velocity_logging(vehicle, speed, 0, 0, pos_file, vel_file)
            # myPos = radio.getRange()
        else:
            send_body_ned_velocity_logging(vehicle, 0, 0, 0, pos_file, vel_file)



filename1 = "pos_gps" + time.strftime("%m_%d_%H%M") + ".txt"
filename2 = "vel_imu" + time.strftime("%m_%d_%H%M") + ".txt"
filename3 = "pos_uwb_filter" + time.strftime("%m_%d_%H%M") + ".txt"
filename4 = "pos_uwb_raw" + time.strftime("%m_%d_%H%M") + ".txt"
pos_file = open(filename1, 'w+')
vel_file = open(filename2, 'w+')
uwb_file = open(filename3, 'w+')
uwb_raw = open(filename4, 'w+')
pos_file.truncate()
vel_file.truncate()
uwb_file.truncate()
uwb_raw.truncate()

try:
    # Connect to the Vehicle.
    print("Connecting to vehicle & initializing UWB & WiFi")

    host = "192.168.1.103"
    port = 5454
    server = serversocket(host=host, port=port)  # wifi init
    vehicle = connect('/dev/ttyS0', wait_ready=True, baud=921600)  # vehicle init
    print "Connecting to UWB radio"
    radio = uwb(a=2000, port='/dev/ttyACM0')  # UWB init
    print 'Connected. Starting to measure position...'
    radiothread = threading.Thread(target=radio.range,
                                   args=(uwb_file, uwb_raw, server))
    radiothread.start()

    # Get some vehicle attributes (state)
    print "Get some vehicle attribute values:"
    print " GPS: %s" % vehicle.gps_0
    print " Battery: %s" % vehicle.battery
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s \n" % vehicle.mode.name    # settable

    t_end = time.time() + (10)
    while time.time() < t_end:
        print "Waiting for filter to settle..."
        time.sleep(1)

    while not vehicle.is_armable:
        print " Is Armable?: %s" % vehicle.is_armable
        time.sleep(1)

    print " Is Armable?: %s" % vehicle.is_armable
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print " Waiting for arming..."
        # print " Mode: %s" % vehicle.mode.name    # settable
        time.sleep(1)



    # while True:
    #     pass

    # print "Taking off!"
    # height = 5
    # vehicle.simple_takeoff(height)
    # while True:
    #     print " Altitude: ", vehicle.location.global_relative_frame.alt
    #     if vehicle.location.global_relative_frame.alt >= height*0.95:
    #         # Trigger just below target alt.
    #         print "Reached target altitude"
    #         break
    #     time.sleep(1)

    print 'Moving to desired position!'

    controlthread = threading.Thread(target=control, args=(500,))
    controlthread.start()

    while True:
        pass

except KeyboardInterrupt:
    pos_file.close()
    vel_file.close()
    uwb_file.close()
    uwb_raw.close()
    radiothread.join()
    vehicle.close()
    sys.exit(0)

# Shut down simulator
# sitl.stop()
