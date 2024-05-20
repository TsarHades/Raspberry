# Import statements: remove all unimportant
import random
import qwiicscale
import time
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import BlynkLib
from pyfirmata import Arduino, util



## Qwiic Opstelling
qwiic = qwiicscale.QwiicScale()
zero_offset = 0
motor = 1
average  = 0
calibrated = False
status = "calone"
avlist = []

## Blynk variabelen
BLYNK_TEMPLATE_ID = "TMPL5E9rUAxOQ"
BLYNK_TEMPLATE_NAME = "Quickstart Template"
BLYNK_AUTH_TOKEN = "WJbSxpdW_KDfcH1BnAtdHlX6vxxeAXRZ"

## Arduino opstelling
board = Arduino("poort van onze arduino")
while not board.is_ready():
    pass

arduino_pin2 = 2
arduino_pin3 = 3

board.digital[arduino_pin2].mode = pyfirmata.OUTPUT
board.digital[arduino_pin3].mode = pyfirmata.OUTPUT

pin2 = board.digital[arduino_pin2]
pin3 = board.digital[arduino_pin3]


def numcal(meetdata):
    result = known_weight*(meetdata-zero_offset)/(measured_weight-zero_offset) #Lineair interpolatie naar gewicht
    return result


if __name__ == '__main__':
    qwiic.begin()
    connection = qwiic.is_connected()
    print(connection)
    qwiic.available()
    blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

    @blynk.on("connected")
    def blynk_connnected():
        print("Raspberry pi connected to Blynk")

 ### Ledjes en zo
    blynk.virtual_write(0,1)
    blynk.virtual_write(2,0)

 ## Blynk Triggers
    @blynk.on("V1")
    def V1_handler(value):
        global status
        print(f'Value = {value[0]}')
        if status == "motor":
            global motor
            motor = value
        if status == "calweight":
            if '1' in value:
                global measured_weight
                measured_weight = qwiic.getAverage(averageAmount=64)
            if '0' in value:
                blynk.virtual_write(0, 0)
                status = "motor"
                blynk.virtual_write(2,1)
                global calibrated
                calibrated = True
        if status == "calone":
            if '1' in value:
                global zero_offset
                zero_offset = qwiic.getAverage(averageAmount=64)
            if '0' in value:
                blynk.virtual_write(0,0)
                status = "calweight"
                time.sleep(2)
                blynk.virtual_write(0,1)



    @blynk.on("V3")
    def V3_handler(weight):
        print(f'Weight received. Weight set = {weight}')
        global known_weight
        known_weight = weight[0]

## Besturen van de motor en doorsturen gekalibreerde data naar blynk
    while True:
        blynk.run()
        while calibrated != True:
            pass
        numbers = numcal(qwiic.getReading())
        if len(avlist) < 12:
            avlist.append(numbers)
        if len(avlist) == 12:
            for i in range(0,len(avlist)):
                average += avlist[i]
            average = average/12
            blynk.virtual_write(4, average)
            average=0
            avlist = []
        if motor == 1:
            pin2.write(1)
            pin3.write(0)
            # Ga omhoog arduino, kan zijn dat 1 of 0 moet omgedraaid worden
        if motor == 0:
            pin2.write(0)
            pin3.write(0)
            # Stop arduino
        if motor == 2:
            pin2.write(0)
            pin3.write(1)
            # Ga omlaag arduino, kan zijn dat 1 of 0 moet omgedraaid worden










