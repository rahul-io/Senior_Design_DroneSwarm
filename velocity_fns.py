###############################################################################
#   velocity_fns.py
#   Rahul Nunna, 2017
#   Custom dronekit velocity functions, create custom mavlink messages.
###############################################################################

from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time
import re


sleeptime = 0.1


def send_body_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        # mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,
        # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 5 Hz cycle
    # print str(vehicle.location.global_relative_frame)
    # print str(vehicle.velocity)
    vehicle.send_mavlink(msg)
    time.sleep(sleeptime)


def send_body_ned_velocity_logging(vehicle, velocity_x, velocity_y,
                                   velocity_z, pos_file, vel_file):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame
        # mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,
        # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    vehicle.send_mavlink(msg)
    latitude = re.search("lat=(.*?),",
                         str(vehicle.location.global_relative_frame)).group(1)
    longitude = re.search("lon=(.*),",
                          str(vehicle.location.global_relative_frame)).group(1)
    altitude = re.search("alt=(.*)",
                         str(vehicle.location.global_relative_frame)).group(1)
    vel_x = re.search("\[(.*?),", str(vehicle.velocity)).group(1)
    vel_y = re.search(", (.*),", str(vehicle.velocity)).group(1)
    vel_z = re.search(".+\, (.+)]", str(vehicle.velocity)).group(1)
    pos_file.write(latitude + ',' + longitude + ',' + altitude + "\n")
    vel_file.write(vel_x + ',' + vel_y + ',' + vel_z + "\n")
    time.sleep(sleeptime)
