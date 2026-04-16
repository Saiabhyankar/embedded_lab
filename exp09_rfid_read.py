from mfrc522 import SimpleMFRC522
from RPi import GPIO

reader = SimpleMFRC522()

try:
    print("Scan RFID tag...")
    id, text = reader.read()
    print("ID:", id)
    print("Text:", text)
finally:
    GPIO.cleanup()
