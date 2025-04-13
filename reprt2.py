

import os
print("current working directory:",
os.getcwd())

import requests
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

#from datetime import datetime

# Step 1: Fetch Weather Data
API_KEY = "fda2923754d1b9c5610530a8aa95efdd"  # Replace with your OpenWeatherMap API key
CITY = 'PUNE'
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

# Step 2: Process Data
weather_data = []
for item in data['list'][:5]:  # Limiting to first 5 entries
    weather_data.append({
        "DateTime": item['dt_txt'],
        "Temperature": item['main']['temp'],
        "Feels Like": item['main']['feels_like'],
        "Humidity": item['main']['humidity'],
        "Description": item['weather'][0]['description']
    })

df = pd.DataFrame(weather_data)

# Step 3: Generate Plot (Temperature vs Time)
plt.figure(figsize=(8, 4))
plt.plot(df["DateTime"], df["Temperature"], marker='o', linestyle='-', color='blue')
plt.xticks(rotation=45)
plt.title(f"Temperature Forecast for {CITY}")
plt.xlabel("DateTime")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.savefig("weather_plot.png")  # Save plot as image
plt.close()

# Step 4: Create PDF Report
doc = SimpleDocTemplate("Weather_Report.pdf")

styles = getSampleStyleSheet()
story = []

story.append(Paragraph(f"Weather Report for {CITY}", styles['Title']))
story.append(Spacer(1, 12))
#story.append(Image("weather_plot.png",width=400,height=200))
doc.build(story)

# Add summary paragraphs
for index, row in df.iterrows():
    summary = f"{row['DateTime']}: {row['Description']}, Temp: {row['Temperature']}°C, Feels like: {row['Feels Like']}°C, Humidity: {row['Humidity']}%"
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 6))

# Add plot
story.append(Spacer(1, 12))
story.append(Image("weather_plot.png", width=400, height=200))

doc.build(story)
print("Weather report generated successfully!")


