def print_header():
    # Stampa un'intestazione migliorata
    header_text = " SLA CHECKER "
    print("\033[1;36m" + "=" * 50 + "\033[0m")
    print("\033[1;36m" + header_text.center(50, " ") + "\033[0m")
    print("\033[1;36m" + "=" * 50 + "\033[0m")

def print_error(message):
    # Stampa un messaggio di errore
    print("\033[91m[ERROR]\033[0m " + message)

def print_success(message):
    # Stampa un messaggio di successo
    print("\033[92m[SUCCESS]\033[0m " + message)

def print_warning(message):
    # Stampa un messaggio di avviso
    print("\033[93m[WARNING]\033[0m " + message)

def print_info(message):
    # Stampa un messaggio informativo
    print("\033[94m[INFO]\033[0m " + message)

def print_debug(message):
    # Stampa un messaggio di debug
    print("\033[95m[DEBUG]\033[0m " + message)

def print_critical(message):
    # Stampa un messaggio critico
    print("\033[91m[CRITICAL]\033[0m " + message)

def print_alert(message):
    # Stampa un messaggio di allerta
    print("\033[1;31m[ALERT]\033[0m " + message)
    print('\a')  # Riproduce un suono (beep)