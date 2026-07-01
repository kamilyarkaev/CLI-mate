# CLI-Mate

CLI-mate is a high-accuracy, lightweight command-line weather forecast utility styled with the eye-pleasing Gruvbox color palette. It features a local JSON database for city caching, automatic day/night emoji rendering based on real-time astronomical sunrise/sunset calculations, and three customizable display modes.

---

## Features

- **Local Database Caching (`data_base.json`):** Saves your cities and their coordinates so you can query them instantly.
- **Dynamic Day/Night Emoji Cycle:** Automatically determines if it is day or night at the forecast time using local sunrise/sunset values, switching between sun ☀️ and moon 🌙 icons.
- **Chronological Timeline Sorting:** Seamlessly merges and sorts weather forecasts, sunrise, and sunset times in absolute chronological order.
- **Three Display Modes:**
  - **Short:** Just the current temperature, weather conditions, and a custom weather ASCII art.
  - **Default:** Current weather plus upcoming 3-hour interval forecasts and tomorrow's midday outlook.
  - **Detailed:** Comprehensive, scroll-safe 42-hour vertical forecast timeline.

---

## Libraries Used (Dependencies)

The application is written in Python 3 and utilizes the following libraries:

- **`requests`**: For making fast, synchronous HTTP requests to the `wttr.in` and `Open-Meteo` meteorological APIs.
- **`rich`**: For building beautiful, color-coded tables, borders, and styled CLI layouts using terminal markup.
- **`datetime`** (Standard Library): For manipulating time, calculating time deltas, and managing timezone-specific formats.
- **`random`** (Standard Library): For choosing random, styled ASCII arts for weather conditions.
- **`json`** (Standard Library): For reading and writing structured data to the local database file.

---




## Installation and Setup

To run CLI-mate locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/kamilyarkaev/CLI-mate.git
cd CLI-mate
```

### 2. Set Up a Virtual Environment (Recommended)
Create and activate an isolated virtual environment to prevent package conflicts with your system Python:

On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install the Dependencies
Install the required external libraries inside your active virtual environment:
```bash
pip install requests rich
```

---

## How to Run the App

With your virtual environment active, run the entry point of the application:

```bash
python3 main.py
```

---

## Project Structure

- `main.py`: The main executable entry point that starts the program loop.
- `Functions.py`: Contains the core logic, API request handling, chronological sorting, and table rendering.
- `Ascii_arts.py`: Houses the pre-escaped, monospace-safe, and color-coded ASCII weather icons.
- `data_base.json`: Your local database used to store saved cities and coordinates.

































































## Development journal


> **From: June 21st 21:33 2026      21.06.2026**.

It's still raw


I'm planning to make it accessible via terminal on Linux with just one command


Using ASCII and Python rich library make a stylish terminal output

>**From: June 22nd 19:19 2026       22.06.2026**.

Added main menu and some options

Implemented json database

Updated backup get_weather to work correctly

Functions that were added today: main_menu, greeting, data_base_reader_no_print, add_city, search_for_city(it uses open-meteo geocoding to find coordinates of the city), choose_an_option

Planning to add: changeable forecast display settings, description on why this programm also uses coordinates, access via terminal with 1 single command(on linux), stylish terminal output using ASCII and Python rich library( I consider this to be the hardest part of the programm)

>**From: June 23rd 17:44 2026      23.06.2026**.

Updated main menu so it looks a lot more clear now and all of the huge text doesn't apper after you look out the weather

I finally know how to use git through command line.
So this is why at this moment on 23 June I already have 15 contributions(this is 5 times my average)

Changeable forecast display, and other minor functions are still in work, I'm sure by the end of the week they'll be ready

> **From June 25th 21:45 2026     25.06.2026**.

I haven't done anything yesterday because of three reasons, first: I felt dizzy the whole morning, I felt asleep in the afternoon, and then when I woke up in the evening there was a power outage in my area, leaving me unable to use my computer


Just now I have introduced myself to Python library "rich", it lets you customize your entire output in terminal,

For this moment I added some colors to outputs, but tomorrow I'm going to replace the current output with tables and ASCII arts.

The customizable weather output is going to be ready tomorrow

> **From June 26th 16:43 2026     26.06.2026**.

I have enhanced the colored output significantly

Made a couple of tests on integration of ASCII arts to the output tables

Just figured out the way the customizable forecast output is going to work, but it'll be ready tomorrow

Created Ascii_arts.py and ascii_art_output_test.py for future functions

>**From June 28th 19:52 2026     28.06.2026**.

I did not contribute anything yesterday(27th June) because I did not have access to my computer all day long

Today I have also done poorly but the changeable forecast settings are going to be ready the very next day


>**From June 29th 16:27 2026     29.06.2026**.
Changeable forecast settings are finally ready!

The forecast display mode is set to default ON default 

Rn I am fixing bugged display of ASCII arts, it's all going to be finished by this evening

>**From June 30th 23:20 2026     30.06.2026**.

Now alongside temperature in any forecast display mode you can see the time of sunrises and sunsets if they ofc are within the forecast

Tomorrow I will work with pyinstaller to make this a 1 file program




