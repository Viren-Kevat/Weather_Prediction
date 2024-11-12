import requests
import datetime
import streamlit as st

def get_weather(location, api_key, date):
    # API URL to fetch weather data
    url = f"https://www.meteosource.com/api/v1/free/point?place_id={location}&sections=all&timezone=UTC&language=en&units=metric&key={api_key}"
    
    # Make the request to the API
    response = requests.get(url)

    # Check if the API request was successful
    if response.status_code == 200:
        return response.json()  # Return the entire response if successful
    else:
        st.error(f"Error: {response.status_code} - {response.text}")  # Print the error details
        return None

def display_weather(weather_data, selected_date):
    # Check if weather data is available
    if weather_data is None:
        st.error("Weather data is unavailable.")
        return
    
    # Debugging: Display the raw weather data
    # st.write("Weather Data:", weather_data)

    try:
        # Extract current, hourly, and daily weather information
        current_weather = weather_data['current']
        hourly_forecast = weather_data['hourly']['data']
        daily_forecast = weather_data['daily']['data']

        # Display current weather
        st.subheader("Weather")
        st.write(f"**Temperature**: {current_weather['temperature']}°C")
        st.write(f"**Weather Condition**: {current_weather['summary']}")
        st.write(f"**Wind Speed**: {current_weather['wind']['speed']} m/s")
        st.write(f"**Cloud Cover**: {current_weather['cloud_cover']}%")

        # Display hourly forecast data
        st.subheader("Hourly Forecast")
        for hour in hourly_forecast:
            hour_time = datetime.datetime.fromisoformat(hour['date']).strftime("%H:%M")
            temp = hour['temperature']
            condition = hour['summary']
            # icon_url = f"http://openweathermap.org/img/wn/{hour['icon']}.png"
            wind_speed = hour['wind']['speed']
            precipitation = hour['precipitation']['total']

            with st.expander(f"Time: {hour_time} - {condition}"):
                # st.image(icon_url, width=50)
                st.write(f"**Temperature**: {temp}°C")
                st.write(f"**Wind Speed**: {wind_speed} m/s")
                st.write(f"**Precipitation**: {precipitation} mm")

       

    except KeyError as e:
        st.error(f"Error: Missing key {e}. Check the structure of the weather data.")

def main():
    # Title and input fields
    st.title("Weather Forecast Application 🌤️")

    # Input field for location
    location = st.text_input("Enter Location", "Navsari")  # Default is "Navsari"
    
    # Date input for selecting the forecast date
    selected_date = st.date_input("Select Date", datetime.date.today())  # Default is today's date
    
    # API key (replace with your own)
    api_key = "md7jlmj2bn45z87p4xr8srmkkplrn15s6g03afek"

    # Search button to fetch the weather data
    if st.button("Get Weather"):
        # Get the weather data from the API
        weather_data = get_weather(location, api_key, selected_date)

        # Display weather data if available
        display_weather(weather_data, selected_date)

if __name__ == "__main__":
    main()
