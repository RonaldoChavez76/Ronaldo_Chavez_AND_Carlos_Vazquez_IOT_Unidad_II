import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky006"
MQTT_CLIENT_ID = "ESP32_KY006"
MQTT_PORT = 1883

# Configuración del Buzzer en el pin 15
buzzer = PWM(Pin(15))
buzzer.freq(1000)  # Frecuencia inicial en Hz
buzzer.duty(0)  # Inicialmente apagado

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

# Función para activar el buzzer
def sonar_buzzer(frecuencia=1000, duracion=1):
    buzzer.freq(frecuencia)
    buzzer.duty(512)  # Activar el buzzer con 50% de ciclo de trabajo
    sleep(duracion)
    buzzer.duty(0)  # Apagar el buzzer

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

# Bucle principal: sonar buzzer cada 5 segundos y enviar estado vía MQTT
while True:
    sonar_buzzer(1500, 1)  # Suena con 1500 Hz por 1 segundo
    mensaje = "Buzzer activo a 1500Hz"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje.encode())
    
    sleep(5)  # Espera 5 segundos antes de repetir
