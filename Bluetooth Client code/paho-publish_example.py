import time
import paho.mqtt.client as mqtt


mqttc=mqtt.Client()
mqttc.username_pw_set('sam','mosquitto1894')
mqttc.connect("130.88.154.7",1894,60)
mqttc.loop_start()

while 1:
    (result,mid)=mqttc.publish("test-topic",'lalala',2)
    time.sleep(1)


