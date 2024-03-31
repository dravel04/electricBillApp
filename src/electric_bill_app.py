import os
from src.test_profile import UserProfile

# Importamos funciones utils
from resources.constants import clear_screen, display_header

class ElectricBillApp:
    def __init__(self):
        self.user_profile = UserProfile()
        clear_screen()

    def display_menu(self):
        print("Seleccione una opción:")
        print("1. Nuevo Perfil")
        if self.user_profile.profiles:
            print("2. Perfiles")

    def run(self):
        ERR_OPT = False
        try:
            while True:
                clear_screen()
                display_header()
                self.display_menu()
                if ERR_OPT:
                    print(f"'{option}' no es una opción válida.\n")
                    ERR_OPT = False
                option = input("Opción: ")
                if option.lower() == "qq":
                    clear_screen()
                    print("\nSaliendo de la aplicación...\n")
                    break
                elif option == "1":
                    clear_screen()
                    display_header()
                    self.user_profile.new_profile()
                elif option == "2" and self.user_profile.profiles:
                    clear_screen()
                    display_header()
                    self.user_profile.show_profiles()
                else:
                    ERR_OPT = True
        except (KeyboardInterrupt, EOFError):
            clear_screen()
            print("\nSaliendo de la aplicación...\n")