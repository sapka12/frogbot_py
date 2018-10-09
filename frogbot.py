from actors import *
from pins import *

motor = MotorActor.start(action_with_direction=go_one_step)
state = StateActor.start(motor_actor_ref=motor, sign=light)


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
