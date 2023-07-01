import tkinter as tk

def create_window():
    myapp = tk.Tk()
    myapp.configure(bg="#038C3E")
    myapp.title("")
    myapp.attributes('-fullscreen', True)
    return myapp

APP = create_window()

def battery_count_window(**battery_values):
    ...

def set_countdown(value: int):
    ...

# myapp.mainloop()
