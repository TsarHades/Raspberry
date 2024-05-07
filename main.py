# Import statements
import datetime
import random

import qwiicscale
import time
import matplotlib as mpl
import numpy as np
import cayenne.client
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation


##Variables, class and functions set
'''qwiic = qwiicscale.QwiicScale()'''
average = []
resultsoutput =[]
calzero = "n"
calweight = "n"
CalibrateZero=0
x=[]
y=[]

'''MQTT_USERNAME = "2444e11b-393c-4cd8-8171-61ad9d5b9c82"
MQTT_PASSWORD = "00000000FA5841E1"
MQTT_CLIENT_ID = "15F9EB1C"
HOSTNAME = "mqtt.zafron.dev"
client = cayenne.client.CayenneMQTTClient()
client.begin(MQTT_USERNAME,MQTT_PASSWORD,MQTT_CLIENT_ID,hostname=HOSTNAME)'''

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
        result = (avgweights/6)-CalibrateZero
        resultsoutput.append(result)
        x = y
        y += 6
        result = 0
        counter +=1
        avgweights = 0
    return resultsoutput



'''if __name__ == '__main__':
    qwiic.begin()
    connection = qwiic.is_connected()
    print(connection)
    qwiic.available()

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
        time.sleep(0.5)'''

print("yes")
while 1 != 2 :
    listtest = [5,8,7,3,3,6,10,4,9,9,4,2,1,3,4,6,5,1,9,10,5,3,10,1]
    numbers = getav(listtest)
    x.append(time.time())
    y.append(random.random())
    time.sleep(0.03)
    print("yes")
    if len(y) > 10:
        y = y[1:]
    if len(x) > 10:
        x = x[1:]
    pyplot.plot(x,y)
    pyplot.draw()
    pyplot.pause(0.033333)

