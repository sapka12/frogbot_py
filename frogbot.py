import RPi.GPIO as GPIO

from actors import *
from gpio_button import GpioButton
from motor import *

motor = MotorActor.start()
state = StateActor.start(motor_actor_ref=motor)

button_pin_forward = 33
button_pin_backward = 37
button_pin_left = 36
button_pin_right = 35
button_pin_ok = 38
button_pin_cancel = 40


def pressed(pin):
    return GPIO.input(pin) == 0


def on_push_forward(pin):
    if pressed(pin):
        print(FORWARD)
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: FORWARD})


def on_push_backward(pin):
    if pressed(pin):
        print(BACKWARD)
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: BACKWARD})


def on_push_left(pin):
    if pressed(pin):
        print(LEFT)
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: LEFT})


def on_push_right(pin):
    if pressed(pin):
        print(RIGHT)
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: RIGHT})


def on_push_ok(pin):
    if pressed(pin):
        print(OK)
        state.tell({ACTION: OK})


def on_push_cancel(pin):
    if pressed(pin):
        print(CANCEL)
        state.tell({ACTION: CANCEL})


if __name__ == '__main__':
    init_gpio()

    GpioButton(button_pin_forward, on_push_forward)
    GpioButton(button_pin_backward, on_push_backward)
    GpioButton(button_pin_left, on_push_left)
    GpioButton(button_pin_right, on_push_right)
    GpioButton(button_pin_ok, on_push_ok)
    GpioButton(button_pin_cancel, on_push_cancel)

    go_one_step(RIGHT)

    while True:
        time.sleep(1)
