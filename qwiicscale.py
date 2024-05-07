
from __future__ import print_function

import qwiic_i2c

import time

NAU7802_PU_CTRL = 0
NAU7802_CTRL1 = 1
NAU7802_CTRL2 = 2
NAU7802_OCAL1_B2 = 3
NAU7802_OCAL1_B1 = 4
NAU7802_OCAL1_B0 = 5
NAU7802_GCAL1_B3 = 6
NAU7802_GCAL1_B2 = 7
NAU7802_GCAL1_B1 = 8
NAU7802_GCAL1_B0 = 9
NAU7802_OCAL2_B2 = 10
NAU7802_OCAL2_B1 = 11
NAU7802_OCAL2_B0 = 12
NAU7802_GCAL2_B3 = 13
NAU7802_GCAL2_B2 = 14
NAU7802_GCAL2_B1 = 15
NAU7802_GCAL2_B0 = 16
NAU7802_I2C_CONTROL = 17
NAU7802_ADCO_B2 = 18
NAU7802_ADCO_B1 = 19
NAU7802_ADCO_B0 = 20
NAU7802_ADC = 21
NAU7802_OTP_B1 = 22
NAU7802_OTP_B0 = 23
NAU7802_PGA = 24
NAU7802_PGA_PWR = 25
NAU7802_DEVICE_REV = 26



NAU7802_PU_CTRL_RR = 0
NAU7802_PU_CTRL_PUD = 1
NAU7802_PU_CTRL_PUA = 2
NAU7802_PU_CTRL_PUR = 3
NAU7802_PU_CTRL_CS = 4
NAU7802_PU_CTRL_CR = 5
NAU7802_PU_CTRL_OSCS = 6
NAU7802_PU_CTRL_AVDDS = 7


NAU7802_CTRL1_GAIN = 2
NAU7802_CTRL1_VLDO = 5
NAU7802_CTRL1_DRDY_SEL = 6
NAU7802_CTRL1_CRP = 7



NAU7802_CTRL2_CALMOD = 0
NAU7802_CTRL2_CALS = 2
NAU7802_CTRL2_CAL_ERROR = 3
NAU7802_CTRL2_CRS = 4
NAU7802_CTRL2_CHS = 7



NAU7802_PGA_CHP_DIS = 0
NAU7802_PGA_INV = 3
NAU7802_PGA_BYPASS_EN = 4
NAU7802_PGA_OUT_EN = 5
NAU7802_PGA_LDOMODE = 6
NAU7802_PGA_RD_OTP_SEL = 7



NAU7802_PGA_PWR_PGA_CURR = 0
NAU7802_PGA_PWR_ADC_CURR = 2
NAU7802_PGA_PWR_MSTR_BIAS_CURR = 4
NAU7802_PGA_PWR_PGA_CAP_EN = 7


NAU7802_LDO_2V4 = 7
NAU7802_LDO_2V7 = 6
NAU7802_LDO_3V0 = 5
NAU7802_LDO_3V3 = 4
NAU7802_LDO_3V6 = 3
NAU7802_LDO_3V9 = 2
NAU7802_LDO_4V2 = 1
NAU7802_LDO_4V5 = 0


NAU7802_GAIN_128 = 7
NAU7802_GAIN_64 = 6
NAU7802_GAIN_32 = 5
NAU7802_GAIN_16 = 4
NAU7802_GAIN_8 = 3
NAU7802_GAIN_4 = 2
NAU7802_GAIN_2 = 1
NAU7802_GAIN_1 = 0



NAU7802_SPS_320 = 7
NAU7802_SPS_80 = 3
NAU7802_SPS_40 = 2
NAU7802_SPS_20 = 1
NAU7802_SPS_10 = 0



NAU7802_CHANNEL_1 = 0
NAU7802_CHANNEL_2 = 1


NAU7802_CAL_SUCCESS = 0
NAU7802_CAL_IN_PROGRESS = 1
NAU7802_CAL_FAILURE = 2



# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic Joystick"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x2A]

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicScale(object):
    """
    QwiicJoystick
        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The QwiicJoystick device object.
        :rtype: Object
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """
            Determine if a Joystick device is conntected to the system..
            :return: True if the device is connected, otherwise False.
            :rtype: bool
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        if not self.reset(): #Reset all registers
            print("\033[91m[error] Could not reset QwiicScale\033[0m")
        if not self.powerUp(): #Power on analog and digital sections of the scale
            print("\033[91m[error] Could not powerup the QwiicScale\033[0m")
        if not self.setLDO(NAU7802_LDO_3V3): #Set LDO to 3.3V
            print("\033[91m[error] Could not LDO\033[0m")
        if not self.setGain(NAU7802_GAIN_1): #Set gain to 128
            print("\033[91m[error] Could not set the gain\033[0m")
        if not self.setSampleRate(NAU7802_SPS_80): #Set samples per second to 10
            print("\033[91m[error] Could not set the sample rate\033[0m")
        if not self.setRegister(NAU7802_ADC, 0x30):#Turn off CLK_CHP. From 9.1 power on sequencing.
            print("\033[91m[error] Could not turn off CLK_CHP\033[0m")
        if not self.setBit(NAU7802_PGA_PWR_PGA_CAP_EN, NAU7802_PGA_PWR): #Enable 330pF decoupling cap on chan 2. From 9.14 application circuit note.
            print("\033[91m[error] Could not enable 330pF decoupling cap on channel 2\033[0m")
        if not self.calibrateAFE(): #Re-cal analog front end when we change gain, sample rate, or +
            print("\033[91m[error] Could not calibrate QwiicScale: timeout expired\033[0m")

        self.setBit(NAU7802_PU_CTRL_CS, NAU7802_PU_CTRL)

        # Basically return True if we are connected...

        return self.is_connected()

    #----------------------------------------------------------------
    # get_horizontal()
    #
    # Returns the 10-bit ADC value of the joystick horizontal position

    #Returns true if Cycle Ready bit is set (conversion is complete)
    def available(self):
        return(self.getBit(NAU7802_PU_CTRL_CR, NAU7802_PU_CTRL))
		

	#Calibrate analog front end of system. Returns true if CAL_ERR bit is 0 (no error)
	#Takes approximately 344ms to calibrate wait up to 5000ms.
	#It is recommended that the AFE be re-calibrated any time the gain, SPS, or channel number is changed.
    def calibrateAFE(self):
        self.beginCalibrateAFE()
        return self.waitForCalibrateAFE(5000)

	#Begin asynchronous calibration of the analog front end.
	# Poll for completion with calAFEStatus() or wait with waitForCalibrateAFE()
    def beginCalibrateAFE(self):
        self.setBit(NAU7802_CTRL2_CALS, NAU7802_CTRL2)

	#Check calibration status.
    def calAFEStatus(self):
        if (self.getBit(NAU7802_CTRL2_CALS, NAU7802_CTRL2)):
            return NAU7802_CAL_IN_PROGRESS

        if (self.getBit(NAU7802_CTRL2_CAL_ERROR, NAU7802_CTRL2)):
            return NAU7802_CAL_FAILURE
	

	  # Calibration passed
        return NAU7802_CAL_SUCCESS
	

	#Wait for asynchronous AFE calibration to complete with optional timeout.
	#If timeout is not specified (or set to 0), then wait indefinitely.
	#Returns true if calibration completes succsfully, otherwise returns false.
    def waitForCalibrateAFE(self, timeout_ms):
	
        begin = int(round(time.time()*1000.0))
        cal_ready = NAU7802_CAL_IN_PROGRESS

        while (cal_ready == NAU7802_CAL_IN_PROGRESS):
            cal_ready = self.calAFEStatus()
            if ((timeout_ms > 0) and ((int(round(time.time()*1000.0)) - begin) > timeout_ms)) :
                break
		
            time.sleep(1)
	

            if (cal_ready == NAU7802_CAL_SUCCESS):
                return (True)

        return (False)
	

	#Set the readings per second
	#10, 20, 40, 80, and 320 samples per second is available
    def setSampleRate(self, rate):
        if (rate > 7):
            rate = 7 #Error check

        value = self.getRegister(NAU7802_CTRL2)
        value = value & 0b10001111 #Clear CRS bits
        value = value | (rate << 4)  #Mask in new CRS bits

        return (self.setRegister(NAU7802_CTRL2, value))
	

	#Select between 1 and 2
    def setChannel(self, channelNumber):
	
        if (channelNumber == NAU7802_CHANNEL_1):
            return (self.clearBit(NAU7802_CTRL2_CHS, NAU7802_CTRL2)) #Channel 1 (default)
        else:
            return (self.setBit(NAU7802_CTRL2_CHS, NAU7802_CTRL2)) #Channel 2
	

	#Power up digital and analog sections of scale
    def powerUp(self):
	
        self.setBit(NAU7802_PU_CTRL_PUD, NAU7802_PU_CTRL)
        self.setBit(NAU7802_PU_CTRL_PUA, NAU7802_PU_CTRL)

        #Wait for Power Up bit to be set - takes approximately 200us
        counter = 0
        while (1):
            val = self.getBit(NAU7802_PU_CTRL_PUR, NAU7802_PU_CTRL)
            # print("val %d" % (val))
            if (val == 8): #self.getBit(NAU7802_PU_CTRL_PUR, NAU7802_PU_CTRL) == 1):
                break #Good to go
            time.sleep(1)
            # print("power up")
		
            if (counter > 100):
                return (False) #Error
            counter = counter + 1
	
        return (True)
	

	#Puts scale into low-power mode
    def powerDown(self):
	
        self.clearBit(NAU7802_PU_CTRL_PUD, NAU7802_PU_CTRL)
        return (self.clearBit(NAU7802_PU_CTRL_PUA, NAU7802_PU_CTRL))
	

	#Resets all registers to Power Of Defaults
    def reset(self):
        self.setBit(NAU7802_PU_CTRL_RR, NAU7802_PU_CTRL) #Set RR
        time.sleep(1)
        return (self.clearBit(NAU7802_PU_CTRL_RR, NAU7802_PU_CTRL)) #Clear RR to leave reset state
	

	#Set the onboard Low-Drop-Out voltage regulator to a given value
	#2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5V are available
    def setLDO(self, ldoValue):
	
        if (ldoValue > 0b111):
            ldoValue = 0b111 #Error check

        #Set the value of the LDO
        value = self.getRegister(NAU7802_CTRL1)
        value =  value & 0b11000111    #Clear LDO bits
        value = value | (ldoValue << 3) #Mask in new LDO bits
        self.setRegister(NAU7802_CTRL1, value)

        return (self.setBit(NAU7802_PU_CTRL_AVDDS, NAU7802_PU_CTRL)) #Enable the internal LDO
	

	#Set the gain
	#x1, 2, 4, 8, 16, 32, 64, 128 are avaialable
    def setGain(self, gainValue):
	
        if (gainValue > 0b111):
            gainValue = 0b111 #Error check

        value = self.getRegister(NAU7802_CTRL1)
        value = value & 0b11111000 #Clear gain bits
        value = value | gainValue  #Mask in new bits

        return (self.setRegister(NAU7802_CTRL1, value))
	

	#Get the revision code of this IC
    def getRevisionCode(self):
	
        revisionCode = self.getRegister(NAU7802_DEVICE_REV)
        return (revisionCode & 0x0F)
	

	#Returns 24-bit reading
	#Assumes CR Cycle Ready bit (ADC conversion complete) has been checked to be 1
    def getReading(self):
        value_list = self._i2c.readBlock(self.address, NAU7802_ADCO_B2,3)
        value = value_list[0]
        value = value << 8
        #value = value | self._i2c.readByte(self.address, NAU7802_ADCO_B2)
        value = (value | value_list[1]) << 8
        value = (value | value_list[2])
        #adByte(self.address, NAU7802_ADCO_B2)
        value = self.sign_extend(value, 32)
		
        return(value)
	
	
    def sign_extend(self,value, bits):
        sign_bit = 1 << (bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)
	

    #Return the average of a given number of readings
	#Gives up after 1000ms so don't call this function to average 8 samples setup at 1Hz output (requires 8s)
    def getAverage(self, averageAmount):
        total = 0
        samplesAquired = 0
        startTime = int(round(time.time()*1000.0))
        while (1):
            if (self.available()):

              total += self.getReading()
              samplesAquired += 1
              if (samplesAquired == averageAmount):
                break #All done
            if (int(round(time.time()*1000.0)) - startTime > 1000):
              return (0) #Timeout - Bail with error

            total /= averageAmount

        return (total)


    #Call when scale is setup, level, at running temperature, with nothing on it
    def calculateZeroOffset(self,averageAmount):
        setZeroOffset(getAverage(averageAmount))
	

    #Sets the internal variable. Useful for users who are loading values from NVM.
    def setZeroOffset(newZeroOffset):
       _zeroOffset = newZeroOffset

	

    def getZeroOffset(self):
	    return (_zeroOffset)

    '''
	#Call after zeroing. Provide the float weight sitting on scale. Units do not matter.
	def calculateCalibrationFactor(float weightOnScale, uint8_t averageAmount):
	
	  int32_t onScale = getAverage(averageAmount)
	  float newCalFactor = (onScale - _zeroOffset) / (float)weightOnScale
	  setCalibrationFactor(newCalFactor)
	

	#Pass a known calibration factor into library. Helpful if users is loading settings from NVM.
	#If you don't know your cal factor, call setZeroOffset(), then calculateCalibrationFactor() with a known weight
	def setCalibrationFactor(float newCalFactor):
	
	  _calibrationFactor = newCalFactor
	

	def getCalibrationFactor():
	
	  return (_calibrationFactor)
	

	#Returns the y of y = mx + b using the current weight on scale, the cal factor, and the offset.
	def getWeight(bool allowNegativeWeights):
	
	  int32_t onScale = getAverage(8)

	  #Prevent the current reading from being less than zero offset
	  #This happens when the scale is zero'd, unloaded, and the load cell reports a value slightly less than zero value
	  #causing the weight to be negative or jump to millions of pounds
	  if (allowNegativeWeights == false):
	
		if (onScale < _zeroOffset):
		  onScale = _zeroOffset #Force reading to zero
	

	  float weight = (onScale - _zeroOffset) / _calibrationFactor
	  return (weight)
    '''

	#Set Int pin to be high when data is ready (default)
    def setIntPolarityHigh(self):
        return(self.clearBit(NAU7802_CTRL1_CRP, NAU7802_CTRL1)) #0 = CRDY pin is high active (ready when 1)
	

	#Set Int pin to be low when data is ready
    def setIntPolarityLow(self):
	
        return(self.setBit(NAU7802_CTRL1_CRP, NAU7802_CTRL1)) #1 = CRDY pin is low active (ready when 0)
	

	#Mask & set a given bit within a register
    def setBit(self, bitNumber, registerAddress):
        value = self.getRegister(registerAddress)
        value = value | (1 << bitNumber) #Set this bit
        return(self.setRegister(registerAddress, value))
	

	#Mask & clear a given bit within a register
    def clearBit(self,  bitNumber, registerAddress):
        value = self.getRegister(registerAddress)
        value = value & ~(1 << bitNumber) #Set this bit
        return(self.setRegister(registerAddress, value))
	

	#Return a given bit within a register
    def getBit(self, bitNumber, registerAddress):
	
        value = self.getRegister(registerAddress)
        value = value & (1 << bitNumber) #Clear all but this bit
        return(value)
	

	#Get contents of a register
    def getRegister(self, registerAddress):
        value = self._i2c.readByte(self.address, registerAddress)
        return(value) #Error
	

	#Send a given value to be written to given address
	#Return true if successful
    def setRegister(self, registerAddress, value):
        self._i2c.writeByte(self.address, registerAddress, value)
        return(True)
	