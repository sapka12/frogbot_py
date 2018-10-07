import RPi.GPIO as GPIO
import time
from envar_manager import *
import multiprocessing

motor_pins_left = [7, 12, 11, 13]
motor_pins_right = [15, 16, 18, 22]
button_pin_forward = 33
button_pin_backward = 37
button_pin_left = 36
button_pin_right = 35
button_pin_ok = 38
button_pin_cancel = 40

delay = 0.001
rounds_move, rounds_rotate = 573, 335

STATE_READ, STATE_GO = "read", "go"
FORWARD, BACKWARD, LEFT, RIGHT = "FORWARD", "BACKWARD", "LEFT", "RIGHT"


def init_gpio():
    GPIO.setmode(GPIO.BOARD)

    pins_out = motor_pins_left + motor_pins_right
    pins_in = [
        button_pin_forward,
        button_pin_backward,
        button_pin_left,
        button_pin_right,
        button_pin_ok,
        button_pin_cancel,
    ]

    GPIO.setup(pins_out, GPIO.OUT, initial=GPIO.LOW)
    for p in pins_in:
        GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def light():
    for pin in motor_pins_right + motor_pins_left:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    for pin in motor_pins_right + motor_pins_left:
        GPIO.output(pin, GPIO.LOW)


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


def pressed(pin):
    return GPIO.input(pin) == 0


def on_push_forward(pin):
    if pressed(pin) and is_state(STATE_READ):
        print(FORWARD)
        add_direction(FORWARD)
        light()


def on_push_backward(pin):
    if pressed(pin) and is_state(STATE_READ):
        print(BACKWARD)
        add_direction(BACKWARD)
        light()


def on_push_left(pin):
    if pressed(pin) and is_state(STATE_READ):
        print(LEFT)
        add_direction(LEFT)
        light()


def on_push_right(pin):
    if pressed(pin) and is_state(STATE_READ):
        print(RIGHT)
        add_direction(RIGHT)
        light()


def run_frog(e):
    while True:
        e.wait()
        while e.is_set():
            directions = get_directions()
            print("directions:", directions)
            if directions:
                head, *tail = directions
                go_one_step(head)
                set_directions(tail)
            else:
                set_state(STATE_READ)
            time.sleep(1)


def listen(pin, callback):
    GPIO.add_event_detect(pin, GPIO.RISING, callback=callback, bouncetime=300)


if __name__ == '__main__':
    init_gpio()

    set_state(STATE_READ)
    set_directions([])

    first_button_pushed = multiprocessing.Event()


    def on_push_ok(pin):
        if pressed(pin) and is_state(STATE_READ):
            print("OK")

            light()
            time.sleep(0.2)
            light()
            time.sleep(0.2)
            light()

            set_state(STATE_GO)
            first_button_pushed.set()


    # TODO add effect
    def on_push_cancel(pin):
        if pressed(pin):
            print("CANCEL")
            first_button_pushed.clear()
            set_directions([])
            set_state(STATE_READ)
            light()


    listen(button_pin_forward, on_push_forward)
    listen(button_pin_backward, on_push_backward)
    listen(button_pin_left, on_push_left)
    listen(button_pin_right, on_push_right)
    listen(button_pin_ok, on_push_ok)
    listen(button_pin_cancel, on_push_cancel)

    process = multiprocessing.Process(name='first_process', target=run_frog, args=(first_button_pushed,))
    process.daemon = True
    process.start()

    go_one_step(RIGHT)

    while True:
        time.sleep(1)
