import tkinter as tk
from tkinter import messagebox
import requests
import geocoder
from PIL import Image, ImageTk
import io

def get_weather_data(city=None):
    if city is None:
        g = geocoder.ip('me') 
        city = g.city
    
    api_key = '7d28d6e9a2ab36376f1147050bcc9863' 
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        
        if response.status_code != 200:
            messagebox.showerror("Error", f"Error fetching weather data for {city}. Status code: {response.status_code}")
            return None
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}. Please check your internet connection.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}.")
        return None

def update_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input", "Please enter a city name.")
        return

    weather_data = get_weather_data(city)

    if weather_data:
        city_name = weather_data['name']
        weather_desc = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        city_label.config(text=f"Weather in {city_name}")
        temp_label.config(text=f"Temperature: {temperature}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        weather_desc_label.config(text=f"Description: {weather_desc.capitalize()}")
        
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_image = requests.get(icon_url).content
        icon_img = Image.open(io.BytesIO(icon_image))
        icon_img = icon_img.resize((50, 50), Image.Resampling.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_img)
        
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

def get_weather_by_gps():
    g = geocoder.ip('me')
    city = g.city
    city_entry.delete(0, tk.END)
    city_entry.insert(0, city)
    update_weather()

root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Weather in:", font=("Helvetica", 16))
city_label.pack()

city_entry = tk.Entry(root, font=("Helvetica", 14))
city_entry.pack()

search_button = tk.Button(root, text="Get Weather", font=("Helvetica", 14), command=update_weather)
search_button.pack()

gps_button = tk.Button(root, text="Use Current Location", font=("Helvetica", 14), command=get_weather_by_gps)
gps_button.pack()

temp_label = tk.Label(root, text="Temperature: -- °C", font=("Helvetica", 14))
temp_label.pack()

humidity_label = tk.Label(root, text="Humidity: -- %", font=("Helvetica", 14))
humidity_label.pack()

wind_label = tk.Label(root, text="Wind Speed: -- m/s", font=("Helvetica", 14))
wind_label.pack()

weather_desc_label = tk.Label(root, text="Description: --", font=("Helvetica", 14))
weather_desc_label.pack()

icon_label = tk.Label(root)
icon_label.pack()

root.geometry("400x450")
root.mainloop()


