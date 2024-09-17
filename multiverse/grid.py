import math

from multiverse.enums import RobotStatus
from multiverse.data import Orientation, Position
from multiverse.exceptions import OutOfBoundsError, PositionsClashError, InstructionError
from multiverse.robot import Robot


class GridTech:
    def __init__(self, max_longitude: int, max_latitude: int):
        self._max_longitude = max_longitude  # x, m
        self._max_latitude = max_latitude  # y, n
        self._robot_data = {}
        self._occupied_positions = set()

    def add_robot(self, robot: Robot, x: int, y: int, orientation: str):
        if x < 0 or y < 0 or x > self._max_longitude or y > self._max_latitude:
            raise OutOfBoundsError("A robot cannot be placed outside the grid")
        elif (x, y) in self._occupied_positions:
            raise PositionsClashError("A robot cannot be placed in the same position as another robot")

        self._robot_data[robot] = {
            "last_known_position": Position(x, y),
            "last_known_orientation": Orientation(orientation),
            "status": RobotStatus.OK
        }
        self._occupied_positions.add(self._robot_data[robot]["last_known_position"].tuple)

    def _calculate_updated_data(self, robot, instruction):
        current_position = self._robot_data[robot]["last_known_position"]
        current_orientation = self._robot_data[robot]["last_known_orientation"]
        distance, degree = robot.move(instruction)

        radians = math.radians(current_orientation.degree)

        new_position =  Position(
            round(current_position.x + math.sin(radians) * distance),
            round(current_position.y + math.cos(radians) * distance)
        )
        new_orientation = current_orientation + Orientation(degree)
        return new_position, new_orientation


    def update_robot_state(self, robot: Robot, instruction: str) -> bool:
        if self._robot_data[robot]["status"] != RobotStatus.OK:
            return False

        current_position = self._robot_data[robot]["last_known_position"]
        new_position, new_orientation = self._calculate_updated_data(robot, instruction)

        if new_position != current_position:
            if new_position.tuple in self._occupied_positions:
                raise PositionsClashError("A robot cannot move into the a position another robot already occupies")

            self._occupied_positions.remove(current_position.tuple)

            if new_position.x < 0 or new_position.y < 0 or new_position.x > self._max_longitude or new_position.y > self._max_latitude:
                self._robot_data[robot]["status"] = RobotStatus.LOST
                return False

            self._occupied_positions.add(new_position.tuple)
            self._robot_data[robot]["last_known_position"] = new_position

        self._robot_data[robot]["last_known_orientation"] = new_orientation
        return True
