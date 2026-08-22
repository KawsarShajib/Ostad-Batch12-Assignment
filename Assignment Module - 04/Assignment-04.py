import requests
import json
from datetime import datetime

# WEATHER_API_URL = "https://wttr.in/{city}?format=j1"
# CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/{base}"

last_fetched_data = None

FILE_NAME = "data.json"


def weather():

    global last_fetched_data

    city = input("Enter city name: ").strip()
    if not city:
        print("City name cannot be empty.\n")
        return
    
    #url = "https://wttr.in/" + city + "?format=j1"
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url)
        # response = requests.get(WEATHER_API_URL.format(city=city), timeout=10)
        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        humidity = current["humidity"]
        wind_speed = current["windspeedKmph"]
        condition = current["weatherDesc"][0]["value"]

        now = datetime.now()
        display_time = now.strftime("%d-%m-%Y %I:%M %p")
        save_time = now.strftime("%Y-%m-%d %H:%M:%S")

        print("\n------ Weather Report -----------------")
        print(f"City\t\t: {city.title()}")
        print(f"Temperature\t: {temperature}°C")
        print(f"Humidity\t: {humidity}%")
        print(f"Wind Speed\t: {wind_speed} km/h")
        print(f"Condition\t: {condition}")
        print(f"Fetched At\t: {display_time}")
        print("-----------------------------------------\n")

        last_fetched_data = {
            "type": "weather",
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "condition": condition,
            "time": save_time
        }

    except Exception:
        print("\nSomething went wrong. Please check the city name or your internet connection.\n")


# ---------------------------------------------------------
# Function 2: Get currency exchange rate
# ---------------------------------------------------------
def currency():
    """Fetch and display the exchange rate between two currencies."""

    global last_fetched_data

    base = input("Base Currency   (e.g. USD): ").strip().upper()
    target = input("Target Currency (e.g. BDT): ").strip().upper()

    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    # url = "https://api.exchangerate-api.com/v4/latest/" + base
    
    if not base or not target:
        print("Base or Target currency cannot be empty.\n")
        return
    
    try:
        response = requests.get(url)
        # response = requests.get(CURRENCY_API_URL.format(base=base), timeout=10)
        data = response.json()

        rate = data["rates"][target]

        now = datetime.now()
        display_time = now.strftime("%d-%m-%Y %I:%M %p")
        save_time = now.strftime("%Y-%m-%d %H:%M:%S")

        print("\n------ Exchange Rate ------------------")
        print("1", base, "=", rate, target)
        print("Fetched At:", display_time)
        print("-----------------------------------------\n")

        last_fetched_data = {
            "type": "currency",
            "base": base,
            "target": target,
            "rate": rate,
            "time": save_time
        }

    except Exception:
        print("\nSomething went wrong. Please check the currency codes or your internet connection.\n")


# ---------------------------------------------------------
# Function 3: Save the last fetched data to a data.json file
# ---------------------------------------------------------
def save_json():

    if last_fetched_data is None:
        print("\nNo data to save yet. Please fetch weather or currency first.\n")
        return

    file = open(FILE_NAME, "w")
    json.dump(last_fetched_data, file, indent=4)
    file.close()

    print("\nData saved to", FILE_NAME, "\n")


# ---------------------------------------------------------
# Function 4: View the previously saved data from data.json file
# ---------------------------------------------------------
def view_json():

    try:
        file = open(FILE_NAME, "r")
        data = json.load(file)
        file.close()
    except FileNotFoundError:
        print("\nNo saved data found. Please save some data first.\n")
        return

    if data["type"] == "weather":
        print("\n------ Weather Report -------------------")
        print("Type\t\t: Weather")
        print("City\t\t:", data["city"])
        print("Temperature\t:", data["temperature"], "°C")
        print("Saved Time\t:", data["time"])
        print("-------------------------------------------\n")

    elif data["type"] == "currency":
        print("\n------ Currency Report -------------------")
        print("Type\t\t: Currency")
        print("Base\t\t:", data["base"])
        print("Target\t\t:", data["target"])
        print("Rate\t\t: 1", data["base"], "=", data["rate"], data["target"])
        print("Saved Time\t:", data["time"])
        print("-------------------------------------------\n")


# ---------------------------------------------------------
# Function 5: Show the menu and take user's choice
# ---------------------------------------------------------
def main_menu():
    """Display the menu and route user choices to the right function."""

    while True:
        print("\n========== Data Fetcher ==========")
        print("1. Current Weather")
        print("2. Currency Exchange Rate")
        print("3. Save Result to JSON File")
        print("4. View Previous Saved Data")
        print("5. Exit")
        print("==================================")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            weather()
        elif choice == "2":
            currency()
        elif choice == "3":
            save_json()
        elif choice == "4":
            view_json()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.\n")


main_menu()