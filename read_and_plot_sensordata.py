from imghdr import what
from pickle import FALSE, TRUE
from statistics import mean
import sys
from turtle import end_fill
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as sci
from scipy.interpolate import interp1d
import matplotlib.ticker as mticker

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

#Trims the data from start to stop
def trim_data(data, start, stop):
    trimmed_data = []
    for i in range(stop - start):
        trimmed_data.append(data[i + start])
    return trimmed_data

#Assumes linear drift in a velocity data-set and compensates for this drift by subtracting that linear function
def drift_compensate(data):
    endvalue = data[len(data) - 1]
    no_points = len(data)
    specific_drift = endvalue / no_points
    comp_data = []
    for i in range(no_points):
        drift = i * specific_drift
        comp_data.append(data[i] - drift)
    return comp_data

#Function to smooth data
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

#Trims all data connected to one position
def trim_accelerations(acc1_x, acc1_y, acc1_z, acc2_x, acc2_y, acc2_z, start, stop):
    a1x = trim_data(acc1_x, start, stop)
    a1y = trim_data(acc1_y, start, stop)
    a1z = trim_data(acc1_z, start, stop)
    a2x = trim_data(acc2_x, start, stop)
    a2y = trim_data(acc2_y, start, stop)
    a2z = trim_data(acc2_z, start, stop)
    return a1x, a1y, a1z, a2x, a2y, a2z

#Interpolates a dataset and returns the dataset with the new desired table-length
def interpolate(data, new_table_length, freq):
    x = np.linspace(0, len(data), len(data))
    # x = np.linspace(0, len(data) / freq, len(data))
    f = interp1d(x, data, kind='linear')
    x_int = np.linspace(0, new_table_length, new_table_length + 1)
    new_y = f(x_int)
    new_x = np.linspace(0, len(new_y) / freq, len(new_y))
    return new_x, new_y

#Returns the mean dataset of dataset 1 and dataset 2, given they both have the same table-length
def mean_data(data1, data2):
    data = []
    for i in range(0, len(data1)):
        data.append((data1[i] + data2[i]) / 2)
    return data

#Returns the length of the shortest run
def find_shortest(run1, run2):
    shortest = len(run1)
    if len(run1) > len(run2):
        shortest = len(run2)
    return shortest

#Extracts the plot data needed to plot two runs in the same position. It returns the data from sensor 2 relative to sensor 2.
# The argument 'what_part' defines if the data from the whole run or just half is returned. 0 = whole run, 1 = half run
def get_plot_data(position, what_part):
    # Sensor 1 = Sit-ski sensor
    # Sensor 2 = Chest sensor

    #Array containing meta-data about each position: [1st run, 2nd run, startvalue1, endvalue1, startvalue2, endvalue2, title]
    what_run = np.array([   ["run1.txt", "run2.txt", 3750, 6280, 3275, 5680, "Position 1"],
                            ["run3.txt", "run4.txt", 1960, 4350, 4085, 6540, "Position 2"],
                            ["run5.txt", "run6.txt", 2650, 5510, 4950, 7700, "Position 3"],
                            ["run7.txt", "run8.txt", 1835, 4600, 4150, 7050, "Position 4"],
                            ["run9.txt", "run10.txt", 2330, 4950, 1800, 4500, "Position 5"],
                            ["run11.txt", "run12.txt", 2725, 5360, 5300, 7660, "Position 6"]])

    #Same array, but the limit-values are limited to before the mid-break
    what_run_fh = np.array([["run1.txt", "run2.txt", 3750, 4750, 3275, 4160, "Position 1"],
                            ["run3.txt", "run4.txt", 1960, 2925, 4085, 5030, "Position 2"],
                            ["run5.txt", "run6.txt", 2650, 3700, 4950, 6010, "Position 3"],
                            ["run7.txt", "run8.txt", 1835, 2980, 4150, 5180, "Position 4"],
                            ["run9.txt", "run10.txt", 2330, 3350, 1800, 2775, "Position 5"],
                            ["run11.txt", "run12.txt", 2725, 3730, 5300, 6250, "Position 6"]])

    #Extract files
    file1 = what_run[position - 1][0]
    file2 = what_run[position - 1][1]
    run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z = file_to_array(file1)
    run2_s1_x, run2_s1_y, run2_s1_z, run2_s2_x, run2_s2_y, run2_s2_z = file_to_array(file2)

    if what_part == 0:
        #Filedata for whole run
        start1 = int(what_run[position - 1][2])
        end1 = int(what_run[position - 1][3])
        start2 = int(what_run[position - 1][4])
        end2 = int(what_run[position - 1][5])
        name = what_run[position - 1][6]
    elif what_part == 1:
        #File data for half run
        start1 = int(what_run_fh[position - 1][2])
        end1 = int(what_run_fh[position - 1][3])
        start2 = int(what_run_fh[position - 1][4])
        end2 = int(what_run_fh[position - 1][5])
        name = what_run_fh[position - 1][6]
    elif what_part == 2:
        return run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z

    run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z = trim_accelerations(run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z, start1, end1)
    run2_s1_x, run2_s1_y, run2_s1_z, run2_s2_x, run2_s2_y, run2_s2_z = trim_accelerations(run2_s1_x, run2_s1_y, run2_s1_z, run2_s2_x, run2_s2_y, run2_s2_z, start2, end2)
    acc_tot_11 = get_total_acceleration_array(run1_s1_x, run1_s1_y, run1_s1_z)
    acc_tot_12 = get_total_acceleration_array(run1_s2_x, run1_s2_y, run1_s2_z)
    acc_tot_21 = get_total_acceleration_array(run2_s1_x, run2_s1_y, run2_s1_z)
    acc_tot_22 = get_total_acceleration_array(run2_s2_x, run2_s2_y, run2_s2_z)
    return acc_tot_11, acc_tot_12, acc_tot_21, acc_tot_22, name, run1_s2_z, run2_s2_z

# FUNKER! Plots the whole acceleration data from two data-sets
def plot_acceleration(run1, run2, title, plot_name1, plot_name2):
    x1 = np.linspace(0, len(run1) - 1, len(run1))
    x2 = np.linspace(0, len(run2) - 1, len(run2))
    plt.plot(x1, run1)
    plt.plot(x2, run2)
    plt.legend([plot_name1, plot_name2])
    plt.xlabel("Datapoint, N")
    plt.ylabel("Acceleration " + r'$[m/s^2]$')
    plt.title(title)
    plt.show()
    return 0

# FUNKER! Takes in 
def plot_relative_acceleration(position, freq):
    a11, a12, a21, a22, name, z1, z2 = get_plot_data(int(position), 0)
    a1 = relvel(a12, a11)
    a2 = relvel(a22, a21)
    x1 = np.linspace(0, len(a1) / freq, len(a1))
    x2 = np.linspace(0, len(a2) / freq, len(a2))
    plt.plot(x1, a1)
    plt.plot(x2, a2)
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration " r'$[m/s^2]$')
    plt.ylim(-15, 15)
    plt.xlim(0, 60)
    plt.legend(["Run 1", "Run 2"], loc=1)
    plt.title(name)
    plt.show()

# FUNKER! Takes in data from 2 runs and plots the velocity from both runs
def plot_velocity(position, freq, drift_comp):
    a11, a12, a21, a22, name, z1, z2 = get_plot_data(int(position), 0)
    rel_acc_run1 = relvel(a12, a11)
    rel_acc_run2 = relvel(a22, a21)
    x1 = np.linspace(0, len(rel_acc_run1) / freq, len(rel_acc_run1))
    x2 = np.linspace(0, len(rel_acc_run2) / freq, len(rel_acc_run2))
    #Transforms from acceleration to velocity
    run1 = acc_to_vel(rel_acc_run1, 0)
    run2 = acc_to_vel(rel_acc_run2, 0)
    #Compensate for linear drift
    if drift_comp == TRUE:
        run1 = drift_compensate(run1)
        run2 = drift_compensate(run2)
    plt.plot(x1, run1)
    plt.plot(x2, run2)
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.legend(["Run 1", "Run 2"], loc = 1)
    plt.title(name)
    plt.show()
    return 0

#FUNKER! Takes in data from 2 runs and plots the acceleration, amplitude and frequency of that data
def plot_acceleration_and_amplitude(run1, run2, title, freq):
    shortest = find_shortest(run1, run2)
    #Creates interpolated functions of the data
    intx1, intrun1 = interpolate(run1, shortest, freq)
    intx2, intrun2 = interpolate(run2, shortest, freq)
    #Smooth data
    intrun1_smooth = smooth(intrun1, 15)
    intrun2_smooth = smooth(intrun2, 15)
    amp_factor = 200
    freq_factor = 10
    #Fourier transform
    intrun1_fft = abs(np.fft.rfft(intrun1_smooth/amp_factor))
    intrun2_fft = abs(np.fft.rfft(intrun2_smooth/amp_factor))
    #Create subplots for viewing fourier transform
    a = plt.subplot(211)
    a.set_xlabel("Time [s]")
    a.set_ylabel('Acceleration ' + r'$[m/s^{2}]$')
    a.grid()
    plt.plot(intx1, intrun1_smooth)
    plt.plot(intx1, intrun2_smooth)
    plt.xlim(0, 22)
    plt.ylim(-8, 6)
    plt.title(title)
    b = plt.subplot(212)
    b.grid(True, which="both")
    b.set_xscale('log')
    b.set_xlabel('Frequency [Hz]')
    b.set_ylabel('|Amplitude| ' + r'$[m/s^{2}]$')
    x = np.linspace(0, len(intrun1_fft) - 1, len(intrun1_fft))
    plt.xlim(1, 4)
    plt.ylim(0, 10)
    plt.plot(x/freq_factor, intrun1_fft)
    plt.plot(x/freq_factor, intrun2_fft)
    plt.subplots_adjust(left=0.114, bottom=0.11, right=0.98, top=0.936, hspace=0.294)
    plt.show()
    return 0

# FUNKER! Plots the velocity calculated from the acceleration from all positions and compares them in one graph
def plot_all_velocities(freq, drift_comp):
    names = []
    for i in range(1, 7):
        a11, a12, a21, a22, name, z1, z2 = get_plot_data(i, 0)
        rel_acc_run1 = relvel(a12, a11)
        rel_acc_run2 = relvel(a22, a21)
        names.append(name)
        run1 = acc_to_vel(rel_acc_run1, 0)
        run2 = acc_to_vel(rel_acc_run2, 0)
        shortest = find_shortest(run1, run2)
        intx1, intrun1 = interpolate(run1, shortest, freq)
        intx2, intrun2 = interpolate(run2, shortest, freq)
        if drift_comp == TRUE:
            intrun1 = drift_compensate(intrun1)
            intrun2 = drift_compensate(intrun2)
        mean_run = mean_data(intrun1, intrun2)
        plt.fill_between(intx1, intrun1, intrun2, alpha=0.3)
        plt.plot(intx1, mean_run)
    plt.legend([names[0], names[1], names[2], names[3], names[4], names[5]])
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.title("All positions")
    plt.show()
    return 0

# FUNKER! Plots acceleration from all positions and the amplitude over frequency for all positions
def plot_all_fourier():
    names = []
    for i in range(1, 7):
        a11, a12, a21, a22, name, r1s2z, r2s2z = get_plot_data(i, 1)
        names.append(name)
        shortest = len(r1s2z)
        if len(r1s2z) > len(r2s2z):
            shortest = len(r2s2z)
        intx1, intrun1 = interpolate(r1s2z, shortest, 50)
        intx2, intrun2 = interpolate(r2s2z, shortest, 50)
        #Smooth data
        intrun1_smooth = smooth(intrun1, 15)
        intrun2_smooth = smooth(intrun2, 15)
        amp_factor = 200
        freq_factor = 10
        #Fourier transform
        intrun1_fft = abs(np.fft.rfft(intrun1_smooth/amp_factor))
        intrun2_fft = abs(np.fft.rfft(intrun2_smooth/amp_factor))
        #Create mean graphs
        mean_run = mean_data(intrun1_smooth, intrun2_smooth)
        mean_fft = mean_data(intrun1_fft, intrun2_fft)
        #Create subplots for viewing fourier transform
        a = plt.subplot(211)
        a.set_xlabel("Time [s]")
        a.set_ylabel("Acceleration [m/s^2]")
        plt.fill_between(intx1, intrun1_smooth, intrun2_smooth, alpha=0.3)
        plt.plot(intx1, mean_run)
        b = plt.subplot(212)
        b.grid()
        b.set_xscale('log')
        b.set_xlabel('frequency [Hz]')
        b.set_ylabel('|amplitude|')
        x = np.linspace(0, len(intrun1_fft) - 1, len(intrun1_fft))
        plt.fill_between(x/freq_factor, intrun1_fft, intrun2_fft, alpha=0.6)
        plt.plot(x/freq_factor, mean_fft)
    plt.legend([names[0], names[1], names[2], names[3], names[4], names[5]])
    plt.title("All positions")
    plt.show()
    return 0

#Makes 8 plots: x, y, z, and avg for two inputs
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
    #Sixth plot
    axs[1, 1].plot(x, acc2_y)
    axs[1, 1].set_title("chest2")
    axs[1, 1].set_ylim([lowerlim, higherlim])
    #Seventh plot
    axs[2, 1].plot(x, acc2_z)
    axs[2, 1].set_title("chest3")
    axs[2, 1].set_ylim([lowerlim, higherlim])
    #Eigth plot
    axs[3, 1].plot(x, acc2_tot)
    axs[3, 1].set_title("chest avg.")
    axs[3, 1].set_ylim([lowerlim, higherlim])
    plt.show()
    return 0

# FUNKER! Plots the acceleration data from all three axes from both sensors
def plot_three_axes(run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z):
    plt.title("Run 1 - Acceleration data")
    a = plt.subplot(311)
    plt.title("x axis")
    plt.plot(run1_s1_x)
    plt.plot(run1_s2_x)
    plt.tick_params('x', labelbottom=False)
    plt.legend(["Sensor 1", "Sensor 2"])
    b = plt.subplot(312, sharex = a)
    plt.title("y axis")
    plt.plot(run1_s1_y)
    plt.plot(run1_s2_y)
    plt.tick_params('x', labelbottom=False)
    plt.ylabel("Acceleration " + r'$[m/s^2]$')
    c = plt.subplot(313, sharex = b)
    plt.title("z axis")
    plt.plot(run1_s1_z)
    plt.plot(run1_s2_z)
    plt.xlabel("Datapoint [N]")
    plt.show()
    return 0

# FUNKER! Takes a list of positions and plots the amplitude and frequency of the z-axis on the chest sensor in those positions from both runs. 
def plot_compare_ftt(positions, freq=50):
    names = []
    for i in positions:
        a11, a12, a21, a22, name, run1, run2 = get_plot_data(i, 1)
        names.append(name)
        shortest = find_shortest(run1, run2)
        amp_factor = 200
        freq_factor = 10
        #Interpolating data
        intx1, intrun1 = interpolate(run1, shortest, freq)
        intx2, intrun2 = interpolate(run2, shortest, freq)
        #Smooth data
        run1_smooth = smooth(intrun1, 15)
        run2_smooth = smooth(intrun2, 15)
        #Fourier transform
        run1_fft = abs(np.fft.rfft(run1_smooth/amp_factor))
        run2_fft = abs(np.fft.rfft(run2_smooth/amp_factor))
        a = plt.subplot()
        a.set_xscale('log')
        a.xaxis.set_major_formatter(mticker.ScalarFormatter())
        mean_fft = mean_data(run1_fft, run2_fft)
        x = np.linspace(0, len(run1_fft) - 1, len(run1_fft))
        plt.fill_between(x/freq_factor, run1_fft, run2_fft, alpha=0.5) 
        plt.plot(x/freq_factor, mean_fft)
        plt.xticks(np.arange(min(x), max(x)+1, 0.1))
        plt.xlim(1, 4)
    plt.subplots_adjust(left=0.05, bottom=0.095, right=0.996, top=0.985, hspace=0.294)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude " + r'$[m/s^2]$')
    plt.grid(True, which="both")
    plt.legend([names[0], names[1], names[2], names[3], names[4], names[5]], loc=1)
    plt.show()
    return 0

def main(position):
    #UNCOMMENT THE PROGRAM YOU WANT TO RUN


    # Program for plotting graph comparing amplitude and frequency of different positions
    positions = [1, 2, 3, 4, 5, 6]
    plot_compare_ftt(positions)

    
    # # Program for plotting acceleration, amplitude and frequency for all positions in the same graph
    # plot_all_fourier()

    
    # # Program for plotting all acceleration-data from a given position in the first run
    # run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z = get_plot_data(int(position), 2)
    # plot_three_axes(run1_s1_x, run1_s1_y, run1_s1_z, run1_s2_x, run1_s2_y, run1_s2_z)

    
    # # Program for plotting the relative acceleration of both runs in each position
    # for i in range(1, 7):
    #     plot_relative_acceleration(i, 50)


    # # Program for plotting velocities in one given position without drift compensation
    # for i in range(1, 7):
    #     plot_velocity(i, 50, FALSE)


    # # Program for plotting velocities in one given position with drift compensation
    # for i in range(1, 7):
    #     plot_velocity(i, 50, TRUE)


    # # Program for plotting velocity calculated from the acceleration data in all positions without drift compensation
    # plot_all_velocities(50, FALSE)


    # # Program for plotting velocity calculated from the acceleration data in all positions with drift compensation
    # plot_all_velocities(50, TRUE)


    # # Program for plotting acceleration, amplitude and frequency for one and one position
    # for i in range(1,7):
    #     a11, a12, a21, a22, name, r1s2z, r2s2z = get_plot_data(i, 1)
    #     plot_acceleration_and_amplitude(r1s2z, r2s2z, "Position " + str(i) + " - Acceleration, Frequency and Amplitude", 50)


    # # Program to find acceleration data of one whole dataset in one run
    # r1s1x, r1s1y, r1s1z, r1s2x, r1s2y, r1s2z = file_to_array("run2.txt")
    # acc_tot_11 = get_total_acceleration_array(r1s1x, r1s1y, r1s1z)
    # acc_tot_12 = get_total_acceleration_array(r1s2x, r1s2y, r1s2z)
    # plot_acceleration(acc_tot_11, acc_tot_12, "Run 2", "Sensor 1", "Sensor 2")

    return 0

if __name__=="__main__":
    main(sys.argv[1])