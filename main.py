# reference: https://github.com/letonai/picotemplogger/

import dht
import gc
import network
import ntptime
import socket
import time
import urequests
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, RTC

# Please fill in your Google Script Link here!
# Click on "Deploy" and then add "/exec" at the end!
sheetURL = ""

ssid = ''
password = ''

def connect():
    #Connect to WLAN
    print("Connecting to network...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection
    
def sendToSpreadsheet(wifi):
    for attempts in range(5):
        try:
            print(sheetURL+wifi)
            res = urequests.get(url=sheetURL+wifi)
            print("Request sent!")
            res.close()
            gc.collect()
            
        except:
            print("Error! Retrying...")
            continue

        else:
            break
        
    if (attempts >= 4):
        print("Unrecoverable error!")
        # do something else here like light up LED.
    
    atttempts = 0
    
def getFormattedCurrTime(adjustTimeZone):
    plusZeroTime = time.time()
    now = time.localtime(plusZeroTime + (adjustTimeZone * 3600))
    #add the %20 into the string for a space - the GET request doesn't process the space!
    timeStr = "{:02}-{:02}-{}%20{:02}:{:02}".format(now[2],now[1],now[0],now[3],now[4])
    return timeStr

ip = connect()
#connection = open_socket(ip)
#serve(connection)

rtc = RTC()
ntptime.settime()

dht11 = dht.DHT11(Pin(15))

prev = 0
timeStr = ''

minutes = 10
timeZone = 8

print("Time is set: ", getFormattedCurrTime(timeZone))

while True:
    curr = time.ticks_ms()
    if(curr - prev >=  minutes * 60 * 1000):
        prev = curr
        dht11.measure()
        timeStr = getFormattedCurrTime(timeZone)
        temp = dht11.temperature()
        humidity = dht11.humidity()
        print("{} - Temp: {}\xBAC, Humidity: {}%".format(timeStr, temp, humidity))
        sendToSpreadsheet("?datetime={}&humidity={}&temperature={}".format(timeStr, humidity, temp)) 
    else:
        time.sleep(minutes * 60)