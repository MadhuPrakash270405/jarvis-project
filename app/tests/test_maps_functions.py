import pytest
from app.utils.maps_functions import get_coordinates,get_route_directions,setup_database

def test_get_coordinates_success(mocker):
    mocker.patch("app.utils.maps_functions.requests.get")
    coordinates = get_coordinates("Cleveland, OH")
    assert coordinates is not None
    # Additional assertions based on the function's return value

def test_get_coordinates_failure(mocker):
    mocker.patch("app.utils.maps_functions.requests.get", side_effect=Exception)
    with pytest.raises(Exception):
        get_coordinates("Cleveland, OH")


def test_get_route_directions_success(mocker):
    mocker.patch("app.utils.maps_functions.requests.get")
    route = get_route_directions("Cleveland, OH", "Los Angeles, CA")
    assert route is not None
    # Additional assertions based on the function's return value

def test_get_route_directions_failure(mocker):
    mocker.patch("app.utils.maps_functions.requests.get", side_effect=Exception)
    with pytest.raises(Exception):
        get_route_directions("Cleveland, OH", "Los Angeles, CA")


def test_setup_database(mocker):
    mocker.patch("app.utils.maps_functions.sqlite3.connect")
    setup_database()
    # Assertions to check if the database setup was successful
