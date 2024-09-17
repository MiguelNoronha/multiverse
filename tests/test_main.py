import pytest
from unittest.mock import MagicMock, call

from constants import INPUT_PROMPT, GRID_MISSING_MESSAGE, RE_PATTERN
from main import run_the_grid, _process_line, _process_match
from multiverse.grid import GridTech
from multiverse.robot import Robot


@pytest.fixture
def match_grid():
    return {"m": "5", "n": "10", "x": None, "y": None, "orientation": None, "instructions": None}


@pytest.fixture
def match_robot():
    return {"m": None, "n": None, "x": "1", "y": "3", "orientation": "N", "instructions": "FLRFLRFF"}


@pytest.fixture
def robot_mock(mocker):
    mock = MagicMock(spec=Robot)
    mocker.patch("main.Robot", return_value=mock)
    return mock


@pytest.mark.parametrize(
    "current_state, prints",
    (
        ({"grid": None}, ""),
        (
            {"grid": MagicMock(spec=GridTech)},
            "The grid has already been defined. If you wish to reset the grid, please type in 'RESET'."
        ),
    )
)
def test__process_match__grid(capfd, match_grid, current_state, prints):
    _process_match(current_state, match_grid)
    stdout, _ = capfd.readouterr()

    assert current_state["grid"]
    assert stdout.strip() == prints


@pytest.mark.parametrize(
    "current_state, call_args, prints",
    (
        (
            {"grid": None},
            {
                "add_robot": [],
                "update_robot_state": [],
            },
            GRID_MISSING_MESSAGE + "\n" + INPUT_PROMPT
        ),
        (
            {"grid": MagicMock(spec=GridTech)},
            {
                "add_robot": [(1, 3, "N")],
                "update_robot_state": "FLRFLRFF",
            },
            ""
        ),
    )
)
def test__process_match__robot(capfd, match_robot, robot_mock, current_state, call_args, prints):
    _process_match(current_state, match_robot)
    stdout, _ = capfd.readouterr()

    if current_state["grid"]:
        current_state["grid"].add_robot.assert_has_calls([call(robot_mock, *args) for args in call_args["add_robot"]])
        current_state["grid"].update_robot_state.assert_has_calls([call(robot_mock, arg) for arg in call_args["update_robot_state"]])

    assert stdout.strip() == prints


@pytest.mark.parametrize(
    "current_state, line, calls, prints",
    (
        (
            {"grid": None},
            "CALC",
            [],
            GRID_MISSING_MESSAGE + "\n" + INPUT_PROMPT
        ),
        (
            {"grid": MagicMock(spec=GridTech, __str__=lambda _: "__str__")},
            "CALC",
            [],
            "__str__"
        ),
        (
            {"grid": None},
            "RESET",
            [],
            "The Grid has been reset\n" + INPUT_PROMPT
        ),
        (
            {"grid": MagicMock(spec=GridTech, __str__=lambda _: "__str__")},
            "RESET",
            [],
            "__str__\nThe Grid has been reset\n" + INPUT_PROMPT
        ),
        (
            {"grid": None},
            "EXIT",
            [],
            "Terminating"
        ),
        (
            {"grid": MagicMock(spec=GridTech, __str__=lambda _: "__str__")},
            "EXIT",
            [],
            "__str__\nTerminating"
        ),
        (
            {},
            "5 10",
            [call(
                {},
                {"m": "5", "n": "10", "x": None, "y": None, "orientation": None, "instructions": None}
            )],
            ""
        ),
        (
            {},
            "Junk Data",
            [],
            "Your input was not valid, please try again."
        ),
    )
)
def test__process_line(capfd, mocker, current_state, line, calls, prints):
    patch = mocker.patch("main._process_match")

    _process_line(current_state, line)
    stdout, _ = capfd.readouterr()

    patch.assert_has_calls(calls)
    assert stdout.strip() == prints
