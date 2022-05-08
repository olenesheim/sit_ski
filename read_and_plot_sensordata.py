import readline
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import scipy.integrate as sci

#Takes in filename and returns values separated by ; as arrays
def file_to_array(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()

    acc1_x = []
    acc1_y = []
    acc1_z = []
    acc2_x = []
    acc2_y = []
    acc2_z = []

    #Manually removing " ; , ( ) " and space from text-line
    for i in lines:
        acc1string = f"{i}".split(";")[0]
        acc2string = f"{i}".split(";")[1]

        #Treating acceleration data from first sensor
        x1 = f"{acc1string}".split(",")[0]
        x1_float = float(f"{x1}".split("(")[1])
        acc1_x.append(x1_float)
        y1 = f"{acc1string}".split(",")[1]
        y1_float = float(f"{y1}".split(" ")[1])
        acc1_y.append(y1_float)
        z1 = f"{acc1string}".split(",")[2]
        z1_2 = f"{z1}".split(")")[0]
        z1_float = float(f"{z1_2}".split(" ")[1])
        acc1_z.append(z1_float)

        #Treating acceleration data from second sensor
        x2 = f"{acc2string}".split(",")[0]
        x2_float = float(f"{x2}".split("(")[1])
        acc2_x.append(x2_float)
        y2 = f"{acc2string}".split(",")[1]
        y2_float = float(f"{y2}".split(" ")[1])
        acc2_y.append(y2_float)
        z2 = f"{acc2string}".split(",")[2]
        z2_2 = f"{z2}".split(")")[0]
        z2_float = float(f"{z2_2}".split(" ")[1])
        acc2_z.append(z2_float)

    return acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z

#Transforms acceleration data to velocity data
def acc_to_vel(acc, init):
    x = np.linspace(0, len(acc) - 1, len(acc))
    y = sci.cumtrapz(acc, x, initial = init)
    return y

#Returns the position/velocity/acceleration of sensor1 relative to sensor2
def relvel(sensor1, sensor2):
    s1 = []
    n = 0
    for i in sensor1:
        s1.append(i - sensor2[n])
        n += 1
    return s1

#Finds the total acceleration using the Euclidean vector-norm
def get_total_acceleration_array(acc_x, acc_y, acc_z):
    total_acceleration = [] 
    for i in range(len(acc_x)):
        total_acceleration.append(np.sqrt(acc_x[i]*acc_x[i] + acc_y[i]*acc_y[i] + acc_z[i]*acc_z[i]))
    return total_acceleration

#Takes in 2 columns of acceleration and plots them and the difference between
def plot_acceleration(acc1, acc2, acc3, title):
    x = np.linspace(0, len(acc1) - 1, len(acc1))

    #acc1 = acc_to_vel(acc1, 0)
    #acc2 = acc_to_vel(acc2, 0)
    #acc2 = acc_to_vel(acc2, 0)
    
    #acc2 = relvel(acc2, acc1)
    # rel_acc = relvel(acc2, acc1)

    plt.plot(x, acc1)
    plt.plot(x, acc2)
    plt.plot(x, acc3)
    #plt.plot(x, rel_acc)
    plt.title(title)
    plt.show()

    return 0

#Makes 4 plots: x, y, z, and avg
def plot_xyz(acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z, acc1_tot, acc2_tot, name_x, name_y, name_z, name_tot, name, lowerlim, higherlim):
    x = np.linspace(0, len(acc1_x) - 1, len(acc1_x))
    fig, axs = plt.subplots(4, 2)
    fig.suptitle(name)
    #First plot
    axs[0, 0].plot(x, acc1_x)
    axs[0, 0].set_title(name_x)
    axs[0, 0].set_ylim([lowerlim, higherlim])
    #Second plot
    axs[1, 0].plot(x, acc1_y)
    axs[1, 0].set_title(name_y)
    axs[1, 0].set_ylim([lowerlim, higherlim])
    #Third plot
    axs[2, 0].plot(x, acc1_z)
    axs[2, 0].set_title(name_z)
    axs[2, 0].set_ylim([lowerlim, higherlim])
    #Fourth plot
    axs[3, 0].plot(x, acc1_tot)
    axs[3, 0].set_title(name_tot)
    axs[3, 0].set_ylim([lowerlim, higherlim])
    #Fifth plot
    axs[0, 1].plot(x, acc2_x)
    axs[0, 1].set_title("chest1")
    axs[0, 1].set_ylim([lowerlim, higherlim])

    axs[1, 1].plot(x, acc2_y)
    axs[1, 1].set_title("chest2")
    axs[1, 1].set_ylim([lowerlim, higherlim])

    axs[2, 1].plot(x, acc2_z)
    axs[2, 1].set_title("chest3")
    axs[2, 1].set_ylim([lowerlim, higherlim])

    axs[3, 1].plot(x, acc2_tot)
    axs[3, 1].set_title("chest4")
    axs[3, 1].set_ylim([lowerlim, higherlim])
    plt.show()
    return 0

# def plot_3d(acc1_x, acc1_y, acc1_z, title):
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#     ax.plot3D(acc1_x, acc1_y, acc1_z, 'gray')
#     ax.scatter3D(acc1_x, acc1_y, acc1_z, c=acc1_z, cmap='Greens')
#     plt.show()
#     return 0

def trim_data(data, start, stop):
    trimmed_data = []
    for i in range(stop - start):
        trimmed_data.append(data[i + start])
    return trimmed_data

def trim_accelerations(acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z, start, stop):
    a1x = trim_data(acc1_x, start, stop)
    a1y = trim_data(acc1_y, start, stop)
    a1z = trim_data(acc1_z, start, stop)
    a2x = trim_data(acc2_x, start, stop)
    a2y = trim_data(acc2_y, start, stop)
    a2z = trim_data(acc2_z, start, stop)
    return a1x, a1y, a1z, a2x, a2y, a2z


def main():
    # Sensor 1 = Sit-ski sensor
    # Sensor 2 = Chest sensor

    acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z = file_to_array("run1.txt") 
    acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z = trim_accelerations(acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z, 3780, 6280)
    acc_tot_1 = get_total_acceleration_array(acc1_x, acc1_y, acc1_z)
    acc_tot_2 = get_total_acceleration_array(acc2_x, acc2_y, acc2_z)

    # plot_acceleration(acc2_x, acc2_y, acc2_z, "Run 1, xyz")

    # plot_3d(acc1_x, acc1_y, acc1_z, "3D plot")
    plot_xyz(acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z, acc_tot_1, acc_tot_2, "x", "y", "z", "Avg.", "Acceleration in individual axes - Run 1", -20, 20)
    # plot_acceleration(acc1_x, acc2_x, "x-acceleration")
    # plot_acceleration(acc_tot_1, acc_tot_2, "Total acceleration")
    return 0

if __name__=="__main__":
    main()