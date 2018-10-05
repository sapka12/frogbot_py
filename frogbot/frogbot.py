import RPi.GPIO as GPIO

motor_pins_left = [1, 2, 3, 4]
motor_pins_right = [5, 6, 7, 8]
button_pin_forward = 10
button_pin_backward = 11
button_pin_left = 12
button_pin_right = 13
button_pin_ok = 14
button_pin_cancel = 9

STATE_READ, STATE_GO = "read", "go"

FORWARD, BACKWARD, LEFT, RIGHT = "FORWARD", "BACKWARD", "LEFT", "RIGHT"


def go_one_step(step):
    print(step)


class FrogBot:
    def __init__(self):
        self.state = STATE_READ
        self.directions = []

    def same_state(self, _state):
        return self.state == _state

    def add_step(self, step):
        self.directions.append(step)

    def go(self):
        if self.directions:
            head, *tail = self.directions
            go_one_step(head)
            self.directions = tail
            self.go()

    def cancel(self):
        self.directions = []


frog = FrogBot


def on_push_forward():
    if frog.same_state(STATE_READ):
        frog.add_step(FORWARD)


def on_push_backward():
    if frog.same_state(STATE_READ):
        frog.add_step(BACKWARD)


def on_push_left():
    if frog.same_state(STATE_READ):
        frog.add_step(LEFT)


def on_push_right():
    if frog.same_state(STATE_READ):
        frog.add_step(RIGHT)


def on_push_ok(_s):
    if frog.same_state(STATE_READ):
        frog.state = STATE_GO
        frog.go()
        frog.state = STATE_READ


def on_push_cancel():
    frog.cancel()


if __name__ == '__main__':
    GPIO.add_event_detect(button_pin_forward, GPIO.RISING, callback=on_push_forward)
    GPIO.add_event_detect(button_pin_backward, GPIO.RISING, callback=on_push_backward)
    GPIO.add_event_detect(button_pin_left, GPIO.RISING, callback=on_push_left)
    GPIO.add_event_detect(button_pin_right, GPIO.RISING, callback=on_push_right)
    GPIO.add_event_detect(button_pin_ok, GPIO.RISING, callback=on_push_ok)
    GPIO.add_event_detect(button_pin_cancel, GPIO.RISING, callback=on_push_cancel)

    input("waiting for action")
