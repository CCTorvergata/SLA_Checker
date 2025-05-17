import re
from sla import *

def process_team_row(team_row, service_names):
    # Estrai le colonne (td) e stampa la SLA
    columns = team_row.find_all("td")
    for i, td in enumerate(columns):
        if i == 0:
            print(f"\n\033[1;33m{'Posizione: ' + td.get_text(strip=True):^50}\033[0m\n")
        elif i != 1 & i != 2:
            sla_text = td.get_text(strip=True)
            #print(sla_text) # Stampa il testo grezzo per debug
            # Estrai i valori tra parentesi tonde: attacco (primo), difesa totale (secondo), flag perse (terzo)
            flag_matches = re.findall(r"\(([-\d]+)\)", sla_text)
            attack_value = flag_matches[0] if len(flag_matches) > 0 else "0"
            if attack_value == "0":
                attack_catched = "0"
                defense_value = flag_matches[1] if len(flag_matches) > 1 else "0"
                flags_lost = flag_matches[2] if len(flag_matches) > 2 else "0"
            else:
                attack_catched = flag_matches[1] if len(flag_matches) > 0 else "0"
                defense_value = flag_matches[2] if len(flag_matches) > 1 else "0"
                if defense_value == "0":
                    flags_lost = "0"
                else:
                    flags_lost = flag_matches[3] if len(flag_matches) > 2 else "0"
            match = re.search(r"(\d+\.\d+%)\s*([+-]\d+\.\d+)?", sla_text)
            if match:
                if i == 4:
                    sla_values = []
                    flag_values = []
                    attack_catched_values = []
                sla_value = match.group(1)
                sla_change = match.group(2) if match.group(2) else ""
                service_name = service_names[i - 5] if (i - 5) < len(service_names) else f"Servizio {i-4}"

                # Usa la funzione estratta per processare i valori
                process_sla_column(
                    sla_value, sla_change, service_name, flags_lost, attack_catched,
                    sla_values, flag_values, attack_catched_values,
                    match, i, columns, service_names
                )