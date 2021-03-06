import sys, getopt
import time
#from networktables import NetworkTables

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"
    
print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded");

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

#ip = "10.51.9.27"
# for the actual bot the ip is 10.51.9.2

#NetworkTables.initialize(server = ip)

#imutable = NetworkTables.getTable("IMU Table")

import logging
logging.basicConfig(level=logging.DEBUG)

# uncomment below to make the network tables work

while True:
  if imu.IMURead():
    # x, y, z = imu.getFusionData()
    # print("%f %f %f" % (x,y,z))
    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    print("roll: %f pitch: %f yaw: %f" % (math.degrees(fusionPose[0])+180, 
        math.degrees(fusionPose[1])+180, math.degrees(fusionPose[2])+180))
    #imutable.putNumber("roll", (math.degrees(fusionPose[0])))
    #imutable.putNumber("pitch", (math.degrees(fusionPose[1])))
    #imutable.putNumber("yaw", (math.degrees(fusionPose[2])))
    time.sleep(poll_interval*1.0/1000.0)

#imutable.putNumber("testVariable2", 101011)
#print(imutable.getNumber("testVariable2", "didn't work"))
#imutable.delete("testVariable2")
#print(imutable.containsKey("testVariable2"))
#print(imutable.getKeys())

