from gpiozero import DigitalInputDevice, LED
from signal import pause

gas = DigitalInputDevice(17)
led = LED(18)

gas.when_activated = led.on
gas.when_deactivated = led.off

pause()




























