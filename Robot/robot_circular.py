from pymycobot.mycobot import MyCobot
import serial
import time
import random
import math
import csv
import threading

def circle_random_select(m, n):
  radius = r *math.sqrt(random.random())
  angle = 2 * math.pi * random.random()
  x = m + radius * math.cos(angle)
  y = n + radius * math.sin(angle)
  return x, y

def read_latest_line():
    global ser
    buffer = b''
    latest_line = None
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            buffer += data
            lines = buffer.split(b'\n')
            if len(lines) >= 3:
                if lines[-1] == b'':
                    latest_line = lines[-2]
                    buffer = b''
            if latest_line is not None:
                return latest_line.decode()
                #else:
                    #buffer = lines[-1] + b'\n'

# Function to move the robot randomly in a circle and read data from the serial port
def move_and_read_data(count):
    global data_counter, file_counter, file, file1, writer1, writer2, writer3
    x, y = circle_random_select(216.7, -34.5)
    print("=====================Count:", count + 1)
    mc.sync_send_coords([x, y, 26, 180, 0, 0], 30, 1)
    cur = mc.get_coords()
    print("move:", cur)

    # Read data from the serial port and write to the respective CSV files
    data_str = read_latest_line()
    writer3.writerow([data_str])

    down = cur
    down[2] = cur[2] - height
    mc.sync_send_coords(down, 20, 1)
    cur1 = mc.get_coords()
    writer2.writerow([cur1])
    print("down:", cur1)

    time.sleep(3)

    data_str1 = read_latest_line()
    writer1.writerow([data_str1])
    data_counter += 1
    time.sleep(1)

    up = down
    up[2] = down[2] + height
    mc.sync_send_coords(up, 30, 1)
    cur2 = mc.get_coords()
    print("up:", cur2)

    if data_counter % 200 == 0:
        # Close the current file
        file.close()
        file1.close()
        file_counter += 1
        file = open(f'output{file_counter}.csv', 'w', newline='')
        file1 = open(f'before{file_counter}.csv', 'w', newline='')
        writer1 = csv.writer(file)
        writer3 = csv.writer(file1)



mc = MyCobot('/dev/ttyAMA0', 1000000)
mc.power_on()
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)


print("Start.")
#time.sleep(3)
#robot starting position is origin
mc.sync_send_coords([200,0,50,180,0,0],12,1)
time.sleep(1)
origin = mc.get_coords()
height = 40
print("origin:",origin)
r = 45  

data_counter = 0
file_counter = 1
file = open(f'output{file_counter}.csv', 'w', newline='')
pos = open(f'coord.csv', 'w', newline='')
file1 = open(f'before{file_counter}.csv', 'w', newline='')
writer1 = csv.writer(file)
writer2 = csv.writer(pos)
writer3 = csv.writer(file1)
# Start the thread to read data from the serial port continuously
serial_thread = threading.Thread(target=read_latest_line)
serial_thread.daemon = True
serial_thread.start()

for count in range(1400):
    move_and_read_data(count)

mc.send_coords(origin,30,1)

    # Close the last file
if not file.closed:
    file.close()
    pos.close()
    file1.close()
