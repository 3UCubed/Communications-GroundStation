import requests
from bs4 import BeautifulSoup

def getTLE(norad_id):
    # Construct the URL
    url = f"https://www.n2yo.com/satellite/?s={norad_id}"
    
    # Make the HTTP request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the TLE data
    tle = soup.find('div', {'id': 'tle'})
    if tle:
        lines = tle.text.strip().split('\n')
        if len(lines) >= 2:
            tle_line1 = lines[0].strip()
            tle_line2 = lines[1].strip()
            return tle_line1, tle_line2
        else:
            print("TLE data not found in the expected format.")
            return None
    else:
        print("TLE data not found.")
        return None

def saveTLE(norad_id, filename):
    tle_data = getTLE(norad_id)
    if tle_data:
        tle_line1, tle_line2 = tle_data
        # print out the tle before saving to file
        if tle_data:
            print(f"TLE Line 1: {tle_line1}")
            print(f"TLE Line 2: {tle_line2}")
        #save to file
        with open(filename, 'w') as file:
            file.write(f"{tle_line1}\n{tle_line2}\n")
        print(f"TLE data saved to {filename}")
    else:
        print("No TLE data to save")

# main
norad_id = input("Enter the NORAD ID: ")
output_file = "tle_test.txt"
saveTLE(norad_id, output_file)
