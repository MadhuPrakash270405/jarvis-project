from datetime import time
from screen_brightness_control import set_brightness
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess
import psutil


def brightness_control(value=100):
    try:
        set_brightness(display=0, value=value)
        return f'Brightness set to {value}'
    except Exception as e:
        return f'Error setting brightness: {e}'



def audio_control():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(-5.0, None) #72%# mute
        return 'Audio muted'
    except Exception as e:
        return f'Error controlling audio: {e}'



def wifi_control():
    try:
        result = subprocess.run(
            ["netsh", "interface", "show", "interface", "Wi-Fi"],
            capture_output=True,
            text=True,
        )
        return result.stdout
    except subprocess.SubprocessError as e:
        return f'Error controlling WiFi: {e}'
    except Exception as e:
        return f'Unexpected error: {e}'


def toggle_audio(enable):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        if enable:
            volume.SetMute(0, None)
            volume.SetMasterVolumeLevel(-5.0, None) #72%
            return "Audio turned on."
        else:
            volume.SetMute(1, None)
            return "Audio turned off."
    except Exception as e:
        return f'Error toggling audio: {e}'



def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            plugged = battery.power_plugged
            percent = battery.percent
            status = "Plugged in" if plugged else "Not Plugged in"
            return f"Charge: {percent}% | Status: {status}"
        else:
            return "Battery status not available"
    except Exception as e:
        return f'Error getting battery status: {e}'



# if __name__ == "__main__":
#     # Example usage
#     print(toggle_audio(enable=True))  # To turn on
#     print(get_battery_status())
