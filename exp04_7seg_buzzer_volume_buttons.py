import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

segments = [2, 3, 4, 17, 27, 22, 10]  # a, b, c, d, e, f, g
BUZZER = 18
BTN_UP = 23
BTN_DOWN = 24

for pin in segments:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

digits = [
    [1,1,1,1,1,1,0],  # 0
    [0,1,1,0,0,0,0],  # 1
    [1,1,0,1,1,0,1],  # 2
    [1,1,1,1,0,0,1],  # 3
    [0,1,1,0,0,1,1],  # 4
    [1,0,1,1,0,1,1],  # 5
    [1,0,1,1,1,1,1],  # 6
    [1,1,1,0,0,0,0],  # 7
    [1,1,1,1,1,1,1],  # 8
    [1,1,1,1,0,1,1],  # 9
]

def display(num):   
    for i, pin in enumerate(segments):
        GPIO.output(pin, GPIO.HIGH if digits[num][i] else GPIO.LOW)

pwm = GPIO.PWM(BUZZER, 1000)
pwm.start(0)

volume = 0
display(volume)
pwm.ChangeDutyCycle(volume * 10)

try:
    while True:
        if GPIO.input(BTN_UP):
            volume = min(9, volume + 1)
            display(volume)
            pwm.ChangeDutyCycle(volume * 10)
            time.sleep(0.25)

        if GPIO.input(BTN_DOWN):
            volume = max(0, volume - 1)
            display(volume)
            pwm.ChangeDutyCycle(volume * 10)
            time.sleep(0.25)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
