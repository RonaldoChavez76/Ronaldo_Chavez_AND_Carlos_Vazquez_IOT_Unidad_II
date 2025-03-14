import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky029"
MQTT_CLIENT_ID = "ESP32_KY029"
MQTT_PORT = 1883

# Configuración del LED de 2 colores en los pines 12 y 14
led_rojo = Pin(12, Pin.OUT)
led_verde = Pin(14, Pin.OUT)

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

# Bucle principal: Alternar entre rojo y verde cada 3 segundos y enviar el estado por MQTT
while True:
    # Encender LED Rojo y apagar Verde
    led_rojo.value(1)
    led_verde.value(0)
    mensaje = "LED Rojo ENCENDIDO, LED Verde APAGADO"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())
    sleep(3)
    
    # Apagar LED Rojo y encender Verde
    led_rojo.value(0)
    led_verde.value(1)
    mensaje = "LED Rojo APAGADO, LED Verde ENCENDIDO"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())
    sleep(3)
