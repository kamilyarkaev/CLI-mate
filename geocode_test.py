import requests

payload = {
    "name": "Moscow",
    "count": 10
}


url = "https://geocoding-api.open-meteo.com/v1/search"
response = requests.get(url,params = payload)
print(response.status_code)
print()
data = response.json()
print(data)
print()
print()
print()
latitude = data["results"][0]["latitude"]
longitude = data["results"][0]["longitude"]
country = data["results"][0]["country"]
name = data["results"][0]["name"]

print(f"City:{name}, Country:{country}")
print(f"Latitude:{latitude}, Longitude:{longitude}")
print("I hope these are correct because otherwise I don't know how to let you choose beetween the avaible options")






for x in data["results"]:
    print(x["name"], x["country"], x["admin1"])