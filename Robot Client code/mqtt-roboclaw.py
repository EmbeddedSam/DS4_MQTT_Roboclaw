import time
import roboclaw
from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import serial
import sys

#Global Vars
address = 0x80              #Roboclaw Address

topic="ds4"                 # MQTT broker topic
user="sam"                  # MQTT broker user
pw="mosquitto1894"          # MQTT broker password
host="130.88.154.7"         # MQTT broker host
port=1894                   # MQTT broker port
value="123"                 # somethin i need for myapp


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (200,50,50)
white = (255,255,255)


#Sense Hat stuff
sense = SenseHat()
sense.clear()


#Roboclaw stuff--------------------------------
#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
def AttemptToConnectToRoboClaw():
    try:
        roboclaw.Open("/dev/ttyACM0",115200)
        #Motor safe state
        roboclaw.ForwardMixed(address, 0)
        roboclaw.TurnRightMixed(address, 0)
        sense.set_pixel(1, 7, green)
    except Exception as e:
        print("problem with roboclaw")
        print e
        sense.set_pixel(1, 7, red)



def on_connect(mqttc, userdata, rc):
    print('connected...rc=' + str(rc))
    mqttc.subscribe(topic, qos=0)
    sense.set_pixel(0, 7, green)

def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))
    sense.set_pixel(0, 7, red)

def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' + 
        str(msg.qos) + ', message: ' + str(msg.payload))

    if(msg.topic == 'ds4') and (msg.payload == 'X'):
        print ('X received')
        sense.set_pixel(7, 0, blue)
        try:
            roboclaw.ForwardM2(address, 32)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()


    if(msg.topic == 'ds4') and (msg.payload == 'Square'):
        print ('Square received')
        sense.set_pixel(7,0, pink)
        try:
            roboclaw.ForwardM2(address, 64)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()

        
    if(msg.topic == 'ds4') and (msg.payload == 'Circle'):
        print ('Circle received')
        sense.set_pixel(7, 0, red)
        try:
            roboclaw.ForwardM2(address, 96)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()


    if(msg.topic == 'ds4') and (msg.payload == 'Triangle'):
        print ('Triangle received')
        sense.set_pixel(7, 0, green)
        try:
            roboclaw.ForwardM2(address, 127)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()


    if(msg.topic == 'ds4') and (msg.payload == 'Options'):
        print ('Options received')
        sense.set_pixel(7, 0, white)
        try:
            roboclaw.ForwardM2(address, 0)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print('subscribed (qos=' + str(granted_qos) + ')')

def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    print('unsubscribed (qos=' + str(granted_qos) + ')')


AttemptToConnectToRoboClaw()

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.username_pw_set(user,pw)
mqttc.connect(host, port, 10)
mqttc.loop_forever() #start unthreaded as we aren't doing anything else here

