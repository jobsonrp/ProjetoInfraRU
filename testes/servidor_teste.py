# FAZENDO OS IMPORTS NECESSARIOS PARA A APLICACAO
import json
import sys
import os, urlparse
import paho.mqtt.client as mqtt
import pymysql
#import cgitb
from datetime import datetime

ipMV = sys.argv[1]

# CONEXAO COM O BANCO - DATABASE, USUARIO, SENHA E HOST
conn = pymysql.connect(
    db='dbru',
    user='admin',
    passwd='admin123',
    host=ipMV)
c = conn.cursor()

#cgitb.enable()

# CODIGO DE CONSULTA AO BANCO

# VERIFICA SE O RFID PASSADO EXISTE NO BANCO
def consulta(num):
    retorno = {}
    retorno["userId"] = 0
    retorno["userName"] = ""
    sql = "SELECT id,nome FROM Usuario WHERE rfid = '%s'" % (num)

    c.execute(sql)

    r = c.fetchall()

    if len(r) > 0:
        retorno["userId"] = int(r[0][0])
        retorno["userName"] = r[0][1] + ""

    return retorno

# VERIFICA SE DADO USUARIO POSSUI REGISTRO ABERTO ASSOCIADO A SEU RFID
# CASO NAO HAJA, O HORARIO E REGISTRADO E TEM SEU SATUS DEFINIDO COMO ABERTO (1).
# CASO HAJA, O HORARIO E REGISTRADO E O STATUS DEFINIDO COMO FECHADO (0)
'''def registro(userData):
    try:
        sql_consulta = "SELECT id FROM History WHERE idUser = %i AND status = 1;" % (userData["userId"])
        c.execute(sql_consulta)
        r = c.fetchall()
        if len(r) > 0:
            timestamp = datetime.now()
            id_hist = r[0][0]
            sql_update = "UPDATE `History` SET `status` = 0, `saida` = '%s' WHERE id = %i;" % (timestamp,id_hist)
            #print sql_update
            c.execute(sql_update)
            conn.commit()
            return "SAINDO/" + userData["userName"]
        else:
            sql_insert = "INSERT INTO History (idUser,status) VALUES (%i,1);" % (userData["userId"])
            c.execute(sql_insert)
            conn.commit()
            return "ENTRANDO/" + userData["userName"]

    except:
        return "ERRO";'''

# SOBREESCREVEMOS O COMPORTAMENTO DE ALGUMAS
# FUNCOES PROPRIAS DO MQTT

# EXECUTADA QUANDO UMA NOVA CONEXAO E FEITA
def on_connect(self, mosq, obj, rc):
    print("rc: " + str(rc))

# EXECUTADA QUANDO UMA NOVA MENSAGEM E LIDA NA FILA
# PUBLICA NA FILA DE RESPOSTA SE O ACESSO FOI/NAO FOI LIBERADO
# + O NOME DO CADASTRADO PARA EXIBICAO NO LCD
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    '''mensagem = msg.payload
    print type(mensagem)
    mjson = json.loads(mensagem)
    print mjson['nome']'''

    cons = consulta(str(msg.payload))

    if(cons["userName"] != ""):
	retorno = "%s" % cons
    else:
    	retorno = "Usuario nao cadastrado."
    mqttc.publish("retorno", retorno)
    print(retorno)

# EXECUTADO A CADA PUBLICACAO
def on_publish(mosq, obj, mid):
    print("Publish: " + str(mid))

# EXECUTADO A CADA FILA QUE UM SUBSCRIBE E DADO
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# EXECUTADO EM CADA ESCRITA NO LOG
def on_log(mosq, obj, level, string):
    print(string)

# CRIACAO DO OBJETO DO TIPO mqtt.Client
mqttc = mqtt.Client()

# SOBRESCRITA DOS METODOS NATIVOS DO MQTT
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# URL DO CLOUDMQTT E DA INSTANCIA AONDE AS FILAS ESTAO
# A URL DA INSTANCIA E COMPOSTA POR: mqtt://m10.cloudmqtt.com: + PORTA
# PORTA PODE SER ENCONTRADO NAS INFORMACOES DA INSTANCIA
url_str = os.environ.get('m10.cloudmqtt.com','mqtt://m10.cloudmqtt.com:16184')
url = urlparse.urlparse(url_str)

# ATRIBUICAO DO USUARIO COM ACESSO AS FILAS
#os parametros do username_pw_set sao os dados usuario e senha do MQTT
mqttc.username_pw_set("adm", "54321")
mqttc.connect(url.hostname, url.port)

# SUBSCRIBE NA FILA ACESSO
mqttc.subscribe("acesso", 0)

# LOOP ENQUANTO UM ERRO NAO FOR ENCONTRADO O NOSSO SERVIDOR ESTARA OUVINDO A FILA
# ACESSO E ESCREVENDO AS RESPOSTAS NA FILA RETORNO
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
