import pytest
from unittest.mock import MagicMock

from multiverse.exceptions import OutOfBoundsError, PositionsClashError
from multiverse.grid import GridTech


@pytest.fixture
def grid():
    return GridTech(5, 10)


@pytest.fixture
def robot_1():
    return MagicMock()


@pytest.fixture
def robot_2():
    return MagicMock()


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
    "initial_state, updates, final_state",
    (
        (
            (0, 0, "N"),
            ["R", "F", "L", "F", "R"],
            {
                "last_known_position": (1, 1),
                "last_known_orientation": "E",
                "status": "OK"
            },
        ),
        (
            (0, 0, "N"),
            ["R", "F", "F", "F", "F", "F", "F", "L", "L", "F", "F"],
            {
                "last_known_position": (5, 0),
                "last_known_orientation": "E",
                "status": "LOST"
            },
        ),
    )
)
def test_update_robot(grid, robot_1, initial_state, updates, final_state):
    grid.add_robot(robot_1, *initial_state)
    for update in updates:
        grid.update_robot_state(*update)

    assert grid._robot_data[robot_1] == final_state


def test_update_robot_error(grid, robot_1, robot_2):
    grid.add_robot(robot_1, 0, 0, "N")
    grid.add_robot(robot_2, 0, 1, "S")
    with pytest.raises(PositionsClashError) as exception_info:
        grid.update_robot_state(robot_2, "F")

    assert "A robot cannot move into the a position another robot already occupies" in str(exception_info.value)
