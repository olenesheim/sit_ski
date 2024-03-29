from mpu6050 import mpu6050
from cmath import sqrt
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD 
import sys
import time

def safe_exit(signum, frame):
    exit(1)

def write_to_lcd(text):
    lcd = LCD()
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.text(text, 1)
    return 0

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
        acc = acc.real
        text = str(round(acc_to_g(acc), 2)) + "G"
        print("Gravity: " + text)
        write_to_lcd(text)
        #print(acc)
        f.write(f"{acc}\n")
        time.sleep(1/freq)

    f.close()    
    return 0

def main(filename, freq, no_datapoints):
    mpu1 = mpu6050(0x68, 1)     #Inititalizes mpu6050 on bus 1
    write_to_file(int(freq), int(no_datapoints), filename, mpu1)  #Writes the sesnsor data from both sensors into a text file

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])