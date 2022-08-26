from cmath import sqrt
from unicodedata import name
from mpu6050 import mpu6050
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

#Takes in a sensor and returns all acceleration-data in 3 different variables
def get_raw_accel_data(sensor):
    acc = sensor.get_accel_data()
    acc_x = acc['x']
    acc_y = acc['y']
    acc_z = acc['z']
    return acc_x, acc_y, acc_z

#Takes in filename and writes data into the .txt file.
#freq is the frequency of the measurements, no_datapoints is the number of datapoints
def write_to_file(freq, no_datapoints, filename, sensor1, sensor2):   
    f = open(filename, "w+")

    for i in range (no_datapoints):
        acc1 = get_raw_accel_data(sensor1)
        acc2 = get_raw_accel_data(sensor2)
        #print(acc1, "       ", acc2)
        f.write(f"{acc1};{acc2}\n")
        time.sleep(1/freq)


    # for i in range (no_datapoints):
    #     acc1 = get_total_acceleration(sensor1)  #Getting acceleration data from sensor 1 (still sensor)
    #     acc2 = get_total_acceleration(sensor2)  #Getting acceleration data from sensor 2 (Chest)
    #     #print(f"{acc1:.5f}".split("+")[0], "       ", f"{acc2:.5f}".split("+")[0])
    #     full_acc1 = sensor1.get_accel_data()
    #     full_acc2 = sensor2.get_accel_data()
    #     print(full_acc1, "         ", full_acc2)
    #     acc1string = f"{acc1:.5f}".split("+")[0]
    #     acc2string = f"{acc2:.5f}".split("+")[0]
    #     f.write(f"{acc1string};{acc2string}\n")
    #     time.sleep(1/freq)

    f.close()    
    return 0

def main(filename, freq, no_datapoints):
    mpu1 = mpu6050(0x68, 1)     #Inititalizes mpu6050 on bus 1
    mpu2 = mpu6050(0x68, 3)     #Inititalizes mpu6050 on bus 3
    write_to_file(int(freq), int(no_datapoints), filename, mpu1, mpu2)  #Writes the sesnsor data from both sensors into a text file

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])