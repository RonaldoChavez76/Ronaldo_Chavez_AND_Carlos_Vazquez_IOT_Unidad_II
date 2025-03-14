import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC_A = "utng/ky038/analogico"
MQTT_TOPIC_D = "utng/ky038/digital"
MQTT_CLIENT_ID = "ESP32_KY038"
MQTT_PORT = 1883

# Configuración del sensor KY-038
sensor_analogico = ADC(Pin(36))  # Salida analógica (A0)
sensor_analogico.width(ADC.WIDTH_10BIT)
sensor_analogico.atten(ADC.ATTN_11DB)

sensor_digital = Pin(39, Pin.IN)  # Salida digital (D0)

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

# Bucle principal: Leer valores y enviar actualización vía MQTT
while True:
    valor_analogico = sensor_analogico.read()  # Leer salida analógica (0-1023)
    valor_digital = sensor_digital.value()  # Leer salida digital (0 o 1)

    mensaje_a = "Intensidad de sonido (A0): {}".format(valor_analogico)
    mensaje_d = "¡Ruido detectado!" if valor_digital == 1 else "Ambiente silencioso"

    print(mensaje_a)
    print(mensaje_d)

    client.publish(MQTT_TOPIC_A, mensaje_a.encode())
    client.publish(MQTT_TOPIC_D, mensaje_d.encode())

    sleep(1)  # Leer cada 1 segundo
