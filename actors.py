import pykka
import time
from pins import go_one_step as go
from pins import light as sign

STATE_READ = "read"
STATE_GO = "go"

ACTION = "action"
ADD_DIRECTION = "add_direction"
NEXT_DIRECTION = "next_direction"
OK = "ok"
CANCEL = "cancel"

DIRECTION = "direction"
SENDER = "sender"


class MotorActor(pykka.ThreadingActor):
    def on_receive(self, msg):
        direction = msg.get(DIRECTION)
        sender = msg.get(SENDER)
        print(">>> MOTOR MOVES:", direction)
        go(direction)
        sender.tell({ACTION: NEXT_DIRECTION})


class StateActor(pykka.ThreadingActor):
    def __init__(self, motor_actor_ref, state=STATE_READ, directions=[]):
        super(StateActor, self).__init__()
        self.motor = motor_actor_ref
        self.state = state
        self.directions = directions

    def _one_step(self):
        if self.directions:
            head, *tail = self.directions
            self.motor.tell({DIRECTION: head, SENDER: self.actor_ref})
            self.directions = tail

    def on_receive(self, msg):
        if self.state == STATE_READ:
            sign()
            if msg.get(ACTION) == ADD_DIRECTION:
                self.directions.append(msg.get(DIRECTION))
            elif msg.get(ACTION) == OK:
                self.state = STATE_GO
                self._one_step()

        if self.state == STATE_GO:
            if msg.get(ACTION) == NEXT_DIRECTION:
                if self.directions:
                    self._one_step()
                else:
                    self.state = STATE_READ
            elif msg.get(ACTION) == CANCEL:
                self.directions = []
                self.state = STATE_READ


if __name__ == '__main__':
    motor = MotorActor.start()
    state = StateActor.start(motor_actor_ref=motor)

    state.tell({ACTION: ADD_DIRECTION, DIRECTION: "left"})
    state.tell({ACTION: ADD_DIRECTION, DIRECTION: "forward"})
    state.tell({ACTION: OK})

    # time.sleep(1)
    # state.tell({ACTION: CANCEL})

    time.sleep(5)

    state.stop()
    motor.stop()
