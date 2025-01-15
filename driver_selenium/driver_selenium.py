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
