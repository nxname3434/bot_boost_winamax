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
