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

#Calculates the total acceleration from x, y and z acceleration
def get_total_acceleration(acc_x, acc_y, acc_z):
    return 0

#Takes in filename and writes data into the .txt file
def write_to_file(filename, data):
    return 0

def main():
    mpu1 = mpu6050(0x68)
    mpu1 = mpu6050(0x????) #Fill out adress



if __name__ == "__main__":
    main()