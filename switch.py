import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def get_N():
    return GPIO.input(18)
def get_S():
    return GPIO.input(19)

if __name__ == '__main__':
    import led
    while True:
        n = GPIO.input(18)
        s = GPIO.input(19)
        if n:
            led.matrix.SetImage(led.letters['N'], 0, 0)
        if s:
            led.matrix.SetImage(led.letters['5'], 0, 9)
        time.sleep(0.2)
        led.matrix.Clear()

