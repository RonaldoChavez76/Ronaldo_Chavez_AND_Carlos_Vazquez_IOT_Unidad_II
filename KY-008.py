import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky008"
MQTT_CLIENT_ID = "ESP32_KY008"
MQTT_PORT = 1883

# Configuración del LED Láser en el pin 14
laser = Pin(14, Pin.OUT)

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

# Bucle principal: Encender y apagar el láser cada 5 segundos y enviar el estado vía MQTT
while True:
    laser.value(1)  # Encender láser
    mensaje = "Láser ENCENDIDO"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())
    
    sleep(5)
    
    laser.value(0)  # Apagar láser
    mensaje = "Láser APAGADO"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())
    
    sleep(5)
