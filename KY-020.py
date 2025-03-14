import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky020"
MQTT_CLIENT_ID = "ESP32_KY020"
MQTT_PORT = 1883

# Configuración del sensor KY-020 en el pin 25
sensor_inclinacion = Pin(25, Pin.IN)

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

# Bucle principal: Detectar inclinación y enviar estado por MQTT
estado_anterior = None

while True:
    estado_actual = sensor_inclinacion.value()
    
    if estado_actual != estado_anterior:  # Solo enviar datos si hay cambio
        if estado_actual == 1:
            mensaje = "Sensor de inclinación ACTIVADO"
        else:
            mensaje = "Sensor de inclinación en posición normal"
        
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje.encode())
        
        estado_anterior = estado_actual  # Actualizar estado anterior

    sleep(0.5)  # Pequeña pausa para evitar envíos constantes
