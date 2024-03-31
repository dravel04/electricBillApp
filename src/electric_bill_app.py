import os
import json

# Variables globales - rutas
ERR_OPT = False
HEADER_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "header.txt")
PROFILES_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "profiles.json")

class ElectricBillApp:
    def __init__(self):
        self.profiles = {}
        self.load_profiles()

    clear_screen = lambda self: os.system("cls" if os.name == "nt" else "clear")
    
    def display_header(self):
        with open(HEADER_FILE_PATH, "r") as file:
            header = file.read()
        print(header)
        
    def display_menu(self):
        print("Seleccione una opción:")
        print("1. Nuevo Perfil")
        if self.profiles:
            print("2. Perfiles")

    def load_profiles(self):
        if os.path.exists(PROFILES_FILE_PATH):
            with open(PROFILES_FILE_PATH, "r") as file:
                self.profiles = json.load(file)

    def save_profiles(self):
        with open(PROFILES_FILE_PATH, "w") as file:
            json.dump(self.profiles, file)

    def new_profile(self):
        self.clear_screen()
        self.display_header()
        print("1. Nuevo Perfil")
        profile_id = input("Identificador del perfil: ")
        power_peak = input("Potencia en Punta (kW): ")
        power_valley = input("Potencia en Valle (kW): ")
        energy_peak = input("Energía en Punta (kWh): ")
        energy_flat = input("Energía en Llano (kWh): ")
        energy_valley = input("Energía en Valle (kWh): ")
        solar = input("¿Tiene energía solar? (s/n): ")
        if solar.lower() == "s":
            solar_excess = input("Excedentes de energía solar (kWh): ")
            solar_price = input("Precio al que se pagan los excedentes (€/kWh): ").replace(",", ".")
        else:
            solar_excess = ""
            solar_price = ""
        self.profiles[profile_id] = {
            "power_peak": float(power_peak),
            "power_valley": float(power_valley),
            "energy_peak": float(energy_peak),
            "energy_flat": float(energy_flat),
            "energy_valley": float(energy_valley),
            "solar_excess": float(solar_excess) if solar_excess else None,
            "solar_price": float(solar_price) if solar_price else None
        }
        self.save_profiles()
        print("\nPerfil creado correctamente.\n")

    def show_profiles(self):
        self.clear_screen()
        self.display_header()
        print("Perfiles existentes:")
        for index, profile_id in enumerate(self.profiles.keys(), 1):
            print(f"{index}. {profile_id}")
            
        while True:
            try:
                profile_index = int(input("Seleccione un perfil para ver las opciones: ")) - 1
                if profile_index < 0 or profile_index >= len(self.profiles):
                    print("Por favor, selecione un perfil válido")
                    continue  # Volver a solicitar la entrada
                selected_profile_id = list(self.profiles.keys())[profile_index]
                break  # Salir del bucle si el número es válido
            except ValueError:
                print("Por favor, selecione un perfil válido")

        selected_profile_id = list(self.profiles.keys())[profile_index]
        self.clear_screen()
        self.display_header()
        print(f"Datos del perfil '{selected_profile_id}':")
        for key, value in self.profiles[selected_profile_id].items():
            print(f"{key}: {value}")
        print(f"\nOpciones:")
        print("1. Editar perfil")
        print("2. Lanzar comparativa")
        print("3. Borrar perfil")
        print("4. Atras")
        option = input("Seleccione una opción: ")
        if option == "1":
            self.edit_profile(selected_profile_id)
        elif option == "2":
            self.launch_comparison(selected_profile_id)
        elif option == "3":
            self.delete_profile(selected_profile_id)
        elif option == "4":
            pass

    def edit_profile(self, profile_id):
        while True:
            self.clear_screen()
            self.display_header()
            print(f"Datos del perfil '{profile_id}':")
            i=1
            print("0. Guardar cambios")
            for key, value in self.profiles[profile_id].items():
                print(f"{i}. {key}: {value}")
                i += 1
            try:
                print("\nSeleccione el número del campo que desea editar:")
                option = int(input("Opción: "))
                if option == 0:
                    self.save_profiles()
                    print("Cambios guardados.")
                    break
                elif option > 0 and option <= len(self.profiles[profile_id]):
                    field_index = option - 1
                    # convierte las claves del diccionario en una lista y luego accede a la clave en la posición field_index de esa lista
                    field_key = list(self.profiles[profile_id].keys())[field_index]
                    new_value = input(f"Ingrese el nuevo valor para '{field_key}': ")
                    self.profiles[profile_id][field_key] = float(new_value.replace(",", "."))
                    print(f"'{field_key}' actualizado a '{new_value}'")
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    def launch_comparison(self, profile_id):
        # Implementa la lógica para comparar tarifas
        print("Función en desarrollo.")

    def delete_profile(self, profile_id):
        confirmation = input(f"¿Estás seguro de que quieres borrar el perfil '{profile_id}'? (s/n): ")
        if confirmation.lower() == "s":
            del self.profiles[profile_id]
            self.save_profiles()
            print(f"Perfil '{profile_id}' eliminado correctamente.")

    def run(self):
        global ERR_OPT
        try:
            while True:
                self.clear_screen()
                self.display_header()
                if ERR_OPT:
                    print(f"'{option}' no es una opción válida.\n")
                    ERR_OPT = False
                self.display_menu()
                option = input("Opción: ")
                if option.lower() == "qq":
                    self.clear_screen()
                    print("\nSaliendo de la aplicación...\n")
                    break
                elif option == "1":
                    self.new_profile()
                elif option == "2" and self.profiles:
                    self.show_profiles()
                else:
                    ERR_OPT = True
        except (KeyboardInterrupt, EOFError):
            self.clear_screen()
            print("\nSaliendo de la aplicación...\n")
