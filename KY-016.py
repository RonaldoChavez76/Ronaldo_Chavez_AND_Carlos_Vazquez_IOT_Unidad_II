import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky016"
MQTT_CLIENT_ID = "ESP32_KY016"
MQTT_PORT = 1883

# Configuración de los pines PWM para el LED RGB
pin_rojo = PWM(Pin(15), freq=1000)  # Rojo
pin_verde = PWM(Pin(2), freq=1000)  # Verde
pin_azul = PWM(Pin(4), freq=1000)   # Azul

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

# Función para cambiar el color del LED
def cambiar_color(r, g, b):
    pin_rojo.duty(r)
    pin_verde.duty(g)
    pin_azul.duty(b)
    mensaje = f"Color RGB -> Rojo: {r}, Verde: {g}, Azul: {b}"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

# Bucle principal: Alternar colores cada 3 segundos y enviar actualización vía MQTT
colores = [
    (1023, 0, 0),    # Rojo
    (0, 1023, 0),    # Verde
    (0, 0, 1023),    # Azul
    (1023, 1023, 0), # Amarillo
    (0, 1023, 1023), # Cian
    (1023, 0, 1023), # Magenta
    (512, 512, 512)  # Blanco suave
]

while True:
    for color in colores:
        cambiar_color(*color)
        sleep(3)  # Cambia cada 3 segundos
