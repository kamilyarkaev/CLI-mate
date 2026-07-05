import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
import time
from datetime import datetime
from Ascii_arts import weather_arts
import random

global emojis_dict




DAY_EMOJIS = {
    "sunny": "☀️",
    "cloudy": "🌤️",
    "foggy": "🌫️",
    "rainy": "🌧️",
    "snowy": "🌨️",
    "sleet": "❄️",
    "storm": "⛈️",
    "windy": "💨"
}

NIGHT_EMOJIS = {
    "sunny": "🌙",     
    "cloudy": "☁️",      
    "foggy": "🌫️",
    "rainy": "🌧️",
    "snowy": "🌨️",
    "sleet": "❄️",
    "storm": "⛈️",
    "windy": "💨"
}







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
menu_table.add_row("  4. Change forecast display settings", style= "bold #b8bb26")
menu_table.add_row("  5. Why does this app use coordinates? (WIP)", style= "bold #b8bb26")
menu_table.add_row("  6. Exit", style= "bold #b8bb26")



def data_base_reader_no_print():
    with open("data_base.json", "r", encoding="utf-8") as file:
        data_base = json.load(file)
        return(data_base)


display_mode = "default"





def determine_time_day_or_night(time):
    pass









def main_menu():
    global display_mode
    
    
    show_menu_box = True
    while True:
        
        db = data_base_reader_no_print()
        
        if show_menu_box:
            console.clear()
            console.print(menu_table)


        show_menu_box = False
        time.sleep(0.5)
        choice = console.input("[bold #fabd2f]You are in menu, choose an option (1-6) or type 'm' to show menu or clear to clear: [/]").strip().lower()
        
        match choice:
            
            case "exit" | "6":
                console.print("\n[bold #fabd2f]Thank you for using CLI-Mate, Mate! Goodbye![/]")
                break
            
            
            
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
                        
                        table_to_print = get_forecasts_by_type(data, city, display_mode)
                        console.print(table_to_print)


            case "2":
                console.print("\n\n[bold #fabd2f]Adding a New City[/]")
                new_city = search_for_city()

                if new_city:
                    add_city(new_city)
                    console.print("[bold #b8bb26]City successfully added![/]")

            case "3":
                if not db:
                    print("\nYour database is empty!")
                else:
                    console.print(saves_cities_and_coords())

            case "4":
                global choice_table
                
                choice_table = Table(
                title=f"[bold #fabd2f]Types of forecast displays,[/] [bold #b8bb26]current: {display_mode}[/]", 
                box=box.ROUNDED,
                show_header=False,  
                border_style="#928374"
                )
                choice_table.add_row("1. Short(just current time)", style= "bold #b8bb26")
                choice_table.add_row("2. Default(this moment, few upcoming hours and short about tomorrow)", style= "bold #b8bb26")
                choice_table.add_row("3. Deatiled(the next 42 hours)", style= "bold #b8bb26")
                
                console.print(choice_table)
                

                
                display_mode_choice = True
                while display_mode_choice:
                    choice = console.input("[bold #fabd2f]Enter a number(1-3) or e to leave: [/]").strip().lower()
                    
                    match choice:
                        case "e":
                            break
                        
                        
                        case "1" | "short":
                            display_mode = "short"
                            display_mode_choice = False
                            console.print("[bold #b8bb26]Set to short[/]")


                        
                        
                        case "2" | "default":
                            display_mode = "default"
                            display_mode_choice = False
                            console.print("[bold #b8bb26]Set to default[/]")                    
                        
                        
                        
                        case "3" | "detailed":
                            display_mode = "detailed" 
                            display_mode_choice = False
                            console.print("[bold #b8bb26]Set to detailed[/]")                        
                        case _:
                            console.print(f"[bold red]Enter a number (1-3)[/]")


                    



            case "5":
                print("\n[WIP] The coordinate explainer is coming tomorrow!")



            case _:
                console.print("\n[bold red]Invalid choice,[/] [bold #b8bb26]please enter a number from 1 to 6.[/]")
                time.sleep(0.5)






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
        return "sunny"  # this is default





def determine_time_day_or_night(data, time):
    
    time_list = time.split(":")
    hour, minutes = tuple(time_list)
    forecast_minutes = int(hour)*60 + int(minutes)
    
    global today_sunrise_mins, today_sunset_mins, tomorrow_sunrise_mins, tomorrow_sunset_mins, tomorrow_sunset_true_time, tomorrow_sunrise_true_time, today_sunrise_true_time, today_sunset_true_time

    sunrise_hours, sunrise_minutes = tuple(data["weather"][0]["astronomy"][0]["sunrise"].split()[0].split(":"))
    sunset_hours, sunset_minutes = tuple(data["weather"][0]["astronomy"][0]["sunset"].split()[0].split(":"))

    today_sunset_mins = int(sunset_hours)*60 + int(sunset_minutes) + 720
    today_sunrise_mins = int(sunrise_hours)*60 + int(sunrise_minutes)
    
    tomorrow_sunrise_hours, tomorrow_sunrise_minutes = tuple(data["weather"][1]["astronomy"][0]["sunrise"].split()[0].split(":"))
    tomorrow_sunset_hours, tomorrow_sunset_minutes = tuple(data["weather"][1]["astronomy"][0]["sunset"].split()[0].split(":"))

    tomorrow_sunset_mins = int(tomorrow_sunset_hours)*60 + int(tomorrow_sunset_minutes) + 720 + 1440
    tomorrow_sunrise_mins = int(tomorrow_sunrise_hours)*60 + int(tomorrow_sunrise_minutes) + 1440
    tomorrow_sunset_true_time = f"{int(tomorrow_sunset_hours) + 12:02d}:{int(tomorrow_sunset_minutes):02d}"
    tomorrow_sunrise_true_time = f"{int(tomorrow_sunrise_hours):02d}:{int(tomorrow_sunrise_minutes):02d}"
    today_sunset_true_time = f"{int(sunset_hours) + 12:02d}:{int(sunset_minutes):02d}"
    today_sunrise_true_time = f"{int(sunrise_hours):02d}:{int(sunrise_minutes):02d}"
    
    
    is_night = (forecast_minutes < today_sunrise_mins) or (forecast_minutes > today_sunset_mins)
    
    
    emojis_dict = NIGHT_EMOJIS if is_night else DAY_EMOJIS

    return emojis_dict
    









def get_forecasts_by_type(data, city_name,choice):
    current_hour = datetime.now().hour
    upcoming = []
    current_time = datetime.now().strftime("%H:%M")
    
    emojis_dict = determine_time_day_or_night(data, current_time)




    match choice:
        
        
        
        
        
        case "default":
            current_time = datetime.now().strftime("%H:%M")
            
            
            for item in data["weather"][0]["hourly"]:
                hour_val = int(item["time"]) // 100  
                if hour_val > current_hour:
                    upcoming.append({
                        "day": "Today",
                        "time": f"{hour_val:02d}:00",
                        "temp": item["tempC"],
                        "desc": item["weatherDesc"][0]["value"],
                        "minutes": hour_val * 60,
                        "type": "forecast"
                    })
            for item in data["weather"][1]["hourly"]:
                hour_val = int(item["time"])//100
                upcoming.append({
                    "day": "Tomorrow",
                    "time": f"{hour_val:02d}:00",
                    "temp": item["tempC"],
                    "desc": item["weatherDesc"][0]["value"],
                    "minutes": hour_val * 60 + 1440,
                    "type": "forecast"
                    })
                if len(upcoming) == 5:
                    break
            
            events_list = []
            

            midday_forecast= data["weather"][1]["hourly"][4]


            events_list.append({
             "day": "Tomorrow",
             "time": "12:00", 
             "temp": midday_forecast["tempC"],
             "desc": midday_forecast["weatherDesc"][0]["value"],
             "minutes": 720 + 1440,
             "type": "forecast"
            })
            
            

            for x in upcoming:
                events_list.append(x)


            current_hour, current_minutes = tuple(current_time.split(":"))
            now_minutes = int(current_hour) * 60 + int(current_minutes)

            events_list.append({
                    "day": "Today",
                    "time": current_time,
                    "temp": None,
                    "desc": None,
                    "minutes": now_minutes,
                    "type": "current_moment",
                    })
            
            
            
            events_list.sort(key= lambda x: x["minutes"])
            earliest_moment = events_list[0]["minutes"]
            latest_moment = events_list[-1]["minutes"]
            if earliest_moment < today_sunrise_mins and latest_moment > today_sunrise_mins:
                events_list.append({
                    "day": "Today",
                    "time": today_sunrise_true_time,
                    "temp": None,
                    "desc": "sunrise",
                    "minutes": today_sunrise_mins,
                    "type": "sunrise",

                    })
            if earliest_moment < today_sunset_mins and latest_moment > today_sunset_mins:
                events_list.append({
                    "day": "Today",
                    "time": today_sunset_true_time,
                    "temp": None,
                    "desc": "sunset",
                    "minutes": today_sunset_mins,
                    "type": "sunset",

                    })
            if earliest_moment < tomorrow_sunrise_mins and latest_moment > tomorrow_sunrise_mins:
                events_list.append({
                    "day": "Tomorrow",
                    "time": tomorrow_sunrise_true_time,
                    "temp": None,
                    "desc": "sunrise",
                    "minutes": tomorrow_sunrise_mins,
                    "type": "sunrise",

                    })
            if earliest_moment < tomorrow_sunset_mins and latest_moment > tomorrow_sunset_mins:
                events_list.append({
                    "day": "Tomorrow",
                    "time": tomorrow_sunset_true_time,
                    "temp": None,
                    "desc": "sunset",
                    "minutes": tomorrow_sunset_mins,
                    "type": "sunset",

                    })
            events_list.sort(key= lambda x: x["minutes"])



            


            
            
            
            
            default_forecast_table = Table(
            title=f"[bold #fabd2f]Upcoming weather in {city_name}[/bold #fabd2f]", 
            box=box.ROUNDED,
            show_header=False,
            border_style="#928374"
            )
            default_forecast_table.add_column("Day", justify= "left", style="#a89984")
            default_forecast_table.add_column("Time", justify= "center", style="#fabd2f")
            default_forecast_table.add_column("Weather", justify= "right", style="#b8bb26")

            upcoming_weather_dict_list_default = upcoming

            
            current_time = datetime.now().strftime("%H:%M")
            current_temp = data["current_condition"][0]["temp_C"]
            current_desc = data["current_condition"][0]["weatherDesc"][0]["value"]
            current_emoji = emojis_dict[get_weather_category(current_desc)]

            default_forecast_table.add_row("Now",current_time,f"{current_desc},{current_emoji}, {current_temp}°C" )
            
            
            
            
            for x in events_list:
                
                
                if x["type"] == "current_moment":
                    continue
                
                
                if x["type"] == "forecast": 
                    emojis_dict = determine_time_day_or_night(data, x["time"])
                    emoji = emojis_dict[get_weather_category(x["desc"])]
                
                
                    default_forecast_table.add_row(
                        x["day"], 
                        x["time"], 
                        f"""{x["desc"]}, {emoji}, {x["temp"]}°C""") 
                    
                if x["type"] == "sunrise":
                    default_forecast_table.add_row(
                        x["day"], 
                        x["time"], 
                        f"""[bold #fabd2f]Sunrise[/], 🌅""")
                    
                if x["type"] == "sunset":
                    default_forecast_table.add_row(
                        x["day"], 
                        x["time"], 
                        f"""[bold #fe8019]Sunset[/], 🌇""")
                

            
            
            
            
            return default_forecast_table            
            
            






        
        
        case "short":
                
                current_time = datetime.now().strftime("%H:%M")
                
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
            current_time = datetime.now().strftime("%H:%M")
            
            
            for item in data["weather"][0]["hourly"]:
                hour_val = int(item["time"]) // 100  
                if hour_val > current_hour:
                    upcoming.append({
                        "day": "Today",
                        "time": f"{hour_val:02d}:00",
                        "temp": item["tempC"],
                        "desc": item["weatherDesc"][0]["value"],
                        "minutes": hour_val * 60,
                        "type": "forecast"
                    })
            for item in data["weather"][1]["hourly"]:
                hour_val = int(item["time"])//100
                upcoming.append({
                    "day": "Tomorrow",
                    "time": f"{hour_val:02d}:00",
                    "temp": item["tempC"],
                    "desc": item["weatherDesc"][0]["value"],
                    "minutes": hour_val * 60 + 1440,
                    "type": "forecast"
                    })
            
            for item in data["weather"][2]["hourly"]:
                hour_val = int(item["time"])//100
                upcoming.append({
                    "day": "Day after tomorrow",
                    "time": f"{hour_val:02d}:00",
                    "temp": item["tempC"],
                    "desc": item["weatherDesc"][0]["value"],
                    "minutes": hour_val * 60 + 2880,
                    "type": "forecast"
                    })    
            
                if len(upcoming) == 14:
                    break
            
            
            
            events_list = []
            for x in upcoming:
                events_list.append(x)


            current_hour, current_minutes = tuple(current_time.split(":"))
            now_minutes = int(current_hour) * 60 + int(current_minutes)

            events_list.append({
                    "day": "Today",
                    "time": current_time,
                    "temp": None,
                    "desc": None,
                    "minutes": now_minutes,
                    "type": "current_moment",
                    })
            
            
            
            events_list.sort(key= lambda x: x["minutes"])
            earliest_moment = events_list[0]["minutes"]
            latest_moment = events_list[-1]["minutes"]
            if earliest_moment < today_sunrise_mins and latest_moment > today_sunrise_mins:
                events_list.append({
                    "day": "Today",
                    "time": today_sunrise_true_time,
                    "temp": None,
                    "desc": "sunrise",
                    "minutes": today_sunrise_mins,
                    "type": "sunrise",

                    })
            if earliest_moment < today_sunset_mins and latest_moment > today_sunset_mins:
                events_list.append({
                    "day": "Today",
                    "time": today_sunset_true_time,
                    "temp": None,
                    "desc": "sunset",
                    "minutes": today_sunset_mins,
                    "type": "sunset",

                    })
            if earliest_moment < tomorrow_sunrise_mins and latest_moment > tomorrow_sunrise_mins:
                events_list.append({
                    "day": "Tomorrow",
                    "time": tomorrow_sunrise_true_time,
                    "temp": None,
                    "desc": "sunrise",
                    "minutes": tomorrow_sunrise_mins,
                    "type": "sunrise",

                    })
            if earliest_moment < tomorrow_sunset_mins and latest_moment > tomorrow_sunset_mins:
                events_list.append({
                    "day": "Tomorrow",
                    "time": tomorrow_sunset_true_time,
                    "temp": None,
                    "desc": "sunset",
                    "minutes": tomorrow_sunset_mins,
                    "type": "sunset",

                    })
            events_list.sort(key= lambda x: x["minutes"])



            


            
            
            
            
            detailed_forecast_table = Table(
            title=f"[bold #fabd2f]Upcoming weather in {city_name}[/bold #fabd2f]", 
            box=box.ROUNDED,
            show_header=False,
            border_style="#928374"
            )
            detailed_forecast_table.add_column("Day", justify= "left", style="#a89984")
            detailed_forecast_table.add_column("Time", justify= "center", style="#fabd2f")
            detailed_forecast_table.add_column("Weather", justify= "right", style="#b8bb26")

            upcoming_weather_dict_list_detailed = upcoming

            
            current_time = datetime.now().strftime("%H:%M")
            current_temp = data["current_condition"][0]["temp_C"]
            current_desc = data["current_condition"][0]["weatherDesc"][0]["value"]
            current_emoji = emojis_dict[get_weather_category(current_desc)]

            detailed_forecast_table.add_row("Now",current_time,f"{current_desc},{current_emoji}, {current_temp}°C" )
            
            
            
            
            for x in events_list:
                
                
                if x["type"] == "current_moment":
                    continue
                
                
                if x["type"] == "forecast": 
                    emojis_dict = determine_time_day_or_night(data, x["time"])
                    emoji = emojis_dict[get_weather_category(x["desc"])]
                
                
                    detailed_forecast_table.add_row(
                        x["day"], 
                        x["time"], 
                        f"""{x["desc"]}, {emoji}, {x["temp"]}°C""") 
                    
                if x["type"] == "sunrise":
                    detailed_forecast_table.add_row(
                        x["day"], 
                        x["time"], 
                        f"""[bold #fabd2f]Sunrise[/], 🌅""")
                    
                if x["type"] == "sunset":
                    detailed_forecast_table.add_row(
                        x["day"], 
                        x["time"], 
                        f"""[bold #fe8019]Sunset[/], 🌇""")
                

            
            
            
            
            return detailed_forecast_table

















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
        
        console.print("[bold #928374]Redirecting to main menu[/]\n\n\n")
        time.sleep(0.5)




def add_city(city):
    
    
        database = data_base_reader_no_print()
        
        
        database[city["City"]] = {
        "Country": city["Country"],
        "latitude": city["latitude"],
        "longitude": city["longitude"]
        }
        
        
        with open("data_base.json", "w", encoding="utf-8") as file:
        
            json.dump(database, file, ensure_ascii=False, indent=4)

        return None


def search_for_city():

    url = "https://geocoding-api.open-meteo.com/v1/search"
    working = True
    work = True
    f = True
    while working:
        try:
            
            while work:
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
                while f:
                    x = console.input(f"[bold #b8bb26]Is this the right place? [Y/n]? (e) to leave: [/]").strip().lower()
                    match x:
                        case "y" | "yes":
                            work = False
                            f = False

                        case "n" | "no":
                            break
                        case "e" | "leave":
                            work = False
                            f = False
                            return None



                    

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

