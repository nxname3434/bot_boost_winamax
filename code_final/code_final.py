#CREATION DRIVER
from selenium_stealth import stealth
import undetected_chromedriver as uc


def create_driver(headless=True):
   
    #Crée un driver avec des options améliorées pour éviter la détection
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        # Masque le mode headless dans l'user agent
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')
        
        # Ajoute des plugins simulés
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-infobars')
        
        # Simule des propriétés WebGL
        options.add_argument('--use-angle=default')
        options.add_argument('--use-gl=desktop')
    
    driver = uc.Chrome(options=options)
    
    # Masque les signatures d'automation de Selenium
    stealth(driver,
            languages=["fr-FR", "fr"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    
    return driver

#FONCTION DE PRISE DE PARI
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



mdp="ton_mdp"
login="ton_login_winamax"
date_naissance="ta_date_naissance"



def placer_pari(extracted_text):
    try :
        #connexion à winamax avec le driver anti-détection
        driver = create_driver()
        wait = WebDriverWait(driver, 10)
        driver.get('https://www.winamax.fr/')
        
        # Accepte les cookies
        coockies = wait.until(EC.element_to_be_clickable((By.ID, 'tarteaucitronPersonalize2')))
        time.sleep(random.uniform(2, 5))
        coockies.click()

        # Se connecte
        login = wait.until(EC.element_to_be_clickable((By.ID, 'login-link')))
        time.sleep(random.uniform(2, 5))
        login.click()

        # Change vers l'iframe de connexion
        iframe = wait.until(EC.presence_of_element_located((By.ID, 'iframe-login')))
        driver.switch_to.frame(iframe)
        
        # Entre les informations de connexion
        identifiant = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-dovzVR.hleAgw.sc-dsqxVi.eEXNCD')))
        password = driver.find_element(By.CSS_SELECTOR, '.sc-dovzVR.hleAgw.sc-dsqxVi.sc-krMcUs.eEXNCD.cufNSR')
        time.sleep(random.uniform(2, 5))
        identifiant.send_keys(login)
        password.send_keys(mdp)
        time.sleep(random.uniform(2, 5))
        password.send_keys(Keys.RETURN)
        print("identifiants envoyés")
        
        # Attend la redirection et revient à la page principale
        driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.ID, 'iframe-login')))
        driver.switch_to.frame(iframe)
        
        # prend un screenshot en debug, pour voir si la connexion est réussie
        time.sleep(random.uniform(2, 5))
        driver.save_screenshot('postconnexion.png')

        try :
            #si on est connecté, met la date de naissance
            date_naissance = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-dovzVR.hleAgw.sc-dsqxVi.sc-gfXbYt.eEXNCD.fdjnFX')))
            print("connexion réussie")
            time.sleep(2)
            date_naissance.send_keys(date_naissance)
        
            # Soumet la date de naissance au site
            driver.switch_to.default_content()
            iframe = wait.until(EC.presence_of_element_located((By.ID, 'iframe-login')))
            driver.switch_to.frame(iframe)
            enter = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-gutikT.sc-huvEkS.sc-dIcdns.gNLNtX.lAAPw.ecbpVV')))
            time.sleep(random.uniform(2, 5))
            enter.click()
            time.sleep(random.uniform(2, 5))
            driver.switch_to.default_content()
            time.sleep(2)
            
            #se dirige vers la page des paris sportifs
            paris_sportifs_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/paris-sportifs"]')))
            time.sleep(2)
            paris_sportifs_link.click()
            print("accés aux pari sportifs")
            
            #ici, on peut si on veut rafraichir la page afin d'éviter les inatendus, comme les pops up winamax à cause d'un nouvel évenement
            
            #se dirige vers l'onglet des cotes boostées
            cote_boostee = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/paris-sportifs/sports/100000"]')))
            time.sleep(2)
            cote_boostee.click()

        
            # Attend le chargement des cotes boostées
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-kYlkCV.gmahBT")))
            print("cotes boostées visibles")
            
            
            # Récupére tous les éléments correspondant aux événements
            evenements = driver.find_elements(By.CLASS_NAME, "sc-kYlkCV.gmahBT")
            
            for evenement in evenements:
                try:
                    # Vérifie si l'intitulé des cotes boostées correspond à la chaîne cible
                    try:
                # Essaye de trouver l'intitulé parmi toutes les cotes boostées
                        intitule = evenement.find_element(By.CLASS_NAME, "sc-fmNzgT.fxGKjy").text
                    except:
                        try:
                            # Si la première classe n'est pas trouvée, essaye avec la seconde classe (les classes des GCB sont parfois différentes)
                            intitule = evenement.find_element(By.CLASS_NAME, "sc-iUJSKd.iWJAHx").text
                        except:
                            # Si aucun des éléments n'est trouvé, définir intitule comme vide (ou autre valeur par défaut)
                            intitule = "fail"
        
                    if intitule == extracted_text:
                        print(f"Intitulé trouvé : {intitule}")
                       
                        # Trouve et clique sur l'élément de cote si l'intitulé correspond
                        cote_element = evenement.find_element(By.CLASS_NAME, "sc-joYSUE.jtELyW")
                        cote_element.click()
                        print("Cote cliquée avec succès")
                        time.sleep(2)               
                        mise = driver.find_element(By.XPATH, "//input[@class='sc-fYBlTd gCyNMg']")
                        mise.click()
                        mise.send_keys(Keys.DELETE)
                        time.sleep(1)
                        
                        #mise de 10 euros sur la cote boostée
                        mise.send_keys(10)
                        print("mise ajustée avec succès")
                        pari=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-gREbXw.kdUkdw')))
                        pari.click()
                        print("pari réussi")
                        
                        #attend, quitte winamax et ferme le navigateur
                        time.sleep(10)
                        driver.quit()
                        break  # Sortir de la boucle si vous voulez cliquer sur le premier événement correspondant
                except Exception as e:
                    print(f"Erreur lors de la vérification de l'événement : {e}")
        except :
            print("échec / le driver a été détecté")
            # Fermeture du navigateur après placement du pari
            driver.quit()
    except :
        print("erreur globale lors de création du driver ou phase d'initialisation de la fonction")

#BOT D'ECOUTE TELEGRAM
from telethon import TelegramClient, events
import re

# Remplacez par vos identifiants donné aprés création de l'application telegram
api_id = ''
api_hash = ''
supergroupe_nom = "" #remplacez par le nom du groupe ou se trouve le bot @grosse_cbot

# Thread principal
async def main():
    # Crée une instance du client Telegram
    client = TelegramClient('session_automatisation', api_id, api_hash)

    # se connecte au client
    await client.start()
    print(f"Connecté à Telegram. En attente de messages dans le supergroupe {supergroupe_nom}...")

    # Gère les nouveaux messages
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        chat = await event.get_chat()
        if chat.title == supergroupe_nom:
            message = event.message.message
            match = re.search(r'💡(.*?)\n', message) #extrait la cote en string du message recu
            
            if match:
                extracted_text = match.group(1).strip()  # Supprime les espaces autour du texte extrait
                print(f"Texte extrait : {extracted_text}")
                
                # Appele la fonction de prise de pari, avec l'intitulé de la cote
                print(f"prise de la cote {extracted_text}")
                #placer_pari(extracted_text) indenté car ce code présente uniquement la partie alerte de sortie d'une cote boostée
                
            else:
                print("Pas de texte à extraire dans ce message.")
            

    # Lance l'écoute en continu
    await client.run_until_disconnected()

# Main
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
