import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
import time
from datetime import datetime
from Ascii_arts import weather_arts
import random
import os



_cached_db = None
_cached_settings = None
global emojis_dict

config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
settings_dir = os.path.join(config_dir, "climate")
settings_path = os.path.join(settings_dir, "forecast_settings.json") 


data_dir = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
DB_dir = os.path.join(data_dir, "climate")
DB_path = os.path.join(DB_dir, "database.json")

os.makedirs(settings_dir, exist_ok=True) 
os.makedirs(DB_dir, exist_ok=True)


console = Console()



WMO_CODES = {
    0: {"day": "☀️", "night": "🌙", "desc": "Clear"},
    1: {"day": "🌤️", "night": "☁️", "desc": "Sunny"},
    2: {"day": "⛅", "night": "☁️", "desc": "Partly"},
    3: {"day": "☁️", "night": "☁️", "desc": "Cloudy"},
    45: {"day": "🌫️", "night": "🌫️", "desc": "Fog"},
    48: {"day": "🌫️", "night": "🌫️", "desc": "Fog"},
    51: {"day": "🌧️", "night": "🌧️", "desc": "Drizzle"},
    53: {"day": "🌧️", "night": "🌧️", "desc": "Drizzle"},
    55: {"day": "🌧️", "night": "🌧️", "desc": "Drizzle"},
    56: {"day": "🌨️", "night": "🌨️", "desc": "Sleet"},
    57: {"day": "🌨️", "night": "🌨️", "desc": "Sleet"},
    61: {"day": "🌦️", "night": "🌧️", "desc": "Rain"},
    63: {"day": "🌧️", "night": "🌧️", "desc": "Rain"},
    65: {"day": "🌧️", "night": "🌧️", "desc": "Rain"},
    66: {"day": "🌨️", "night": "🌨️", "desc": "Sleet"},
    67: {"day": "🌨️", "night": "🌨️", "desc": "Sleet"},
    71: {"day": "🌨️", "night": "🌨️", "desc": "Snow"},
    73: {"day": "🌨️", "night": "🌨️", "desc": "Snow"},
    75: {"day": "🌨️", "night": "🌨️", "desc": "Snow"},
    77: {"day": "🌨️", "night": "🌨️", "desc": "Snow"},
    80: {"day": "🌦️", "night": "🌧️", "desc": "Showers"},
    81: {"day": "🌧️", "night": "🌧️", "desc": "Showers"},
    82: {"day": "⛈️", "night": "⛈️", "desc": "Storm"},
    85: {"day": "🌨️", "night": "🌨️", "desc": "Snow"},
    86: {"day": "🌨️", "night": "🌨️", "desc": "Snow"},
    95: {"day": "⛈️", "night": "⛈️", "desc": "Storm"},
    96: {"day": "⛈️", "night": "⛈️", "desc": "Storm"},
    99: {"day": "⛈️", "night": "⛈️", "desc": "Storm"}
}


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






menu_table = Table(
    title="[bold #fabd2f]CLI-Mate Menu[/bold #fabd2f]", 
    box=box.ROUNDED,
    show_header=False,
    border_style="#928374"
)
menu_table.add_row("  1. Get weather for a saved city", style= "bold #b8bb26")
menu_table.add_row("  2. Add a new city", style= "bold #b8bb26")
menu_table.add_row("  3. View or delete saved cities and coordinates", style= "bold #b8bb26")
menu_table.add_row("  4. Change forecast display settings", style= "bold #b8bb26")
menu_table.add_row("  5. Change daily(whole week) forecast parameters", style= "bold #b8bb26 ")
menu_table.add_row("  6. Why does this app use coordinates?", style= "bold #b8bb26")
menu_table.add_row("  7. Exit", style= "bold #b8bb26")


def validate(file_option, data):
    if file_option == "database":
        if not isinstance(data, dict):
            return {}
        
        valid_db = {}
        for city, info in data.items():
            if isinstance(info, dict) and "Country" in info and "latitude" in info and "longitude" in info:
                try:
                    float(info["latitude"])
                    float(info["longitude"])
                    valid_db[city] = info
                except (ValueError, TypeError):
                    continue
        return valid_db
        
    elif file_option == "daily_settings":
        default_settings = {
            "display_mode": "default",
            "daily_display": {
                "Weather_desc": True,
                "Emoji": True,
                "Max_apparent_temp": True,
                "UV_index": True,
                "Rain_chance": True,
                "Sunrise": True,
                "Sunset": True
            }
        }
        
        if not isinstance(data, dict):
            return default_settings
            
        valid_settings_dict = {}
        try:
            allowed_modes = ["default", "detailed", "short", "daily"]
            mode = data.get("display_mode")
            valid_settings_dict["display_mode"] = mode if mode in allowed_modes else "default"

            valid_settings_dict["daily_display"] = {}
            
            user_display = data.get("daily_display", {})
            if not isinstance(user_display, dict):
                user_display = {}

            settings_keys = ["Weather_desc", "Emoji", "Max_apparent_temp", "UV_index", "Rain_chance", "Sunrise", "Sunset"]
            
            for key in settings_keys:
                val = user_display.get(key)
                
                if isinstance(val, bool):
                    valid_settings_dict["daily_display"][key] = val
                else:
                    valid_settings_dict["daily_display"][key] = True
                    
            return valid_settings_dict
            
        except Exception: 
            return default_settings

def data_base_reader_no_print():
    global _cached_db
    
    if _cached_db is None:
        if not os.path.exists(DB_path):
            with open(DB_path, "w", encoding="utf-8") as file:
                json.dump({}, file)
            
        try:
            with open(DB_path, "r", encoding="utf-8") as file:
                data_base = json.load(file)
            _cached_db = validate("database", data_base)
        except (json.JSONDecodeError, TypeError, OSError):
            with open(DB_path, "w", encoding="utf-8") as file:
                json.dump({}, file)
            _cached_db = {}
            
    return _cached_db


def data_base_reader_no_print_settings():
    global _cached_settings
    
    if _cached_settings is None:
        Default_settings = {
            "display_mode": "default",
            "daily_display": {
                "Weather_desc": True,
                "Emoji": True,
                "Max_apparent_temp": True,
                "UV_index": True,
                "Rain_chance": True,
                "Sunrise": True,
                "Sunset": True
            }
        }
        
        if not os.path.exists(settings_path):
            with open(settings_path, "w", encoding="utf-8") as file:
                json.dump(Default_settings, file, ensure_ascii=False, indent=4)
            
        try:
            with open(settings_path, "r", encoding="utf-8") as file:
                data_base = json.load(file)
                
            validated_settings = validate("daily_settings", data_base)
            
            if validated_settings != data_base:
                with open(settings_path, "w", encoding="utf-8") as file:
                    json.dump(validated_settings, file, ensure_ascii=False, indent=4)
                    
            _cached_settings = validated_settings
        except (json.JSONDecodeError, TypeError, OSError):
            with open(settings_path, "w", encoding="utf-8") as file:
                json.dump(Default_settings, file, ensure_ascii=False, indent=4)
            _cached_settings = Default_settings

    return _cached_settings

def data_base_reader_no_print_display_mode():
    settings = data_base_reader_no_print_settings()
    return settings.get("display_mode", "default")




def get_initial_display_mode():
    try:
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as file:
                return json.load(file).get("display_mode", "default")
    except Exception:
        pass
    return "default"

display_mode = get_initial_display_mode()




def main_menu():
    global display_mode
    
    if do_a_break == True:
        console.print("\n[bold #fabd2f]Thank you for using CLI-Mate, Mate! Goodbye![/]")
        return None
    
    else:
        show_menu_box = True
        while True:
            
            db = data_base_reader_no_print()
            
            if show_menu_box:
                console.clear()
                console.print(menu_table)


            show_menu_box = False
            choice = console.input("[bold #fabd2f]You are in menu, choose an option (1-6) or type 'm' to show menu or clear to clear: [/]").strip().lower()
            
            match choice:
                
                case "exit" | "7" | "e" | "leave" | "x":
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
                        weather_request_results = tuple(get_weather(selected_city, lat, lon))
                        if weather_request_results:
                            data, city = weather_request_results
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
                        console.print("\n[bold red]Your database is empty![/]")
                    else:
                        view_or_delete_saved_cities_and_coords()

                case "4":
                    global choice_table
                    
                    display_mode = data_base_reader_no_print_display_mode()
                    choice_table = Table(
                    title=f"[bold #fabd2f]Types of forecast displays,[/] [bold #b8bb26]current: {display_mode}[/]", 
                    box=box.ROUNDED,
                    show_header=False,  
                    border_style="#928374"
                    )
                    choice_table.add_row("1. Short(just current time)", style= "bold #b8bb26")
                    choice_table.add_row("2. Default(this moment, few upcoming hours and short about tomorrow)", style= "bold #b8bb26")
                    choice_table.add_row("3. Deatiled(the next 42 hours)", style= "bold #b8bb26")
                    choice_table.add_row("4. Daily(for the whole week)", style= "bold #b8bb26")
                    
                    console.print(choice_table)
                    

                    
                    display_mode_choice = True
                    while display_mode_choice:
                        choice = console.input("[bold #fabd2f]Enter a number(1-3) or e to leave: [/]").strip().lower()
                        
                        match choice:
                            case "e":
                                break
                            
                            
                            case "1" | "short":
                                display_mode = "short"
                                database = data_base_reader_no_print_settings()
                                database["display_mode"] = display_mode
                                with open(settings_path, "w", encoding="utf-8") as file:
        
                                    json.dump(database, file, ensure_ascii=False, indent=4)
                                display_mode_choice = False
                                console.print("[bold #b8bb26]Set to short[/]")


                            
                            
                            case "2" | "default":
                                display_mode = "default"
                                database = data_base_reader_no_print_settings()
                                database["display_mode"] = display_mode
                                with open(settings_path, "w", encoding="utf-8") as file:
        
                                    json.dump(database, file, ensure_ascii=False, indent=4)
                                display_mode_choice = False
                                
                                
                                display_mode_choice = False
                                console.print("[bold #b8bb26]Set to default[/]")                    
                            
                            
                            
                            case "3" | "detailed":
                                display_mode = "detailed" 
                                database = data_base_reader_no_print_settings()
                                database["display_mode"] = display_mode
                                with open(settings_path, "w", encoding="utf-8") as file:
        
                                    json.dump(database, file, ensure_ascii=False, indent=4)
                                display_mode_choice = False
                                console.print("[bold #b8bb26]Set to detailed[/]")                        
                            
                            case "4" | "Daily":
                                display_mode = "daily"
                                database = data_base_reader_no_print_settings()
                                database["display_mode"] = display_mode
                                with open(settings_path, "w", encoding="utf-8") as file:
        
                                    json.dump(database, file, ensure_ascii=False, indent=4)
                                
                                display_mode_choice = False
                                console.print("[bold #b8bb26]Set to daily[/]")
                            
                            case _:
                                console.print(f"[bold red]Enter a number (1-3)[/]")


                        



                case "6":
                    explain_why_coordinates()



                
                case "5":
                    possible_choices_list = ["e","leave","exit","x","l", "rain","chance", "uv", "index_uv","index","max_temp","max_apparant", "apparant_temp","apparant","temp","emoji","weather_emoji","weatheremoji","weatherdesc","weather", "weather_desc", "max_apparant_temp", "uv_index", "rain_chance","sunrise","sunset"]
                    valid_digits = ["1", "2", "3", "4", "5", "6", "7"]
                    console.print(saved_settings())
                    choosing = True
                    database = data_base_reader_no_print_settings()
                    all_valid = valid_digits + possible_choices_list
                    
                    while choosing:
                        choice = console.input("[bold #fabd2f]Enter the number of the setting you want to change:(or 'e' to leave)[/] ").strip().lower()
                    
                        if choice not in all_valid:
                            console.print("[bold red]Error,[/] [bold #b8bb26]type again[/]")
                            continue

                        match choice:
                            case "1"| "weather"|"weatherdesc"|"weather_desc":
                                database["daily_display"]["Weather_desc"] = not database["daily_display"]["Weather_desc"]
                                status = database["daily_display"]["Weather_desc"]
                                color = "#b8bb26" if status else "red"  
                                console.print(f"[bold #8ec07c]'Weather_desc' set to [/][bold {color}]{status}[/]")
                                
                            case "2"| "emoji"| "weather_emoji"|"weatheremoji":
                                database["daily_display"]["Emoji"] = not database["daily_display"]["Emoji"]
                                status = database["daily_display"]["Emoji"]
                                color = "#b8bb26" if status else "red"
                                console.print(f"[bold #8ec07c]'Emoji' set to [/][bold {color}]{status}[/]")
                                
                            case "3"| "apparant"| "temp"| "apparant_temp"| "max_apparant"| "max_temp"| "max_apparant_temp":
                                database["daily_display"]["Max_apparent_temp"] = not database["daily_display"]["Max_apparent_temp"]
                                status = database["daily_display"]["Max_apparent_temp"]
                                color = "#b8bb26" if status else "red"
                                console.print(f"[bold #8ec07c]'Max_apparent_temp' set to [/][bold {color}]{status}[/]")
                                
                            case "4"| "uv"| "uv_index"| "index_uv"| "index":
                                database["daily_display"]["UV_index"] = not database["daily_display"]["UV_index"]
                                status = database["daily_display"]["UV_index"]
                                color = "#b8bb26" if status else "red"
                                console.print(f"[bold #8ec07c]'UV_index' set to [/][bold {color}]{status}[/]")
                                
                            case "5"| "rain"| "rain_chance"| "chance":
                                database["daily_display"]["Rain_chance"] = not database["daily_display"]["Rain_chance"]
                                status = database["daily_display"]["Rain_chance"]
                                color = "#b8bb26" if status else "red"
                                console.print(f"[bold #8ec07c]'Rain_chance' set to [/][bold {color}]{status}[/]")
                                
                            case "6"| "sunrise":
                                database["daily_display"]["Sunrise"] = not database["daily_display"]["Sunrise"]
                                status = database["daily_display"]["Sunrise"]
                                color = "#b8bb26" if status else "red"
                                console.print(f"[bold #8ec07c]'Sunrise' set to [/][bold {color}]{status}[/]")
                                
                            case "7"| "sunset":
                                database["daily_display"]["Sunset"] = not database["daily_display"]["Sunset"]
                                status = database["daily_display"]["Sunset"]
                                color = "#b8bb26" if status else "red"
                                console.print(f"[bold #8ec07c]'Sunset' set to [/][bold {color}]{status}[/]")
                                
                            case "e"| "leave"|"exit"|"x"|"l":
                                choosing = False
                                break

                    # Код записи теперь стоит ЗДЕСЬ и гарантированно сработает сразу после выхода из цикла настройки
                    with open(settings_path, "w", encoding="utf-8") as file:
                         json.dump(database, file, ensure_ascii=False, indent=4)
                
                
                
                
                
                case _:
                    console.print("\n[bold red]Invalid choice,[/] [bold #b8bb26]please enter a number from 1 to 6.[/]")
                    time.sleep(0.5)





def explain_why_coordinates():
    explanation_text = (
        "\n[bold #fabd2f]Why does CLI-Mate use coordinates?[/]\n\n"
        "[bold #928374]CLI-Mate uses geographic coordinates (Latitude & Longitude) [/]"
        "[bold #928374]for one specific reason:[/]\n\n"
        
        "[bold #fe8019]Backup Weather Provider (Open-Meteo)[/]\n"
        "[bold #928374]Our primary weather source is[/] [bold #b8bb26]wttr.in[/][bold #928374], which we query directly using your city's name.[/] "
        "[bold #928374]However, if [/][bold #b8bb26]wttr.in [/][bold #928374]is down or unresponsive,[/][bold #b8bb26] CLI-Mate [/][bold #928374]automatically switches to our backup[/] "
        "[bold #928374]provider,[/] [bold #fe8019]Open-Meteo[/] [bold #928374](which runs in a simplified, non-colorized mode).[/]\n\n"
        
        "[bold #928374]Unlike[/] [bold #b8bb26]wttr.in[/][bold #928374],[/][bold #fe8019] Open-Meteo [/][bold #928374]cannot[/] [bold #b8bb26]search for weather by city names, it strictly requires[/] "
        "[bold #928374]precise[/][bold #b8bb26] latitude and longitude coordinates[/][bold #928374]. Saving these coordinates in data_base.json[/] "
        "[bold #928374]when you first add a city ensures that our backup weather request works instantly and[/] "
        "[bold #928374]reliably whenever the [/][bold #b8bb26]primary website is unavailable![/]\n"
    )
    console.print(explanation_text)
    console.rule(style="bold #928374")



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
    
    global day_after_tomorrow_sunrise_true_time, day_after_tomorrow_sunset_true_time, day_after_tomorrow_sunrise_mins, day_after_tomorrow_sunset_mins, day_after_tomorrow_sunrise_hours, day_after_tomorrow_sunrise_minutes, day_after_tomorrow_sunset_hours, day_after_tomorrow_sunset_minutes, today_sunrise_mins, today_sunset_mins, tomorrow_sunrise_mins, tomorrow_sunset_mins, tomorrow_sunset_true_time, tomorrow_sunrise_true_time, today_sunrise_true_time, today_sunset_true_time

    sunrise_hours, sunrise_minutes = tuple(data["weather"][0]["astronomy"][0]["sunrise"].split()[0].split(":"))
    sunset_hours, sunset_minutes = tuple(data["weather"][0]["astronomy"][0]["sunset"].split()[0].split(":"))

    
    tomorrow_sunrise_hours, tomorrow_sunrise_minutes = tuple(data["weather"][1]["astronomy"][0]["sunrise"].split()[0].split(":"))
    tomorrow_sunset_hours, tomorrow_sunset_minutes = tuple(data["weather"][1]["astronomy"][0]["sunset"].split()[0].split(":"))

    day_after_tomorrow_sunset_hours, day_after_tomorrow_sunset_minutes  = tuple(data["weather"][2]["astronomy"][0]["sunset"].split()[0].split(":"))
    day_after_tomorrow_sunrise_hours, day_after_tomorrow_sunrise_minutes  = tuple(data["weather"][2]["astronomy"][0]["sunrise"].split()[0].split(":"))
    

    today_sunset_mins = int(sunset_hours)*60 + int(sunset_minutes) + 720
    today_sunrise_mins = int(sunrise_hours)*60 + int(sunrise_minutes)   
    
    tomorrow_sunset_mins = int(tomorrow_sunset_hours)*60 + int(tomorrow_sunset_minutes) + 720 + 1440
    tomorrow_sunrise_mins = int(tomorrow_sunrise_hours)*60 + int(tomorrow_sunrise_minutes) + 1440
    
    tomorrow_sunset_true_time = f"{int(tomorrow_sunset_hours) + 12:02d}:{int(tomorrow_sunset_minutes):02d}"
    tomorrow_sunrise_true_time = f"{int(tomorrow_sunrise_hours):02d}:{int(tomorrow_sunrise_minutes):02d}"
    
    today_sunset_true_time = f"{int(sunset_hours) + 12:02d}:{int(sunset_minutes):02d}"
    today_sunrise_true_time = f"{int(sunrise_hours):02d}:{int(sunrise_minutes):02d}"
    
    day_after_tomorrow_sunset_mins = int(day_after_tomorrow_sunset_hours)*60 + int(day_after_tomorrow_sunset_minutes) + 720 + 2880
    day_after_tomorrow_sunrise_mins = int(day_after_tomorrow_sunrise_hours)*60 + int(day_after_tomorrow_sunrise_minutes) + 2880
    
    day_after_tomorrow_sunrise_true_time = f"{int(day_after_tomorrow_sunrise_hours):02d}:{int(day_after_tomorrow_sunrise_minutes):02d}"
    day_after_tomorrow_sunset_true_time = f"{int(day_after_tomorrow_sunset_hours):02d}:{int(day_after_tomorrow_sunset_minutes):02d}"
   
   
    is_night = (forecast_minutes < today_sunrise_mins) or (forecast_minutes > today_sunset_mins)
    
    
    emojis_dict = NIGHT_EMOJIS if is_night else DAY_EMOJIS

    return emojis_dict
    







def build_openmeteo_timeline(data):

    events = []
    
    for idx in range(len(data["hourly"]["time"])):
        if idx % 3 == 0:
            events.append({
                "type": "forecast",
                "idx": idx,
                "minutes": idx * 60
            })
        
    for d, sunrise_str in enumerate(data["daily"]["sunrise"]):
        if "T" in sunrise_str:
            time_part = sunrise_str.split("T")[1]
            h, m = map(int, time_part.split(":"))
            events.append({
                "type": "sunrise",
                "time": time_part,
                "minutes": d * 1440 + h * 60 + m
            })
            
    for d, sunset_str in enumerate(data["daily"]["sunset"]):
        if "T" in sunset_str:
            time_part = sunset_str.split("T")[1]
            h, m = map(int, time_part.split(":"))
            events.append({
                "type": "sunset",
                "time": time_part,
                "minutes": d * 1440 + h * 60 + m
            })
            
    events.sort(key=lambda x: x["minutes"])
    return events


def get_forecasts_by_type(data, city_name,choice):
    current_hour = datetime.now().hour
    upcoming = []
    current_time = datetime.now().strftime("%H:%M")
    
    if choice != "daily" and "weather" in data:
        emojis_dict = determine_time_day_or_night(data, current_time)




    match choice:
        
        
        
        
        
            case "default":
                if "current_condition" in data:
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
                    
                    if int(upcoming[-1]["time"].split()[0].split(":")[0]) < 12:
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
                
                else:
                    current_temp = data["current"]["temperature_2m"]
                    current_code = data["current"]["weather_code"]
                    is_day = data["current"]["is_day"] == 1
                
                    current_wmo = WMO_CODES.get(current_code, {"desc": "Clear", "day": "☀️", "night": "🌙"})
                    current_desc = current_wmo["desc"]
                    current_emoji = current_wmo["day"] if is_day else current_wmo["night"]
                
                    default_forecast_table = Table(
                        title=f"[bold #fabd2f]Upcoming weather in {city_name}[/bold #fabd2f]", 
                        box=box.ROUNDED,
                        show_header=False,
                        border_style="#928374"
                        )
                    default_forecast_table.add_column("Period", justify="left", style="#a89984")
                    default_forecast_table.add_column("Time/Day", justify="center", style="#fabd2f")
                    default_forecast_table.add_column("Weather", justify="right", style="#b8bb26")
                    
                    default_forecast_table.add_row("Now", datetime.now().strftime("%H:%M"), f"{current_desc} {current_emoji}, {current_temp}°C")
                    
                    events = build_openmeteo_timeline(data)
                    start_min = current_hour * 60
                    end_min = (current_hour + 4) * 60
                    
                    for ev in events:
                        if start_min < ev["minutes"] <= end_min:
                            if ev["type"] == "forecast":
                                idx = ev["idx"]
                                time_part = data["hourly"]["time"][idx].split("T")[1]
                                h_temp = data["hourly"]["temperature_2m"][idx]
                                h_code = data["hourly"]["weather_code"][idx]
                                h_hour = int(time_part.split(":")[0])
                                h_is_day = 6 <= h_hour < 21
                                h_wmo = WMO_CODES.get(h_code, {"desc": "Clear", "day": "☀️", "night": "🌙"})
                                h_emoji = h_wmo["day"] if h_is_day else h_wmo["night"]
                                
                                default_forecast_table.add_row("Today", time_part, f"{h_wmo['desc']} {h_emoji}, {h_temp}°C")
                            elif ev["type"] == "sunrise":
                                default_forecast_table.add_row("Today", ev["time"], "[bold #fabd2f]Sunrise[/] 🌅")
                            elif ev["type"] == "sunset":
                                default_forecast_table.add_row("Today", ev["time"], "[bold #fe8019]Sunset[/] 🌇")
                    
                    tomorrow_max = data["daily"]["temperature_2m_max"][1]
                    tomorrow_min = data["daily"]["temperature_2m_min"][1]
                    tomorrow_code = data["daily"]["weather_code"][1]
                    tomorrow_wmo = WMO_CODES.get(tomorrow_code, {"desc": "Clear", "day": "☀️", "night": "🌙"})
                    
                    default_forecast_table.add_row("Tomorrow", "Day", f"{tomorrow_wmo['desc']} {tomorrow_wmo['day']}, {int(tomorrow_min)}°C..{int(tomorrow_max)}°C")
                    return default_forecast_table
            
            
            
                    
            
            






        
        
            case "short":
                if "current_condition" in data:    
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
                else:
                    current_temp = data["current"]["temperature_2m"]
                    current_code = data["current"]["weather_code"]
                    is_day = data["current"]["is_day"] == 1
                
                    wmo_info = WMO_CODES.get(current_code, {"desc": "Clear", "day": "☀️", "night": "🌙"})
                    current_weather_description = wmo_info["desc"]
                    current_emoji = wmo_info["day"] if is_day else wmo_info["night"]
                
                    random_art = random.choice(weather_arts[get_weather_category(current_weather_description)])

                    weather_table = Table(
                        title=f"[bold #fabd2f]Current weather in {city_name}[/bold #fabd2f]", 
                        box=box.ROUNDED,
                        show_header=False,  
                        border_style="#928374"
                        )
                    weather_table.add_column("Art", justify="center", vertical="middle")
                    weather_table.add_column("Info", justify="left", vertical="middle")

                    left_column = f"[bold #b8bb26]The weather is {current_weather_description} {current_emoji}\n\n{random_art}[/]"
                    right_column = f"[bold #928374]It is [/] [bold #fe8019]{current_temp}[/][bold #83a598]°C[/] in [bold #fabd2f]{city_name}[/]"
                    weather_table.add_row(left_column, right_column)
                    return weather_table



            case "daily":
                
            

                #  Daily data  по дням
                # Все переменные ниже — это обычные списки из 7 элементов (на неделю вперед)
                daily_time = data["daily"]["time"]  # Список дат ["2026-07-10", "2026-07-11" итд])
                daily_weather_code = data["daily"]["weather_code"]
                daily_temperature_2m_max = data["daily"]["temperature_2m_max"]
                daily_temperature_2m_min = data["daily"]["temperature_2m_min"]
                daily_sunset = data["daily"]["sunset"]  
                daily_uv_index_clear_sky_max = data["daily"]["uv_index_clear_sky_max"]
                daily_uv_index_max = data["daily"]["uv_index_max"]
                daily_rain_sum = data["daily"]["rain_sum"]
                daily_showers_sum = data["daily"]["showers_sum"]
                daily_snowfall_sum = data["daily"]["snowfall_sum"]
                daily_apparent_temperature_max = data["daily"]["apparent_temperature_max"]
                daily_precipitation_probability_max = data["daily"]["precipitation_probability_max"]
                daily_sunrise = data["daily"]["sunrise"]  

                settings_database = data_base_reader_no_print_settings()
                
                weekly_table = Table(
                title=f"[bold #fabd2f]Weekly forecast for {city_name}[/bold #fabd2f]", 
                box=box.ROUNDED,
                show_header=True,
                border_style="#928374"
                )

                Weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                start_day = datetime.now().weekday()



                
                weekly_table.add_column("[bold #fabd2f]Metric[/]", justify= "left", style="bold #fabd2f")

                daily_weather_desc = []
                for x in daily_weather_code:
                    daily_weather_desc.append(WMO_CODES[x])



                for x in range(7):
                    if x == 0:
                        day_name = "[bold #b8bb26]Today[/]"
                    elif x == 1:
                        day_name = "[bold #a89984]Tmrw[/]"
                    else:

                        day_index = (start_day + x) % 7
                        weekday = Weekdays[day_index]
                        
                        if weekday in ["Sat", "Sun"]:
                            day_name = f"[bold #fe8019]{weekday}[/]"
                        else:
                            day_name = f"[bold #a89984]{weekday}[/]"
                            

                    weekly_table.add_column(day_name, justify="left", style="bold #a89984")



                max_temps_row = [ f"{int(x)}°C" for x in daily_temperature_2m_max[:7]]
                weekly_table.add_row("Max temp", *max_temps_row, style= "#fe8019")
                min_temps_row = [f"{int(x)}°C" for x in daily_temperature_2m_min[:7]]
                weekly_table.add_row("Min temp",*min_temps_row, style= "#83a598")
                
                if settings_database["daily_display"]["Max_apparent_temp"] == True:
                    app_max_temps_row = [f"{int(x)}°C" for x in daily_apparent_temperature_max[:7]]
                    weekly_table.add_row("Apparent temp", *app_max_temps_row,  style= "#fe8019")
                
                if settings_database["daily_display"]["Emoji"] == True:
                    emojis_row = [WMO_CODES.get(code, {"day": "❓"})["day"] for code in daily_weather_code[:7]]
                    weekly_table.add_row("Emoji", *emojis_row)
                
                if settings_database["daily_display"]["Weather_desc"] == True:
                    daily_desc_row = [f"{x["desc"]}" for x in daily_weather_desc[:7]]
                    weekly_table.add_row("Weather", *daily_desc_row, style= "bold #fabd2f")
                
                if settings_database["daily_display"]["Rain_chance"] == True:
                    precipation_max_row = [f"{int(x)}%" for x in daily_precipitation_probability_max[:7]]
                    weekly_table.add_row("Rain chance", *precipation_max_row, style= "#8ec07c")
                
                if settings_database["daily_display"]["UV_index"] == True:
                    uv_row = [f"[bold #fabd2f]{int(uv)}[/]" for uv in daily_uv_index_max[:7]]
                    weekly_table.add_row("UV Index", *uv_row)
                
                if settings_database["daily_display"]["Sunrise"] == True:
                    daily_sunrise_row = [f"{x.split("T")[1]}" for x in daily_sunrise[:7]]
                    weekly_table.add_row("Sunrise", *daily_sunrise_row, style="#d3869b")
                
                if settings_database["daily_display"]["Sunset"] == True:
                    daily_sunset_row = [f"{x.split("T")[1]}" for x in daily_sunset[:7]]
                    weekly_table.add_row("Sunset", *daily_sunset_row, style= "#fe8019")
                

                return weekly_table





        
        
        
        
        
        
        
        
        
        
        
        
        
        
            case "detailed":
                if "current_condition" in data:
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
                    
                    if earliest_moment < day_after_tomorrow_sunset_mins and latest_moment > day_after_tomorrow_sunset_mins:
                        events_list.append({
                            "day": "Day after tomorrow",
                            "time": day_after_tomorrow_sunset_true_time,
                            "temp": None,
                            "desc": "sunset",
                            "minutes": day_after_tomorrow_sunset_mins,
                            "type": "sunset",

                            })
                    
                    if earliest_moment < day_after_tomorrow_sunrise_mins and latest_moment > day_after_tomorrow_sunrise_mins:
                        events_list.append({
                            "day": "Day after tomorrow",
                            "time": day_after_tomorrow_sunrise_true_time,
                            "temp": None,
                            "desc": "sunrise",
                            "minutes": day_after_tomorrow_sunrise_mins,
                            "type": "sunrise",

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
                else:
                    detailed_forecast_table = Table(
                    title=f"[bold #fabd2f]Detailed 42-Hour Forecast for {city_name}[/bold #fabd2f]", 
                    box=box.ROUNDED,
                    show_header=False,
                    border_style="#928374"
                    )
                    detailed_forecast_table.add_column("Day", justify="left", style="#a89984")
                    detailed_forecast_table.add_column("Time", justify="center", style="#fabd2f")
                    detailed_forecast_table.add_column("Weather details", justify="right", style="#b8bb26")
                    
                    start_min = current_hour * 60
                    end_min = (current_hour + 42) * 60
                    day_labels = ["Today", "Tomorrow", "Day after tmrw", "In 3 days", "In 4 days"]
                    
                    events = build_openmeteo_timeline(data)
                    
                    for ev in events:
                        if start_min <= ev["minutes"] < end_min:
                            day_idx = ev["minutes"] // 1440
                            day_label = day_labels[day_idx] if day_idx < len(day_labels) else "Upcoming"
                            
                            if ev["type"] == "forecast":
                                idx = ev["idx"]
                                time_part = data["hourly"]["time"][idx].split("T")[1]
                                h_temp = data["hourly"]["temperature_2m"][idx]
                                h_code = data["hourly"]["weather_code"][idx]
                                h_hour = int(time_part.split(":")[0])
                                h_is_day = 6 <= h_hour < 21
                                h_wmo = WMO_CODES.get(h_code, {"desc": "Clear", "day": "☀️", "night": "🌙"})
                                h_emoji = h_wmo["day"] if h_is_day else h_wmo["night"]
                                
                                detailed_forecast_table.add_row(day_label, time_part, f"{h_wmo['desc']} {h_emoji}, {h_temp}°C")
                                
                            elif ev["type"] == "sunrise":
                                detailed_forecast_table.add_row(day_label, ev["time"], "[bold #fabd2f]Sunrise[/] 🌅")
                                
                            elif ev["type"] == "sunset":
                                detailed_forecast_table.add_row(day_label, ev["time"], "[bold #fe8019]Sunset[/] 🌇")
                                
                    return detailed_forecast_table






def saved_settings():
    current_db = data_base_reader_no_print_settings()
    saved_settings_dict = current_db["daily_display"]
    daily_settings_table = Table(
        title="[bold #fabd2f]Daily forecast settings[/bold #fabd2f]", 
        box=box.ROUNDED,
        show_header=False,
        border_style="#928374"
    )
    counter = 1
    for x in saved_settings_dict:

        val = saved_settings_dict[x]
        if val is True: 
            daily_settings_table.add_row(f"[bold #928374]{counter}. show[/] [bold #fabd2f]{x}[/][bold #928374]:[/]", f"[bold #b8bb26]{val}[/]")
        else:
            daily_settings_table.add_row(f"[bold #928374]{counter}. show[/] [bold #fabd2f]{x}[/][bold #928374]:[/]", f"[bold #fe8019]{val}[/]")
        counter += 1   
    return daily_settings_table






def view_or_delete_saved_cities_and_coords():
        
        current_db = data_base_reader_no_print()
        
        saved_cities_table = Table(
        title="[bold #fabd2f]Saved Cities and Coordinates[/bold #fabd2f]", 
        box=box.ROUNDED,
        show_header=False,
        border_style="#928374"
        )
        
        counter = 1
        
        indexes_list = []
        
        for city_name, coords in current_db.items():
            saved_cities_table.add_row(f"[bold #83a598]{counter}[/] [bold #fabd2f]{city_name}[/] ([bold #b8bb26]{coords['Country']}[/]) — [bold #928374]Latitude:[/] [bold #fe8019]{coords['latitude']}[/], [bold #928374]Longitude:[/] [bold #83a598]{coords['longitude']}[/]")
            indexes_list.append(counter)
            counter +=1
        
        working = True
        
        console.print(saved_cities_table)
        
        while working:
            choice = console.input("[bold #b8bb26]Type the number of the city you want to delete, or 'e' to leave: [/]")
            
            
            if choice.strip().lower() == "e" or  choice.strip().lower() == "exit" or choice.strip().lower() == "l" or choice.strip().lower() == "x" or choice.strip().lower() == "leave" or choice.strip().lower() == "escape" or choice.strip().lower() == "q" or choice.strip().lower() == "quit":
                break
            
            if int(choice) not in indexes_list:
                console.print(f"[bold red]Enter a number that matches a city[/]")
                continue


            
            if int(choice) in indexes_list:
                
                current_cities_list = []
                
                for x in current_db:
                    current_cities_list.append(x)
                
                deleted_city_name = current_cities_list[int(choice) - 1]

                current_db.pop(deleted_city_name, None)
                
                
                with open(DB_path, "w", encoding="utf-8") as file:
        
                    json.dump(current_db, file, ensure_ascii=False, indent=4)
                
                
                console.print(f"[bold #b8bb26]Deleted city:[/] [bold #fabd2f]{deleted_city_name}[/]\n")
                
                working = False
                
                  

        
        
        
        return None




def greeting():
    console.print("[bold #fabd2f]Hello, this is a CLI forecast program, or CLI-Mate[/]")
    length = len(data_base_reader_no_print())
    global do_a_break
    if length < 1:
        new_city = search_for_city()
        if new_city:
            add_city(new_city)
            do_a_break = False
        else:
            do_a_break = True
    else: 
        do_a_break = False
        console.print("[bold #928374]Redirecting to main menu[/]\n\n\n")
        time.sleep(0.5)




def add_city(city):
    
    
        database = data_base_reader_no_print()
        
        
        database[city["City"]] = {
        "Country": city["Country"],
        "latitude": city["latitude"],
        "longitude": city["longitude"]
        }
        
        
        with open(DB_path, "w", encoding="utf-8") as file:
        
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
                city = console.input("""[bold #b8bb26]Enter your city's name or 'e' to leave: [/]""").strip().lower()
                if city == "e" or city == "leave":
                        
                    work = False
                    working = False
                    return None
                    

                
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
    while True:
        user_input = console.input("[bold #b8bb26]Choose the number of the saved city to see weather: [/]").strip()
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(current_list):
                return current_list[choice - 1]
        console.print("[bold red]Invalid option. Please enter a valid number.[/]")





def get_weather_backup(city_name):
    url = f"https://wttr.in/{city_name}"
    parameters = {
        "format": "j1", 
        "lang": "en"    
    }
    try:
        response = requests.get(url, parameters, timeout=3)
        if response.status_code == 200:
            console.print("[bold #b8bb26]\nRequest to backup (wttr.in): success[/]")
            data = response.json()
            return data, city_name
    except Exception as e:
        console.print(f"[bold red]Backup wttr.in failed: {e}[/]")
    return None


###Main weather getting function

def get_weather(city_name, lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunset", "uv_index_clear_sky_max", "uv_index_max", "rain_sum", "showers_sum", "snowfall_sum", "apparent_temperature_max", "precipitation_probability_max", "sunrise"],
        "hourly": ["temperature_2m", "weather_code", "snowfall", "showers", "rain", "precipitation", "visibility", "wind_speed_10m", "apparent_temperature", "precipitation_probability", "wind_direction_10m"],
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "timezone": "auto",
    }
    
    try:
        response = requests.get(url, params, timeout=3)
        if response.status_code == 200:
            console.print("[bold #b8bb26]\nRequest to Open-Meteo: success[/]")
            data = response.json()
            return data, city_name
        else:
            console.print(f"[bold red]Primary Open-Meteo failed: {response.status_code}[/]")
            print("[bold #fabd2f]Attempting backup website (wttr.in)[/]")
            return get_weather_backup(city_name)
            
    except Exception as e:
        console.print(f"[bold red]Connection error: {e}[/]")
        print("[bold #fabd2f]Attempting backup website (wttr.in)[/]")
        return get_weather_backup(city_name)






