import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
import time
from Ascii_arts import weather_arts


console = Console()





city = "Andijan"
lat = "40.78338"
lon = "72.35067"




def get_weather(city_name, lat, lon):
    try:

        weather_table = Table(
            title=f"[bold #fabd2f]Current weather in {city_name}[/bold #fabd2f]", 
            box=box.ROUNDED,
            show_header=False,  
            border_style="#928374"
        )
        
        weather_table.add_column("Art", justify="center", vertical="middle")
        weather_table.add_column("Info", justify="left", vertical="middle")
        
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
        
            current_temp = data["current_condition"][0]["temp_C"]
            current_weather_description = data["current_condition"][0]["weatherDesc"][0]["value"]


            selected_art = weather_arts["1"]


            weather_info = (
                f"[bold #928374]Temperature:[/] [bold #fe8019]{current_temp}[/][bold #83a598]°C[/]\n"
                f"[bold #928374]Condition:[/] [bold #b8bb26]{current_weather_description}[/]"
            )


            weather_table.add_row(selected_art, weather_info)
            

            console.print(weather_table)
            
    except Exception as e:
        print(f"Something went wrong: {e}")



get_weather(city, lat, lon)