import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky005"
MQTT_CLIENT_ID = "ESP32_KY005"
MQTT_PORT = 1883

# Configuración del emisor infrarrojo KY-005 en el pin 15
led_ir = Pin(15, Pin.OUT)

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

# Bucle principal: Encender y apagar el LED IR cada segundo
while True:
    led_ir.on()
    mensaje = "LED IR encendido"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(1)

    led_ir.off()
    mensaje = "LED IR apagado"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(1)
