from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromadb
from chromadb.config import Settings
import time
import re
import pandas as pd
def driver_open():
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_subclasss()-> list[str]:
    driver = driver_open()
    driver.get('https://help.netflix.com/es')
    # Lista para almacenar los enlaces de las subcategorías
    subcategory_links = []

    try:
        # Abrir la página principal de ayuda de Netflix
        driver.get("https://help.netflix.com/es")

        # Encontrar todas las categorías principales
        categories = driver.find_elements(By.CSS_SELECTOR, "div.category.category-card")
        print(categories)
        # Iterar sobre cada categoría
        for category in categories:
            # Hacer clic en el título de la categoría para expandir las subcategorías
            category.click()
            time.sleep(1)  # Pausa para permitir que las subcategorías se carguen

            # Encontrar las subcategorías dentro de la categoría
            subcategories = category.find_elements(By.CSS_SELECTOR, "div.subcategories a")

            for subcategory in subcategories:
                # Obtener el enlace de la subcategoría
                subcategory_url = subcategory.get_attribute("href")
                subcategory_links.append(subcategory_url)

        # Imprimir los enlaces de las subcategorías
        for link in subcategory_links:
            print(link)

    finally:
        # Cerrar el navegador
        driver.quit() 
    
    return subcategory_links


def get_subcat_info(link:str):
    driver = driver_open()
    try:
        driver.get(link)
        wait = WebDriverWait(driver, 10)
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.kb-title")))
        title = title.text
        data = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.left-pane')))
        data = data.text
        element = [title, data]

    finally:
        driver.quit()
    return element

def clean_data_subcat(data):
    data = re.sub(r"¿El artículo fue de utilidad\?.*", "", data, flags=re.DOTALL)
    return data.strip()


def scrapping_help_netflix()->None:
    '''
    This function takes the main subsections of the help page in netflix.com and
    returns the info in each of this subsections and save it at data/processed_data.

    '''
    subcategory_links = get_subclasss()
    data_subcat = []
    for subcat in subcategory_links:
        data_raw = get_subcat_info(subcat)
        data_clean = [data_raw[0], clean_data_subcat(data_raw[1])]
        data_subcat.append(data_clean)

    return data_subcat

data = scrapping_help_netflix()
print(data) 
data_csv = pd.DataFrame(data,columns=['Title','data'])
data_csv.to_csv("data/processed_data/netflix_help.csv", index_label=None)
print(data_csv)


data_csv = pd.read_csv("data/processed_data/netflix_help.csv", index_col=None)
print(data_csv)

