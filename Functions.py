import requests
import json






def main_menu():
    while True:
        db = data_base_reader_no_print()

        print("\n--- CLI-Mate Menu ---")
        print("1. Get weather for a saved city")
        print("2. Add a new city")
        print("3. View saved cities and coordinates")
        print("4. Change forecast display settings #Not done yet")
        print("5. Why does this app use coordinates? #Not done yet")
        print("6. Exit")
        print("---------------------")

        choice = input("Choose an option (1-6): ").strip()

        match choice:
            case "1":
                if not db:
                    print("\nYour database is empty! Please add a city first (Option 2).")
                else:
                    selected_city = choose_an_option()
                    lat = db[selected_city]["latitude"]
                    lon = db[selected_city]["longitude"]
                    get_weather(selected_city, lat, lon)

            case "2":
                print("\n--- Adding a New City ---")
                add_city(search_for_city())

            case "3":
                if not db:
                    print("\nYour database is empty!")
                else:
                    print("\n--- Saved Cities and Coordinates ---")
                    for city_name, coords in db.items():
                        print(f"* {city_name} ({coords['Country']}) — Latitude: {coords['latitude']}, Longitude: {coords['longitude']}")

            case "4":
                print("\n[WIP] This setting will be available tomorrow!")

            case "5":
                print("\n[WIP] The coordinate explainer is coming tomorrow!")

            case "6":
                print("\nThank you for using CLI-Mate! Goodbye!")
                break

            case _:
                print("\nInvalid choice, please enter a number from 1 to 6.")












def greeting():
    print("---Hello, this is a CLI forecast program, or CLI-Mate---")
    length = len(data_base_reader_no_print())
    if length < 1:
        add_city(search_for_city())

    
    else:
        print("Redirecting to main menu")





def data_base_reader_no_print():
    with open("data_base.json", "r", encoding="utf-8") as file:
        data_base = json.load(file)
        return(data_base)



def add_city(city):
    database = data_base_reader_no_print()
    
    
    database[city["City"]] = {
    "Country": city["Country"],
    "latitude": city["latitude"],
    "longitude": city["longitude"]
    }
    
    
    with open("data_base.json", "w", encoding="utf-8") as file:
    
        json.dump(database, file, ensure_ascii=False, indent=4)


def search_for_city():
    city = input("Enter you city's name: ")
    
    payload = {
        "name": city 
    }

    url = "https://geocoding-api.open-meteo.com/v1/search"
    working = True
    
    while working:
        try:
            response = requests.get(url,params = payload)
            print(response.status_code)
            data = response.json()
            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]
            country = data["results"][0]["country"]
            name = data["results"][0]["name"]

            print(f"City:{name}, Country:{country}")
            print(f"Latitude:{latitude}, Longitude:{longitude}")
            dict = {
                "City": name, "Country": country, "latitude": latitude, "longitude": longitude
            }
            return dict
        except:
            print("Invalid, try again")
            continue






db = data_base_reader_no_print()

cities_list = list(db.keys())

def choose_an_option():
    current_db = data_base_reader_no_print()
    current_list = list(current_db.keys())
    
    print("\nYour saved cities:")
    for index, city_name in enumerate(current_list, 1):
        print(f"{index}. {city_name}")
        
    choice = int(input("Choose the number of the saved city to see weather: "))
    selected_city = current_list[choice - 1]
    return selected_city





def get_weather_backup(backup_url, backup_parameters, city_name):
    
    
    try:

        response = requests.get(backup_url, backup_parameters)

        if response.status_code == 200:
            print("Request success")
            print("Received text:")
            data = response.json()
        
            current_temp = data["current_weather"]["temperature"]

            # 2. Выводим информацию без строки "The weather is..."
            print("--- Information (Backup) ---\n")
            print(f"Current temperature in {city_name}: {current_temp} degrees celsius")
            print("Weather retrieved successfully via coordinates.")
        
   
        else:
            print(f"Request error: {response.status_code}")
            print("No other options left, you got to wait till everything's ok")

            print("HTTP Status Code Guide:",)
            print("200-299  Success! Everything worked perfectly.") 
            print("300-399  Redirect. The page moved somewhere else.")
            print("400-499  Client Error. The problem is on YOUR side (check inputs, URLs, or login).")
            print("500-599  Server Error. The problem is on THEIR side (the website/API is broken).")
            



    except:
        print("Something went wrong, idk what")




####  Main weather getting function

def get_weather(city_name, lat, lon):
    try:

        url = f"https://wttr.in/{city_name}"
        parameters = {
            "format": "j1", 
            "lang": "en"    
        }
        
        backup_url = "https://api.open-meteo.com/v1/forecast"
        backup_parameters = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        
        
        response = requests.get(url, parameters)

        if response.status_code == 200:
            print("Request success")
            print("Received text:")
            data = response.json()
        
            current_temp = data["current_condition"][0]["temp_C"]
            current_weather_description = data["current_condition"][0]["weatherDesc"][0]["value"]


            print("--- Information---\n")
            print(f"Current temperature in {city_name}:{current_temp} degrees celsius")
            print(f"The weather is {current_weather_description}")
        
        
        
        
   
        else:
            print(f"Request error: {response.status_code}")
            print("Attempting backup website")
            get_weather_backup(backup_url, backup_parameters, city_name)
            
            print("HTTP Status Code Guide:")
            print("200-299  Success! Everything worked perfectly.") 
            print("300-399  Redirect. The page moved somewhere else.")
            print("400-499  Client Error. The problem is on YOUR side, and it's not about the programm, I(da developer) am precise at coding.")
            print("500-599  Server Error. The problem is on THEIR side (the website/API is broken).")
            
            
    except:
        print("Something went wrong, idk what")

