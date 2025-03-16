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
