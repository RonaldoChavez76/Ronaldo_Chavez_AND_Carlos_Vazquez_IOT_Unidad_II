import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/mq-5"
MQTT_CLIENT_ID = "ESP32_MQ5"
MQTT_PORT = 1883

# Configuración del sensor MQ-5 (Pin 34 en ESP32)
mq5 = ADC(Pin(34))
mq5.atten(ADC.ATTN_11DB)  # Permite medir hasta ~3.3V

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

# Función para leer el sensor MQ-5
def leer_mq5():
    return mq5.read()  # Devuelve un valor entre 0 y 4095

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

valor_anterior = leer_mq5()
umbral = 30  # Umbral para evitar fluctuaciones pequeñas

# Bucle principal: actualiza solo si hay cambios significativos
while True:
    valor_actual = leer_mq5()
    
    # Solo actualiza si la diferencia es mayor al umbral
    if abs(valor_actual - valor_anterior) > umbral:
        mensaje = "MQ-5: Lectura = {}".format(valor_actual)
        print(mensaje)  # Mostrar en consola
        client.publish(MQTT_TOPIC, mensaje.encode())  # Enviar a MQTT
        valor_anterior = valor_actual  # Guardar último valor
    
    sleep(0.5)  # Menor delay para mejor actualización
