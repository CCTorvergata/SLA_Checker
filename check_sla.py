from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
import os

# Configurazione
URL = "http://10.10.0.1/scoreboard"
TEAM_IP = "10.60.61.1"
WAIT_TIME = 5  # Tempo di attesa per il caricamento JS
LOOP_INTERVAL = 1 # Intervallo tra i controlli (in secondi)
SERVICE = ["service1", "service2", "service3"]  # Servizi da controllare

# Imposta Chrome in modalità headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

while True:
    driver = webdriver.Chrome(options=options)
    try:
        print(f"\033[94m[INFO]\033[0m Caricamento della pagina: {URL}")
        driver.get(URL)
        time.sleep(WAIT_TIME)  # Attendi che il JS abbia finito di popolare i dati

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Trova la seconda riga del thead che contiene i nomi dei servizi
        thead_rows = soup.select("thead tr")
        if len(thead_rows) >= 2:
            services_row = thead_rows[1]
            service_names = [th.get_text(strip=True) for th in services_row.find_all("th")[3:]]  # Salta le prime 4 colonne (Team, Score...)
            os.system('cls' if os.name == 'nt' else 'clear')    # Pulisci la console

            print("\033[92mServizi trovati:\033[0m")
            header = " | ".join([f"{name:^15}" for name in service_names])
            width = len(header)
            print("\n" + header.center(width))
            print("-" * width)
            print("\n\033[94m[INFO]\033[0m Controllo SLA per i servizi...")
        else:
            print("Impossibile trovare la riga dei servizi nel thead.")

        # Trova tutte le righe della tabella
        rows = soup.find_all("tr")
        if not rows:
            print("\033[91m[ERROR]\033[0m Nessuna riga trovata nella tabella. I maledetti hanno cambiato tutto!")
            driver.quit()
            exit(1)

        team_row = None

        for tr in rows:
            text = tr.get_text(strip=True)
            if TEAM_IP in text:
                team_row = tr
                break

        if team_row:
            print(f"\033[94m[INFO]\033[0m Trovata riga per IP: {TEAM_IP}")
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
                    defense_value = flag_matches[1] if len(flag_matches) > 1 else "0"
                    flags_lost = flag_matches[2] if len(flag_matches) > 2 else "0"
                    match = re.search(r"(\d+\.\d+%)\s*([+-]\d+\.\d+)?", sla_text)
                    if match:
                        sla_value = match.group(1)
                        sla_change = match.group(2) if match.group(2) else ""
                        service_name = service_names[i - 5] if (i - 5) < len(service_names) else f"Servizio {i-4}"
                        # Salva i valori per la stampa successiva
                        if i == 4:
                            sla_values = []
                            flag_values = []
                        sla_values.append(f"{sla_value} {sla_change if sla_change else ''}")
                        # Colora il valore delle flag perse
                        if flags_lost == "0":
                            flag_colored = f"\033[1;32m{flags_lost:^15}\033[0m"  # Verde se 0
                        elif flags_lost.startswith("-") or int(flags_lost) > 0:
                            flag_colored = f"\033[1;31m{flags_lost:^15}\033[0m"  # Rosso se >0 o negativo
                        else:
                            flag_colored = f"\033[1;33m{flags_lost:^15}\033[0m"  # Giallo per altri casi
                        flag_values.append(flag_colored)

                        # Dopo aver raccolto tutti i valori, stampa la matrice su due righe con colori e centrata
                        if i == len(columns) - 1:
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
                            width = len(header)-10
                            print("\n" + header.center(width))
                            print("-" * width)
                            print(values_line.center(width))
                            print(flag_line.center(width) + "\n")
                        if sla_change and not sla_change.startswith("+"):
                            print("\n\033[1;31m[ALERT] SLA change is negative!\033[0m\n")
                            print('\a')  # Riproduce un suono (beep)
                    # else:
                    #     print("\033[91m[ERROR]\033[0m Unable to parse SLA data.")
        else:
            print(f"\033[91m[ERROR]\033[0m Nessuna riga trovata contenente l'IP {TEAM_IP}")

    except Exception as e:
        os.system('cls' if os.name == 'nt' else 'clear')    # Pulisci la console
        print(f"\033[91m[ERROR]\033[0m Si è verificato un errore: {e}")

    finally:
        driver.quit()

    print(f"\n\033[94m[INFO]\033[0m Attesa di {LOOP_INTERVAL} secondi prima del prossimo controllo...")
    time.sleep(LOOP_INTERVAL)
