import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

API__KEY = os.getenv("API__KEY")

st.title("Weather App")

city = st.text_input("Enter a city name:")
if city.strip() == "":
    st.info("Please enter a city name to get the weather data.")
    st.stop()

url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API__KEY}"

geo_response = requests.get(url).json()
if not isinstance(geo_response, list) or len(geo_response) == 0:
    st.error("City not found or API error")
    st.write("API response:", geo_response)
    st.stop()

lat = geo_response[0]["lat"]
lon = geo_response[0]["lon"]

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API__KEY}&units=metric"
weather = requests.get(weather_url).json()

if weather.get("cod") != 200:
    st.error("⚠️ Weather API error")
    st.write(weather)
    st.stop()

st.subheader("🌤 Current Weather")
st.write(f"🌡 Temperature: {weather['main']['temp']} °C")
st.write(f"💧 Humidity: {weather['main']['humidity']}%")
st.write(f"☁ Description: {weather['weather'][0]['description']}")

forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API__KEY}&units=metric"
forecast = requests.get(forecast_url).json()

if forecast.get("cod") != "200":
    st.error("⚠️ Forecast API error")
    st.write(forecast)
    st.stop()

df = pd.DataFrame(forecast["list"])
df["date"] = pd.to_datetime(df["dt_txt"])
df["cloudiness"] = df["clouds"].apply(lambda x: x["all"])

st.subheader("☁ Cloudiness Forecast")

fig = px.line(
    df,
    x="date",
    y="cloudiness",
    title="Cloudiness Forecast Over Time",
    labels={"date": "Date", "cloudiness": "Cloudiness (%)"},
)

st.plotly_chart(fig)



