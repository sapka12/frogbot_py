from actors import *
from output_pins import *
from input_pins import frog

if __name__ == '__main__':
    init_gpio()

    frog(buttons=[
        (button_pin_forward, {ACTION: ADD_DIRECTION, DIRECTION: FORWARD}),
        (button_pin_backward, {ACTION: ADD_DIRECTION, DIRECTION: BACKWARD}),
        (button_pin_left, {ACTION: ADD_DIRECTION, DIRECTION: LEFT}),
        (button_pin_right, {ACTION: ADD_DIRECTION, DIRECTION: RIGHT}),
        (button_pin_ok, {ACTION: OK}),
        (button_pin_cancel, {ACTION: CANCEL}),
    ])
