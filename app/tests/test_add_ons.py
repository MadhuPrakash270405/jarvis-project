import pytest
import requests
from app.utils.add_ons import get_random_joke

def test_get_random_joke_success():
    joke = get_random_joke()
    assert joke is not None, "Joke should not be None"

def test_get_random_joke_specific_category():
    joke = get_random_joke("Programming")
    assert joke is not None, "Joke should not be None in the Programming category"

def test_get_random_joke_invalid_category():
    joke = get_random_joke("InvalidCategory")
    assert "Error fetching joke." in joke, "Should return error message for invalid category"

def test_get_random_joke_network_error(mocker):
    mocker.patch('app.utils.add_ons.requests.get', side_effect=requests.exceptions.ConnectionError)
    joke = get_random_joke()
    assert "Network error" in joke, "Should handle network errors"

def test_get_random_joke_timeout_error(mocker):
    mocker.patch('app.utils.add_ons.requests.get', side_effect=requests.exceptions.Timeout)
    joke = get_random_joke()
    assert "Timeout error" in joke, "Should handle timeout errors"
