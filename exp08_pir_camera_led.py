from gpiozero import MotionSensor, LED
from picamera import PiCamera
from time import sleep
import datetime

pir = MotionSensor(17)
led = LED(18)
camera = PiCamera()

camera.resolution = (1024, 768)
camera.brightness = 60
camera.contrast = 20
camera.image_effect = 'none'

try:
    while True:
        pir.wait_for_motion()
        for i in range(3):
            led.on()
            sleep(0.2)
            led.off()
            sleep(0.2)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        camera.capture(f"shot1_{stamp}.jpg")
        sleep(1)
        camera.capture(f"shot2_{stamp}.jpg")
        pir.wait_for_no_motion()
except KeyboardInterrupt:
    pass
finally:
    camera.close()
