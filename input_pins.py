from gpiozero import Button

from MqttProxy import MqttProxy, commands
from actors import MotorActor, StateActor
from output_pins import go_one_step, light


def frog(buttons):
    motor = MotorActor.start(action_with_direction=go_one_step)
    state = StateActor.start(motor_actor_ref=motor, sign=light)

    print("init buttons")
    for button_pin, msg in buttons:
        print("init button:", button_pin)
        button = Button(button_pin)
        button.when_released = lambda: state.tell(msg)

    def hqtt_on_msg(msg):
        if msg in commands.keys():
            state.tell(commands[msg])

    print("init mqtt")
    MqttProxy(hqtt_on_msg)

    print("light")
    light()
