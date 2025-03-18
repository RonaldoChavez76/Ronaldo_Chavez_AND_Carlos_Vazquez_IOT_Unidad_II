#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "arg/salon/nivel_agua"

MQTT_PORT = 1883

# Configuración del sensor de agua en el pin 15
sensor_agua = Pin(15, Pin.IN)

#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Aqui va el nombre de tu internet', 'Aqui va la contraseña de tu internet')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi Conectada!")

#Funcion para subscribir al broker, topic
def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID,
    MQTT_BROKER, port=MQTT_PORT,
    user=MQTT_USER,
    password=MQTT_PASSWORD,
    keepalive=0)
    client.connect()
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

#Conectar a wifi
conectar_wifi()
#Subscripción a un broker mqtt
client = subscribir()

estado_anterior = None

#Ciclo infinito
while True:
    estado_actual = sensor_agua.value()
    
    if estado_actual != estado_anterior:  # Solo enviamos cambios en el estado del agua
        mensaje = "Agua detectada" if estado_actual == 1 else "No hay agua"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje)
    
    estado_anterior = estado_actual
    sleep(2)