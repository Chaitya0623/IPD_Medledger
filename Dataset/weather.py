import requests
import csv
from datetime import datetime, timedelta
from collections import Counter

# API key and base URL
api_key = "e1f10a1e78da46f5b10a1e78da96f525"
base_url = "https://api.weather.com/v1/location/VIDP:9:IN/observations/historical.json"

# Date range from 01-01-2009 to 23-02-2024
start_date = datetime(2022, 2, 2)
end_date = datetime(2022, 12, 31)

# Open CSV file for writing
with open('weather_data_2009_2024(1).csv', 'w', newline='') as csvfile:
    fieldnames = ['Date','Average Temperature (C)', 'Average Temperature (F)', 'Most Repeated Weather Phrase',
                  'Average Wind Speed (mph)', 'Average Wind Speed (kph)', 'Average Wind Degree',
                  'Most Repeated Wind Direction', 'Average Pressure', 'Average Dew Point',
                  'Average Heat Index', 'Average Visibility', 'Most Repeated Cloud Cover',
                  'Average UV Index']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header with "dd-mm-yyyy" format
    writer.writeheader()

    # Loop through the date range
    current_date = start_date
    while current_date <= end_date:
        # Format date as yyyymmdd for API request
        formatted_date_api = current_date.strftime('%Y%m%d')

        # API request for the current date
        api_url = f"{base_url}?apiKey={api_key}&units=e&startDate={formatted_date_api}"
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract temperatures from the response, skipping None values
            temperatures = [observation['temp'] for observation in data.get('observations', []) if observation.get('temp') is not None]

            # Calculate average temperature
            if temperatures:
                average_temperature = sum(temperatures) / len(temperatures)
                average_temperature_cel = (average_temperature - 32) * 5 / 9
            else:
                average_temperature = 'No data'

            # Extract additional parameters
            phrase = [observation['wx_phrase'] for observation in data.get('observations', [])]
            most_repeated_phrase = Counter(phrase).most_common(1)[0][0] if phrase else 'No data'

            wind_speed = [observation['wspd'] for observation in data.get('observations', [])]
            wind_speed = [speed for speed in wind_speed if speed is not None]  # Filter out None values

            if wind_speed:
                average_wind_speed_mph = sum(wind_speed) / len(wind_speed)
                average_wind_speed_kph = average_wind_speed_mph * 1.60934
            else:
                average_wind_speed_mph = 'No data'
                average_wind_speed_kph = 'No data'


            wind_deg = [observation['wdir'] for observation in data.get('observations', [])]
            wind_deg = [deg for deg in wind_deg if deg is not None]  # Filter out None values

            if wind_deg:
                average_wind_deg = sum(wind_deg) / len(wind_deg)
            else:
                average_wind_deg = 'No data'


            wind_dir = [observation['wdir_cardinal'] for observation in data.get('observations', [])]
            most_repeated_winddir = Counter(wind_dir).most_common(1)[0][0] if wind_dir else 'No data'

            pressure = [observation['pressure'] for observation in data.get('observations', [])]
            pressure = [p for p in pressure if p is not None]  # Filter out None values

            if pressure:
                average_pressure = sum(pressure) / len(pressure)
            else:
                average_pressure = 'No data'


            dewPt = [observation['dewPt'] for observation in data.get('observations', [])]
            dewPt = [d for d in dewPt if d is not None]  # Filter out None values

            if dewPt:
                average_dewPt = sum(dewPt) / len(dewPt)
            else:
                average_dewPt = 'No data'


            heat_index = [observation['heat_index'] for observation in data.get('observations', [])]
            heat_index = [index for index in heat_index if index is not None]  # Filter out None values

            if heat_index:
                average_heat_index = sum(heat_index) / len(heat_index)
            else:
                average_heat_index = 'No data'


            vis = [observation['vis'] for observation in data.get('observations', [])]
            average_vis = sum(vis) / len(vis) if vis else 'No data'

            clds = [observation['clds'] for observation in data.get('observations', [])]
            most_repeated_clds = Counter(clds).most_common(1)[0][0] if clds else 'No data'

            uv_index = [observation['uv_index'] for observation in data.get('observations', [])]
            average_uv_index = sum(uv_index) / len(uv_index) if uv_index else 'No data'

            writer.writerow({
    'Date': current_date.strftime('%d-%m-%Y'),
    'Average Temperature (C)': average_temperature_cel,
    'Average Temperature (F)': average_temperature,
    'Most Repeated Weather Phrase': most_repeated_phrase,
    'Average Wind Speed (mph)': average_wind_speed_mph,
    'Average Wind Speed (kph)': average_wind_speed_kph,
    'Average Wind Degree': average_wind_deg,
    'Most Repeated Wind Direction': most_repeated_winddir,
    'Average Pressure': average_pressure,
    'Average Dew Point': average_dewPt,
    'Average Heat Index': average_heat_index,
    'Average Visibility': average_vis,
    'Most Repeated Cloud Cover': most_repeated_clds,
    'Average UV Index': average_uv_index
})

        else:
            print(f"Failed to fetch data for {current_date.strftime('%d-%m-%Y')}. Status Code: {response.status_code}")
        current_date += timedelta(days=1)

print("Data saved to weather_data_2009_2016.csv")