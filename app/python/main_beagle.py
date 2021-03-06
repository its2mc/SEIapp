#!/usr/bin/python
# This work has been done by Phillip Ochola Mak'Anyengo
# as part of the Smart Energy Integrator Project together
# with Frankline Mogoi.
# 
# Email: its2uraps@gmail.com
#
# This work uses open source code and open use libraries
# but the application itself is neither open source or 
# allowed for open use. 
# 
# Users who wish to use parts of this
# work MUST contact the authors before use, failure to which
# the user risks being prosecuted.


#Importing all libraries
import threading
import time
import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.ADC as adc
import json
#--mysql--#
import pymysql
#--logger--#
import logging
#--Zero MQ python library--#
import zmq
from pymysql import NULL


#Declare constants
MAX_PIN_VOLTAGE_VAL = 1.49
MAX_PIN_READING_VAL = 0.9994

MAX_CURRENT_VAL = 30
MAX_SENSOR_READING_VAL = 1.4
TRIGGER_CHARGE_LEVEL = 0.8

SOCKET_ADDR = "tcp://localhost:9992"
#--switch pin mapping, each number represents the power source--#
CIRCUIT_ONE = {'1': "P8_14", '2':"P8_11",'3':"P8_8"}
CIRCUIT_TWO = {'1': "P8_13", '2':"P8_10",'3':"P8_9"}
CIRCUIT_THREE =  {'1': "P8_12", '2':"P8_7",'3':"P8_15"}
#--sensor pin mapping--#
SENSOR_PINS = {'1': "P9_39"}
#--charger pin mappings--#
CONTROL_PINS = {'grid':"P9_18",'source2':"",'solar':"P8_19",'charge':""}
#--led pin mapping--#
LED_PINS = {'status': "", 'error':"", 'process':""}


#Prepare environment
adc.setup()
#--assign switch pins functions--#
for powerSource, boardPin in CIRCUIT_ONE.iteritems():
    gpio.setup(boardPin,gpio.OUT)
    gpio.output(boardPin,gpio.HIGH)
for powerSource, boardPin in CIRCUIT_TWO.iteritems():
    gpio.setup(boardPin,gpio.OUT)
    gpio.output(boardPin,gpio.HIGH)
for powerSource, boardPin in CIRCUIT_THREE.iteritems():
    gpio.setup(boardPin,gpio.OUT)
    gpio.output(boardPin,gpio.HIGH)
#--assign led pins functions--# not included yet
for led, boardPin in LED_PINS.iteritems():
    gpio.setup(boardPin,gpio.OUT)
#--setup declaration--#
for sensor, boardPin in SENSOR_PINS.iteritems():
    gpio.setup(boardPin,gpio.IN)
#--setup control pins --#
gpio.setup(CONTROL_PINS['grid'],gpio.OUT)
gpio.output(CONTROL_PINS['grid'],gpio.HIGH)
gpio.setup(CONTROL_PINS['solar'],gpio.OUT)
gpio.output(CONTROL_PINS['solar'],gpio.HIGH)

#Prepare Logger (File Logger and Console Error Logger)
#--create logger with 'the SEI app'--#
logger = logging.getLogger('SEI_app')
logger.setLevel(logging.DEBUG)
#--create file handler which logs debug messages--#
fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)
#--create formatter and add it to the handlers--#
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
#--add the handlers to the logger--#
logger.addHandler(fh)
logger.info('Application starting. Logging Enabled.')

#This function will reset the relays to off incase of any error
def reset():
    for powerSource, boardPin in CIRCUIT_ONE.iteritems():
        gpio.output( boardPin, gpio.HIGH)
    for powerSource, boardPin in CIRCUIT_TWO.iteritems():
        gpio.output(boardPin, gpio.HIGH)
    for powerSource, boardPin in CIRCUIT_THREE.iteritems():
        gpio.output( boardPin, gpio.HIGH)
    
#Status LED class.. i.e. error led, status led, process led
def processLED():
    gpio.output(LED_PINS["process"],gpio.HIGH)
    time.sleep(0.1)
    gpio.output(LED_PINS["process"],gpio.LOW)
    time.sleep(0.1)
    gpio.output(LED_PINS["process"],gpio.HIGH)
    time.sleep(0.1)
    gpio.output(LED_PINS["process"],gpio.LOW)
    
def errorLED():
    gpio.output(LED_PINS["error"],gpio.HIGH)
    gpio.output(LED_PINS["status"],gpio.LOW)
    
def statusLED():
    gpio.output(LED_PINS["status"],gpio.HIGH)

#Change switch method
def switchCircuit(circuitNo,sourceNo):
    logger.info('Switching circuits')
    if(circuitNo == '1'):
        logger.info('Resetting gpio outputs for circuit 1 to 0V')
        for powerSource, boardPin in CIRCUIT_ONE.iteritems():
            gpio.output(boardPin,gpio.HIGH)
#--time for the gpio pins to settle--#
        time.sleep(1)
        logger.info('Setting Circuit 1 to power source '+sourceNo)
        for powerSource, boardPin in CIRCUIT_ONE.iteritems():
            if(powerSource == sourceNo):
                gpio.output(boardPin,gpio.LOW)
            else:
                gpio.output(boardPin,gpio.HIGH)
        return 1
    elif(circuitNo == '2'):
        logger.info('Resetting gpio outputs for circuit 2 to 0V')
        for powerSource, boardPin in CIRCUIT_TWO.iteritems():
            gpio.output(boardPin,gpio.HIGH)
#--time for the gpio pins to settle--#
        time.sleep(1)
        logger.info('Setting Circuit 2 to power source '+sourceNo)
        for powerSource, boardPin in CIRCUIT_TWO.iteritems():
            if(powerSource == sourceNo):
                gpio.output(boardPin,gpio.LOW)
            else:
                gpio.output(boardPin,gpio.HIGH)
        return 1
    elif(circuitNo == '3'):
        logger.info('Resetting gpio outputs for circuit 3 to 0V')
        for powerSource, boardPin in CIRCUIT_TWO.iteritems():
            gpio.output(boardPin,gpio.HIGH)
#--time for the gpio pins to settle--#
        time.sleep(1)
        logger.info('Setting Circuit 3 to power source '+sourceNo)
        for powerSource, boardPin in CIRCUIT_TWO.iteritems():
            if(powerSource == sourceNo):
                gpio.output(boardPin,gpio.LOW)
            else:
                gpio.output(boardPin,gpio.HIGH)
        return 1
    
#Read Sensor data method, reads sensor info and sends to server ... this is not included for now
def readSensors():
#    processLED()
#--setting up mysql connection parameters--#
    logger.info('Setting up mysql settings')
    conn = pymysql.connect(host='localhost',port=3306,user='seiuser',passwd='r1o2o3t4`',db='seidb')
    cur = conn.cursor()
#--preparing variables and the environment--#
    id = NULL
    sensorId = NULL
    data = NULL
    timestamp = NULL
    
    logger.info('Starting sensor loop')
    for sensor, boardPin in SENSOR_PINS.iteritems():
#-read gpio sensors--#
        logger.info('Reading sensor '+sensor)
        sensorId = sensor
        #--assign sensor pins functions--# not included yet
        for i in range(100):
            #--prepare for database entries--#
            timestamp = time.time()
            #--format gpio pin readings--#
            data = adc.read(boardPin) * (MAX_PIN_VOLTAGE_VAL/MAX_PIN_READING_VAL) *(MAX_CURRENT_VAL/MAX_SENSOR_READING_VAL)
            #--execute query--#
            cur.execute("INSERT INTO sensorData (id,sensorID,data,timestamp) values (%s,%s,%s,%s)",(id,sensorId,data,timestamp))
           
#--closing connection and cursor--#        
#    processLED()
    logger.info('Cleaning up cursor and mysql connection')
    cur.close()
    conn.close()

#Code to check if the charger is 
def checkCharge():
#    processLED()
    logger.info('Checking charge level')
    charge = adc.read(CONTROL_PINS['sensor'])
    if (charge< TRIGGER_CHARGE_LEVEL):
        gpio.output(CONTROL_PINS['charge'],gpio.LOW)
    else: 
        gpio.output(CONTROL_PINS['charge'],gpio.HIGH)
        
    
#Messages Class has message handling methods, send/receive/reply
class messenger():
    
    def __init__ (self):
        self.temp = ''
#--a dictionary containing the command-function matches--#
        self.options = {
                        "switchCircuit":self.switch,
                        "stats":self.getStats,
                        "reset":reset
                        }
#--internal switching function--#
    def switch(self):
#       processLED()
        logger.info('Attempting to Switch circuit '+self.temp["circuitNo"]+' to source '+self.temp["sourceNo"])
        if(switchCircuit(self.temp["circuitNo"],self.temp["sourceNo"])==1):
            return {"msg": "Switch successful"}
        else:
            return {"msg": "Switching error"}

#--gets statistics on device runtime.. basically checks if the device is running--#
    def getStats(self):
#        processLED()
        return {"msg": "ok"}

#--receives commands from the server and processes them--#    
    def processCmd(self,msg,conn):
#        processLED()
        logger.info('Processing Command from server')
        self.temp = json.loads(msg)
        self.options[self.temp["command"]]()


class sensorThread(threading.Thread):

    def __init__ (self):
        threading.Thread.__init__(self)
        self.count = 0

#--sensor thread--#
    def run(self):
#        processLED()
        logger.info('Sensor thread started')
        while True: 
#            self.count += 1
            time.sleep(600)
#            time.sleep(450)
#            checkCharge()
            readSensors()
#           if(self.count <)


class commsThread(threading.Thread):
    
    def __init__ (self):
        threading.Thread.__init__(self)
        self.messenger = messenger()

#--communication thread--#
    def run(self):
#        processLED()
        logger.info('Command thread started')
        context = zmq.Context()
        logger.info('connecting to comms Server')
#--socket to receive messages on--#
        conn = context.socket(zmq.REP)
        conn.connect(SOCKET_ADDR)
        # Process tasks forever
        while True:
            msg = conn.recv()
            logger.info('Message recieved:'+msg)
            conn.send_json(self.messenger.processCmd(msg,conn),0)
                

#Run the main thread
try:
#    statusLED()
    threadA = sensorThread()
    threadB = commsThread()
    logger.info('Starting sensor thread')
    threadA.start()
    logger.info('Starting command thread')
    threadB.start()
except Exception, e:
    reset()
#    errorLED()
    logger.error(str(e))
    

    