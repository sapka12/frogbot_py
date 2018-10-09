import time
from actors import *

if __name__ == '__main__':
    def wait(direction):
        print(direction)
        time.sleep(1)


    motor = MotorActor.start(action_with_direction=wait)
    state = StateActor.start(motor_actor_ref=motor)


    def scenario_1():
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "left"})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "forward"})
        state.tell({ACTION: OK})


    def scenario_2():
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "left"})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "forward"})
        state.tell({ACTION: OK})
        time.sleep(1)
        state.tell({ACTION: CANCEL})


    def scenario_3():
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "left"})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "forward"})
        state.tell({ACTION: OK})
        time.sleep(1)
        state.tell({ACTION: OK})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "left"})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "forward"})
        state.tell({ACTION: OK})

    def scenario_4():
        state.tell({ACTION: OK})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "left"})
        state.tell({ACTION: ADD_DIRECTION, DIRECTION: "forward"})
        state.tell({ACTION: OK})


    scenario_4()

    time.sleep(5)

    state.stop()
    motor.stop()
