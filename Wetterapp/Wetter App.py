# Import Module                              # programmed by M.M.@ #

import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap


# Funktion für die Wetterinfos von Openwettermap API

def get_weather(city):
    api_key = "5bf7b2d25e56f28895371028c8a62f30"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},&lang=de&appid={api_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    # Parse JSON für die wetterinfos
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    pressure = weather['main']['pressure']
    humidity = weather['main']['humidity']
    city = weather['name']
    country = weather['sys']['country']

    # icon URL  für wetter-symbole und rückgabe der wetterinfos
    icon_url = f" https://openweathermap.org/img/wn/10d@2x.png"
    return icon_url, temperature, description, pressure, humidity, city, country


# Funktion zum suchen der wetterdaten der stadt

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    # stadt gefunden und entpacken der wetterdaten
    icon_url, temperature, description, pressure, humidity, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # wetter icons von der URL fürs icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # update temperatur und description label
    temperature_label.configure(text=f"Temperatur: {temperature:.2f}°C")
    description_label.configure(text=f"Vorhersage: {description}")
    pressure_label.configure(text=f"Luftdruck: {pressure:.0f}HPa")
    humidity_label.configure(text=f"Luftfeuchtigkeit: {humidity:.0f}%")


root = ttkbootstrap.Window(themename="morph")
root.title("WETTER -APP")
root.geometry("500x550")

# eingabe stadt-Name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# knopf  zum bestätigen der Stadteingabe
search_button = ttkbootstrap.Button(root, text="SUCHE", command=search)
search_button.pack(pady=10)

# Label  zum anzeigen der stadt ( name )
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Label  zum anzeigen von icons ( wetter )
icon_label = tk.Label(root)
icon_label.pack()

# Label  zum anzeigen der temeratur
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# Label  zum anzeigen der vorhersage
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

# Label  zum anzeigen des luftdrucks
pressure_label = tk.Label(root, font="Helvetica, 20")
pressure_label.pack()

# Label  zum anzeigen der luftfeuchtigkeit
humidity_label = tk.Label(root, font="Helvetica, 20")
humidity_label.pack()

root.mainloop()
