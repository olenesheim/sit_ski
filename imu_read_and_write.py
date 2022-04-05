from cmath import sqrt
from unicodedata import name
from mpu6050 import mpu6050
import time

#Takes in a sensor and returns the total accelearation based on 3D pytagoras
def get_total_acceleration(sensor):
    acc = sensor.get_accel_data()
    acc_x = acc['x']
    acc_y = acc['y']
    acc_z = acc['z']
    total_acceleration = sqrt(acc_x*acc_x + acc_y*acc_y + acc_z*acc_z)
    return total_acceleration


#Takes in filename and creates a .txt file for later use
def create_file():
    created_file = 0
    return created_file

#Takes in filename and writes data into the .txt file
def write_to_file(filename, data):
    return 0



def main():
    mpu1 = mpu6050(0x68, 1)     #Inititalizes mpu6050 on bus 1
    mpu2 = mpu6050(0x68, 3)     #Inititalizes mpu6050 on bus 3

    f = open("test5.txt", "w+")

#    while True:
    for i in range(50):

        acc1 = get_total_acceleration(mpu1)
        acc2 = get_total_acceleration(mpu2)

        print("%s;%s\n" % (acc1, acc2))

        #f.write("%s;%s\n" % (acc1, acc2))
        acc1string = f"{acc1:.5f}".split("+")[0]
        acc2string = f"{acc2:.5f}".split("+")[0]
        f.write(f"{acc1string};{acc2string}\n")

        time.sleep(0.5)
    f.close()



if __name__ == "__main__":
    main()