from bs4 import BeautifulSoup
import time
from team_row import *
from printer import *
from console import *
from chrome import *
from service import *
from selenium.common.exceptions import WebDriverException

# Configurazione
URL = "http://10.10.0.1/scoreboard"
TEAM_IP = "10.60.61.1"
WAIT_TIME = 5  # Tempo di attesa per il caricamento JS
LOOP_INTERVAL = 1 # Intervallo tra i controlli (in secondi)

def main():
    clear_console()
    print_header()
    print_info(f"Caricamento della pagina {URL}...")
    while True:
        driver = start_chrome()
        try:
            driver.get(URL)
            time.sleep(WAIT_TIME)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            thead_rows = soup.select("thead tr")
            service_names = extract_service_names(thead_rows)
            rows = soup.find_all("tr")

            if not rows:
                error_message("Nessuna riga trovata nella tabella. I maledetti hanno cambiato tutto!", driver)

            team_row = next((tr for tr in rows if TEAM_IP in tr.get_text(strip=True)), None)

            if team_row:
                print_info(f"Riga trovata per IP: {TEAM_IP}")
                process_team_row(team_row, service_names)
            else:
                print_error(f"Nessuna riga trovata contenente l'IP {TEAM_IP}")

        except WebDriverException as e:
            print_error(f"Errore WebDriver: {e.msg}")
            if driver:
                stop_chrome(driver)
            print_info("Riavvio il driver tra 5 secondi...")
            time.sleep(5)
            continue  # Riprova subito il ciclo
        except Exception as e:
            clear_console()
            print_error("Si è verificato un errore durante il caricamento della pagina o l'analisi dei dati: " + str(e))
        finally:
            stop_chrome(driver)

        print_info(f"Attesa di {LOOP_INTERVAL} secondi prima del prossimo controllo...")
        time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main()
