import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/mq-9"
MQTT_CLIENT_ID = "ESP32_MQ9"
MQTT_PORT = 1883

# Configuración del sensor MQ-9 (Pin 34 para ESP32)
mq9 = ADC(Pin(34))
mq9.atten(ADC.ATTN_11DB)  # Permite medir hasta ~3.3V

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

# Función para leer el sensor MQ-9
def leer_mq9():
    return mq9.read()  # Devuelve un valor entre 0 y 4095 (12 bits)

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

valor_anterior = leer_mq9()
umbral = 30  # Umbral para evitar fluctuaciones insignificantes

# Bucle principal: actualiza el log rápidamente
while True:
    valor_actual = leer_mq9()
    
    # Solo publica si hay una variación significativa
    if abs(valor_actual - valor_anterior) > umbral:
        mensaje = "MQ-9: Lectura = {}".format(valor_actual)
        print(mensaje)  # Log en consola
        client.publish(MQTT_TOPIC, mensaje.encode())  # Enviar a MQTT
        valor_anterior = valor_actual  # Actualizar referencia
    
    sleep(0.5)  # Reduce el delay para actualización más rápida

