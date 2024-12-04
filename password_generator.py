import random
import string
import pyperclip
import tkinter as tk
from tkinter import messagebox

def generate_password():
    try:
        length = int(password_length_entry.get())

        user_input = user_input_entry.get()

        if length <= 0 or length > 100:
            messagebox.showerror("Invalid Length", "Password length must be between 1 and 100 characters.")
            return

        if not user_input:
            messagebox.showerror("Invalid Input", "Please enter a valid string (letters, digits, or special characters) for password generation.")
            return

        complexity = complexity_var.get()

        characters = user_input 

        if complexity == "Medium":
            characters += string.ascii_uppercase
        elif complexity == "High":
            characters += string.ascii_uppercase + string.digits
        elif complexity == "Very High":
            characters += string.ascii_uppercase + string.digits + string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))

        if complexity == "High" or complexity == "Very High":
            while not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
                password = ''.join(random.choice(characters) for _ in range(length))

        if complexity == "Very High":
            while not any(c in string.punctuation for c in password):
                password = ''.join(random.choice(characters) for _ in range(length))

        password_display_var.set(password)

        copy_button.config(state=tk.NORMAL)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the password length.")

def copy_to_clipboard():
    password = password_display_var.get()
    if password:  
        pyperclip.copy(password)  
        messagebox.showinfo("Success", "Password copied to clipboard!")
    else:
        messagebox.showerror("No Password", "Please generate a password first.")

root = tk.Tk()
root.title("Advanced Password Generator")

root.geometry("400x400")

password_length_label = tk.Label(root, text="Password Length (numeric value):")
password_length_label.pack(pady=10)
password_length_entry = tk.Entry(root)
password_length_entry.pack(pady=5)
password_length_entry.insert(tk.END, "12")  

user_input_label = tk.Label(root, text="Enter characters for password generation:")
user_input_label.pack(pady=10)
user_input_entry = tk.Entry(root)
user_input_entry.pack(pady=5)
user_input_entry.insert(tk.END, "aB2$")  

complexity_label = tk.Label(root, text="Complexity:")
complexity_label.pack(pady=10)
complexity_var = tk.StringVar(value="Medium")
complexity_options = ["Low", "Medium", "High", "Very High"]

for option in complexity_options:
    tk.Radiobutton(root, text=option, variable=complexity_var, value=option).pack()

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=10)

password_display_var = tk.StringVar(value="")
password_display_label = tk.Label(root, textvariable=password_display_var, width=30, height=2, relief="sunken")
password_display_label.pack(pady=10)

copy_button = tk.Button(root, text="Copy to Clipboard", state=tk.DISABLED, command=copy_to_clipboard)
copy_button.pack(pady=10)

root.mainloop()


