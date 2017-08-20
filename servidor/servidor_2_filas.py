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
    retornoNodeMCU = {}
    retornoNodeMCU["userId"] = 0
    retornoNodeMCU["userName"] = ""
    sql = "SELECT id,nome FROM Usuario WHERE rfid = '%s'" % (num)

    c.execute(sql)

    r = c.fetchall()

    if len(r) > 0:
        retornoNodeMCU["userId"] = int(r[0][0])
        retornoNodeMCU["userName"] = r[0][1] + ""

    return retornoNodeMCU

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
def on_connect_fila1(self, mosq, obj, rc):
    print("rc: " + str(rc))

# EXECUTADA QUANDO UMA NOVA MENSAGEM E LIDA NA FILA
# PUBLICA NA FILA DE RESPOSTA SE O ACESSO FOI/NAO FOI LIBERADO
# + O NOME DO CADASTRADO PARA EXIBICAO NO LCD
def on_message_fila1(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    #mensagem = '{"userName":"Usuario1","userId":"1"}' #msg.payload
    mensagem = msg.payload
    print "tipo da mensagem = ", mensagem
    mjson = json.loads(mensagem)
    print "RFID = ", mjson['RFID']

    '''cons = consulta(str(msg.payload))

    if(cons["userName"] != ""):
	retornoNodeMCU = "%s" % cons
    else:
    	retornoNodeMCU = "Usuario nao cadastrado."
    mqttcF1.publish("retornoNodeMCU", retornoNodeMCU)
    print(retornoNodeMCU)'''

# EXECUTADO A CADA PUBLICACAO
def on_publish_fila1(mosq, obj, mid):
    print("Publish: " + str(mid))

# EXECUTADO A CADA FILA QUE UM SUBSCRIBE E DADO
def on_subscribe_fila1(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# EXECUTADA QUANDO UMA NOVA CONEXAO E FEITA
def on_connect_fila2(self, mosq, obj, rc):
    print("rc: " + str(rc))

# EXECUTADA QUANDO UMA NOVA MENSAGEM E LIDA NA FILA
# PUBLICA NA FILA DE RESPOSTA SE O ACESSO FOI/NAO FOI LIBERADO
# + O NOME DO CADASTRADO PARA EXIBICAO NO LCD
def on_message_fila2(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    mensagem = msg.payload
    print "tipo da mensagem = ", mensagem
    mjson = json.loads(mensagem)
    print "RFID = ", mjson['RFID']

    '''cons = consulta(str(msg.payload))

    if(cons["userName"] != ""):
	retornoNodeMCU = "%s" % cons
    else:
    	retornoNodeMCU = "Usuario nao cadastrado."
    mqttcF2.publish("retornoAndroid", retornoNodeMCU)
    print(retornoNodeMCU)'''

# EXECUTADO A CADA PUBLICACAO
def on_publish_fila2(mosq, obj, mid):
    print("Publish: " + str(mid))

# EXECUTADO A CADA FILA QUE UM SUBSCRIBE E DADO
def on_subscribe_fila2(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# EXECUTADO EM CADA ESCRITA NO LOG
def on_log(mosq, obj, level, string):
    print(string)

# CRIACAO DO OBJETO DO TIPO mqtt.Client
mqttcF1 = mqtt.Client()
# CRIACAO DO OBJETO DO TIPO mqtt.Client
mqttcF2 = mqtt.Client()

# SOBRESCRITA DOS METODOS NATIVOS DO MQTT
mqttcF1.on_message = on_message_fila1
mqttcF1.on_connect = on_connect_fila1
mqttcF1.on_publish = on_publish_fila1
mqttcF1.on_subscribe = on_subscribe_fila1

# SOBRESCRITA DOS METODOS NATIVOS DO MQTT
mqttcF2.on_message = on_message_fila2
mqttcF2.on_connect = on_connect_fila2
mqttcF2.on_publish = on_publish_fila2
mqttcF2.on_subscribe = on_subscribe_fila2

# URL DO CLOUDMQTT E DA INSTANCIA AONDE AS FILAS ESTAO
# A URL DA INSTANCIA E COMPOSTA POR: mqtt://m10.cloudmqtt.com: + PORTA
# PORTA PODE SER ENCONTRADO NAS INFORMACOES DA INSTANCIA
url_str = os.environ.get('m10.cloudmqtt.com','mqtt://m10.cloudmqtt.com:16184')
url = urlparse.urlparse(url_str)

# ATRIBUICAO DO USUARIO COM ACESSO AS FILAS
#os parametros do username_pw_set sao os dados usuario e senha do MQTT
mqttcF1.username_pw_set("adm", "54321")
mqttcF1.connect(url.hostname, url.port)
mqttcF2.username_pw_set("adm", "54321")
mqttcF2.connect(url.hostname, url.port)

# SUBSCRIBE NA FILA ACESSO
mqttcF1.subscribe("acessoNodeMCU", 0)
mqttcF2.subscribe("acessoAndroid", 0)

# LOOP ENQUANTO UM ERRO NAO FOR ENCONTRADO O NOSSO SERVIDOR ESTARA OUVINDO A FILA
# ACESSO E ESCREVENDO AS RESPOSTAS NA FILA RETORNO
rc = 0
while rc == 0:
    rcF1 = mqttcF1.loop()
    rcF2 = mqttcF2.loop()		
    rc = mqttcF1.loop() + mqttcF2.loop()
print("rcF1:" + str(rcF1) + " | rcF2:" + str(rcF2) )
