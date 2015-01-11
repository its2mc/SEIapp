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
import RPi.GPIO as gpio
import json
#--mysql--#
import pymysql
##import random
#--logger--#
import logging
#--Zero MQ python library--#
import zmq
from pymysql import NULL


#Declare constants
SOCKET_ADDR = "tcp://localhost:6665"
#--switch pin mapping, each number represents the power source--#
CIRCUIT_ONE = {'1': 8, '2':10, '3':11}
CIRCUIT_TWO = {'1': 12, '2':13, '3':15}
#--sensor pin mapping--#
SENSOR_PINS = {'1': 0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
#--led pin mapping--#
LED_PINS = {'1': 0, '2':0, '3':0}


#Prepare environment
#--setup gpio mode--#
gpio.setmode(gpio.BOARD)  # use P1 header pin numbering convention
gpio.setwarnings(False)   # don't want to hear about how pins are already in use
#--assign switch pins functions--#
for powerSource, boardPin in CIRCUIT_ONE.iteritems():
    gpio.setup(boardPin,gpio.OUT)
for powerSource, boardPin in CIRCUIT_TWO.iteritems():
    gpio.setup(boardPin,gpio.OUT)
#--assign sensor pins functions--# not included yet
#for sensor, boardPin in SENSOR_PINS.iteritems():
#    gpio.setup(boardPin,gpio.IN)
#--assign led pins functions--# not included yet
#for led, boardPin in LED_PINS.iteritems():
#    gpio.setup(boardPin,gpio.OUT)
#--setup declaration--#



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


#Status LED class.. i.e. error led, okay led, communication led


#Change switch method
def switchCircuit(circuitNo,sourceNo):
    logger.info('Switching circuits')
    if(circuitNo == '1'):
        logger.info('Resetting gpio outputs for circuit 1 to 0V')
        for powerSource, boardPin in CIRCUIT_ONE.iteritems():
            gpio.output(boardPin,False)
#--time for the gpio pins to settle--#
        time.sleep(1)
        logger.info('Setting Circuit 1 to power source '+sourceNo)
        for powerSource, boardPin in CIRCUIT_ONE.iteritems():
            if(powerSource == sourceNo):
                gpio.output(boardPin,True)
            else:
                gpio.output(boardPin,False)
        return 1
    elif(circuitNo == '2'):
        logger.info('Resetting gpio outputs for circuit 2 to 0V')
        for powerSource, boardPin in CIRCUIT_TWO.iteritems():
            gpio.output(boardPin,False)
#--time for the gpio pins to settle--#
        time.sleep(1)
        logger.info('Setting Circuit 2 to power source '+sourceNo)
        for powerSource, boardPin in CIRCUIT_TWO.iteritems():
            if(powerSource == sourceNo):
                gpio.output(boardPin,True)
            else:
                gpio.output(boardPin,False)
        return 1
    
    
#Read Sensor data method, reads sensor info and sends to server ... this is not included for now
def readSensors():
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
    for i in range(2000):
#-read gpio sensors--#
        print('Reading sensors')
#--format gpio pin readings to numbers--#

#--prepare for database entries--#
        cur.execute("INSERT INTO sensorData (id,sensorID,data,timestamp) values (%s,%s,%s,%s)",(id,sensorId,data,timestamp))    
#--closing connection and cursor--#        
    logger.info('Cleaning up cursor and mysql connection')
    cur.close()
    conn.close()


#Messages Class has message handling methods, send/receive/reply
class messenger():
    
    def __init__ (self):
        self.temp = ''
#--a dictionary containing the command-function matches--#
        self.options = {
                        "switchCircuit":self.switch,
                        "stats":self.getStats
                        }
#--internal switching function--#
    def switch(self):
        logger.info('Attempting to Switch circuit'+self.temp["circuitNo"]+' to source '+self.temp["sourceNo"])
        if(switchCircuit(self.temp["circuitNo"],self.temp["sourceNo"])==1):
            return {"msg": "Switch successful"}
        else:
            return {"msg": "Switching error"}

#--gets statistics on device runtime.. basically checks if the device is running--#
    def getStats(self):
        return {"msg": "ok"}

#--receives commands from the server and processes them--#    
    def processCmd(self,msg,conn):
        logger.info('Processing Command from server')
        self.temp = json.loads(msg)
        self.options[self.temp["command"]]()


class sensorThread(threading.Thread):

    def __init__ (self):
        threading.Thread.__init__(self)

#--sensor thread--#
    def run(self):
        logger.info('Sensor thread started')
        while True: 
            time.sleep(3000)
            readSensors()


class commsThread(threading.Thread):
    
    def __init__ (self):
        threading.Thread.__init__(self)
        self.messenger = messenger()

#--communication thread--#
    def run(self):
        logger.info('Command thread started')
        context = zmq.Context()
        logger.info('connecting to comms Server')
#--socket to receive messages on--#
        conn = context.socket(zmq.REP)
        conn.connect(SOCKET_ADDR)
        # Process tasks forever
        while True:
            msg = conn.recv()
            print msg
            logger.info('Message recieved:'+msg)
            conn.send_json(self.messenger.processCmd(msg,conn),0)
                

#Run the main thread
try:
#    threadA = sensorThread()
    threadB = commsThread()
#    logger.info('Starting sensor thread')
#    print("Started Sensor Thread.")
#    threadA.start()
    logger.info('Starting command thread')
    threadB.start()
    print ("Started Communications Thread.")
except Exception, e:
    for powerSource, boardPin in CIRCUIT_ONE.iteritems():
        gpio.output(boardPin,False)
    for powerSource, boardPin in CIRCUIT_TWO.iteritems():
        gpio.output(boardPin,False)
    print(str(e))
    logger.error(str(e))
    

    