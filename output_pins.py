from gpiozero import LED
import time

from settings import *

FORWARD, BACKWARD, LEFT, RIGHT = "FORWARD", "BACKWARD", "LEFT", "RIGHT"


def light():
    pins, d = motor_pins_right + motor_pins_left, 0.01
    pins = pins + list(reversed(pins))
    for pin in pins:
        LED(pin).on()
        time.sleep(d)
        LED(pin).off()
        time.sleep(d)


def go_one_step(direction):
    def is_direction(d):
        return direction == d

    rounds = rounds_move if is_direction(FORWARD) or is_direction(BACKWARD) else rounds_rotate

    init_state = [0, 0, 0, 0]

    stages = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]

    stages_l = stages if is_direction(FORWARD) or is_direction(RIGHT) else list(reversed(stages))
    stages_r = stages if is_direction(FORWARD) or is_direction(LEFT) else list(reversed(stages))

    def set_motor_state(stage, motor):
        for i in range(len(stage)):
            if stage[i] == 1:
                LED(motor[i]).on()
            else:
                LED(motor[i]).off()
        time.sleep(delay)

    for _ in range(rounds):
        for i in range(len(stages)):
            set_motor_state(stages_l[i], motor_pins_left)
            set_motor_state(stages_r[i], motor_pins_right)

    set_motor_state(init_state, motor_pins_left)
    set_motor_state(init_state, motor_pins_right)
