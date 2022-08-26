from mpu6050 import mpu6050
from cmath import sqrt
import sys
import time

#Takes in a sensor and returns the total accelearation based on the euclidean vector norm
def get_total_acceleration(sensor):
    acc = sensor.get_accel_data()
    acc_x = acc['x']
    acc_y = acc['y']
    acc_z = acc['z']
    total_acceleration = sqrt(acc_x*acc_x + acc_y*acc_y + acc_z*acc_z)
    return total_acceleration

def acc_to_g(acc):
    g = acc / 9.81
    return g

#Takes in filename and writes data into the .txt file.
#freq is the frequency of the measurements, no_datapoints is the number of datapoints
def write_to_file(freq, no_datapoints, filename, sensor):   
    f = open(filename, "w+")

    for i in range (no_datapoints):
        acc = get_total_acceleration(sensor)
        print("G´s: " + str(round(acc_to_g(acc), 2)))
        f.write(f"{acc}\n")
        time.sleep(1/freq)

    f.close()    
    return 0