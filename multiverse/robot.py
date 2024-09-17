from multiverse.exceptions import InstructionError


class Robot:
    @staticmethod
    def move(instruction: str) -> tuple[int, int]:
        if instruction == "L":
            return 0, -90
        elif instruction == "R":
            return 0, 90
        elif instruction == "F":
            return 1, 0
        else:
            raise InstructionError("The instruction provided is not valid")