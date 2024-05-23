# Import statements
import qwiicscale
import time
import BlynkLib
import RPi.GPIO as GPIO
import matplotlib
from matplotlib import pyplot

## Qwiic Opstelling
qwiic = qwiicscale.QwiicScale()
zero_offset = 0
motor = ['0']
average  = 0
calibrated = False
status = "calone"
avlist = []
x = []
y = []

## Blynk variabelen
BLYNK_TEMPLATE_ID = "TMPL5E9rUAxOQ"
BLYNK_TEMPLATE_NAME = "Quickstart Template"
BLYNK_AUTH_TOKEN = "WJbSxpdW_KDfcH1BnAtdHlX6vxxeAXRZ"

## Arduino opstelling


def numcal(meetdata):
    result = known_weight*(meetdata-zero_offset)/(measured_weight-zero_offset) #Lineair interpolatie naar gewicht
    return result


if __name__ == '__main__':
    qwiic.begin()
    GPIO.setmode(GPIO.BCM)
    connection = qwiic.is_connected()
    print(connection)
    qwiic.available()
    blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)


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
                measured_weight = int(round(qwiic.getAverage(averageAmount=64)))
            if '0' in value:
                blynk.virtual_write(0, 0)
                status = "motor"
                blynk.virtual_write(2,1)
                global calibrated
                calibrated = True
        if status == "calone":
            if '1' in value:
                global zero_offset
                zero_offset = int(round(qwiic.getAverage(averageAmount=64)))
            if '0' in value:
                blynk.virtual_write(0,0)
                status = "calweight"
                time.sleep(2)
                blynk.virtual_write(0,1)



    @blynk.on("V3")
    def V3_handler(weight):
        print(f'Weight received. Weight set = {weight[0]} g')
        global known_weight
        known_weight = int(weight[0])

## Besturen van de motor en doorsturen gekalibreerde data naar blynk
    while True:
        blynk.run()
        if calibrated == True:
            numbers = numcal(int(qwiic.getReading()))
            if len(avlist) < 10:
                avlist.append(numbers)
            if len(avlist) == 10:
                for i in range(0,len(avlist)):
                    average += avlist[i]
                average = average/10
                x.append(time.time())
                y.append(numbers)
                time.sleep(0.03)
                if len(y) > 10:
                    y = y[1:]
                if len(x) > 10:
                    x = x[1:]
                pyplot.clf()
                pyplot.plot(x,y)
                pyplot.draw()
                pyplot.pause(0.033333)
                pyplot.pause(0.03)
                blynk.virtual_write(4, average)
                average=0
                avlist = []
            if "1" in motor:
                GPIO.output(20, GPIO.HIGH)
                GPIO.output(26, GPIO.LOW)
                # Ga omhoog arduino, kan zijn dat 1 of 0 moet omgedraaid worden
            if "0" in motor:
                GPIO.output(20, GPIO.LOW)
                GPIO.output(26, GPIO.LOW)
                # Stop arduino
            if "2" in motor:
                GPIO.output(20, GPIO.LOW)
                GPIO.output(26, GPIO.HIGH)
                # Ga omlaag arduino, kan zijn dat 1 of 0 moet omgedraaid worden



