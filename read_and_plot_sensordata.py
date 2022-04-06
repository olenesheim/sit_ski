import readline
import matplotlib.pyplot as plt
import numpy as np

#Takes in filename and returns values separated by ; as arrays
def file_to_array(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()

    acc1 = []
    acc2 = []

    for i in lines:
        acc1string = f"{i}".split(";")[0]
        acc2string = f"{i}".split(";")[1]
        acc1.append(float(acc1string))
        acc2.append(float(acc2string))
    
    return acc1, acc2

#Takes in 2 columns of acceleration and plots them and the difference between
def plot_acceleration(acc1, acc2):
    x = np.linspace(0, len(acc1) - 1, 300)
    fig, axs = plt.subplots(2)
    fig.suptitle("Sensors")
    axs[0].plot(x, acc1)
    axs[0].set_title("Sensor 1")
    axs[1].plot(x, acc2)
    axs[1].set_title("Sensor 2")
    plt.show()

    # plt.plot(x, acc1)
    # plt.legend(["Sensor 1"])
    # plt.title("Sensor 1")
    # plt.plot(x, acc2)
    # plt.legend(["Sensor 2"])
    # plt.title("Sensor 2")
    # plt.show()
    
    return 0


def main():
    acc1, acc2 = file_to_array("test13.txt")
    plot_acceleration(acc1, acc2)
    return 0

if __name__=="__main__":
    main()