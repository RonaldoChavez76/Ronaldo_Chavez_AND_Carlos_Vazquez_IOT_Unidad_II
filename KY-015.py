import network
from umqtt.simple import MQTTClient
from machine import Pin
import dht
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC_TEMPERATURA = "utng/ky015/temperatura"
MQTT_TOPIC_HUMEDAD = "utng/ky015/humedad"
MQTT_CLIENT_ID = "ESP32_KY015"
MQTT_PORT = 1883

# Configuración del sensor DHT11 en el pin 4
sensor_dht = dht.DHT11(Pin(4))

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

# Bucle principal: Leer temperatura y humedad y enviar datos vía MQTT
while True:
    try:
        sensor_dht.measure()
        temperatura = sensor_dht.temperature()  # Temperatura en °C
        humedad = sensor_dht.humidity()  # Humedad en %

        # Enviar temperatura
        mensaje_temp = "Temperatura: {:.2f} °C".format(temperatura)
        print(mensaje_temp)
        client.publish(MQTT_TOPIC_TEMPERATURA, mensaje_temp.encode())

        # Enviar humedad
        mensaje_hum = "Humedad: {:.2f} %".format(humedad)
        print(mensaje_hum)
        client.publish(MQTT_TOPIC_HUMEDAD, mensaje_hum.encode())

    except Exception as e:
        print("Error al leer el sensor:", e)

    sleep(5)  # Leer cada 5 segundos
