import network
import onewire, ds18x20
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "utng/ky001"
MQTT_CLIENT_ID = "ESP32_KY001"
MQTT_PORT = 1883

# Configuración del sensor KY-001 (DS18B20) en el pin 4
ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

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

# Detectar dispositivos en el bus 1-Wire
roms = ds_sensor.scan()
print("Dispositivos encontrados:", roms)

temperatura_anterior = None
umbral = 0.5  # Cambio mínimo para enviar actualización

# Bucle principal: leer temperatura y enviar cambios vía MQTT
while True:
    ds_sensor.convert_temp()
    sleep(1)  # Esperar conversión
    for rom in roms:
        temperatura = ds_sensor.read_temp(rom)
        if temperatura_anterior is None or abs(temperatura - temperatura_anterior) > umbral:
            mensaje = "Temperatura: {:.2f} C".format(temperatura)
            print(mensaje)
            client.publish(MQTT_TOPIC, mensaje.encode())
            temperatura_anterior = temperatura
    sleep(2)
