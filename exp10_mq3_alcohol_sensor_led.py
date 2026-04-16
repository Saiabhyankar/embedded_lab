from gpiozero import DigitalInputDevice, LED
from signal import pause

alcohol = DigitalInputDevice(17)
led = LED(18)

alcohol.when_activated = led.on
alcohol.when_deactivated = led.off

pause()
