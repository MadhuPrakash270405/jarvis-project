




from utils.weather_functions import handle_weather_command
from utils.audio_functions import text_to_voice
from utils.add_ons import get_random_joke
from utils.general_tasks import brightness_control, toggle_audio, wifi_control, get_battery_status
from utils.spotify_music import play_random_song, stop_music
from utils.maps_functions import handle_maps_voice_command
from datetime import datetime
import re

def parse_brightness_command(command):
    match = re.search(r"brightness to (\d+)(%|\spercent)?", command.lower())
    if match:
        return int(match.group(1))  # Convert the captured group to an integer
    return None  # If the pattern does not match



def handle_voice_command(command):
    action = parse_command(command)
    print('Parsed Action',action)
    if  action == "joke":
        joke=get_random_joke(category="Any")
        return joke
    elif action == "set_brightness_max":
        return brightness_control()
    elif action == "current_time":
        return f'Time is {datetime.now().strftime("%I:%M:%S %p")}'
    elif action == "current_date":
        return f'Todays Date is {datetime.now().strftime("%Y-%m-%d")}'
    elif action == "set_brightness_level":
        print(command)
        print(parse_brightness_command(command))
        parsed_brightness = parse_brightness_command(command)
        if parsed_brightness:
            return brightness_control(parsed_brightness)
    elif action == "mute_audio":
        return toggle_audio(False)
    elif action == "wifi_status":
        return wifi_control()
    elif action == "battery_status":
        return get_battery_status()
    elif action == "play_music":
        play_random_song()
        return 'Music Started'
    elif action == "stop_music":
        stop_music()
        return 'Music stopped'
    elif action == "get_directions":
        return handle_maps_voice_command(command)
    elif action == "weather_query":
        return handle_weather_command(command)
    else:
        return "Sorry, I didn't understand that command."
        # print("Sorry, I didn't understand that command.")



def parse_command(command):
    command = command.lower()
    if re.search(r"set brightness to (maximum|max)", command):
        return "set_brightness_max"
    elif re.search(r"brightness to (\d+)", command):
        return "set_brightness_level"
    elif re.search(r"mute (audio|sound)", command):
        return "mute_audio"
    elif re.search(r"unmute (audio|sound)", command):
        return "unmute_audio"
    elif re.search(r"(wifi|wireless) status", command):
        return "wifi_status"
    elif re.search(r"battery status", command):
        return "battery_status"
    elif re.search(r"tell (me )?a joke", command):
        return "joke"
    elif re.search(r"play (a )?(song|music)", command):
        return "play_music"
    elif re.search(r"stop (the )?(music|song)", command):
        return "stop_music"
       # Pattern for current time
    elif re.search(r"what (is )?the (current )?time", command):
        return "current_time"
    # Pattern for today's date
    elif re.search(r"what('s| is) (the )?(today('s)? )?date", command):
        return "current_date"
    elif re.search(r"get (the )?(distance|direction|directions|coordinates)", command):
        return "get_directions"
    elif re.search(r"what'?s the weather (like )?in ([\w\s]+)|weather (in|for) ([\w\s]+)|forecast (in|for) ([\w\s]+)", command):
        return "weather_query"
    return None



def process_the_audio_command(transcript):
    transcript=transcript.lower()
    print(transcript)
    output_text=handle_voice_command(transcript)
    text_to_voice(output_text)
    return output_text


# commands = [
#     "Set brightness to maximum",
#     "Brightness to 50",
#     "Can you mute the audio?",
#     "Please unmute the sound",
#     "What's the wifi status?",
#     "How's the battery status?",
#     "Tell me the weather",
#     "Tell me a joke",
#     "Play a song",
#     "Stop the music",
#     "Get directions to the nearest café",
#     "what is the weather in New York"
# ]

# for cmd in commands:
#     action = parse_command(cmd)
#     print(f"Command: '{cmd}' => Action: {action}")