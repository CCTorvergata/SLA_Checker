from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time

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
        print(f"[INFO] Caricamento della pagina: {URL}")
        driver.get(URL)
        time.sleep(WAIT_TIME)  # Attendi che il JS abbia finito di popolare i dati

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Trova la seconda riga del thead che contiene i nomi dei servizi
        thead_rows = soup.select("thead tr")
        if len(thead_rows) >= 2:
            services_row = thead_rows[1]
            service_names = [th.get_text(strip=True) for th in services_row.find_all("th")[4:]]  # Salta le prime 4 colonne (Team, Score...)

            print("Servizi trovati:")
            for name in service_names:
                SERVICE.append(name)
                print(name)
        else:
            print("Impossibile trovare la riga dei servizi nel thead.")

        # Trova tutte le righe della tabella
        rows = soup.find_all("tr")
        if not rows:
            print("[ERROR] Nessuna riga trovata nella tabella. I maledetti hanno cambiato tutto!")
            driver.quit()
            exit(1)

        team_row = None

        for tr in rows:
            text = tr.get_text(strip=True)
            if TEAM_IP in text:
                team_row = tr
                break

        if team_row:
            print(f"[INFO] Trovata riga per IP: {TEAM_IP}")
            # Estrai le colonne (td) e stampa la SLA
            columns = team_row.find_all("td")
            for i, td in enumerate(columns):
                if i == 0:
                   print(f"Posizione: {td.get_text(strip=True)}")
                elif i != 1 & i != 2 & i != 3:
                    sla_text = td.get_text(strip=True)
                    match = re.search(r"(\d+\.\d+%)\s*([+-]\d+\.\d+)?", sla_text)
                    if match:
                        sla_value = match.group(1)
                        sla_change = match.group(2) if match.group(2) else ""
                        print(f"SLA {sla_value} {sla_change}")
                        if sla_change and not sla_change.startswith("+"):
                            print("[ALERT] SLA change is negative!")
                    else:
                        print("[ERROR] Unable to parse SLA data.")
        else:
            print(f"[ERROR] Nessuna riga trovata contenente l'IP {TEAM_IP}")

    except Exception as e:
        print(f"[ERROR] Si è verificato un errore: {e}")

    finally:
        driver.quit()

    print(f"[INFO] Attesa di {LOOP_INTERVAL} secondi prima del prossimo controllo...")
    time.sleep(LOOP_INTERVAL)
