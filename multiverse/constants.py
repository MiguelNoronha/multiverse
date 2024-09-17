DEGREE_INSTRUCTIONS = {
    "F": 0,
    "L": -90,
    "R": 90
}

DEGREE_TO_ORIENTATION = {
    0: "N",
    90: "E",
    180: "S",
    270: "W",
}

DISTANCE_INSTRUCTIONS = {
    "F": 1,
    "L": 0,
    "R": 0
}

ORIENTATION_TO_DEGREE = {v: k for k, v in DEGREE_TO_ORIENTATION.items() }