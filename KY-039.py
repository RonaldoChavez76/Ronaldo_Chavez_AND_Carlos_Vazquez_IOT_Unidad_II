import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky039"
MQTT_CLIENT_ID = "ESP32_KY039"
MQTT_PORT = 1883

# Configuración del sensor KY-039 en el pin 36 (entrada analógica)
sensor_pulso = ADC(Pin(36))
sensor_pulso.width(ADC.WIDTH_10BIT)
sensor_pulso.atten(ADC.ATTN_11DB)

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

# Bucle principal: Leer el pulso y enviar datos por MQTT
while True:
    valor_pulso = sensor_pulso.read()  # Leer salida analógica (0-1023)
    voltaje = valor_pulso * (3.3 / 1023)  # Convertir a voltaje

    mensaje = "Nivel de pulso: {:.2f} V".format(voltaje)
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(1)  # Leer
