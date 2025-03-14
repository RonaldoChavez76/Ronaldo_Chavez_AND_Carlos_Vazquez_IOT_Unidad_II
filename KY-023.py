import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de WiFi
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# Configuración MQTT
MQTT_BROKER = "broker.emqx.io"
NMQTT_TOPIC_X = "utng/ky023/x"
MQTT_TOPIC_Y = "utng/ky023/y"
MQTT_TOPIC_BTN = "utng/ky023/boton"
MQTT_CLIENT_ID = "ESP32_KY023"
MQTT_PORT = 1883

# Configuración del joystick
joy_x = ADC(Pin(34))  # Eje X
joy_x.width(ADC.WIDTH_10BIT)
joy_x.atten(ADC.ATTN_11DB)

joy_y = ADC(Pin(35))  # Eje Y
joy_y.width(ADC.WIDTH_10BIT)
joy_y.atten(ADC.ATTN_11DB)

boton = Pin(32, Pin.IN, Pin.PULL_UP)  # Botón del joystick

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

# Bucle principal: Leer valores del joystick y enviar actualización vía MQTT
while True:
    x_val = joy_x.read()  # Leer eje X (0-1023)
    y_val = joy_y.read()  # Leer eje Y (0-1023)
    boton_val = boton.value()  # Leer botón (0=presionado, 1=no presionado)

    mensaje_x = "Joystick X: {}".format(x_val)
    mensaje_y = "Joystick Y: {}".format(y_val)
    mensaje_btn = "Botón PRESIONADO" if boton_val == 0 else "Botón NO PRESIONADO"

    print(mensaje_x)
    print(mensaje_y)
    print(mensaje_btn)

    client.publish(MQTT_TOPIC_X, mensaje_x.encode())
    client.publish(MQTT_TOPIC_Y, mensaje_y.encode())
    client.publish(MQTT_TOPIC_BTN, mensaje_btn.encode())

    sleep(1)  # Leer cada 1 segundo
