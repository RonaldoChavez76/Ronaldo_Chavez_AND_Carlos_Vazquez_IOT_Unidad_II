import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky002"
MQTT_CLIENT_ID = "ESP32_KY002"
MQTT_PORT = 1883

# Configuración del sensor KY-002 en el pin 15
sensor_vibracion = Pin(15, Pin.IN)

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

estado_anterior = None

# Bucle principal: detectar vibración y enviar cambios vía MQTT
while True:
    estado_actual = sensor_vibracion.value()
    if estado_actual != estado_anterior:
        if estado_actual == 1:
            mensaje = "Vibracion detectada"
        else:
            mensaje = "Sin vibracion"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje.encode())
        estado_anterior = estado_actual
    sleep(0.1)
