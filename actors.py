import pykka

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
    def __init__(self, action_with_direction):
        super(MotorActor, self).__init__()
        self.action_with_direction = action_with_direction

    def on_receive(self, msg):
        direction = msg.get(DIRECTION)
        sender = msg.get(SENDER)
        print(">>> MOTOR MOVES:", direction)
        self.action_with_direction(direction)
        sender.tell({ACTION: NEXT_DIRECTION})


class StateActor(pykka.ThreadingActor):
    def __init__(self, motor_actor_ref, state=STATE_READ, directions=[], sign=print):
        super(StateActor, self).__init__()
        self.motor = motor_actor_ref
        self.state = state
        self.directions = directions
        self.sign = sign

    def _one_step(self):
        head, *tail = self.directions
        self.motor.tell({DIRECTION: head, SENDER: self.actor_ref})
        self.directions = tail

    def on_receive(self, msg):
        print()
        print("before", msg, self.state, self.directions)

        if msg.get(ACTION) == CANCEL:
            self.sign()
            self.directions = []
            self.state = STATE_READ

        elif self.state == STATE_READ:
            self.sign()
            if msg.get(ACTION) == ADD_DIRECTION:
                self.directions.append(msg.get(DIRECTION))
            elif msg.get(ACTION) == OK and self.directions:
                self.state = STATE_GO
                self._one_step()

        elif self.state == STATE_GO:
            if msg.get(ACTION) == NEXT_DIRECTION:
                if self.directions:
                    self._one_step()
                else:
                    self.state = STATE_READ

        print("after", msg, self.state, self.directions)
