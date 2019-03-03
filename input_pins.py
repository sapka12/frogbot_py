import RPi.GPIO as GPIO

from MqttProxy import MqttProxy, commands
from actors import MotorActor, StateActor
from output_pins import go_one_step, light, bouncetime


def frog(buttons):
    motor = MotorActor.start(action_with_direction=go_one_step)
    state = StateActor.start(motor_actor_ref=motor, sign=light)

    def on_push(msg):
        def pressed(pin):
            return GPIO.input(pin) == 0

        def f(pin):
            if pressed(pin):
                state.tell(msg)

        return f

    def gpio_button(channel, on_push):
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel, GPIO.RISING, callback=on_push, bouncetime=bouncetime)

    for button_pin, msg in buttons:
        gpio_button(button_pin, on_push(msg))

    def hqtt_on_msg(msg):
        if msg in commands.keys():
            state.tell(commands[msg])

    MqttProxy(hqtt_on_msg)

    light()
