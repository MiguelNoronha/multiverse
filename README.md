# Multiverse Tech Task - Mars Rover

by Miguel dos Santos Veríssimo Noronha

## Setup

To set up the project you'll need to ensure python, along with some python packages, are installed.<br>
In the order that follows, ensure the software is already installed on your machine - if not, install it as instructed:

1. Install [brew](https://docs.brew.sh/Installation);
2. Install [python3.12](https://docs.brew.sh/Homebrew-and-Python) - for a simple installation run
    ```shell
    brew install python@3.12
    ```
3. Install [pipx](https://github.com/pypa/pipx/blob/main/docs/installation.md);
4. To ensure `pipx` is fully functional, restart your terminal;
5. Run
    ```shell
    poetry install
    ```
    to install all the project's python dependencies;

_Unless you know what you are doing_, please make sure **_not_** to run `poetry lock`/`make install` - this may affect
dependency compatability.

## Performing tasks with the project

### Running the terminal app

To run the project (after everything is installed) use
```shell
make run
```

The project will then print out a small 'hello' message.

**TODO**: Implement the project
**TODO**: Review this section

### Running tests

To run the test suit simply use
```shell
make test
```
and `pytest` will identify and run all tests in the project.

**TODO**: Implement the tests
**TODO**: Review this section

## Assumptions

Before starting to work on the implementation I have spent a bit of time thinking of how to approach it.<br>
This problem could easily be solved in a 1-file script.
However, that approach would not mimic the real-life scenario very well. It would also not be very nice to look through.

Instead, I opted by an OO approach where there will be a class representing the robots, and a class representing the technology maintaining the grid.<br>
Within this approach (again, attempting to think about real-life conditions), the robots won't necessarily know their exact position and direction - but their sensors will very accurately be able to tell how much distance they move or how far they turn in a given direction.

Still following this approach, the grid would not necessarily be able to tell all of a robot's movement's accurately, but instead rely on what the robot reports back to it.<br>
Especially if it were to happen that the robot encountered an obstacle, as it may not be able to move as normal.

A lot of these aspects are not present in the challenge brief, and they make the task more complex, but I am considering the possibility that the project may need to evolve beyond those parameters in the future.

Regarding orientation, it will probably be implemented as a degree (0-359). I considered the possibility of using a deque as it's representation, but it could be clunkier to update if any changes are necessary in the future.<br>
I also considered using a state machine (`{"N": {"L": "W", "R": "E"}, ...}`) for maintaining orientation - this could work well within the frame of the problem depending on how other parts were implemented, but it would not scale well if we wished to introduce more precision to the compasses.

**TODO**: Review this section

## Limitations, or the things I would have done with infinite time

None yet, though the project isn't complete yet either.
If I have the time, I will attempt to implement an ASCII visualisation of the grid.

Note: the versions of python/poetry/etc ran for this project are the versions I have been using for a few months - they may be slightly behind the most up-to-date ones.

**TODO**: Review this section

### Actually broken things

None yet, though the project isn't complete yet either.

**TODO**: Review this section

## Use of make commands

Throughout this README I've employed the use of `make` commands.<br>
Feel free to ignore them and use the alternatives described below:
- `make test`
    ```shell
    find . -name '*.pyc' -delete
	rm -rf .pytest_cache
	find . -name '__pycache__' -delete
    poetry run pytest
    ```
- `make run`
    ```shell
    find . -name '*.pyc' -delete
	rm -rf .pytest_cache
	find . -name '__pycache__' -delete
    poetry run python main.py
    ```
