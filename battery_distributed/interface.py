from random import randint
from threading import Thread
from time import sleep
import tkinter as tk
from tkinter import EW, NS, X, Canvas, Frame, Label, StringVar
from PIL import ImageTk, Image
from battery_distributed.model import MachineSession
import qrcode


APP = tk.Tk()
APP.geometry("1024x600")
APP.title("")
APP.configure(bg="#038C3E")
#APP.attributes('-fullscreen', True)

images = {}


def load_img(img_path, key):
    img_original = Image.open(img_path)
    img_resized = img_original.resize((65, 65))
    images[key] = ImageTk.PhotoImage(img_resized)


load_img("assets/battery.png", "battery")


def monta_frame_label(widget, linha, coluna, ipadx, ipady, lipady, **label_args):
    frame = Frame(widget, bg="#038C3E")
    label = Label(frame, **label_args)
    label.pack(fill=X, expand=True, ipady=lipady)
    frame.grid(row=linha, column=coluna, ipadx=ipadx, ipady=ipady, sticky=NS + EW)
    return label


def monta_linha(
    widget, linha, valor1, valor2, img=False, lipady=16, bg="#F4F4F8", fg="#000000"
):
    if img:
        monta_frame_label(
            widget, linha, 0, 10, 10, 0, image=images["battery"], bg=bg, fg=fg
        )
    else:
        monta_frame_label(
            widget, linha, 0, 10, 10, lipady, text="", font=("Arial", 20), bg=bg, fg=fg
        )

    monta_frame_label(
        widget, linha, 1, 50, 0, lipady, text=valor1, font=("Arial", 20), bg=bg, fg=fg
    )
    return monta_frame_label(
        widget, linha, 2, 10, 0, lipady, text=valor2, font=("Arial", 20), bg=bg, fg=fg
    )


def monta_linhas(pilhas):
    frame = Frame(APP)

    for i in range(3):
        frame.columnconfigure(i, weight=1)

    pilhas_widgets = {}

    monta_linha(
        frame, 0, "Tipo", "Pilhas Inseridas", lipady=0, bg="#038C3E", fg="#F4F4F8"
    )
    for linha, valores in enumerate(pilhas.items(), 1):
        pilhas_widgets[valores[0]] = monta_linha(
            frame, linha, valores[0], valores[1], True
        )

    return frame, pilhas_widgets


def configure_columns(columns):
    APP.rowconfigure(0, weight=1)
    APP.columnconfigure(0, weight=2 if columns == 2 else 1)
    APP.columnconfigure(1, weight=1 if columns == 2 else 0)


def cria_widget_principal(pilhas):
    widget_primario, pilhas_widgets = monta_linhas(pilhas)
    return widget_primario, pilhas_widgets


def cria_widget_logo():
    logo_widget = Frame(APP)
    message_top_label = tk.Label(
        logo_widget,
        text="Reciclador de Pilha",
        font=("Arial", 20, "bold"),
        bg="#038C3E",
        fg="#F4F4F8",
    )
    message_top_label.pack(fill="both", ipady=20, ipadx=55)

    path = "assets/logo.png"
    logo_image = ImageTk.PhotoImage(
        Image.open(path).resize((220, 220)), master=logo_widget
    )

    logo_image_label = tk.Label(logo_widget, image=logo_image, bg="#038C3E")
    logo_image_label.image = logo_image
    logo_image_label.pack(fill="both", ipadx=20)

    message_bottom_label = tk.Label(
        logo_widget,
        text="Insira uma pilha para começar...",
        font=("Arial", 20, "bold"),
        bg="#038C3E",
        fg="#F4F4F8",
    )
    message_bottom_label.pack(fill="both", ipady=20, ipadx=55, side="top")
    return logo_widget


def cria_widget_qrcode(qr_data):
    message = "Sucesso!\nEscaneie o código\ncom o aplicativo."

    widget_secundario = Frame(APP)
    qr = qrcode.QRCode()
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="#000000", back_color="#F4F4F8").resize((220, 250))
    qr_photo = ImageTk.PhotoImage(
        qr_image, master=widget_secundario, width=200, height=200
    )

    qr_label = tk.Label(widget_secundario, image=qr_photo, bg="#038C3E")
    qr_label.image = qr_photo
    qr_label.pack()

    message_label = tk.Label(
        widget_secundario, text=message, font=("Arial", 20), bg="#038C3E", fg="#F4F4F8"
    )
    message_label.pack(fill="both", ipady=15)
    return widget_secundario


def cria_widget_timer(message_top, timer, message_bottom, bg="#038C3E", fg="#F4F4F8"):
    widget_secundario = Frame(APP)
    string_var = StringVar()
    string_var.set(timer)

    message_top_label = tk.Label(
        widget_secundario, text=message_top, font=("Arial", 20, "bold"), bg=bg, fg=fg
    )
    message_top_label.pack(fill="both", ipady=20, ipadx=55, side="top")
    message_timer_label = tk.Label(
        widget_secundario,
        textvariable=string_var,
        font=("Arial", 50, "bold"),
        bg=bg,
        fg=fg,
    )
    message_timer_label.pack(fill="both", ipady=5, ipadx=55, side="top")
    message_label = tk.Label(
        widget_secundario, text="segundos", font=("Arial", 20), bg=bg, fg=fg
    )
    message_label.pack(fill="both", ipady=5, ipadx=55, side="top")
    message_bottom_label = tk.Label(
        widget_secundario, text=message_bottom, font=("Arial", 20, "bold"), bg=bg, fg=fg
    )
    message_bottom_label.pack(fill="both", ipady=20, ipadx=55, side="top")
    return widget_secundario, string_var


def cria_widget_status(message, image_path, bg, fg, resize=200):
    widget_secundario = Frame(APP)

    image = ImageTk.PhotoImage(
        Image.open(image_path).resize((resize, resize)), master=widget_secundario
    )

    image_label = tk.Label(widget_secundario, image=image, bg=bg)
    image_label.image = image
    image_label.pack(fill="both", ipadx=20)
    message_label = tk.Label(
        widget_secundario, text=message, font=("Arial", 20, "bold"), bg=bg, fg=fg
    )
    message_label.pack(fill="both", ipady=20, ipadx=20, side="top")
    return widget_secundario


pilhas = {"AAA": 0, "AA": 0, "C": 0, "D": 0, "V9": 0}

widget_logo = cria_widget_logo()
widget_primario, widget_pilhas = cria_widget_principal(pilhas)
widget_secundario_timer, label_timer = cria_widget_timer(
    "Coloque uma pilha\ndentro de:", 5, "para não encerrar\no processo"
)
widget_secundario_warn = cria_widget_status(
    "Processando pilha ...\nNão insira outra\naté encerrar o processo.",
    "assets/warn_image.png",
    "#038C3E",
    "#F4F4F8",
)
widget_secundario_error = cria_widget_status(
    "Erro no processamento. \nPilha não identificada.\nDevolvendo ...",
    "assets/error_image.png",
    "#038C3E",
    "#F4F4F8",
    resize=180,
)

MAIN = 0
SESSION = 1
SESSION_PROCESSING = 2
SESSION_ERROR = 3
SESSION_END = 4

current_screen = None
current_widget = None


def change_to_main_screen():
    global current_screen, current_widget
    if current_screen == MAIN:
        return

    configure_columns(1)
    widget_logo.grid(row=0, column=0)
    if current_screen != MAIN and current_screen is not None:
        widget_primario.grid_forget()
        current_widget.grid_forget()
    current_screen = MAIN


def change_to_session_screen():
    global current_screen, current_widget
    configure_columns(2)
    widget_primario.grid(row=0, column=0)
    if current_screen == MAIN:
        widget_logo.grid_forget()
    current_screen = SESSION
    current_widget = None


def session_screen(func):
    def inner(*args, **kwargs):
        global current_widget, current_screen

        if current_screen < SESSION:
            change_to_session_screen()

        screen, widget = func(*args, **kwargs)

        if current_widget:
            current_widget.grid_forget()

        current_widget = widget
        current_screen = screen

    return inner

def add_session_state(machine: MachineSession):
    if current_screen < SESSION:
        change_to_session_screen()

    for battery_type in ["AA", "AAA", "V9", "C", "D"]:
        widget_pilhas[battery_type].configure(
            text=getattr(machine, f"{battery_type.lower()}_count")
        )


@session_screen
def change_to_processing():
    widget_secundario_warn.grid(row=0, column=1)
    return SESSION_PROCESSING, widget_secundario_warn


@session_screen
def change_to_session_error():
    widget_secundario_error.grid(row=0, column=1)
    return SESSION_ERROR, widget_secundario_error


@session_screen
def change_to_session_end(machine: MachineSession, request):
    widget_qrcode = cria_widget_qrcode(request)
    widget_qrcode.grid(row=0, column=1)
    return SESSION_END, widget_qrcode

@session_screen
def change_to_session_countdown():
    widget_secundario_timer.grid(row=0, column=1)
    return SESSION, widget_secundario_timer

def set_countdown(countdown: int):
    label_timer.set(str(countdown))
    if current_screen != SESSION:
        change_to_session_countdown()

def run():
    change_to_main_screen()
    APP.mainloop()
