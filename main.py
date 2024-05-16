# Import statements: remove all unimportant
import random
import qwiicscale
import time
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import BlynkLib



##Variables, class and functions set
qwiic = qwiicscale.QwiicScale()
average = []
resultsoutput =[]
CalibrateZero=0
motor = 1
calibrated = False
status = "calone"
BLYNK_TEMPLATE_ID = "TMPL5E9rUAxOQ"
BLYNK_TEMPLATE_NAME = "Quickstart Template"
BLYNK_AUTH_TOKEN = "WJbSxpdW_KDfcH1BnAtdHlX6vxxeAXRZ"



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
        result = (calweight*result)/(CalibrateWeight-CalibrateZero) #Lineair interpolatie naar gewicht
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
    blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

    @blynk.on("connected")
    def blynk_connnected():
        print("Raspberry pi connected")

 ### Defined calibration, nog uit te testen? Should work met blynk
    blynk.virtual_write(0,1)
    blynk.virtual_write(2,0)

    @blynk.on("V1")
    def V1_handler(value):
        global status
        print(f'value = {value}')
        if status == "motor":
            global motor
            motor = value
        if status == "calweight":
            if '1' in value:
                global CalibrateWeight
                CalibrateWeight = qwiic.getAverage(averageAmount=64)
            if '0' in value:
                blynk.virtual_write(0, 0)
                status = "motor"
                blynk.virtual_write(2,1)
                global calibrated
                calibrated = True
        if status == "calone":
            if '1' in value:
                global CalibrateZero
                CalibrateZero = qwiic.getAverage(averageAmount=64)
            if '0' in value:
                blynk.virtual_write(0,0)
                status = "calweight"
                time.sleep(2)
                blynk.virtual_write(0,1)



    @blynk.on("V3")
    def V3_handler(weight):
        print(f'Weight received. Weight set = {weight}')
        global calweight
        calweight = weight[0]


    while True:
        blynk.run()
        while calibrated != True:
            pass
        numbers = getav(qwiic.getReading())
        for i in range(0,len(numbers)):
            blynk.virtual_write(4,numbers[i])
        if motor == 0:
            pass
            #Ga omhoog arduino
        if motor == 1:
            pass
            #Stop arduino
        if motor == 2:
            pass
            #Ga omlaag arduino










