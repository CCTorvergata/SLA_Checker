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

        # Trova tutte le righe della tabella
        rows = soup.find_all("tr")
        print(f"[DEBUG] Righe totali trovate: {len(rows)}")

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
                print(f"Colonna {i + 1}: {td.get_text(strip=True)}")
        else:
            print(f"[ERROR] Nessuna riga trovata contenente l'IP {TEAM_IP}")

    except Exception as e:
        print(f"[ERROR] Si è verificato un errore: {e}")

    finally:
        driver.quit()

    print(f"[INFO] Attesa di {LOOP_INTERVAL} secondi prima del prossimo controllo...")
    time.sleep(LOOP_INTERVAL)
