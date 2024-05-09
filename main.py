# Import statements
import random
import qwiicscale
import time
import matplotlib as mpl
import numpy as np
import cayenne.client
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import keyboard
import blynklib


##Variables, class and functions set
qwiic = qwiicscale.QwiicScale()
average = []
resultsoutput =[]
calzero = "n"
calweight = "n"
CalibrateZero=0
x=[]
y=[]
timeav = []


listtest = [5, 8, 7, 3, 3, 6, 10, 4, 9, 9, 4, 2, 1, 3, 4, 6, 5, 1, 9, 10, 5, 3, 10, 1]



def getav(numbers):
    resultsoutput = []
    x=0
    avgweights=0
    y=6
    counter = 0
    for z in range(0,len(numbers)):
        average.append(numbers[z])
    while counter != 4:
        for i in range(x,y):
            avgweights += average[i]
        result = (avgweights/6)-CalibrateZero
        resultsoutput.append(result)
        timeav.append(time.time()-timebegin)
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
    blynk = blynklib.Blynk('WJbSxpdW_KDfcH1BnAtdHlX6vxxeAXRZ')
    @blynk.
    while calzero != "n":
        input('Qwiic calibration. Press any key when device is not under strain.')
        CalibrateZero = qwiic.getAverage(averageAmount=64)
        calzero = input(f'Calibration succeeded. Current offset set to {CalibrateZero}. Redo calibration? (y/n)')
    while calweight != "n":
        input("Qwiic calibration. Press any key when device is under known weight.")
        CalibrateWeight = qwiic.getAverage(averageAmount=64)
        knownweight = int(input("How much does the weight equal in kilos?"))*9.81
        calweight = input(f'Calibration succeeded. Current strain set to {CalibrateWeight} under a force of {knownweight}.')






    while input() != "scalestop":
        currentreading = qwiic.getReading()
        print(currentreading)
        getav(currentreading)
        time.sleep(0.5)

looping = True
time2 = int(input("Hoeveel seconden wil je de grafiek zien? "))
timebegin = time.time()


'''while looping:
    timeav =[]
    currentreading = qwiic.getReading()
    print(currentreading)
    numbers = getav(currentreading)
    numbers = getav(listtest)
    for z in range(0,4):
        y.append(numbers[z])
        x.append(timeav[z])
    x.append(time.time())
    y.append(random.random())
    if time.time()-timebegin > time2:
        x = x[4:]
        y = y[4:]
    pyplot.clf()
    pyplot.plot(x,y)
    pyplot.draw()
    pyplot.pause(0.03) # Tijd instellen op basis van metingen per seconde => momenteel 16 per seconde'''


