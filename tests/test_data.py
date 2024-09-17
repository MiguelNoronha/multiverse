import pytest

from multiverse.data import Orientation, Position
from multiverse.constants import ORIENTATION_TO_DEGREE


@pytest.fixture
def position():
    return Position(1, 2)


@pytest.fixture
def orientation():
    return Orientation(270)


@pytest.mark.parametrize(
    "vector, result",
    (
        (Position(2, 3), Position(3, 5)),
        (Position(-2, -3), Position(-1, -1)),
    )
)
def test_position__add(position, vector, result):
    new_position = position + vector

    assert new_position == result


@pytest.mark.parametrize(
    "vector, result",
    (
        (Position(2, 3), Position(3, 5)),
        (Position(-2, -3), Position(-1, -1)),
    )
)
def test_position__iadd(position, vector, result):
    position += vector

    assert position == result


def test_position__error(position):
    with pytest.raises(TypeError) as exception_info:
        _ = position + 1

    assert "A Position can only be added to another Position" in str(exception_info.value)

    with pytest.raises(TypeError) as exception_info:
        position += 1

    assert "A Position can only be added to another Position" in str(exception_info.value)


@pytest.mark.parametrize(
    "degree",
    (270, "W")
)
def test_orientation__init(degree):
    orientation = Orientation(degree)

    assert orientation.degree == ORIENTATION_TO_DEGREE["W"]


def test_orientation__init__error():
    with pytest.raises(KeyError):
        Orientation("Some Direction")


@pytest.mark.parametrize(
    "update, result",
    (
        (Orientation(23), Orientation(293)),
        (Orientation(230), Orientation(140)),
        (Orientation(-29), Orientation(241)),
        (Orientation(-290), Orientation(340)),
    )
)
def test_orientation__add(orientation, update, result):
    new_orientation = orientation + update

    assert new_orientation == result


@pytest.mark.parametrize(
    "update, result",
    (
        (Orientation(23), Orientation(293)),
        (Orientation(230), Orientation(140)),
        (Orientation(-29), Orientation(241)),
        (Orientation(-290), Orientation(340)),
    )
)
def test_orientation__iadd(orientation, update, result):
    orientation += update

    assert orientation == result


def test_orientation__error(orientation):
    with pytest.raises(TypeError) as exception_info:
        _ = orientation + "1"

    assert "An Orientation can only be added to another Orientation" in str(exception_info.value)

    with pytest.raises(TypeError) as exception_info:
        orientation += 1

    assert "An Orientation can only be added to another Orientation" in str(exception_info.value)


def test_orientation__str(orientation):
    assert str(orientation) == "W"