import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

# 3.0

## AGGIORNAMENTO PRINCIPALE – Refactor logico e miglioramenti UX/QoL

## CHANGELOG:
# - Introdotta una gestione avanzata degli errori per richieste HTTP e input dell’utente 
# - Ottimizzata la logica di selezione tra player disponibili e qualità dello stream  
# - Implementata un’opzione per procedere senza fare l'aggiornamento dell'applicazione (NB: Utilizzerai la versione attuale, consigliamo di fare gli aggiornamenti
#   per mantenere il programma aggiornato da eventuali bug riscontrati e/o migliorie generali.)


def check_for_updates():
    try:
        # Link al file della versione remota
        version_url = "https://pastebin.com/raw/asYWrVC0"
        remote_version = requests.get(version_url).content.decode('utf-8').strip()
        
        # Lettura della versione locale
        local_version_path = 'version.txt'
        if not os.path.exists(local_version_path):
            # Se il file locale non esiste, crearlo con una versione predefinita
            with open(local_version_path, 'w') as f:
                f.write("0.0.0")
        local_version = open(local_version_path, 'r').read().strip()
        
        if remote_version != local_version:
            print(f"Una nuova versione ({remote_version}) è disponibile.")
            user_choice = input("Vuoi scaricare l'aggiornamento? (s/n): ").strip().lower()
            if user_choice == 's':
                # Link ai file aggiornati
                main_file_url = "https://raw.githubusercontent.com/xLamday/Twitch-Viewer-Bot/refs/heads/main/main.py"  # URL al file main.py
                version_file_url = "https://pastebin.com/raw/asYWrVC0"  # URL al file version.txt

                try:
                    # Scarica e salva main.py
                    print("Scaricamento di main.py...")
                    main_content = requests.get(main_file_url).content.decode('utf-8')
                    with open('main.py', 'w', encoding='utf-8') as main_file:
                        main_file.write(main_content)

                    # Scarica e salva version.txt
                    print("Scaricamento di version.txt...")
                    version_content = requests.get(version_file_url).content.decode('utf-8')
                    with open('version.txt', 'w') as version_file:
                        version_file.write(version_content)

                    print("Aggiornamento completato con successo!")
                    time.sleep(5)
                    os.system("cls")
                except requests.RequestException as errore:
                    print(f"Errore durante il download dei file: {errore}")
                return False
            else:
                print('')
                print(f"Aggiornamento annullato. Procedo con la versione attuale!\n\nVersione attuale: {local_version}")
                main()
                return False
        else:
            #print("Il programma è già aggiornato.")
            return True
    except requests.RequestException as errore:
        print(f"Errore durante il controllo degli aggiornamenti: {errore}")
        return True

def save_settings(twitch_username, set_160p):
    with open('settings.txt', 'w') as file:
        file.write(f"Twitch Username: {twitch_username}\n")
        file.write(f"Set 160p: {set_160p}\n")    

def load_settings():
    try:
        with open('settings.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                twitch_username = lines[0].split(': ')[1].strip()
                set_160p = lines[1].split(': ')[1].strip()
                return twitch_username, set_160p
    except:
        pass
    return None, None

def set_stream_quality(driver):
    wait = WebDriverWait(driver, 15)

    try:
        element_video_xpath = "//div[@data-test-selector='sad-overlay' or @data-a-target='player-overlay-click-handler']"
        element_video = wait.until(EC.presence_of_element_located((By.XPATH, element_video_xpath)))
    except Exception as errore:
        print("Impossibile trovare il video. Assicurati che il video sia caricato.")
        print(f"{errore}")
        return

    # Porta il cursore sul video per mostrare i controlli
    actions = ActionChains(driver)
    actions.move_to_element(element_video).perform()

    # Clicca il pulsante Impostazioni
    try:
        settings_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Impostazioni']")))
        settings_button.click()
    except Exception as errore:
        print("Non è stato possibile trovare il pulsante Impostazioni.")
        print(f"{errore}")
        return

    # Clicca sull'opzione 'Qualità'
    try:
        quality_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Qualità']")))
        quality_option.click()
    except Exception as errore:
        print("Non è stato possibile trovare l'opzione Qualità.")
        print(f"{errore}")
        return

    # Seleziona il livello di qualità più basso
    try:
        quality_levels_parent = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-a-target='player-settings-menu']")))
        quality_levels = quality_levels_parent.find_elements(By.XPATH, './*')

        # Seleziona l'ultima opzione (bassa qualità)
        if quality_levels:
            last_quality_option = quality_levels[-1]
            last_quality_option.click()
        else:
            print("Non sono stati trovati livelli di qualità.")
    except Exception as errore:
        print("Errore durante il caricamento delle opzioni di qualità.")
        print(f"{errore}")
        return

def main():
    
    twitch_username, set_160p = load_settings()

    os.system(f"title xLamday - Twitch Viewer Bot @xLamday ")

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
           

                    ██╗  ██╗██╗      █████╗ ███╗   ███╗██████╗  █████╗ ██╗   ██╗
                    ╚██╗██╔╝██║     ██╔══██╗████╗ ████║██╔══██╗██╔══██╗╚██╗ ██╔╝
                     ╚███╔╝ ██║     ███████║██╔████╔██║██║  ██║███████║ ╚████╔╝ 
                     ██╔██╗ ██║     ██╔══██║██║╚██╔╝██║██║  ██║██╔══██║  ╚██╔╝  
                    ██╔╝ ██╗███████╗██║  ██║██║ ╚═╝ ██║██████╔╝██║  ██║   ██║   
                    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   
  
 E' possibile fare migliorie al codice. Se riscontri un errore, visita il mio discord.
                             Discord discord.gg/yzreKA4xZD   
                             Github  github.com/xLamday    """)))

    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    # Seleziona proxy server
    print(Colors.green, "Proxy Server 1 è raccomandato")
    print(Colorate.Vertical(Colors.green_to_blue, "Seleziona un proxy server (1,2,3..):"))
    for i in range(1, 7):
        print(Colorate.Vertical(Colors.red_to_blue, f"Proxy Server {i}"))
    try:
        proxy_choice = int(input("> "))
        proxy_url = proxy_servers.get(proxy_choice, proxy_servers[1])
    except ValueError:
        print("Scelta non valida. Imposto la proxy di default (1).")
        proxy_url = proxy_servers[1]

    if twitch_username is None or set_160p is None:
        twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Inserisci il nome del canale (e.g xlamday): "))
        set_160p = input(Colorate.Vertical(Colors.purple_to_red, "Vuoi impostare la qualità a 160p? (si/no): "))
        save_settings(twitch_username, set_160p)
    else:
        use_settings = input(Colorate.Vertical(Colors.green_to_blue, "Vuoi utilizzare le tue impostazioni salvate? (si/no): "))
        if use_settings.lower() == "no":
            twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Inserisci il nome del canale (e.g xlamday): "))
            set_160p = input(Colorate.Vertical(Colors.purple_to_red, "Vuoi impostare la qualità a 160p? (si/no): "))
            save_settings(twitch_username, set_160p)

    try:
        proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "Quanti spettatori vuoi inviare? ")))
    except ValueError:
        print("Input o numero non valido.")
        time.sleep(2)
        proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "Quanti spettatori vuoi inviare? ")))

    if not twitch_username and not set_160p:
        if not twitch_username and not set_160p:
            print("Non hai inserito nessun valore!")
        elif not twitch_username:
            print("Inserisci un nickname di uno streamer!")
        else:  # set_160p non impostato
            print("Impossibile avviare lo script senza specificare la qualità bassa o meno")
        time.sleep(2)
        os.system("cls") 
        main()
        return # Assicurati di uscire dalla funzione dopo main()

    os.system("cls")
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""

                    ██╗  ██╗██╗      █████╗ ███╗   ███╗██████╗  █████╗ ██╗   ██╗
                    ╚██╗██╔╝██║     ██╔══██╗████╗ ████║██╔══██╗██╔══██╗╚██╗ ██╔╝
                     ╚███╔╝ ██║     ███████║██╔████╔██║██║  ██║███████║ ╚████╔╝ 
                     ██╔██╗ ██║     ██╔══██║██║╚██╔╝██║██║  ██║██╔══██║  ╚██╔╝  
                    ██╔╝ ██╗███████╗██║  ██║██║ ╚═╝ ██║██████╔╝██║  ██║   ██║   
                    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   

 E' possibile fare migliorie al codice. Se riscontri un errore, visita il mio discord.
                             Discord discord.gg/yzreKA4xZD    
                             Github  github.com/xLamday    """)))
    print('')
    print('')

    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")

    ## INIT DRIVER AS NONE
    driver = None
    
    # ADBLOCK EXT
    extension_path = 'adblock.crx'
    chrome_options.add_extension(extension_path)
    
    ## CHECK FOR DRIVER_PATH
    if driver_path:
        driver = webdriver.Chrome(options=chrome_options)
    
    print('')
    print(Colors.red, Center.XCenter("Inizializzo gli spettatori... Aspetta qualche minuto... non chiudere questa finestra!"))
    print('')
    print(Colors.red, Center.XCenter("Se gli spettatori non dovessero funzionare correttamente, prova a riavviare il programma e rifare le operazioni."))
    print('')
    
    try:
        driver.get(proxy_url)
        for i in range(proxy_count):
            driver.switch_to.new_window('tab')
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)
        

            try:
                # Trova la casella di testo e inserisce l'URL di Twitch
                text_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'url'))
                )
                text_box.send_keys(f'www.twitch.tv/{twitch_username}')
                text_box.send_keys(Keys.RETURN)
                print(f"[{i}] Spettatore aggiunto.")
            except Exception as e:
                print(f"[{i + 1}] Errore durante l'aggiunta dello spettatore: {e}")

        if set_160p in ["yes", "si"]:
            for i in range(proxy_count):
                driver.switch_to.window(driver.window_handles[i+1])
                element_video_xpath = "//div[@data-a-target='player-overlay-click-handler']"
                WebDriverWait(driver, 30).until( EC.presence_of_element_located((By.XPATH, element_video_xpath)))
                try:
                    set_stream_quality(driver)
                    print(f"[{i}] Qualità bassa impostata!")
                except Exception as err:
                    print(f"[{i}] Impossibile impostare la qualità bassa")
        else:
            for i in range(proxy_count):
                driver.switch_to.window(driver.window_handles[i+1])

        while True:
            time.sleep(60)
            print("Riavvio in corso delle pagine!")
            for pagine in driver.window_handles:
                driver.switch_to.window(pagine)
                driver.refresh()
    finally:
        if driver:
            driver.quit()
            


if __name__ == '__main__':
    check_for_updates()
    main()
