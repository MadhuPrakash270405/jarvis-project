import requests

def get_random_joke(category="Any"):
    try:
        url = f"https://v2.jokeapi.dev/joke/{category}?blacklistFlags=nsfw,religious"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        joke_data = response.json()

        if joke_data["error"]:
            return "Error fetching joke."

        if joke_data["type"] == "single":
            return joke_data["joke"]
        else:
            return f"{joke_data['setup']} - {joke_data['delivery']}"
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError:
        return "Network error: Unable to connect to the joke service."
    except requests.exceptions.Timeout:
        return "Timeout error: The joke service did not respond in time."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
