import RPi.GPIO as GPIO
import time
import sqlite3

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# --- DATABASE SETUP ---
conn = sqlite3.connect("walking_speed.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS sessions (avg_speed REAL)")
conn.commit()

# --- DISTANCE FUNCTION ---
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        end = time.time()

    distance = (end - start) * 17150
    return distance  # in cm

# --- MAIN LOGIC ---
prev_distance = get_distance()
prev_time = time.time()

speeds = []
last_motion_time = time.time()

SESSION_TIMEOUT = 3   # seconds (no movement → session ends)
MOVEMENT_THRESHOLD = 2  # cm change

print("System Ready...")

while True:
    curr_distance = get_distance()
    curr_time = time.time()

    # change in distance
    delta_d = abs(curr_distance - prev_distance)
    delta_t = curr_time - prev_time

    if delta_t > 0:
        speed = delta_d / delta_t   # cm/sec

        # detect movement
        if delta_d > MOVEMENT_THRESHOLD:
            print("Speed:", round(speed, 2), "cm/s")
            speeds.append(speed)
            last_motion_time = time.time()

    # check if session ended
    if time.time() - last_motion_time > SESSION_TIMEOUT:
        if speeds:
            avg_speed = sum(speeds) / len(speeds)
            print("Session Ended. Avg Speed:", round(avg_speed, 2))

            # store in DB
            c.execute("INSERT INTO sessions VALUES (?)", (avg_speed,))
            conn.commit()

            speeds = []  # reset for next session

        last_motion_time = time.time()

    prev_distance = curr_distance
    prev_time = curr_time

    time.sleep(0.5)