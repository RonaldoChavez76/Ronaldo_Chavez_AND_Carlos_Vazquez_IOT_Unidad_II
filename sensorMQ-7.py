import network
import time
import machine
from umqtt.simple import MQTTClient

# --- Configuración WiFi ---
SSID = "Ronaldo SIUUU"
PASSWORD = "11111111"

# --- Configuración MQTT ---
MQTT_BROKER = "broker.emqx.io"
MQTT_CLIENT_ID = b"ESP32_MQ7"  # client_id en bytes
MQTT_TOPIC = "utng/sensors"
MQTT_PORT = 1883

# --- Configuración del sensor MQ-7 ---
# Canal analógico (AO)
mq7_ao = machine.ADC(machine.Pin(32))
mq7_ao.atten(machine.ADC.ATTN_11DB)   # Permite leer de 0 a ~3.3V
mq7_ao.width(machine.ADC.WIDTH_12BIT) # Resolución de 12 bits (0 a 4095)

# Canal digital (DO), si tu módulo lo proporciona
mq7_do = machine.Pin(33, machine.Pin.IN)

# Pin para controlar el ciclo del calentador del sensor
heater_control = machine.Pin(25, machine.Pin.OUT)

def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print("\nWiFi conectada:", sta_if.ifconfig())

def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=60)
    client.connect()
    print("Conectado al broker MQTT:", MQTT_BROKER)
    return client

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

def publicar_estado(estado, valor_ao, valor_do):
    global client  # Usamos la variable global para re-asignarla en caso de error
    mensaje = "{} | AO: {} | DO: {}".format(estado, valor_ao, valor_do)
    print("Publicando:", mensaje)
    try:
        client.publish(MQTT_TOPIC, mensaje)
    except OSError as e:
        print("Error al publicar:", e)
        client = conectar_mqtt()  # Reintenta la conexión

while True:
    # ------------------------------
    # Fase de calentamiento (alta tensión: ~5V)
    # ------------------------------
    print("Fase de calentamiento: 60 segundos a alta tensión")
    heater_control.on()   # Activa la alta tensión (calentamiento)
    time.sleep(60)

    # ------------------------------
    # Fase de medición (baja tensión: ~1.4V)
    # ------------------------------
    print("Fase de medición: 90 segundos a baja tensión")
    heater_control.off()  # Cambia a baja tensión para medir

    # Esperamos unos segundos para que el sensor se estabilice en la fase de medición
    time.sleep(5)

    # Durante la fase de medición (restantes 85 segundos), lee constantemente
    measurement_duration = 85  # segundos
    sample_interval = 1        # intervalo de 1 segundo entre lecturas
    start_time = time.time()
    
    while time.time() - start_time < measurement_duration:
        valor_analogico = mq7_ao.read()
        valor_digital = mq7_do.value()
        
        # Define un umbral (ajusta este valor según tu calibración)
        UMBRAL = 1200  
        if valor_analogico >= UMBRAL:
            estado = "gas detectado"
        else:
            estado = "sin gas"
        
        print("Lectura MQ-7 -> AO: {} | DO: {} => {}".format(valor_analogico, valor_digital, estado))
        publicar_estado(estado, valor_analogico, valor_digital)
        time.sleep(sample_interval)
