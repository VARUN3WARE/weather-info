# Weather Forecasting and Activity Suggestion System

This repository provides a Python-based tool for querying weather information based on a location, generating a weather report, and suggesting an activity based on the current weather conditions. The system utilizes OpenCage Geocoding API to obtain coordinates for a location, the Open-Meteo API to fetch the weather data, and the Ollama Llama model for generating location and activity-based suggestions.

## Features

- **Geocoding:** Converts a given location (e.g., city name) into geographic coordinates (latitude and longitude) using the OpenCage API.
- **Weather Data Retrieval:** Fetches the current weather data (temperature, wind speed, humidity, and weather condition) for the given location using the Open-Meteo API.
- **Weather Descriptions:** Maps numerical weather codes to human-readable weather descriptions (e.g., "Clear sky", "Light rain").
- **Activity Suggestion:** Based on the weather condition, an activity suggestion is provided using an Ollama model.

## Requirements

- Python 3.x
- `requests` library
- `pydantic` library
- `ollama` Python package (to interact with Ollama models)

## Installation

1. Install the required dependencies using `pip`:
   ```bash
   pip install requests pydantic ollama
   ```

2. Replace `api_key` in the code with your own [OpenCage API key](https://opencagedata.com/).

3. Set up the Ollama environment with a model like `"llama3.2"` (or any suitable model).

## Usage

### 1. Geocode a Location:
The function `get_coordinates(location_name)` takes a location name (e.g., `"Bhilai, Chhattisgarh"`) and returns its latitude and longitude using OpenCage's Geocoding API.

### 2. Fetch Weather Data:
The function `get_weather(latitude, longitude)` retrieves the current weather conditions, including temperature, wind speed, humidity, and weather code.

### 3. Generate Weather Description:
The weather code from the Open-Meteo API response is mapped to a human-readable weather description (e.g., "Clear sky").

### 4. Suggest an Activity:
The system sends the weather condition as a prompt to the Ollama Llama model to suggest an activity. The activity is returned in a simple format like `{ activity: something }`.

## Example

```python
user_prompt = "What's the weather like in Bhilai, Chhattisgarh today?"
response = ollama.chat(
    model="llama3.2",  
    messages=[
        {"role": "system", "content": "Don't provide any info but rather just see it as a sentence and find me the name of location being talked about { Place: something}"},
        {"role": "user", "content": user_prompt}
    ]
)

# Extract location from response
location = response.message.content  # Location name extracted from the prompt
latitude, longitude = get_coordinates(location)

# Fetch weather data using coordinates
weather_data = get_weather(latitude, longitude)

# Map weather code to description
weather_descriptions = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Heavy drizzle", 56: "Freezing drizzle", 57: "Heavy freezing drizzle",
    61: "Light rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Freezing rain",
    67: "Heavy freezing rain", 71: "Light snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains", 80: "Light showers of rain", 81: "Moderate showers of rain",
    82: "Heavy showers of rain", 85: "Light snow showers", 86: "Heavy snow showers"
}

weather_condition = weather_descriptions.get(weather_data["weather_code"], "Unknown")

# Suggest activity based on weather condition
activity_response = ollama.chat(
    model="llama3.2",  
    messages=[
        {"role": "system", "content": "Based on weather condition provide or suggest an activity for me and just provide it in a format of this only with no extra words { activity: something }"},
        {"role": "user", "content": f"Weather condition is {weather_condition}"}
    ]
)
activity_suggestion = activity_response.message.content

# Output the weather data and suggested activity
print(f"Suggested Activity: {activity_suggestion}")
print(f"Temperature: {weather_data['temperature']}°C")
print(f"Humidity: {weather_data['humidity']}%")
print(f"Wind Speed: {weather_data['wind_speed']} km/h")
```

### Example Output:
```
Suggested Activity: { activity: Go for a walk in the park }
Temperature: 28°C
Humidity: 70%
Wind Speed: 10 km/h
```

## Notes

- Ensure that you are using valid API keys for both OpenCage Geocoding and Open-Meteo APIs.
- The Ollama Llama model can be replaced with any other suitable model based on your preferences and requirements.
- You can adjust the system prompts to modify the activity suggestions or how the weather data is presented.
