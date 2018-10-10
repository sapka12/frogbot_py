import RPi.GPIO as GPIO
import time

from settings import *

FORWARD, BACKWARD, LEFT, RIGHT = "FORWARD", "BACKWARD", "LEFT", "RIGHT"


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    pins_out = motor_pins_left + motor_pins_right
    GPIO.setup(pins_out, GPIO.OUT, initial=GPIO.LOW)


def light():
    pins, d = motor_pins_right + motor_pins_left, 0.01
    pins = pins + list(reversed(pins))
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(d)
        GPIO.output(pin, GPIO.LOW)
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
                GPIO.output(motor[i], GPIO.HIGH)
            else:
                GPIO.output(motor[i], GPIO.LOW)
        time.sleep(delay)

    for _ in range(rounds):
        for i in range(len(stages)):
            set_motor_state(stages_l[i], motor_pins_left)
            set_motor_state(stages_r[i], motor_pins_right)

    set_motor_state(init_state, motor_pins_left)
    set_motor_state(init_state, motor_pins_right)
