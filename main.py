from PIL import Image, ImageTk
from tkinter import messagebox
import requests
import tkinter as tk
import time
import datetime
import threading
import customtkinter
import pprint
import os
import json
#---------------------
customtkinter.set_appearance_mode("dark")
#---VARIABLE----------



ENTRY_COLOR = "#737475"
BUTTON_COLOR = ["#d6d6d6","#cfcbca"]
FONT = ("Bahnschrift", 20)
ENTRY_WIDTH = 250
TEMP_FONT = ("Bahnschrift", 35)
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


#---IMAGE-AND-CMD-----
SEARCH_ICON_PATH = 'img\search_icon.png'
def open_image(path):
    return customtkinter.CTkImage(dark_image=Image.open(path))

def count():
    sec = 2
    while True:
        submit_city.configure(text=sec, image="")
        time.sleep(1)
        sec = sec - 1
        if sec < 0 :
            submit_city.configure(state= tk.NORMAL, text="", image= open_image(SEARCH_ICON_PATH))
            break

def timestamp_to_utc(timestamp):
    # Convert Unix timestamp to UTC datetime
    utc_datetime = datetime.datetime.utcfromtimestamp(timestamp).strftime("%H:%M %p")
    return utc_datetime

#---CODE--------------


def requests_city():
    global BASE_URL
    if city_entry.get() == "":
        return
    params = {
    "q": city_entry.get(),
    "appid": "ad614b8789dcf2f58e4b8531333f6301",
    "units": "metric"  # You can change this to "imperial" for Fahrenheit.
    }
    r  = requests.get(BASE_URL, params=params).json()
    submit_city.configure(state= tk.DISABLED)
    try:
        temperature_label.configure(text=f'{round(r["main"]["temp"], 1)}°C')
        peak_temp_label.configure(text=f'Nhiệt độ cao nhất: {round(r["main"]["temp_max"], 1)}°C')
        low_temp_label.configure(text=f'Nhiệt độ thấp nhất: {round(r["main"]["temp_min"], 1)}°C')
        feel_temp_label.configure(text=f'Cảm nhận: {round(r["main"]["feels_like"], 1)}°C')
        update_time_label.configure(text=f'Cập nhật: {timestamp_to_utc(r["dt"]+25200)}')
        sun_rise_label.configure(text=f'Mặt trời mọc: {timestamp_to_utc(r["sys"]["sunrise"]+r["timezone"])}')
        sun_set_label.configure(text=f'Mặt trời lặn: {timestamp_to_utc(r["sys"]["sunset"]+r["timezone"])}')
        visibility_label.configure(text=f'Tầm nhìn: {r["visibility"]/1000} km')
        pressure_label.configure(text=f'Áp suất: {r["main"]["pressure"]} hPa')
        humidity_label.configure(text=f'Độ ẩm: {r["main"]["humidity"]} %')
        th = threading.Thread(target=count)
        th.start()
    except Exception:
        submit_city.configure(state= tk.NORMAL)
        messagebox.showerror(title="Lỗi", message="Không tìm thấy vị trí !")
    
#---USER-INTERFACE----

windows = customtkinter.CTk()
inf_frame = customtkinter.CTkFrame(windows)
inf_frame.pack(side=tk.LEFT)

type_frame = customtkinter.CTkFrame(windows)
type_frame.pack()

temperature_frame = customtkinter.CTkFrame(windows)
temperature_frame.pack()

city_entry = customtkinter.CTkEntry(type_frame, placeholder_text="City", fg_color=ENTRY_COLOR, font=FONT, width=ENTRY_WIDTH)
city_entry.grid(row=0, column=0, padx=10, pady=10)

submit_city = customtkinter.CTkButton(type_frame, image=open_image(SEARCH_ICON_PATH), fg_color=BUTTON_COLOR[0],hover_color=BUTTON_COLOR[1], font=FONT, text="", command=requests_city)
submit_city.grid(row=0, column=1)

temperature_label = customtkinter.CTkLabel(temperature_frame, font=TEMP_FONT, text="")
temperature_label.pack()

peak_temp_label = customtkinter.CTkLabel(windows, font=FONT, text="")
peak_temp_label.pack()

low_temp_label = customtkinter.CTkLabel(windows, font=FONT, text="")
low_temp_label.pack()

feel_temp_label = customtkinter.CTkLabel(windows, font=FONT, text="")
feel_temp_label.pack()

update_time_label = customtkinter.CTkLabel(inf_frame, font=FONT, text="")
update_time_label.pack()

sun_rise_label = customtkinter.CTkLabel(inf_frame, font=FONT, text="")
sun_rise_label.pack()

sun_set_label = customtkinter.CTkLabel(inf_frame, font=FONT, text="")
sun_set_label.pack()

visibility_label = customtkinter.CTkLabel(inf_frame, font=FONT, text="")
visibility_label.pack()

pressure_label = customtkinter.CTkLabel(inf_frame, font=FONT, text="")
pressure_label.pack()

humidity_label = customtkinter.CTkLabel(inf_frame, font=FONT, text="")
humidity_label.pack()

windows.title("Weather Forecast 1.0 by mahiru7229 <3")
windows.resizable(width=False, height=False)
windows.mainloop()