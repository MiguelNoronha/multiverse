import pytest

from multiverse.exceptions import OutOfBoundsError, PositionsClashError
from multiverse.grid import GridTech


@pytest.fixture
def grid():
    return GridTech(5, 10)


@pytest.fixture
def robot_patch(mocker):
    return mocker.patch("multiverse.robot.Robot", autospec=True)


@pytest.fixture
def robot_1(robot_patch):
    return robot_patch()


@pytest.fixture
def robot_2(robot_patch):
    return robot_patch()


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
def test_add_robot(request, grid, robots, coordinates):
    for i in range(len(robots)):
        grid.add_robot(request.getfixturevalue(robots[i]), *coordinates[i])

    assert False  # TODO: We'll be able to assert the internal state of the grid once implemented


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
        grid.add_robot(robot_1, x, y)

    assert "Not sure what'll be in here yet" in str(exception_info.value)


def test_add_robot_error__clash(grid, robot_1, robot_2):
    grid.add_robot(robot_1, 0, 0)
    with pytest.raises(PositionsClashError) as exception_info:
        grid.add_robot(robot_2, 0, 0)

    assert "Not sure what'll be in here yet" in str(exception_info.value)
