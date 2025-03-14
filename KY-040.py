import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky040"
MQTT_CLIENT_ID = "ESP32_KY040"
MQTT_PORT = 1883

# Configuración del encoder KY-040
clk = Pin(32, Pin.IN, Pin.PULL_UP)  # Pin CLK
dt = Pin(33, Pin.IN, Pin.PULL_UP)   # Pin DT
sw = Pin(25, Pin.IN, Pin.PULL_UP)   # Botón pulsador

# Variables para el estado del encoder
clk_anterior = clk.value()

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

# Bucle principal: Detectar rotaciones y clics en el botón
while True:
    clk_actual = clk.value()
    if clk_actual != clk_anterior:  # Detectar cambio en CLK
        if dt.value() != clk_actual:
            mensaje = "Rotación en sentido horario"
        else:
            mensaje = "Rotación en sentido antihorario"

        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje.encode())

    clk_anterior = clk_actual  # Guardar estado anterior

    if sw.value() == 0:  # Detectar pulsación del botón
        mensaje = "Botón del encoder PRESIONADO"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje.encode())
        sleep(0.5)  # Pequeño retardo para evitar rebotes

    sleep(0.1)  # Evitar lecturas muy rápidas
