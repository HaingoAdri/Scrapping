import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Récupérer l'URL passée en argument
url = sys.argv[1]

# Configurer les options de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extract_data(url):
    info = {'URL': url}

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        try:
            div_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.PZPZlf.ssJ7i.xgAzOe, .PZPZlf.ssJ7i.B5dxMb')))
            info['Nom Google'] = div_element.text
        except Exception:
            info['Nom Google'] = "Non trouvé"

        try:
            span_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'LrzXr')))
            info['Adresse'] = span_element.text
        except Exception:
            info['Adresse'] = "Non trouvée"

        try:
            phone_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-dtype="d3ph"]')))
            info['Numéro de téléphone'] = phone_link.text
        except Exception:
            info['Numéro de téléphone'] = "Non trouvé"

        try:
            a_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.n1obkb.mI8Pwc')))
            info['URL du lien'] = a_element.get_attribute('href')
        except Exception:
            info['URL du lien'] = "Non trouvé"

        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "WgFkxc")]')))
            rows = table.find_elements(By.XPATH, './/tr')
            horaires = {}
            for row in rows:
                cells = row.find_elements(By.XPATH, './/td[contains(@class, "SKNSIb")]')
                cells2 = row.find_elements(By.XPATH, './/td[not(contains(@class, "SKNSIb"))]')
                if len(cells) == 1 and len(cells2) == 1:
                    day = driver.execute_script("return arguments[0].innerText;", cells[0])
                    hours = driver.execute_script("return arguments[0].innerText;", cells2[0])
                    horaires[day] = hours
            info['Horaires'] = horaires
        except Exception:
            info['Horaires'] = "Non trouvés"

    except Exception as e:
        print(f"Erreur lors de l'extraction des données pour l'URL {url}: {e}")

    return info

# Extraire les données
data = extract_data(url)

# Afficher les résultats
print(data)

# Fermer le navigateur
driver.quit()
