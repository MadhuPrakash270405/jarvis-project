import pytest
from app.utils.general_tasks import brightness_control, audio_control
from screen_brightness_control import ScreenBrightnessError
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Test cases for brightness_control function
def test_brightness_control_success(mocker):
    mocker.patch("app.utils.general_tasks.set_brightness")
    result = brightness_control(50)
    assert result == "Brightness set to 50"

def test_brightness_control_failure(mocker):
    mocker.patch("app.utils.general_tasks.set_brightness", side_effect=ScreenBrightnessError)
    result = brightness_control(50)
    assert "Error setting brightness" in result

# Test cases for audio_control function
def test_audio_control_success(mocker):
    mocker.patch("app.utils.general_tasks.AudioUtilities.GetSpeakers")
    mocker.patch("app.utils.general_tasks.cast")
    result = audio_control()
    # Assuming the function returns a success message
    assert "Audio muted" in result

def test_audio_control_failure(mocker):
    mocker.patch("app.utils.general_tasks.AudioUtilities.GetSpeakers", side_effect=Exception)
    result = audio_control()
    assert "Error controlling audio" in result

# Additional test cases can be added for other functions in app.utils.general_tasks.py
