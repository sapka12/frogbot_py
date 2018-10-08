import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


def pressed(pin):
    return GPIO.input(pin) == 0


class GpioButton(object):
    def __init__(self, channel, on_push):
        self.channel = channel
        self.on_push = on_push
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel, GPIO.RISING, callback=self.__on_push, bouncetime=300)

    def __on_push(self):
        if pressed(self.channel):
            self.on_push()
