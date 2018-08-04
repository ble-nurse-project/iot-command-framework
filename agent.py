# Dependencies Import
import sys
import paho.mqtt.client as mqtt
from subprocess import Popen, PIPE
from subprocess import check_output, STDOUT, CalledProcessError

# Global value initialize
MQTT_SERVER = sys.argv[1]
DEVICE_NAME = sys.argv[2]
TOPIC_NAME = "ble/" + DEVICE_NAME
RESPONSE_TOPIC_NAME = TOPIC_NAME  + "/response"

# MQTT Initialize
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print("Connected to  %s" % MQTT_SERVER)
    client.subscribe(TOPIC_NAME);
    print("Subscribed " + TOPIC_NAME)
# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    if(msg.topic == TOPIC_NAME):
        try:
            output = check_output(str(msg.payload).split(), stderr=STDOUT)
            client.publish(RESPONSE_TOPIC_NAME, output)
        except CalledProcessError as exc:
            client.publish(RESPONSE_TOPIC_NAME, exc.output)
    else:
        print("This is not what i'm subscribing")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

client.publish(RESPONSE_TOPIC_NAME, "connected")
# Start collecting beacon sensor data
client.loop_forever()
