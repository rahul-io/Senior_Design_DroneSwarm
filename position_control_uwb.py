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

# print "Start simulator (SITL)"
# sitl = dronekit_sitl.start_default()
# connection_string = sitl.connection_string()


def control(offset):
    myPos = radio.getRange()
    gain = 0
    desiredPos = myPos + offset
    while (abs(desiredPos - myPos) > 5):
        speed = (desiredPos - myPos)*gain
        send_body_ned_velocity_logging(0, speed, 0, pos_file, vel_file)
        myPos = radio.getRange()


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
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # wifi init
    vehicle = connect('/dev/ttyS0', wait_ready=True, baud=921600)  # vehicle init
    print "Connecting to UWB radio"
    radio = uwb(a=140, port='/dev/ttyACM0')  # UWB init
    print 'Connected. Starting to measure position...'
    radiothread = threading.Thread(target=radio.getRawDist)
    # radiothread = threading.Thread(target=radio.range,
    #                                args=(uwb_file,
    #                                      uwb_raw,
    #                                      serverSocket,
    #                                      host,
    #                                      port
    #                                      )
    #                                     )
    radiothread.start()

    # Get some vehicle attributes (state)
    print "Get some vehicle attribute values:"
    print " GPS: %s" % vehicle.gps_0
    print " Battery: %s" % vehicle.battery
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s \n" % vehicle.mode.name    # settable

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

    t_end = time.time() + (20)
    while time.time() < t_end:
        print "Waiting for filter to settle..."
        time.sleep(1)

    print "Taking off!"
    height = 5
    vehicle.simple_takeoff(height)
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        if vehicle.location.global_relative_frame.alt >= height*0.95:
            # Trigger just below target alt.
            print "Reached target altitude"
            break
        time.sleep(1)

    print 'Moving to desired position!'

    controlthread = threading.Thread(target=control, args=(500,))
    controlthread.start()

    for i in range(1, int(round(5/0.2))):
        send_body_ned_velocity_logging(0, 0, 0, pos_file, vel_file)

    print("Completed")
    pos_file.close()
    vel_file.close()
    uwb_file.close()
    uwb_raw.close()

    while True:
        send_body_ned_velocity(0, 0, 0)

    # Close vehicle object before exiting script
    # vehicle.close()

except KeyboardInterrupt:
    pos_file.close()
    vel_file.close()
    uwb_file.close()
    uwb_raw.close()
    radiothread.join()
    sys.exit(0)

# Shut down simulator
# sitl.stop()
