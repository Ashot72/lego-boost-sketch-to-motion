from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase


def main():
    left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    right_motor = Motor(Port.B, Direction.CLOCKWISE)
    robot = DriveBase(left_motor, right_motor, wheel_diameter=30, axle_track=65)
    robot.settings(straight_speed=200, turn_rate=150)

    # --- HOST_COMMANDS_START ---
    robot.straight(200)
    robot.turn(-90)
    # --- HOST_COMMANDS_END ---


if __name__ == "__main__":
    main()
