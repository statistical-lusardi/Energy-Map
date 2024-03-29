import requests
import pandas as pd
import matplotlib.pyplot as plt
import board
import neopixel


# Define a function to convert percent_change to RGB color
def percent_change_to_color(percent_change):
    if percent_change >= 0:
        return 'rgb({},0,0)'.format(int(255 * percent_change))
    else:
        return 'rgb(0,0,{})'.format(int(-255 * percent_change))


url = "https://api.eia.gov/v2/electricity/rto/region-data/data/?frequency=hourly&data[0]=value&facets[respondent][]=AVA&facets[respondent][]=AVRN&facets[respondent][]=BANC&facets[respondent][]=BPAT&facets[respondent][]=CHPD&facets[respondent][]=CISO&facets[respondent][]=DOPD&facets[respondent][]=GCPD&facets[respondent][]=GRID&facets[respondent][]=IID&facets[respondent][]=IPCO&facets[respondent][]=NEVP&facets[respondent][]=NWMT&facets[respondent][]=PACE&facets[respondent][]=PACW&facets[respondent][]=PGE&facets[respondent][]=PSEI&facets[respondent][]=SCL&facets[respondent][]=TPWR&start=2024-03-01T00&end=2024-03-01T01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
api_key = "94e8b0bb1fbf7a092e4546c7ba7bdf7f"

headers = {
    "X-Api-Key": api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Request was successful
    data = response.json()
    # Process the data as needed
    print(data)
else:
    # Request failed
    print("Error:", response.status_code)

def json_to_dataframe(json_response):
    # Extracting the 'response' key from the JSON response
    response_data = json_response.get('response', {})

    # Extracting the 'data' key from the response data
    data = response_data.get('data', [])

    # Creating DataFrame
    df = pd.DataFrame(data)

    return df


# Example usage:
# Assuming json_response is your JSON response
df = json_to_dataframe(data)
# Convert 'period' column to datetime format
df['period'] = pd.to_datetime(df['period'])
# Select rows where 'type' is 'D'
df = df[df['type'] == 'D']
# Convert 'value' column to numeric
df['value'] = pd.to_numeric(df['value'])

df = df[['period', 'respondent', 'value']]
df=pd.DataFrame(df)
# Sort by 'period' before grouping
df = df.sort_values(by='period')

# Group by 'respondent'
grouped = df.groupby('respondent')

# Calculate lagged_hour within each group
df['lagged_hour'] = grouped['value'].shift(1)
df['hour'] = df['value']

# Drop rows with missing values
df = df.dropna()
# Calculate the percent change
df['percent_change'] = (df['lagged_hour'] - df['hour']) / df['hour']
# Apply the function to create the color column
df['color'] = df['percent_change'].apply(percent_change_to_color)

# Displaying DataFrame
print(df)


# Define the NeoPixel parameters
NUM_LEDS = 1  # Number of LEDs
PIN = board.D18  # Pin number
ORDER = neopixel.RGB  # Pixel color channel order

# Initialize the NeoPixel object
pixels = neopixel.NeoPixel(PIN, NUM_LEDS, pixel_order=ORDER)

# Function to convert RGB color string to tuple
def rgb_str_to_tuple(rgb_str):
    # Extract RGB values from string and convert to integers
    rgb_values = [int(val) for val in rgb_str.strip('rgb()').split(',')]
    return tuple(rgb_values)

# Assign color to NeoPixel
def assign_color_to_led(color_str):
    color_tuple = rgb_str_to_tuple(color_str)
    pixels.fill(color_tuple)

# Light up the LED with the specified color
assign_color_to_led(df['color'][0])
