import streamlit as st
import pandas as pd
import requests

# Function to get weather data from OpenWeatherMap API
def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    return response.json()

# Function to read uploaded file and extract city names
def load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

# Streamlit app layout
st.title("Weather App")

# Input fields for API key and file upload
api_key = st.text_input("Enter your OpenWeatherMap API key:", type="password")
uploaded_file = st.file_uploader("Upload a CSV or Excel file with city names", type=["csv", "xlsx"])

if st.button("Get Weather"):
    if api_key and uploaded_file:
        city_data = load_file(uploaded_file)
        if city_data is not None and 'city' in city_data.columns:
            st.write("### Weather Information")
            for city in city_data['city']:
                weather_data = get_weather(city, api_key)
                if weather_data['cod'] == 200:
                    st.write(f"**City:** {city.capitalize()}")
                    st.write(f"**Temperature:** {weather_data['main']['temp']}°C")
                    st.write(f"**Weather:** {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
                    st.write(f"**Wind Speed:** {weather_data['wind']['speed']} m/s")
                    st.write("---")
                else:
                    st.write(f"City {city} not found. Please check the city name.")
        else:
            st.error("The uploaded file must contain a column named 'city'.")
    else:
        st.write("Please enter the API key and upload a file.")
