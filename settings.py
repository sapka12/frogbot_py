pins = {
    7: 4,
    12: 18,
    11: 17,
    13: 27,
    15: 22,
    16: 23,
    18: 24,
    22: 25,
    33: 13,
    37: 26,
    36: 16,
    35: 19,
    38: 20,
    40: 21,
}

button_pin_forward = pins[33]
button_pin_backward = pins[37]
button_pin_left = pins[36]
button_pin_right = pins[35]
button_pin_ok = pins[38]
button_pin_cancel = pins[40]

motor_pins_left = [pins[p] for p in [7, 12, 11, 13]]
motor_pins_right = [pins[p] for p in [15, 16, 18, 22]]

delay = 0.0005
rounds_move, rounds_rotate = 562, 339
bouncetime=300
