import requests
import pandas as pd
#import matplotlib.pyplot as plt
import board
import neopixel
import datetime

led_mapping ={
'SCL':0,'CHPD':1,'DOPD':2,'AVA':3,'GCPD':4,'PSEI':5,'TWPR':6,'PGE':7,'BPAT':8,'PACW':9,
'BANC':11,'TIDC':12,'CISO':13,'LDWP':14,'WALC':15,'IID':16,'AZPS':18,'SRP':19,'TEPC':20,'EPE':22,
'PNM':23,'NEVP':27,'IPCO':29,'NWMT':31,'WAUW':32,'PACE':34,'WACM':36,'PSCO':37,'SWPP':39,'AECI':41,
'MISO':42,'SPA':44,'ERCO':47,'AEC':50,'SOCO':51,'TAL':52,'SEC':53,'TEC':54,'HST':55,'FPL':56,
'FMPP':57,'FPC':58,'GVL':59,'JEA':60,'SCEG':61,'SC':62,'CPLE':63,'DUK':64,'CPLW':65,'TVA':67,
'LGEE':68,'OVEC':69,'PJM':70,'NYIS':72,'ISNE':74
}






PUSHBULLET_API_KEY =#YOUR KEY HERE
# Define function to send pushbullet notification
def send_push_notification(title, body):
    url ='https://api.pushbullet.com/v2/pushes'
    headers= {
    'Access-Token':PUSHBULLET_API_KEY,
    'Content-Type':'application/json'
    }
    data={
    'type':'note',
    'title':title,
    'body':body
    }
    response=requests.post(url,headers=headers,json=data)
    if response.status_code==200:
        print('Push notification sent')
    else:
        print('Failed to send notification')



# Define a function to convert percent_change to RGB color
def percent_change_to_color(percent_change):
    if percent_change >= 0:
        return '({},0,0)'.format(int(255 * percent_change))
    else:
        return '(0,0,{})'.format(int(-255 * percent_change))

# Define the NeoPixel parameters
NUM_LEDS =   100 # Number of LEDs
PIN = board.D18  # Pin number
ORDER = neopixel.RGB  # Pixel color channel order



# Initialize the NeoPixel object
pixels = neopixel.NeoPixel(PIN, NUM_LEDS, pixel_order=ORDER)
try:

    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/?frequency=hourly&data[0]=value&facets[type][]=D&facets[respondent][]=AEC&facets[respondent][]=AECI&facets[respondent][]=AVA&facets[respondent][]=AZPS&facets[respondent][]=BANC&facets[respondent][]=BPAT&facets[respondent][]=CHPD&facets[respondent][]=CISO&facets[respondent][]=CPLE&facets[respondent][]=CPLW&facets[respondent][]=DOPD&facets[respondent][]=DUK&facets[respondent][]=EPE&facets[respondent][]=ERCO&facets[respondent][]=FMPP&facets[respondent][]=FPC&facets[respondent][]=FPL&facets[respondent][]=GCPD&facets[respondent][]=GVL&facets[respondent][]=HST&facets[respondent][]=IID&facets[respondent][]=IPCO&facets[respondent][]=ISNE&facets[respondent][]=JEA&facets[respondent][]=LDWP&facets[respondent][]=LGEE&facets[respondent][]=MISO&facets[respondent][]=NEVP&facets[respondent][]=NWMT&facets[respondent][]=NYIS&facets[respondent][]=OVEC&facets[respondent][]=PACE&facets[respondent][]=PACW&facets[respondent][]=PGE&facets[respondent][]=PJM&facets[respondent][]=PNM&facets[respondent][]=PSCO&facets[respondent][]=PSEI&facets[respondent][]=SC&facets[respondent][]=SCEG&facets[respondent][]=SCL&facets[respondent][]=SEC&facets[respondent][]=SOCO&facets[respondent][]=SPA&facets[respondent][]=SRP&facets[respondent][]=SWPP&facets[respondent][]=TAL&facets[respondent][]=TEC&facets[respondent][]=TEPC&facets[respondent][]=TIDC&facets[respondent][]=TPWR&facets[respondent][]=TVA&facets[respondent][]=WACM&facets[respondent][]=WALC&facets[respondent][]=WAUW&start=2024-03-01T00&end=2024-03-01T01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
    api_key =#YOUR KEY HERE

# Get current time

    end_time = datetime.datetime.utcnow()-datetime.timedelta(hours=1)
    start_time=end_time-datetime.timedelta(hours=1)

#Format the current time as needed
    start_time_str=start_time.strftime('%Y-%m-%dT%H')
    end_time_str= end_time.strftime('%Y-%m-%dT%H')

# modify url to use current time
    url=url.replace("start=2024-03-01T00","start="+start_time_str)

    url=url.replace("end=2024-03-01T01","end="+end_time_str)
    headers = {
    "X-Api-Key": api_key
    }
    print("Querying...")
    response = requests.get(url, headers=headers)
    print("Query complete")
    if response.status_code == 200:
    # Request was successful
        data = response.json()
    # Process the data as needed
    #print(data)
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
    # Replace NaN values with a default value, such as -1
        df.fillna(-1, inplace=True)

        return df


# Example usage:
# Assuming json_response is your JSON response
    df = json_to_dataframe(data)
    print(df)
# Convert 'period' column to datetime format
    df['period'] = pd.to_datetime(df['period'])
# Select rows where 'type' is 'D'
    df = df[df['type'] == 'D']
# Convert 'value' column to numeric
    df['value'] = pd.to_numeric(df['value'])
# Replace negative values with 0
    df['value']=df['value'].clip(lower=0)

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
# Calculate the percent change, handling division by zero
    df['percent_change'] = df.apply(lambda row: (row['hour'] - row['lagged_hour']) / row['hour'] if row['hour'] != 0 else 0, axis=1)
#clip the upper and lower bound to 100% for color rgb values
    df['percent_change'] = df['percent_change'].clip(lower=-1,upper=1)
# need to remove/ replace nas but maintain order on led strip
    df['percent_change']=df['percent_change'].round(2)
# Apply the function to create the color column
    df['color'] = df['percent_change'].apply(percent_change_to_color)

    df=df.sort_values(by='respondent')
# Displaying DataFrame
    print(df[['period','respondent','lagged_hour','hour','percent_change','color']])



# Function to convert RGB color string to tuple
    def rgb_str_to_tuple(rgb_str):
    # Extract RGB values from string and convert to integers
        rgb_values = [int(val) for val in rgb_str.strip('()').split(',')]
        return tuple(rgb_values)

# Assign color to NeoPixel
    def assign_color_to_led(color_str):
        color_tuple = rgb_str_to_tuple(color_str)
        pixels.fill(color_tuple)

    for led_index, color in df['color'].items():
        led_name=df.loc[led_index,'respondent']
        neo_pixel_index=led_mapping.get(led_name,-1)
        if neo_pixel_index != -1:
            pixels[neo_pixel_index]=rgb_str_to_tuple(color)
     
    print("Script executed Sucessfully")

except Exception as e:
    error_message=f'An error occured: {str(e)}'
    print(error_message)
    send_push_notification("Script Error",error_message)
else:
    send_push_notification("Script Sucess","Script executed Sucessfully")


