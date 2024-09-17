import re

INPUT_DESCRIPTION = (
    "Please input the size of the grid followed by the starting position and instructions for each robot:"
    "\n- The size of the grid should be inputted as 2 integers separated by a whitespace;"
    "\n- The position of a robot should be expressed as a tuple with 2 integers - denoting its initial position - and"
    " a capital letter - denoting its initial orientation (N/E/S/W);"
    "\n- Instructions for a rover should be added after its initial position, as a string with only the characters 'F',"
    " 'L', and 'R' to represent the 'Move Forward', 'Turn Left', 'Turn Right' actions;"
 )
EXAMPLE = (
    "Please see the example below:"
    "\n>>> EXAMPLE START <<<"
    "\n4 8"
    "\n(2, 3, E) LFRFF"
    "\n(0, 2, N) FFLFRFF"
    "\n>>>  EXAMPLE END  <<<"
)
COMMANDS = (
    "Commands:"
    "\n- To calculate the final positions of each rover, please type in 'CALC' - you can do this any number of times"
    " without resetting the grid. Each time, all robots will be displayed;"
    "\n- To reset the grid, please type in 'RESET' - this will calculate the data for any remaining robots before"
    " resetting and display all robots;"
    "\n- To terminate the program, please type in 'EXIT' - this will calculate the data for any remaining robots"
    " before termination and display all robots;"
    "\n- To read the instructions again, please type in 'HELP';"
)
INPUT_PROMPT = "\nPlease input the details for the grid, followed by details for the robots, below:"
HELP_TEXT = f"\n\n{INPUT_DESCRIPTION}\n\n{EXAMPLE}\n\n{COMMANDS}\n\n{INPUT_PROMPT}"

GRID_MISSING_MESSAGE = "The grid has not been defined yet."

RE_GRID = r"^(?P<m>\d+) (?P<n>\d+)$"
RE_ROBOT = r"^\((?P<x>\d+), (?P<y>\d+), (?P<orientation>[NESW])\) (?P<instructions>[FLR]+)$"
RE_MATCH = RE_GRID + r"|" + RE_ROBOT
RE_PATTERN = re.compile(RE_MATCH)
