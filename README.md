# CLI-Mate

CLI-mate is a high-accuracy, command-line weather forecast utility styled with Gruvbox color palette. It features a local JSON database for city caching, automatic day/night emoji rendering based on real-time sunrise/sunset calculations, and three display modes.

---

## Features

- **Local Database Caching (`data_base.json`):** Saves your cities and their coordinates so you can query them instantly.
- **Dynamic Day/Night Emoji Cycle:** Automatically determines if it is day or night at the forecast time using local sunrise/sunset values, switching between sun ☀️ and moon 🌙 icons.
- **Chronological Timeline Sorting:** Seamlessly merges and sorts weather forecasts, sunrise, and sunset times in chronological order.
- **Three Display Modes:**
  - **Short:** Just the current temperature, weather conditions, and a custom weather ASCII art.
  - **Default:** Current weather plus upcoming 3-hour interval forecasts and tomorrow's midday outlook.
  - **Detailed:** Comprehensive, scroll-safe 42-hour vertical forecast timeline.

---

## Libraries Used (Dependencies)

The application is written in Python 3 and utilizes the following libraries:

- **`requests`**: For making HTTP requests to the `wttr.in` and `Open-Meteo` meteorological APIs.
- **`rich`**: For building beautiful, color-coded tables, borders, and styled CLI layouts using terminal markup.
- **`datetime`** (Standard Library): For manipulating time, calculating time deltas, and managing timezone-specific formats.
- **`random`** (Standard Library): For choosing random, styled ASCII arts for weather conditions.
- **`json`** (Standard Library): For reading and writing structured data to the local database file.

---




## Installation and Setup

You can install **climate** on your system using one of the following methods:

### Method 1: Install via .deb Package (Recommended for Ubuntu/Debian)
This is the easiest way to install. It automatically registers the global `climate` command and resolves all system-wide dependencies.

1. Go to the [Releases](https://github.com/kamilyarkaev/CLI-mate/releases) page of this repository.
2. Download the latest `.deb` package (e.g., `climate_1.1_linux_amd64.deb`).
3. Open your terminal in the directory where the file was downloaded and run:
   ```bash
   sudo apt install ./climate_1.1_linux_amd64.deb
   ```
4. Run the application from anywhere by typing:
   ```bash
   climate
   ```

### Method 2: Setup from Source Code (For testing or non-Debian systems)
If you want to run the raw source code or you are on a system that does not support `.deb` packages:

1. Clone the repository:
   ```bash
   git clone https://github.com/kamilyarkaev/CLI-mate.git
   cd CLI-mate
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies inside the virtual environment:
   ```bash
   pip install requests rich
   ```
4. Run the application:
   ```bash
   python3 main.py
   ```







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

>**From July 2nd/3rd/4th/9th/15th 21:52 2026     02.07.2026**.

I did not work on CLI-Mate today because I am swamped with my homework right now, sorry if anyone cares

>**From July 5th,6th,7th,11th,12th,13th 21:30 2026    07.07.2026**.

Fixing minor problems and adding slightly more flexible functional, rn I am working on making a deb package out of all this

>**From July 10th 20:47 2026     10.07.2026**.

New display type has been added to the program, and it is 'daily',
it uses open-meteo api as the main api for it because wttr.in does not provide a weekly forecast. 

Also I decided to leave the idea with a singular file made with pyinstaller because the developing direction is different now, 

I want so that anyone on linux could download my program via 'sudo apt install'.

Therefore I need to upload my program to the downstream debian repo, 

There are also still a few issues with database file paths, as I need to make sure they comply with XDG standards and don't clutter the user's home directory.

>**From July 14th 21:40 2026   14.07.2026**.

Added validate() function to confirm if the files have the proper containings and structure, and also if the user decides to test the program by changing the containings of the files

I have also moved all system paths away from direct home directory clutter (~/.climate_database.json and ~/.cli-mate_forecast_settings) to follow modern Linux packaging standards

Now: 

Configuration: ~/.config/climate/forecast_settings.json 

Saved Cities Database: ~/.local/share/climate/database.json

Also I integrated automated directory creation using os.makedirs(.....) to prevent file path errors on clean installations

Configured Open-Meteo as the primary API provider for all forecast modes (short, default, detailed, daily), utilizing its high uptime and rich dataset (wind direction, speed, UV index, native day/night flags)

Implemented inmemory lazy loading caching _cached_db and _cached_settings, reducing slow filesystem read operations to just once per application lifecycle

I'm still planning to add delete_city() function and implement wind direction, wind speed, rain chance,uv index and wind busts to regular forecast modes for information saturation


>**From July 16th 20:20 2026   16.07.2026**.

Cli-Mate is now fully ready for use!



