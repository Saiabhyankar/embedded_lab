import smbus2
import bme280
import time

PORT = 1
ADDRESS = 0x76

bus = smbus2.SMBus(PORT)
calibration_params = bme280.load_calibration_params(bus, ADDRESS)

try:
    while True:
        data = bme280.sample(bus, ADDRESS, calibration_params)
        print(f"Temperature: {data.temperature:.2f} C")
        print(f"Pressure: {data.pressure:.2f} hPa")
        print(f"Humidity: {data.humidity:.2f} %")
        print("-" * 30)
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    bus.close()
