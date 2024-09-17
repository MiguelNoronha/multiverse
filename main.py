from re import Match
from typing import Optional

from constants import INPUT_PROMPT, HELP_TEXT, RE_PATTERN, GRID_MISSING_MESSAGE
from multiverse.grid import GridTech
from multiverse.robot import Robot


def _process_match(current_state: dict, match_groups: dict):
    if match_groups["m"] is not None:
        # The grid dimensions
        if current_state["grid"]:
            print("The grid has already been defined. If you wish to reset the grid, please type in 'RESET'.")
        else:
            current_state["grid"] = GridTech(int(match_groups["m"]), int(match_groups["n"]))
    else:
        # A new robot
        if current_state["grid"]:
            robot = Robot()
            current_state["grid"].add_robot(robot, int(match_groups["x"]), int(match_groups["y"]), match_groups["orientation"])
            for instruction in match_groups["instructions"]:
                current_state["grid"].update_robot_state(robot, instruction)
        else:
            print(GRID_MISSING_MESSAGE)
            print(INPUT_PROMPT)


def _process_line(current_state: dict, line: str):
    if line in ["CALC", "RESET", "EXIT"]:
        if current_state["grid"]:
            print(current_state["grid"])
        elif line == "CALC":
            print(GRID_MISSING_MESSAGE)
            print(INPUT_PROMPT)
            return

        if line == "EXIT":
            current_state["running"] = False
            print("Terminating")
        elif line == "RESET":
            current_state["grid"] = None
            print("The Grid has been reset")
            print(INPUT_PROMPT)

        return

    match = RE_PATTERN.match(line)
    if match:
        _process_match(current_state, match.groupdict())
    else:
        print("Your input was not valid, please try again.")


def run_the_grid():
    print("Welcome to The Grid - Program for the Mars Rover")
    print(HELP_TEXT)

    current_state = {"grid": None, "running": True}

    while current_state["running"]:
        line = input()
        _process_line(current_state, line)


if __name__ == "__main__":
    run_the_grid()
