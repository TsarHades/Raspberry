# Import statements
import qwiicscale
import time
import matplotlib as mpl
import numpy as np


##Variables, class and functions set
qwiic = qwiicscale.QwiicScale()
average = []
resultsoutput =[]
def getav(numbers):
    x=0
    avgweights=0
    y=6
    counter = 0
    for z in range(0,len(numbers)):
        average.append(numbers[z])
    while counter != 4:
        for i in range(x,y):
            avgweights += average[i]
            print(average[i])
        print(avgweights)
        print("done")
        result = avgweights/6
        resultsoutput.append(result)
        x = y
        y += 6
        result = 0
        counter +=1
        avgweights = 0
    return resultsoutput



if __name__ == '__main__':
    qwiic.begin()
    connection = qwiic.is_connected()
    print(connection)
    qwiic.available()


    input('Qwiic calibration. Press any key when device is not under strain.')
    qwiic.calculateZeroOffset(64)
    print(f"Offset set to: {qwiic.getZeroOfset()}")

    while input() != "scalestop":
        currentreading = qwiic.getReading()
        print(currentreading)
        getav(currentreading)
        time.sleep(0.5)




