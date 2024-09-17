import pytest
from unittest.mock import MagicMock

from multiverse.constants import DISTANCE_INSTRUCTIONS, DEGREE_INSTRUCTIONS
from multiverse.data import Position, Orientation
from multiverse.enums import RobotStatus
from multiverse.exceptions import OutOfBoundsError, PositionsClashError
from multiverse.grid import GridTech
from multiverse.robot import Robot


@pytest.fixture
def grid():
    return GridTech(5, 10)


@pytest.fixture
def robot_1():
    return MagicMock(spec=Robot, move=lambda s: (DISTANCE_INSTRUCTIONS[s], DEGREE_INSTRUCTIONS[s]))


@pytest.fixture
def robot_2():
    return MagicMock(spec=Robot, move=lambda s: (DISTANCE_INSTRUCTIONS[s], DEGREE_INSTRUCTIONS[s]))


@pytest.mark.parametrize(
    "robots, coordinates",
    (
        (["robot_1"], [(0, 0)]),
        (["robot_1"], [(5, 0)]),
        (["robot_1"], [(0, 10)]),
        (["robot_1"], [(5, 10)]),
        (["robot_1", "robot_2"], [(0, 0), (5, 10)]),
    )
)
def test_add_robots(request, grid, robots, coordinates):
    for i in range(len(robots)):
        grid.add_robot(request.getfixturevalue(robots[i]), *coordinates[i], "N")

    assert len(grid._robot_data) == len(robots)
    assert len(grid._occupied_positions) == len(coordinates)


@pytest.mark.parametrize(
    "x, y",
    (
        (-1, 0),
        (0, -1),
        (-1, -1),
        (6, 0),
        (5, -1),
        (6, -1),
        (-1, 10),
        (0, 11),
        (-1, 11),
        (6, 10),
        (5, 11),
        (6, 11),
    )
)
def test_add_robot_error__bounds(grid, robot_1, x, y):
    with pytest.raises(OutOfBoundsError) as exception_info:
        grid.add_robot(robot_1, x, y, "N")

    assert "A robot cannot be placed outside the grid" in str(exception_info.value)


def test_add_robot_error__clash(grid, robot_1, robot_2):
    grid.add_robot(robot_1, 0, 0, "N")
    with pytest.raises(PositionsClashError) as exception_info:
        grid.add_robot(robot_2, 0, 0, "N")

    assert "A robot cannot be placed in the same position as another robot" in str(exception_info.value)


@pytest.mark.parametrize(
    "initial_state, instruction, result",
    (
        ((0, 0, "N"), "R", (Position(0, 0), Orientation("E"))),
        ((0, 0, "E"), "F", (Position(1, 0), Orientation("E"))),
        ((1, 0, "E"), "L", (Position(1, 0), Orientation("N"))),
        ((1, 0, "N"), "F", (Position(1, 1), Orientation("N"))),
        ((1, 1, "N"), "R", (Position(1, 1), Orientation("E"))),
        ((1, 1, "E"), "F", (Position(2, 1), Orientation("E"))),
        ((2, 1, "E"), "F", (Position(3, 1), Orientation("E"))),
        ((3, 1, "E"), "F", (Position(4, 1), Orientation("E"))),
        ((4, 1, "E"), "F", (Position(5, 1), Orientation("E"))),
        ((5, 1, "E"), "F", (Position(6, 1), Orientation("E"))),
    )
)
def test__calculate_updated_data(grid, robot_1, initial_state, instruction, result):
    grid.add_robot(robot_1, *initial_state)

    assert grid._calculate_updated_data(robot_1, instruction) == result


@pytest.mark.parametrize(
    "initial_state, updates, mocked_data, final_state",
    (
        (
            (0, 0, "N"),
            ["R", "F", "L", "F", "R"],
            [
                (Position(0, 0), Orientation("E")),
                (Position(1, 0), Orientation("E")),
                (Position(1, 0), Orientation("N")),
                (Position(1, 1), Orientation("N")),
                (Position(1, 1), Orientation("E")),
            ],
            {
                "last_known_position": Position(1, 1),
                "last_known_orientation": Orientation("E"),
                "status": RobotStatus.OK,
                "order": 0
            },
        ),
        (
            (0, 0, "N"),
            ["R", "F", "F", "F", "F", "F", "F", "L", "L", "F", "F"],
            [
                (Position(0, 0), Orientation("E")),
                (Position(1, 0), Orientation("E")),
                (Position(2, 0), Orientation("E")),
                (Position(3, 0), Orientation("E")),
                (Position(4, 0), Orientation("E")),
                (Position(5, 0), Orientation("E")),
                (Position(6, 0), Orientation("E")),
            ],
            {
                "last_known_position": Position(5, 0),
                "last_known_orientation": Orientation("E"),
                "status": RobotStatus.LOST,
                "order": 0
            },
        ),
    )
)
def test_update_robot(mocker, grid, robot_1, initial_state, updates, mocked_data, final_state):
    mocker.patch.object(GridTech, "_calculate_updated_data", side_effect=mocked_data)

    grid.add_robot(robot_1, *initial_state)
    for update in updates:
        grid.update_robot_state(robot_1, update)

    assert grid._robot_data[robot_1] == final_state


def test_update_robot_error(grid, robot_1, robot_2):
    grid.add_robot(robot_1, 0, 0, "N")
    grid.add_robot(robot_2, 0, 1, "S")
    with pytest.raises(PositionsClashError) as exception_info:
        grid.update_robot_state(robot_2, "F")

    assert "A robot cannot move into the a position another robot already occupies" in str(exception_info.value)


@pytest.mark.parametrize(
    "robot_data, result",
    (
        ({}, ""),
        (
            {1: {
                "last_known_position": Position(1, 2),
                "last_known_orientation": Orientation("N"),
                "status": RobotStatus.OK,
                "order": 1
            }},
            "(1, 2, N)"
        ),
        (
            {
                1: {
                    "last_known_position": Position(1, 2),
                    "last_known_orientation": Orientation("N"),
                    "status": RobotStatus.OK,
                    "order": 1
                },
                2: {
                    "last_known_position": Position(10, 3),
                    "last_known_orientation": Orientation(90),
                    "status": RobotStatus.OK,
                    "order": 2
                },
                3: {
                    "last_known_position": Position(1, 2),
                    "last_known_orientation": Orientation("S"),
                    "status": RobotStatus.LOST,
                    "order": 3
                },
            },
            "(1, 2, N)\n(10, 3, E)\n(1, 2, S) LOST"
        ),
    )
)
def test__str(grid, robot_data, result):
    grid._robot_data = robot_data
    assert str(grid) == result
