import os
from printer import *
from chrome import *

def clear_console():
    # Pulisce la console
    os.system('cls' if os.name == 'nt' else 'clear')

def error_message(message, driver):
    print_error(message)
    stop_chrome(driver)
    exit(1)

def color_value(value):
    # Colora il valore delle flag perse
    if value == "0":
        value_colored = f"\033[1;32m{value:^15}\033[0m"  # Verde se 0
    elif value.startswith("-") or int(value) > 0:
        value_colored = f"\033[1;31m{value:^15}\033[0m"  # Rosso se >0 o negativo
    else:
        value_colored = f"\033[1;33m{value:^15}\033[0m"  # Giallo per altri casi
    return value_colored