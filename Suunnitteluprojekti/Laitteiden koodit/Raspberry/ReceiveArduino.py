 
#!/usr/bin/env python
#!/usr/bin/python

import demjson

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

db = MySQLdb.connect("172.16.7.120", "jessetestaa", "password", "mittaridata")
curs=db.cursor()

import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev




 
GPIO.setmode(GPIO.BCM)
 
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
 
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
 
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
 
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
 
radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()
 
while(1):
    # ackPL = [1]
    while not radio.available(0):
        print("Tämä on viestin tarkistus looppi")
        time.sleep(1 / 1)
    
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))
    print("tarkastus")

    MeterID = receivedMessage[0]
    Humidity = receivedMessage[2]
    Temperature = receivedMessage[4]

    #for i in range(len(receivedMessage)):
     #   print(i,receivedMessage[i]);

    print(MeterID)
    print(Humidity)
    print(Temperature)

    json = demjson.encode(Temperature)
    json2 = demjson.encode(MeterID)
    json3 = demjson.encode(Humidity)
    #print(json)
    #print(json2)
    #print(json3)
   # print("Translating the receivedMessage into unicode characters")
    #string = ""
    #for n in receivedMessage:
        # Decode into standard unicode set
     #   if (n >= 32 and n <= 126):
     #       string += chr(n)
    #print("Out received message decodes to: {}".format(string))
    with db:
        curs.execute ("INSERT INTO measuredata (tdate, ttime, meterID, humidity, temperature) VALUES(CURRENT_DATE(), NOW(), "+str(MeterID)+", "+str(Humidity)+", "+str(Temperature)+" )")
        db.commit()
        print("data committed")


    
