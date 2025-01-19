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
                except Exception as e:
                    print(f"Errore durante il download dei file: {e}")
                return False
            else:
                print("Aggiornamento annullato.")
                return False
        else:
            return True
    except Exception as e:
        print(f"Errore durante il controllo degli aggiornamenti: {e}")
        return True

def save_settings(twitch_username):
    with open('settings.txt', 'w') as file:
        file.write(f"Twitch Username: {twitch_username}\n")
        #file.write(f"Set 160p: {set_160p}\n")    

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

def print_announcement():
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/announcement.txt", headers={"Cache-Control": "no-cache"})
        announcement = r.content.decode('utf-8').strip()
        return announcement
    except:
        print("Could not retrieve announcement from GitHub.\n")

def reopen_pages(driver, proxy_url, twitch_username, proxy_count):
    """Funzione per chiudere e riaprire periodicamente le pagine proxy."""
    while True:
        print(Colors.yellow, Center.XCenter("Chiudendo e riaprendo le pagine proxy..."))

        # Chiude tutte le finestre tranne la prima
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()

        # Riapre le finestre richieste
        driver.switch_to.window(driver.window_handles[0])
        for i in range(proxy_count):
            driver.execute_script("window.open('')")  # Open a new empty window
            new_window_handle = driver.window_handles[-1]  # Get the handle of the newly opened window
            driver.switch_to.window(new_window_handle)
            driver.get(proxy_url)

            time.sleep(2)  # Aggiungi un ritardo per il caricamento della pagina

            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)

        time.sleep(60)  # Attendi 60 secondi prima di riaprire

def main():
    if not check_for_updates():
        return

    twitch_username = load_settings()

    os.system(f"title xLamday - Twitch Viewer Bot @xLamday ")

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
           

                    __                          __             
             _  __ / /   ____ _ ____ ___   ____/ /____ _ __  __
            | |/_// /   / __ `// __ `__ \ / __  // __ `// / / /
            _>  < / /___/ /_/ // / / / / // /_/ // /_/ // /_/ / 
            /_/|_|/_____/\__,_//_/ /_/ /_/ \__,_/ \__,_/ \__, /  
                                                        /____/   

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

    # Selecting proxy server
    print(Colors.green, "Proxy Server 1 è raccomandato")
    print(Colorate.Vertical(Colors.green_to_blue, "Seleziona un proxy server (1,2,3..):"))
    for i in range(1, 7):
        print(Colorate.Vertical(Colors.red_to_blue, f"Proxy Server {i}"))
    proxy_choice = int(input("> "))
    proxy_url = proxy_servers.get(proxy_choice)

    if twitch_username is None:
        twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Inserisci il nome del canale (e.g xlamday): "))
        save_settings(twitch_username)
    else:
        use_settings = input(Colorate.Vertical(Colors.green_to_blue, "Vuoi utilizzare le tue impostazioni salvate? (si/no): "))
        if use_settings.lower() == "no":
            twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Inserisci il nome del canale (e.g xlamday): "))
            save_settings(twitch_username)

    proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "Quanti spettatori vuoi inviare? ")))
    os.system("cls")
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""

                        __                          __             
                _  __ / /   ____ _ ____ ___   ____/ /____ _ __  __
                | |/_// /   / __ `// __ `__ \ / __  // __ `// / / /
                _>  < / /___/ /_/ // / / / / // /_/ // /_/ // /_/ / 
                /_/|_|/_____/\__,_//_/ /_/ /_/ \__,_/ \__,_/ \__, /  
                                                            /____/   

 E' possibile fare migliorie al codice. Se riscontri un errore, visita il mio discord.
                             Discord discord.gg/yzreKA4xZD    
                             Github  github.com/xLamday    """)))
    print('')
    print('')
    print(Colors.red, Center.XCenter("Spettatori in invio. Non avere fretta. Se gli spettatori non dovessero funzionare correttamente, prova a riavviare il programma e rifare le operazioni."))

    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    # ADBLOCK EXT
    extension_path = 'adblock.crx'
    chrome_options.add_extension(extension_path)
    driver = webdriver.Chrome(options=chrome_options)

    # pagine iniziali
    driver.get(proxy_url)
    for i in range(proxy_count):
        driver.switch_to.new_window('tab')
        driver.get(proxy_url)

        time.sleep(0.3)  # ritardo per il caricamento della pagina

        text_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'url'))
        )
        text_box.send_keys(f'www.twitch.tv/{twitch_username}')
        text_box.send_keys(Keys.RETURN)

    # Riapri periodicamente le pagine
    reopen_pages(driver, proxy_url, twitch_username, proxy_count)

if __name__ == '__main__':
    main()
