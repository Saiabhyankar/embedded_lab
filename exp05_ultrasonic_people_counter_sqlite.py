import RPi.GPIO as GPIO
import time
import sqlite3

GPIO.setmode(GPIO.BCM)

TRIG1, ECHO1 = 23, 24
TRIG2, ECHO2 = 17, 27

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

conn = sqlite3.connect("people.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    direction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def get_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.05)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    timeout = start_time + 0.03

    while GPIO.input(echo) == 0:
        if time.time() > timeout:
            return 999
        pulse_start = time.time()

    timeout = time.time() + 0.03
    while GPIO.input(echo) == 1:
        if time.time() > timeout:
            return 999
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = duration * 17150
    return distance

THRESHOLD = 20.0

try:
    while True:
        d1 = get_distance(TRIG1, ECHO1)
        d2 = get_distance(TRIG2, ECHO2)

        if d1 < THRESHOLD:
            time.sleep(0.3)
            if get_distance(TRIG2, ECHO2) < THRESHOLD:
                print("Left -> Right")
                cursor.execute("INSERT INTO movement(direction) VALUES (?)", ("L->R",))
                conn.commit()
                time.sleep(0.5)

        elif d2 < THRESHOLD:
            time.sleep(0.3)
            if get_distance(TRIG1, ECHO1) < THRESHOLD:
                print("Right -> Left")
                cursor.execute("INSERT INTO movement(direction) VALUES (?)", ("R->L",))
                conn.commit()
                time.sleep(0.5)

        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    conn.close()
