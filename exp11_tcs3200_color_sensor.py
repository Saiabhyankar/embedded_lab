import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

S0 = 5
S1 = 6
S2 = 13
S3 = 19
OUT = 26

GPIO.setup(S0, GPIO.OUT)
GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)

GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.LOW)   # 20% scaling

def set_filter(s2, s3):
    GPIO.output(S2, s2)
    GPIO.output(S3, s3)
    time.sleep(0.05)

def read_frequency(sample_time=0.2):
    count = 0
    end = time.time() + sample_time
    last = GPIO.input(OUT)

    while time.time() < end:
        current = GPIO.input(OUT)
        if current != last:
            count += 1
            last = current
    return count

try:
    while True:
        set_filter(GPIO.LOW, GPIO.LOW)   # Red
        red = read_frequency()

        set_filter(GPIO.HIGH, GPIO.HIGH)  # Green
        green = read_frequency()

        set_filter(GPIO.LOW, GPIO.HIGH)   # Blue
        blue = read_frequency()

        print(f"Red: {red}  Green: {green}  Blue: {blue}")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
