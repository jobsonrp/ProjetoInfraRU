import time
import json
import os
import urlparse
import paho.mqtt.client as mqtt

def on_connect(
    self,
    mosq,
    obj,
    rc,
    ):
    print 'rc: ' + str(rc)

def on_publish(mosq, obj, mid):
    print 'Publish: J1' + str(mid)

def on_log(
    mosq,
    obj,
    level,
    string,
    ):
    print string

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

url_str = os.environ.get('m10.cloudmqtt.com',
                         'mqtt://m10.cloudmqtt.com:16184')

url = urlparse.urlparse(url_str)

mqttc.username_pw_set('adm', '54321')
mqttc.connect(url.hostname, url.port)

usuario = {}
usuario['OP'] = 'SALDO'
usuario['CPF'] = '111'

mqttc.publish('acessoAndroid', json.dumps(usuario))

time.sleep(1)

usuario = {}
usuario['OP'] = 'RECARGA'
usuario['CPF'] = '123456'
usuario['VALOR'] = '4.64'

mqttc.publish('acessoAndroid', json.dumps(usuario))

time.sleep(1)

usuario = {}
usuario['OP'] = 'CADASTRO'
usuario['NOME'] = 'Joao'
usuario['CPF'] = '98743'
usuario['RFID'] = '888'

mqttc.publish('acessoAndroid', json.dumps(usuario))

time.sleep(1)

usuario = {}
usuario['OP'] = 'SALDO'
usuario['CPF'] = '123456'

mqttc.publish('acessoAndroid', json.dumps(usuario))
