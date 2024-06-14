from main.configs.broker_configs import mqtt_broker_configs
from main.mqtt_connection.callbacks import *
from main.mqtt_connection.mqtt_client_conection import MqttClientConnection
import paho.mqtt.client as mqtt
import json
import uuid

class Publisher:
    def __init__(self):
        #self.client_id = 'client_' + os.urandom(4).hex()
        self.client_id = 'client_' + hex(uuid.getnode())
        self.__mqtt_connection = MqttClientConnection(
            mqtt_broker_configs["HOST"], mqtt_broker_configs["PORT"], self.client_id, mqtt_broker_configs["KEEPALIVE"])
        self.__mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.__mqtt_client.on_connect = on_connect_all_response
        self.__mqtt_client.on_message = on_message_all_response
        self.__mqtt_connection.start_connection(self.__mqtt_client)
        self.__mqtt_client.loop_start()

    ## REQUEST FILE METHODS
    def sendToRequestFileTopic(self, topic: str):
        message = {
            'client_id': self.client_id
        }
        #print('Me inscrevi no tópico ' + mqtt_broker_configs['RESPONSE_FILE_TOPIC'] + topic + "/" + self.client_id)
        self.__mqtt_client.subscribe(mqtt_broker_configs['RESPONSE_FILE_TOPIC'] + topic + "/" + self.client_id, qos=2)
        #print('Publiquei a mensagem ' + json.dumps(message) + ' no tópico ' + mqtt_broker_configs['REQUEST_FILE_TOPIC'] + topic)
        self.__mqtt_client.publish(topic=mqtt_broker_configs['REQUEST_FILE_TOPIC'] + topic, payload=json.dumps(message), qos=2)

    ## UPLOAD FILE METHODS
    def sendToUploadFileTopic(self, topic: str):
        #print('Me inscrevi no tópico ' + mqtt_broker_configs['REQUEST_FILE_TOPIC'] + topic)
        self.__mqtt_client.subscribe(mqtt_broker_configs['REQUEST_FILE_TOPIC'] + topic, qos=2)

    ## STOP METHODS
    def stop(self):
        self.__mqtt_client.loop_stop()
        self.__mqtt_client.disconnect()
