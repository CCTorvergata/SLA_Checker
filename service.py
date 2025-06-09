from printer import *
from console import *
from main import URL

def extract_service_names(thead_rows):
    service_names = []
    # Cerca la riga che contiene le intestazioni dei servizi (dopo Team, Score, ecc.)
    services_row = None
    for row in thead_rows:
        ths = row.find_all("th")
        # Cerca una riga con almeno 5 colonne (Team, Score, e almeno un servizio)
        if len(ths) >= 5:
            # Prendi i nomi dei servizi saltando le prime 3 colonne (icone, Team, Score)
            service_names = [th.get_text(strip=True) for th in ths[3:]]
            services_row = row
            break
    if services_row:
        clear_console()

        print_header()
        print_info(f"Caricamento della pagina {URL}...")
        print("\033[92mServizi trovati:\033[0m")
        header = " | ".join([f"{name:^15}" for name in service_names])
        width = len(header)
        print("\n" + header.center(width))
        print("-" * width)
        print_info("Controllo SLA per i servizi...")
    else:
        print("Impossibile trovare la riga dei servizi nel thead.")
    return service_names

def print_service_matrix(service_names, sla_values, flag_values, attack_catched_values):
    # Colori per le intestazioni e i valori
    header = " | ".join([f"\033[1;36m{name:^15}\033[0m" for name in service_names])
    values = []
    for val in sla_values:
        if "-" in val:
            values.append(f"\033[1;31m{val:^15}\033[0m")  # Rosso per valori negativi
        elif val.strip().startswith("0.00% -"):
            values.append(f"\033[1;33m{val:^15}\033[0m")  # Giallo per valori appena diminuiti
        else:
            values.append(f"\033[1;32m{val:^15}\033[0m")  # Verde per valori positivi
    values_line = " | ".join(values)
    flag_line = " | ".join(flag_values)
    attack_line = " | ".join(attack_catched_values)
    width = len(header)-10
    print("\n" + f"{'Name':<8} | {header}".center(width))
    print("-" * width)
    print(f"{'SLA':<8} | {values_line}".center(width))
    print(f"{'defense':<8} | {flag_line}".center(width))
    print(f"{'attack':<8} | {attack_line}".center(width) + "\n")