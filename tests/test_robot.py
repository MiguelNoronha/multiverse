import pytest

from multiverse.exceptions import InstructionError
from multiverse.robot import Robot


@pytest.fixture
def robot():
    return Robot()


@pytest.mark.parametrize(
    "instruction, distance, degree",
    (
        ("F", 1, 0),
        ("L", 0, -90),
        ("R", 0, 90),
    )
)
def test_move(robot, instruction, distance, degree):
    assert robot.move(instruction) == (distance, degree)


@pytest.mark.parametrize(
    "instruction", ("FL", "LF", "a", 1)
)
def test_move_error(robot, instruction):
    with pytest.raises(InstructionError) as exception_info:
        robot.move(instruction)

    assert "Not sure what'll be in here yet" in str(exception_info.value)
