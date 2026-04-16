import RPi.GPIO as GPIO
import time

LED = 18
BTN_UP = 17
BTN_DOWN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pwm = GPIO.PWM(LED, 1000)
pwm.start(0)

duty = 0

try:
    while True:
        if GPIO.input(BTN_UP):
            duty = min(100, duty + 5)
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.25)

        if GPIO.input(BTN_DOWN):
            duty = max(0, duty - 5)
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.25)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
