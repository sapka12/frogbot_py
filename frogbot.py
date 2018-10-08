import RPi.GPIO as GPIO

from actors import *
from pins import *

motor = MotorActor.start()
state = StateActor.start(motor_actor_ref=motor)

button_pin_forward = 33
button_pin_backward = 37
button_pin_left = 36
button_pin_right = 35
button_pin_ok = 38
button_pin_cancel = 40


def on_push(msg):
    def f(pin):
        if pressed(pin):
            state.tell(msg)

    return f


if __name__ == '__main__':
    init_gpio()

    gpio_button(button_pin_forward, on_push({ACTION: ADD_DIRECTION, DIRECTION: FORWARD}))
    gpio_button(button_pin_backward, on_push({ACTION: ADD_DIRECTION, DIRECTION: BACKWARD}))
    gpio_button(button_pin_left, on_push({ACTION: ADD_DIRECTION, DIRECTION: LEFT}))
    gpio_button(button_pin_right, on_push({ACTION: ADD_DIRECTION, DIRECTION: RIGHT}))
    gpio_button(button_pin_ok, on_push({ACTION: OK}))
    gpio_button(button_pin_cancel, on_push({ACTION: CANCEL}))

    light()
