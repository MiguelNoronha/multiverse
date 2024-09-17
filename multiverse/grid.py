from multiverse.exceptions import OutOfBoundsError, PositionsClashError
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
            "last_known_position": (x, y),
            "last_known_orientation": orientation,
            "status": "OK"
        }
        self._occupied_positions.add(self._robot_data[robot]["last_known_position"])


    def update_robot_state(self, robot: Robot, instruction: str) -> bool:
        raise NotImplementedError
