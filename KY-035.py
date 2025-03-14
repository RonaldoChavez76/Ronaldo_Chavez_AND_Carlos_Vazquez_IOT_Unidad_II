import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky035"
MQTT_CLIENT_ID = "ESP32_KY035"
MQTT_PORT = 1883

# Configuración del sensor KY-035 en el pin 36 (entrada analógica)
sensor_hall = ADC(Pin(36))
sensor_hall.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits (0-1023)
sensor_hall.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V

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

# Bucle principal: Leer la intensidad del campo magnético y enviar datos por MQTT
while True:
    valor_hall = sensor_hall.read()  # Leer valor entre 0-1023
    voltaje = valor_hall * (3.3 / 1023)  # Convertir a voltaje

    mensaje = "Intensidad del campo magnético: {:.2f} V".format(voltaje)
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(1)  # Leer cada 1 segundo
