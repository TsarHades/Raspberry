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
import BlynkLib


##Variables, class and functions set
qwiic = qwiicscale.QwiicScale()
average = []
resultsoutput =[]
V1 = 0
V2 = 0
CalibrateZero=0
weight = False
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
    blynk.connect()

    @blynk.on("connected")
    def blynk_connnected():
        print("Raspberry pi connected")

 ### Defined calibration, nog uit te testen? Should work met blynk
    blynk.virtual_write("V0",1)
    while V1 != 1:
        @blynk.on("V1")
        def V1_handler(value):
                if value == 1:
                    CalibrateZero = qwiic.getAverage(averageAmount=64)
                if value == 0:
                    blynk.virtual_write("V0",0)
                    V1 = 0

    blynk.virtual_write("V2,1")
    while V1 != 1:
        @blynk.on("V1")
        def V2_handler(value):
            if value == 1:
                CalibrateWeight = qwiic.getAverage(averageAmount=64)
                while weight == False:
                    @blynk.on("V3")
                    def V3_handler(weight):
                        calweight = weight
                        weight= True
            if value ==0:
                blynk.virtual_write("V2",0)

    while True:
        blynk.run()
        numbers = getav(qwiic.getReading())
        for i in range(0,len(numbers)):
            blynk.virtual_write("V4",numbers[i])







