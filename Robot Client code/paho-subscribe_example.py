import paho.mqtt.client as mqtt

topic="ds4"                 # MQTT broker topic
myclient="my-paho-client"           # MQTT broker My Client
user="sam"                     # MQTT broker user
pw="mosquitto1894"                       # MQTT broker password
host="130.88.154.7"                # MQTT broker host
port=1894                       # MQTT broker port
value="123"                     # somethin i need for myapp

def on_connect(mqttc, userdata, rc):
    print('connected...rc=' + str(rc))
    mqttc.subscribe(topic, qos=0)

def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))

def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' + 
          str(msg.qos) + ', message: ' + str(msg.payload))

def on_subscribe(mqttc, userdata, mid, granted_qos):
    print('subscribed (qos=' + str(granted_qos) + ')')

def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    print('unsubscribed (qos=' + str(granted_qos) + ')')

mqttc = mqtt.Client(myclient)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.username_pw_set(user,pw)
mqttc.connect(host, port, 60)
mqttc.loop_forever()

