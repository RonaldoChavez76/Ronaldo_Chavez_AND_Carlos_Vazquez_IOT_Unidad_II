import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky013"
MQTT_CLIENT_ID = "ESP32_KY013"
MQTT_PORT = 1883

# Configuración del sensor KY-013 en el pin 34 (entrada analógica)
sensor_temp = ADC(Pin(34))
sensor_temp.width(ADC.WIDTH_10BIT)  # 10 bits de resolución (0-1023)
sensor_temp.atten(ADC.ATTN_11DB)  # Rango 0-3.3V

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

# Función para leer la temperatura (estimación basada en voltaje)
def leer_temperatura():
    valor_analogico = sensor_temp.read()  # Leer valor entre 0-1023
    voltaje = valor_analogico * (3.3 / 1023)  # Convertir a voltaje
    temperatura = (voltaje - 0.5) * 100  # Aproximación de temperatura en °C
    return temperatura

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

# Bucle principal: Leer temperatura y enviar actualización vía MQTT
while True:
    temperatura = leer_temperatura()
    mensaje = "Temperatura: {:.2f} °C".format(temperatura)
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

    sleep(5)  # Leer cada 5 segundos
