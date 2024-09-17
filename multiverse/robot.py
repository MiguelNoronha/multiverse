from multiverse.constants import DEGREE_INSTRUCTIONS, DISTANCE_INSTRUCTIONS
from multiverse.exceptions import InstructionError


class Robot:
    @staticmethod
    def move(instruction: str) -> tuple[int, int]:
        try:
            distance = DISTANCE_INSTRUCTIONS[instruction]
        except KeyError:
            raise InstructionError("The instruction provided is not valid")

        try:
            degree = DEGREE_INSTRUCTIONS[instruction]
        except KeyError:
            raise InstructionError("The instruction provided is not valid")

        return distance, degree
