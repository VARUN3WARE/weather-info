import json
import requests
import ollama
from pydantic import BaseModel, Field

# --------------------------------------------------------------
# Geocoding function to convert location name into latitude and longitude
# --------------------------------------------------------------

def get_coordinates(location_name):
    """Convert location name into latitude and longitude using OpenCage Geocoding API."""
    api_key = "1e5a8a24f5dc4974ab27802522a7c7e8"  # Replace with your OpenCage API key
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location_name}&key={api_key}"

    response = requests.get(url)
    data = response.json()
    
    if data["results"]:
        latitude = data["results"][0]["geometry"]["lat"]
        longitude = data["results"][0]["geometry"]["lng"]
        return latitude, longitude
    else:
        raise ValueError(f"Could not get coordinates for location: {location_name}")

# --------------------------------------------------------------
# Define the tool (function) that we want to call
# --------------------------------------------------------------

def get_weather(latitude, longitude):
    """This is a publicly available API that returns the weather for a given location."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weathercode"
    
    try:
        response = requests.get(url)
        
        # Check if the response status is OK (200)
        if response.status_code == 200:
            data = response.json()
            # Ensure we have the expected keys in the response
            if "current" in data:
                current_weather = data["current"]
                return {
                    "temperature": current_weather["temperature_2m"],
                    "wind_speed": current_weather["wind_speed_10m"],
                    "humidity": current_weather["relative_humidity_2m"],
                    "weather_code": current_weather["weathercode"]
                }
            else:
                raise ValueError(f"Unexpected response format: {data}")
        else:
            raise ValueError(f"API request failed with status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --------------------------------------------------------------
# Step 1: Define system prompt and call Ollama model
# --------------------------------------------------------------
user_prompt="What's the weather like in bhilai,chattisgarh today?"
response = ollama.chat(
    model="llama3.2",  # Replace with the correct model if necessary
    messages=[
        {"role": "system", "content": "Don't provide any info but rather just see it as a sentece and find me the name of location being talked about { Place: something}"},
        {"role": "user", "content": user_prompt}
    ]
)

# --------------------------------------------------------------
# Step 3: Extract the content from the response
# --------------------------------------------------------------

# Extract the content from the message
location = response.message.content  # The event data in content field

# Print the extracted content for debugging
print("Extracted location information:")
print(location)
print("++++++++++++++++++++++++++++++++++++++++")


# Get the latitude and longitude using the geocoding function
latitude, longitude = get_coordinates(location)

# --------------------------------------------------------------
# Step 3: Execute get_weather function
# --------------------------------------------------------------

# Call the function directly with dynamically fetched latitude and longitude
weather_data = get_weather(latitude, longitude)


# --------------------------------------------------------------
# Step 4: Generate Detailed Weather Response
# --------------------------------------------------------------

# Mapping weather codes to human-readable weather descriptions
weather_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light showers of rain",
    81: "Moderate showers of rain",
    82: "Heavy showers of rain",
    85: "Light snow showers",
    86: "Heavy snow showers",
}

weather_condition = weather_descriptions.get(weather_data["weather_code"], "Unknown")


response = ollama.chat(
    model="llama3.2",  # Replace with the correct model if necessary
    messages=[
        {"role": "system", "content": "Based on weather condition provideor suggest an activity for me and just provide it in a format of this only with no extra words{ activity: something}"},
        {"role": "user", "content": f" weather condition is {weather_condition}"}
    ]
)
activity_suggestion = response.message.content  # The event data in content field

# Print the extracted content for debugging
print("Suggested Activity:")
print(activity_suggestion)
print("++++++++++++++++++++++++++++++++++++++++")
print(f"Temperature: {weather_data['temperature']}°C")
print(f"Humidity: {weather_data['humidity']}%")
print(f"Wind Speed: {weather_data['wind_speed']}km/h")
