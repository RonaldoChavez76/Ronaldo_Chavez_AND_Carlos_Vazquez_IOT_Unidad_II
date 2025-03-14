import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky018"
MQTT_CLIENT_ID = "ESP32_KY018"
MQTT_PORT = 1883

# Configuración del sensor KY-018 en el pin 36 (entrada analógica)
ldr_sensor = ADC(Pin(36))
ldr_sensor.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits (0-1023)
ldr_sensor.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V

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

# Bucle principal: Leer la intensidad de luz y enviar datos por MQTT
while True:
    valor_ldr = ldr_sensor.read()  # Leer valor entre 0-1023
    porcentaje_luz = (valor_ldr / 1023) * 100  # Convertir a porcentaje

    mensaje = "Nivel de luz: {:.2f}%".format(porcentaje_luz)
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(5)  # Leer cada 5 segundos
