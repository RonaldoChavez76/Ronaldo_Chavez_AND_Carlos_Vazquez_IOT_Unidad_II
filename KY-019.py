import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky019"
MQTT_CLIENT_ID = "ESP32_KY019"
MQTT_PORT = 1883

# Configuración del relevador en el pin 26
relevador = Pin(26, Pin.OUT)

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi conectada! IP:", sta_if.ifconfig()[0])

# Función para conectarse al broker MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Conectado a MQTT Broker:", MQTT_BROKER)
    return client

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

# Bucle principal: Encender y apagar el relevador cada 5 segundos y enviar estado por MQTT
while True:
    relevador.value(1)  # Encender relevador
    mensaje = "Relevador ACTIVADO"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(5)
    
    relevador.value(0)  # Apagar relevador
    mensaje = "Relevador DESACTIVADO"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(5)
