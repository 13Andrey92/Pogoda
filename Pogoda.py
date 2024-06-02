import os
import sys
from tkinter import *
import requests
from PIL import Image, ImageTk
from tkinter.messagebox import showerror


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def save_image(url):
    response = requests.get(url)
    with open(resource_path("weather_icon.png"), "wb") as file:
        file.write(response.content)
    image = Image.open(resource_path("weather_icon.png"))
    return ImageTk.PhotoImage(image)


def show_weather():
    cityname = weather_entry.get()
    if not cityname:
        weather_info.config(text="")
        picture.config(image="", background="#F0F0F0")
        showerror("Ошибка", "Строка не может быть пустой")
    else:
        responce = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=3faa8133371792ef1aacd11949472dc8&lang=ru")
        if responce.status_code != 404:
            responce = responce.json()
            img = save_image(f"http://openweathermap.org/img/wn/{responce["weather"][0]["icon"]}@2x.png")
            picture.config(image=img, background="Grey")
            picture.image = img
            weather_info.config(text=f"{(responce["weather"][0]["description"]).capitalize()}\n"
                                     f"Температура: {round(responce["main"]["temp"]-273.15)} C\n"
                                     f"Скорость ветра: {responce["wind"]["speed"]} м/с")
        else:
            weather_info.config(text="")  # удаление текста и картинки при ошибке
            picture.config(image="", background="#F0F0F0")
            showerror("Ошибка", "Указанный город не найден!")


window = Tk()
window.geometry("500x500")
window.title("Погода")
window.iconbitmap("pogoda.ico")
window.resizable(False, False)

welcome_text = Label(window, text="Прогноз погоды", font=("Time New Roman", 30, "bold"))
welcome_text.pack()

weather_entry = Entry(window)
weather_entry.pack(pady=10)
weather_entry.focus()

btn = Button(window, text="Показать погоду", command=show_weather)
btn.pack(pady=10)

picture = Label(window)
picture.pack()

weather_info = Label(window, font=("Time New Roman", 30))
weather_info.pack()

window.mainloop()
