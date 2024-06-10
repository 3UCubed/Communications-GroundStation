import requests
from bs4 import BeautifulSoup
import time

def get_tle(norad_id):
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

def save_tle_to_file(tle_history, filename):
    with open(filename, 'w') as file:
        for tle in tle_history:
            file.write(f"{tle[0]}\n{tle[1]}\n")
    print(f"TLE data updated and saved to {filename}")

def main():
    norad_id = input("Enter the NORAD ID: ")
    output_filename = "tle_history.txt"
    tle_history = []

    while True:
        tle_data = get_tle(norad_id)
        if tle_data:
            # Print the TLE data to the terminal
            tle_line1, tle_line2 = tle_data
            print(f"TLE Line 1: {tle_line1}")
            print(f"TLE Line 2: {tle_line2}")
            
            # Check if this TLE is different from the last one
            if not tle_history or tle_data != tle_history[-1]:
                tle_history.append(tle_data)
                # Keep only the last 5 TLEs
                if len(tle_history) > 5:
                    tle_history.pop(0)
                # Save the TLE history to file
                save_tle_to_file(tle_history, output_filename)
        
        # Wait for a specified time before checking again (60sec)
        time.sleep(60)

if __name__ == "__main__":
    main()

