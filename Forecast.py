import requests




def greeting():
    print("---Hello, this is a CLI forecast program---")
    input("Choose an option:")




current_city = "Andijan"


params = {
    "format": "j1", 
    "lang": "en"    
}


main_url = "https://wttr.in/"


target_url = f"{main_url}{current_city}"

backup_url = "https://api.open-meteo.com/v1/forecast"

def get_weather(url, parameters):

    try:



        response = requests.get(url, parameters)

        if response.status_code == 200:
            print("Request success")
            print("Received text:")
            data = response.json()
        
            current_temp = data["current_condition"][0]["temp_C"]
            current_weather_description = data["current_condition"][0]["weatherDesc"][0]["value"]


            print("--- Information---\n")
            print(f"Current temperature in {current_city}:{current_temp} celsius")
            print(f"The weather is {current_weather_description}")
        
        
        
        
        
        
        
    
        
        
        
        
        
        
        
        
        
        else:
            print(f"Request error: {response.status_code}")
    except:
        return 0





get_weather(target_url,params)