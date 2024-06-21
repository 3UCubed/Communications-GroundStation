## Created by: Erika Diaz Ramirez
## Last updated: 06-21-24
## This code uses an API call to get the TLE from the website N2YO.com
## This can be an alternate way to get TLEs that's faster than web-scraping.
## Currently, the code is set so that it makes an API call every 15 minutes. 
## You can change the time it takes in between the API calls on line 87.

import requests
import time

API_KEY = '8W7LNM-52TLGK-H2PDD7-59TG'  #this is my personal API key from N2YO 

def get_tle(norad_id):
    # Construct the API URL
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}&apiKey={API_KEY}"
    print(f"Requesting URL: {url}") 
    # Make the HTTP request
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    # Parse the JSON content
    try:
        data = response.json()
    except ValueError:
        print("Failed to parse JSON response.")
        return None
    # Debugging information
    # print(f"Response JSON: {data}")
    # Extract TLE data
    tle_data = data.get('tle')
    if tle_data:
        tle_lines = tle_data.split('\r\n')
        if len(tle_lines) >= 2:
            tle_line1 = tle_lines[0]
            tle_line2 = tle_lines[1]
            return tle_line1, tle_line2
        else:
            print("TLE data not found in the expected format.")
            return None
    else:
        print("TLE data not found in the API response.")
        return None

def save_tle_to_file(tle_history, filename):
    with open(filename, 'w') as file:
        for tle in tle_history:
            file.write(f"{tle[0]}\n{tle[1]}\n")
    print(f"TLE data updated and saved to {filename}")

def get_valid_norad_id():
    while True:
        norad_id = input("Enter the NORAD ID: ")
        if norad_id.isdigit():
            return norad_id
        else:
            print("Invalid NORAD ID. Please enter a numeric value.") 

def main():
    output_filename = "tle_history.txt"
    tle_history = []
    norad_id = get_valid_norad_id()

    initial_tle_data = get_tle(norad_id)
    if initial_tle_data:
        tle_history.append(initial_tle_data)
        save_tle_to_file(tle_history, output_filename) #save initial tle
    else:
        print("Failed to retrieve initial TLE data.")
        return

    while True:
        tle_data = get_tle(norad_id)
        if tle_data:
            # Print the TLE data to the terminal
            tle_line1, tle_line2 = tle_data
            print(f"TLE Confirmation")
            print(f"TLE Line 1: {tle_line1}")
            print(f"TLE Line 2: {tle_line2}")
            # Check if this TLE is different from the last one
            if not tle_history or tle_data != tle_history[-1]: 
                print("New TLE data detected, updating history.")
                tle_history.append(tle_data)
                # Keep only the last 5 TLEs
                if len(tle_history) > 5:
                    tle_history.pop(0)
                # Save the TLE history to file
                save_tle_to_file(tle_history, output_filename)
            else:
                print("TLE data hasn't changed.")
        # Wait for a specified time before checking again (15 mins)
        # The 15 mins is to ensure we do not pass the 1000 transactions/hr
        # This limit can and should be modified for later
        time.sleep(60)


if __name__ == "__main__":
    main()




