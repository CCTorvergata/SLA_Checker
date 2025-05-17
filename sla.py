from printer import *
from console import *
from service import *

def process_sla_column(sla_value, sla_change, service_name, flags_lost, attack_catched,
                      sla_values, flag_values, attack_catched_values,
                      match, i, columns, service_names):
    # Estrai valori da match e service_names
    sla_value = match.group(1)
    sla_change = match.group(2) or ""
    service_name = service_names[i - 5] if (i - 5) < len(service_names) else f"Servizio {i-4}"

    # Inizializza le liste solo se necessario
    if i == 4:
        sla_values.clear()
        flag_values.clear()
        attack_catched_values.clear()

    # Aggiungi valori colorati alle rispettive liste
    sla_values.append(f"{sla_value} {sla_change}".strip())
    flag_values.append(color_value(flags_lost))
    attack_catched_values.append(color_value(attack_catched))

    # Stampa la matrice se è l'ultima colonna
    if i == len(columns) - 1:
        print_service_matrix(service_names, sla_values, flag_values, attack_catched_values)

    # Avvisa se lo SLA è negativo
    if sla_change and not sla_change.startswith("+"):
        print_alert(f"SLA change is negative for \033[1;31m{service_name}\033[0m: \033[91m{sla_change}\033[0m")