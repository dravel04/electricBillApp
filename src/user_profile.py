import os
import json
from tabulate import tabulate

# Agregar la ruta al directorio que contiene constants.py al sys.path
from resources.constants import PROFILES_FILE_PATH,TARIFFS_FILE_PATH, TARIFFS_DAYS
from resources.constants import clear_screen, display_header


class UserProfile:
    def __init__(self):
        self.profiles = {}
        self.load_profiles()

    def load_profiles(self):
        if os.path.exists(PROFILES_FILE_PATH):
            try:
                with open(PROFILES_FILE_PATH, "r") as file:
                    self.profiles = json.load(file)
            except json.decoder.JSONDecodeError:
                # Si el archivo JSON está vacío o no tiene un formato válido,
                # inicializa self.profiles como un diccionario vacío
                self.profiles = {}

    def save_profiles(self):
        with open(PROFILES_FILE_PATH, "w") as file:
            json.dump(self.profiles, file)

    def new_profile(self):
        clear_screen()
        display_header()
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
        else:
            solar_excess = ""
        self.profiles[profile_id] = {
            "power_peak": float(power_peak),
            "power_valley": float(power_valley),
            "energy_peak": float(energy_peak),
            "energy_flat": float(energy_flat),
            "energy_valley": float(energy_valley),
            "solar_excess": float(solar_excess) if solar_excess else None,
        }
        self.save_profiles()
        print("\nPerfil creado correctamente.\n")

    def show_profiles(self):
        clear_screen()
        display_header()
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
        clear_screen()
        display_header()
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
        ERR_OPT = False
        while True:
            clear_screen()
            display_header()
            if ERR_OPT:
                print(f"'{option}' no es una opción válida.\n")
                ERR_OPT = False
            print(f"Datos del perfil '{profile_id}':")
            i=1
            print("0. Guardar cambios")
            for key, value in self.profiles[profile_id].items():
                if key == 'solar_excess' and value is None:
                    print(f"{i}. Añadir información solar (solar_excess)")
                else:
                    print(f"{i}. {key}: {value}")
                i += 1
            print(f"{i}. Atras")
            try:
                print("\nSeleccione el número del campo que desea editar:")
                option = input("Opción: ")
                option = int(option)
                if option == 0:
                    self.save_profiles()
                    print("Cambios guardados.")
                    break
                elif option == i:
                    break
                elif option > 0 and option <= len(self.profiles[profile_id]):
                    if option == 6 and self.profiles[profile_id]['solar_excess'] is None:
                        # Agregar información solar si solar_excess son None
                        solar_excess = input("Excedentes de energía solar (kWh): ")
                        self.profiles[profile_id]['solar_excess'] = float(solar_excess)
                        print("Información solar agregada correctamente.")
                        continue
                    field_index = option - 1
                    # convierte las claves del diccionario en una lista y luego accede a la clave en la posición field_index de esa lista
                    field_key = list(self.profiles[profile_id].keys())[field_index]
                    new_value = input(f"Ingrese el nuevo valor para '{field_key}': ")
                    self.profiles[profile_id][field_key] = float(new_value.replace(",", "."))
                    print(f"'{field_key}' actualizado a '{new_value}'")
                else:
                    ERR_OPT = True
            except ValueError:
                ERR_OPT = True

    def delete_profile(self, profile_id):
        confirmation = input(f"¿Estás seguro de que quieres borrar el perfil '{profile_id}'? (s/n): ")
        if confirmation.lower() == "s":
            del self.profiles[profile_id]
            self.save_profiles()
            print(f"Perfil '{profile_id}' eliminado correctamente.")

    def launch_comparison(self, profile_id):
        # Cargar las tarifas desde el archivo JSON
        tariffs = self.load_tariffs()
        # Obtener el perfil del usuario
        user_profile = self.profiles[profile_id]

        # Calcular el coste total para cada tarifa y almacenarlos en un diccionario
        costs = []
        for tariff_name, tariff_data in tariffs.items():
            # total_cost = self.calculate_total_cost(user_profile, tariff_data)
            power_cost, energy_cost, solar_cost, total_cost = self.calculate_total_cost(user_profile, tariff_data)
            # costs.append([tariff_name, total_cost])
            costs.append([tariff_name, power_cost, energy_cost, solar_cost, total_cost ])

        # Crear tabla de comparación
        # headers = ["Tarifa", "Coste Total"]
        headers = ["Tarifa","Coste Potencia","Coste Energia","Excendentes","Coste Total"]
        table = tabulate(costs, headers=headers, tablefmt="grid")

        # Mostrar tabla
        clear_screen()
        display_header()
        print("Comparativa de Tarifas:")
        print(table)

        # Encontrar la tarifa más conveniente
        best_tariff = min(costs, key=lambda x: x[1])
        # Mostrar resultados al usuario
        print("\nTarifa más interesante:", best_tariff[0])
        print("Coste total:", best_tariff[headers.index("Coste Total")], '€')

        # 'Bloqueamos' la pantalla para poder leer la comparitva
        input(f"\n(pulse cualquier tecla para continuar)")


    def load_tariffs(self):
        # Cargar las tarifas desde el archivo JSON
        with open(TARIFFS_FILE_PATH, "r") as file:
            tariffs = json.load(file)
        return tariffs

    def calculate_total_cost(self, user_profile, tariff_data):
        # Calcular el coste total para una tarifa específica
        power_cost = (user_profile["power_peak"] * tariff_data["power_peak"] + user_profile["power_valley"] * tariff_data["power_valley"]) * TARIFFS_DAYS
        energy_cost = user_profile["energy_peak"] * tariff_data["energy_peak"] + user_profile["energy_flat"] * tariff_data["energy_flat"] + user_profile["energy_valley"] * tariff_data["energy_valley"]
        
        # Verificar si hay excedentes de energía solar y calcular su coste
        solar_cost = 0
        if user_profile["solar_excess"] is not None:
            solar_cost = user_profile["solar_excess"] * tariff_data["solar_excess"]

        # Calcular el coste total sumando todos los componentes y añadiendo el coste de la batería virtual
        total_cost = power_cost + energy_cost + solar_cost + tariff_data.get("virtual_baterry", 0)

        # return total_cost
        return power_cost, energy_cost, solar_cost, total_cost
