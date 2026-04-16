import Adafruit_DHT
import time

SENSOR = Adafruit_DHT.DHT22
PIN = 4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(SENSOR, PIN)

        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f} C   Humidity: {humidity:.1f} %")
        else:
            print("Failed to read DHT sensor")

        time.sleep(2)
except KeyboardInterrupt:
    pass
