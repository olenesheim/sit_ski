from cmath import sqrt
from unicodedata import name
from mpu6050 import mpu6050
import time

#Takes in filename and creates a .txt file for later use
def create_file():
    created_file = 0
    return created_file

#Takes in the specific sensor and returns the acceleration data (x, y and z)
def get_acceleration(sensor):
    return 0

#Takes in a sensor and returns the total accelearation based on 3D pytagoras
def get_total_acceleration(sensor):
    acc = sensor.get_accel_data()
    acc_x = acc['x']
    acc_y = acc['y']
    acc_z = acc['z']
    total_acceleration = sqrt(acc_x*acc_x + acc_y*acc_y + acc_z*acc_z)
    return total_acceleration

#Takes in filename and writes data into the .txt file
def write_to_file(filename, data):
    return 0

def main():
    mpu1 = mpu6050(0x68, 1)     #Inititalizes mpu6050 on bus 1
    mpu2 = mpu6050(0x68, 3)     #Inititalizes mpu6050 on bus 3

    while True:

        acc = get_total_acceleration(mpu2)
        print(acc)


  #      acc1 = mpu1.get_accel_data()
 #       acc2 = mpu2.get_accel_data()

#        print("Sensor 1: ", str(acc1['x']), "; Sensor 2: ", str(acc2['x']), "\n")
        time.sleep(0.05)



if __name__ == "__main__":
    main()