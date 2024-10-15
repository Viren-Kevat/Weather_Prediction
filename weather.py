import streamlit as st
import requests
import datetime

# Function to fetch weather data
@st.cache_data(show_spinner=False)
def get_weather(location, api_key, date):
    url = f"http://api.weatherapi.com/v1/future.json?key={api_key}&q={location}&dt={date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Display weather information with images for each hourly section
def display_weather(weather_data):
    location = weather_data['location']
    forecast = weather_data['forecast']['forecastday'][0]['hour']
    
    st.subheader(f"Weather Forecast for {location['name']}, {location['region']}, {location['country']}")
    
    # Organize forecast data into sections with images
    for hour in forecast:
        time = hour['time'].split(" ")[1]  # Display only the hour
        temp_c = hour['temp_c']
        condition = hour['condition']['text']
        icon_url = "http:" + hour['condition']['icon']  # Get the weather condition icon
        wind_speed = hour['wind_kph']
        rain_chance = hour['chance_of_rain']

        # Display weather data in an expandable section
        with st.expander(f"Time: {time} - {condition}"):
            st.image(icon_url, width=50)  # Display the weather icon
            st.write(f"**Temperature**: {temp_c}°C")
            st.write(f"**Wind Speed**: {wind_speed} kph")
            st.write(f"**Chance of Rain**: {rain_chance}%")
            st.write("---")

# Main function for the app
def main():
    st.title("Weather Forecast Application 🌤️")
    
    api_key = "0688e70c58c8418c87f200132241510"
    
    # Input field for location
    location = st.text_input("Enter location (e.g., 'New York')", "")
    
    # Select date (with a default of tomorrow)
    date = st.date_input("Select date for forecast", min_value=datetime.date.today() + datetime.timedelta(days=1))
    
    # Handle button click
    if st.button("Get Weather Forecast"):
        if location.strip():  # Check for valid input
            with st.spinner("Fetching weather data..."):
                weather_data = get_weather(location, api_key, date)
            if weather_data:
                display_weather(weather_data)
            else:
                st.error("Failed to retrieve data. Please check the location or try again later.")
        else:
            st.warning("Please enter a location.")

if __name__ == "__main__":
    main()
