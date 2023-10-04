#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rospy
import serial
from math import sin, pi
from std_msgs.msg import Float64
import time
import utm
import sys
# import argparse

from gps_lab.msg import gps_msg

if __name__ == '__main__':
    

    serial_port = str(sys.argv[1])
    print(serial_port.split(","))
    SENSOR_NAME = "gps_sensor"
    pub= rospy.Publisher("gps",gps_msg,queue_size=10)
    rospy.init_node('gps_sensor')
   
    baud_rate = rospy.get_param('~baudrate',4800)
    sampling_rate = rospy.get_param('~sampling_rate',5.0)
    port = serial.Serial(serial_port, baud_rate, timeout=3.)
    rospy.logdebug("Using gps sensor on port "+serial_port+" at "+str(baud_rate))
    rospy.logdebug("Initializing sensor with *0100P4\\r\\n ...")
    
    sampling_count = int(round(1/(sampling_rate*0.007913)))
    rospy.sleep(0.2)        

    rospy.logdebug("Initialization complete")
    
    rospy.loginfo("Publishing longitude and latitutde.")

    msg=gps_msg()
    i=1
    try:
        while not rospy.is_shutdown():
            msg.header.seq=i
            line = port.readline()
            line2=line.decode('latin-1')
            #print(line2)
            if line == '':
                rospy.logwarn("DEPTH: No data")
            else:
                if line2.startswith("$GPGGA") :
                    s =line2.split(",")
                    lat = s[2]
                    lon = s[4]
                    lat_dir = s[3]
                    lon_dir = s[5]
                    utc_time = s[1]
                    alt = s[9]

                    lat_degree=int(float(lat)/100)
                    minutes_lat=float(lat)-(lat_degree*100)
                    lon_degree=int(float(lon)/100)
                    minutes_lon=float(lon)-(lon_degree*100)
                    dd_lat= float(lat_degree) + float(minutes_lat)/60
                    dd_lon= float(lon_degree) + float(minutes_lon)/60 
                    if lon_dir == 'W':
                        dd_lon *= -1
                    if lat_dir == 'S':
                        dd_lat *= -1
 
                    utm_data3=utm.from_latlon(dd_lat,dd_lon)
                    print(utm_data3)
                    msg.header.stamp=rospy.get_rostime()
                    msg.header.frame_id="GPS_Data"
                    msg.latitude=dd_lat
                    msg.longitude=dd_lon
                    msg.altitude=float(alt)
                    msg.utm_easting=utm_data3[0]
                    msg.utm_northing=utm_data3[1]
                    msg.zone=float(utm_data3[2])
                    msg.letter_field=utm_data3[3]
                    rospy.loginfo(msg)
                    pub.publish(msg)
    except rospy.ROSInterruptException:
        port.close()
    
    except serial.serialutil.SerialException:
        rospy.loginfo("Shutting down paro_depth node...")
