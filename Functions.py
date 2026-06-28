import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
import time
from datetime import datetime
from Ascii_arts import weather_arts
import random







console = Console()
menu_table = Table(
    title="[bold #fabd2f]CLI-Mate Menu[/bold #fabd2f]", 
    box=box.ROUNDED,
    show_header=False,
    border_style="#928374"
)
menu_table.add_row("  1. Get weather for a saved city", style= "bold #b8bb26")
menu_table.add_row("  2. Add a new city", style= "bold #b8bb26")
menu_table.add_row("  3. View saved cities and coordinates", style= "bold #b8bb26")
menu_table.add_row("  4. Change forecast display settings (WIP)", style= "bold #b8bb26")
menu_table.add_row("  5. Why does this app use coordinates? (WIP)", style= "bold #b8bb26")
menu_table.add_row("  6. Exit", style= "bold #b8bb26")



def data_base_reader_no_print():
    with open("data_base.json", "r", encoding="utf-8") as file:
        data_base = json.load(file)
        return(data_base)





def main_menu():
    show_menu_box = True
    while True:
        
        db = data_base_reader_no_print()
        
        if show_menu_box:
            console.clear()
            console.print(menu_table)


        show_menu_box = False
        choice = console.input("[bold #fabd2f]Choose an option (1-6) or type 'm' to show menu or clear to clear terminal: [/]").strip().lower()
        
        match choice:
            case "m":
                show_menu_box = True
                continue
        
            
            case "clear":
                console.clear()
                continue



            case "1":
                if not db:
                    console.print("\n[bold red]Your database is empty! Please add a city first (Option 2)[/bold red].")
                else:
                    selected_city = choose_an_option()
                    lat = db[selected_city]["latitude"]
                    lon = db[selected_city]["longitude"]
                    data, city = get_weather(selected_city, lat, lon)
                    if data:
                        
                        table_to_print = get_forecasts_by_type(data, city, choice)
                        console.print(table_to_print)


            case "2":
                console.print("\n\n[bold #fabd2f]Adding a New City[/]")
                add_city(search_for_city())

            case "3":
                if not db:
                    print("\nYour database is empty!")
                else:
                    console.print(saves_cities_and_coords())

            case "4":
                choice_table = Table(
                title=f"[bold #fabd2f]Types of forecast displays I can code[/bold #fabd2f]", 
                box=box.ROUNDED,
                show_header=False,  
                border_style="#928374"
                )
                choice_table.add_row("Short(just current time)", style= "bold #b8bb26")
                choice_table.add_row("Default(this moment, few upcoming hours and short about tomorrow)", style= "bold #b8bb26")
                choice_table.add_row("Deatiled(the next 24 hours)", style= "bold #b8bb26")
                
                choice = console.input("bold #fabd2f]Enter a number(1-3)[/]")

                match choice:
                    case "1":
                        pass




            case "5":
                print("\n[WIP] The coordinate explainer is coming tomorrow!")

            case "6":
                console.print("\n[bold #fabd2f]Thank you for using CLI-Mate, Mate! Goodbye![/]")
                break

            case _:
                console.print("\n[bold red]Invalid choice,[/] [bold #b8bb26]please enter a number from 1 to 6.[/]")






def get_weather_category(description):
    desc = description.lower()
    if "thunder" in desc or "storm" in desc:
        return "storm"
    elif "snow" in desc or "ice" in desc or "hail" in desc:
        return "snowy"
    elif "sleet" in desc or "freezing" in desc:
        return "sleet"
    elif "rain" in desc or "drizzle" in desc or "shower" in desc:
        return "rainy"
    elif "fog" in desc or "mist" in desc or "haze" in desc:
        return "foggy"
    elif "cloud" in desc or "overcast" in desc:
        return "cloudy"
    elif "wind" in desc or "blizzard" in desc:
        return "windy"
    else:
        return "sunny"  # default




def get_forecasts_by_type(data, city_name,choice):
    current_hour = datetime.now().hour
    upcoming = []

    match choice:
        
        
        case "default":
    
            for item in data["weather"][0]["hourly"]:
                hour_val = int(item["time"]) // 100  
                if hour_val > current_hour:
                    upcoming.append({
                        "day": "Today",
                        "time": f"{hour_val:02d}:00",
                        "temp": item["temp_C"],
                        "desc": item["weatherDesc"][0]["value"]
                    })

            if len(upcoming) < 2:
                for item in data["weather"][1]["hourly"]:
                    hour_val = int(item["time"]) // 100
                    upcoming.append({
                        "day": "Tomorrow",
                        "time": f"{hour_val:02d}:00",
                        "temp": item["temp_C"],
                        "desc": item["weatherDesc"][0]["value"]
                    })
                    if len(upcoming) >= 2:
                        break


            return upcoming[:2]
        

        case "short":
                current_temp = data["current_condition"][0]["temp_C"]
                current_weather_description = data["current_condition"][0]["weatherDesc"][0]["value"]

                
                
                random_art = random.choice(weather_arts[get_weather_category(current_weather_description)])


                weather_table = Table(
                title=f"[bold #fabd2f]Current weather in {city_name}[/bold #fabd2f]", 
                box=box.ROUNDED,
                show_header=False,  
                border_style="#928374"
                )
        
                weather_table.add_column("Art", justify="center", vertical="middle")
                weather_table.add_column("Info", justify="left", vertical="middle")
                
                


                left_column = f"[bold #b8bb26]The weather is {current_weather_description}\n\n{random_art}[/]"
                right_column = f"[bold #928374]It is [/] [bold #fe8019]{current_temp}[/][bold #83a598]°C[/] in [bold #fabd2f]{city_name}[/]"
                
                weather_table.add_row(left_column, right_column)
                
                return weather_table
        

        




        case "detailed":
            for item in data["weather"][0]["hourly"]:
                hour_val = int(item["time"]) // 100  
                if hour_val > current_hour:
                    upcoming.append({
                        "day": "Today",
                        "time": f"{hour_val:02d}:00",
                        "temp": item["temp_C"],
                        "desc": item["weatherDesc"][0]["value"]
                    })
            for item in data["weather"][1]["hourly"]:
                hour_val = int(item["time"])//100
                upcoming.append({
                    "day": "Tomorrow",
                    "time": f"{hour_val:02d}:00",
                    "temp": item["temp_C"],
                    "desc": item["weatherDesc"][0]["value"]
                    })
                if len(upcoming) == 8:
                    break
            return upcoming

















def saves_cities_and_coords():
        current_db = data_base_reader_no_print()
        
        saved_cities_table = Table(
        title="[bold #fabd2f]Saved Cities and Coordinates[/bold #fabd2f]", 
        box=box.ROUNDED,
        show_header=False,
        border_style="#928374"
        )
        for city_name, coords in current_db.items():
            saved_cities_table.add_row(f" [bold #fabd2f]{city_name}[/] ([bold #b8bb26]{coords['Country']}[/]) — [bold #928374]Latitude:[/] [bold #fe8019]{coords['latitude']}[/], [bold #928374]Longitude:[/] [bold #83a598]{coords['longitude']}[/]")

        return saved_cities_table




def greeting():
    console.print("[bold #fabd2f]Hello, this is a CLI forecast program, or CLI-Mate[/]")
    length = len(data_base_reader_no_print())
    if length < 1:
        add_city(search_for_city())
        time.sleep(1.1)

    else:
        console.print("[bold #928374]Choose a forecast display type[/]\n\n\n")
        time.sleep(0.5)

    
    choice_table = Table(
    title=f"[bold #fabd2f]Types of forecast displays[/bold #fabd2f]", 
    box=box.ROUNDED,
    show_header=False,  
    border_style="#928374"
    )
    choice_table.add_row("1. Short(just current time)", style= "bold #b8bb26")
    choice_table.add_row("2. Default(this moment, few upcoming hours and short about tomorrow)", style= "bold #b8bb26")
    choice_table.add_row("3. Detailed(the next 24 hours)", style= "bold #b8bb26")
    console.print(choice_table)

    working = True

    global display_mode
    
    
    while working:
        choice = console.input("[bold #fabd2f]Enter a number(1-3)[/]")
        #validation of choice
        match choice:
            case "1":
                choice = "short"
                working = False
            case "2":
                choice = "default"
                working = False

            case "3":
                choice = "detailed"
                working = False
            case _:
                continue

        
        
        
        #console.print("[bold #928374]Redirecting to main menu[/]\n\n\n")
        #time.sleep(0.5)




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

    url = "https://geocoding-api.open-meteo.com/v1/search"
    working = True
    
    while working:
        try:
            
            city = console.input("[bold #b8bb26]Enter your city's name: [/]")
            
            payload = {
                "name": city 
                }   
            response = requests.get(url,params = payload)
            data = response.json()
            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]
            country = data["results"][0]["country"]
            name = data["results"][0]["name"]

            console.print(f"[bold #928374]City:[/][bold #fabd2f]{name}[/], [bold #928374]Country:[/][bold #b8bb26]{country}[/]", highlight= False)
            console.print(f"[bold #928374]Latitude:[/][bold #fe8019]{latitude}[/], [bold #928374]Longitude:[/][bold #83a598]{longitude}[/]\n",highlight= False)
            console.rule(style="bold #928374")
            dict = {
                "City": name, "Country": country, "latitude": latitude, "longitude": longitude
            }
            return dict
        except Exception :
            console.print(f"[bold red]Error,[/][bold #b8bb26]Try to write the name differently[/]")
            continue






db = data_base_reader_no_print()

cities_list = list(db.keys())

def choose_an_option():
    current_db = data_base_reader_no_print()
    current_list = list(current_db.keys())
    
    if len(current_list) == 1:
        selected_city = current_list[0]
        return selected_city
    
    
    saved_cities_table = Table(
        title="[bold #fabd2f]Saved Cities[/]",
        box = box.ROUNDED,
        border_style="#928374",
        show_header= False
    )
    
    for index, city_name in enumerate(current_list, 1):
        saved_cities_table.add_row(f"{index}. [bold yellow]{city_name}[/]")
    console.print(saved_cities_table)
    console.rule(style="bold #928374")
    choice = int(console.input("[bold #b8bb26]Choose the number of the saved city to see weather: [/]"))
    selected_city = current_list[choice - 1]
    return selected_city





def get_weather_backup(backup_url, backup_parameters, city_name):
    
    backup_weather_table = Table(
    title="[bold #fabd2f]Current weather[/bold #fabd2f]", 
    box=box.ROUNDED,
    show_header=False,
    border_style="#928374"
    )
    
    try:

        response = requests.get(backup_url, backup_parameters)

        if response.status_code == 200:
            console.print("[bold #b8bb26]\nRequest to open meteo: success[/]")
            data = response.json()
        
            current_temp = data["current_weather"]["temperature"]

            backup_weather_table.add_row(f"[bold #928374]Current temperature in [/][bold #fabd2f]{city_name}[/] [bold #928374]is[/] [bold #fe8019]{current_temp}[/][bold #83a598]°C[/]")
            console.print(backup_weather_table)
            
   
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


def print_weather(data, city_name):
    pass















####  Main weather getting function

def get_weather(city_name, lat, lon):
    try:
        
        weather_table = Table(
        title="[bold #fabd2f]Current weather[/bold #fabd2f]", 
        box=box.ROUNDED,
        show_header=False,
        border_style="#928374"
        )
        
        
        
        
        
        
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
            console.print("[bold #b8bb26]\nRequest to wttr.in: success[/]")
            data = response.json()
        
            #current_temp = data["current_condition"][0]["temp_C"]
            #current_weather_description = data["current_condition"][0]["weatherDesc"][0]["value"]

            #weather_table.add_row(f"[bold #928374]Current temperature in [/][bold #fabd2f]{city_name}[/] [bold #928374]is[/] [bold #fe8019]{current_temp}[/][bold #83a598]°C[/]")
            #weather_table.add_row(f"[bold #928374]The weather is [/][bold #b8bb26]{current_weather_description}[/]")
            #console.print(weather_table)
            return data, city_name
        
        
   
        else:
            print(f"Request error: {response.status_code}")
            print("Attempting backup website")
            get_weather_backup(backup_url, backup_parameters, city_name)
            
            print("HTTP Status Code Guide:")
            print("200-299  Success! Everything worked perfectly.") 
            print("300-399  Redirect. The page moved somewhere else.")
            print("400-499  Client Error. The problem is on YOUR side, and it's not about the programm, I(da developer) am precise.")
            print("500-599  Server Error. The problem is on THEIR side (the website/API is broken).")
            
            
    except:
        print("Something went wrong, idk what")

