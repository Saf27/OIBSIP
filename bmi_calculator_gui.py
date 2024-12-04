import tkinter as tk
from tkinter import messagebox, ttk
import csv
import matplotlib.pyplot as plt
import numpy as np

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(weight, height, bmi, category):
    with open('bmi_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([weight, height, bmi, category])

def load_data():
    try:
        with open('bmi_data.csv', mode='r') as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []

def display_history():
    for row in tree.get_children():
        tree.delete(row)

    data = load_data()
    for entry in data:
        tree.insert("", "end", values=entry)

def analyze_trend():
    data = load_data()
    if len(data) == 0:
        messagebox.showwarning("No Data", "No historical data available for trend analysis.")
        return

    bmi_values = [float(entry[2]) for entry in data]
    timestamps = np.arange(len(bmi_values))  

    plt.figure(figsize=(8, 5))
    plt.plot(timestamps, bmi_values, marker='o', linestyle='-', color='b')
    plt.title("BMI Trend Over Time")
    plt.xlabel("Time (Entries)")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.show()

def on_calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return
        
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        
        save_data(weight, height, bmi, category)
        
        result_label.config(text=f"Your BMI is: {bmi:.2f}")
        category_label.config(text=f"Your BMI category is: {category}")
        
        display_history()
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for weight and height.")

root = tk.Tk()
root.title("BMI Calculator")

weight_label = tk.Label(root, text="Enter your weight (in kg):")
weight_label.pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

height_label = tk.Label(root, text="Enter your height (in meters):")
height_label.pack()
height_entry = tk.Entry(root)
height_entry.pack()

calculate_button = tk.Button(root, text="Calculate BMI", command=on_calculate)
calculate_button.pack()

result_label = tk.Label(root, text="Your BMI will be shown here.")
result_label.pack()

category_label = tk.Label(root, text="BMI Category will be shown here.")
category_label.pack()

history_frame = tk.Frame(root)
history_frame.pack()

history_label = tk.Label(history_frame, text="Historical Data")
history_label.pack()

tree = ttk.Treeview(history_frame, columns=("Weight", "Height", "BMI", "Category"), show="headings")
tree.heading("Weight", text="Weight (kg)")
tree.heading("Height", text="Height (m)")
tree.heading("BMI", text="BMI")
tree.heading("Category", text="Category")
tree.pack()

view_history_button = tk.Button(root, text="View History", command=display_history)
view_history_button.pack()

analyze_trend_button = tk.Button(root, text="Analyze BMI Trend", command=analyze_trend)
analyze_trend_button.pack()

root.mainloop()
