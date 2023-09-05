from pymycobot.mycobot import MyCobot
import time
import random




mc = MyCobot('/dev/ttyAMA0',1000000)

time.sleep(5)
corner1= mc.get_coords()
print("corner1: " + str(corner1) + "\n")
time.sleep(8)
corner2= mc.get_coords()
print("corner2: " + str(corner2) + "\n")
time.sleep(8)
corner3= mc.get_coords()
print("corner3: " + str(corner3) + "\n")
time.sleep(8)
corner4= mc.get_coords()
print("corner4: " + str(corner4) + "\n")
time.sleep(8)
