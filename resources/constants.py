import os

# Variables globales - rutas
HEADER_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "header.txt")
PROFILES_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "profiles.json")
TARIFFS_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "tariffs.json")
TARIFFS_DAYS = 31

# Funciones globales - utils
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_header():
    with open(HEADER_FILE_PATH, "r") as file:
        header = file.read()
    print(header)