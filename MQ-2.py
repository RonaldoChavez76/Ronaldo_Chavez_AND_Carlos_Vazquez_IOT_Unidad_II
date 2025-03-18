import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/mq2"
MQTT_CLIENT_ID = "ESP32_MQ2"
MQTT_PORT = 1883

# Configuración del sensor MQ-2 (salida analógica en pin 34)
mq2 = ADC(Pin(34))
mq2.atten(ADC.ATTN_11DB)  # Permite medir hasta 3.3V

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

# Función para leer el sensor MQ-2
def leer_mq2():
    return mq2.read()  # Devuelve un valor entre 0 y 4095

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

valor_anterior = None
umbral = 50  # Umbral para detectar cambios significativos

# Bucle principal: lee el sensor y publica cambios vía MQTT
while True:
    valor_actual = leer_mq2()
    if valor_anterior is None or abs(valor_actual - valor_anterior) > umbral:
        mensaje = "MQ-2: Lectura = {}".format(valor_actual)
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje.encode())
        valor_anterior = valor_actual
    sleep(1)
