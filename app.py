import streamlit as st
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session


retry_strategy = Retry(
    total=3,  # Número de reintentos
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options
    )
    
    return driver

# Configura el driver y navega a Instagram
driver = get_driver()
driver.implicitly_wait(10)

def login_to_instagram(driver, user, passwd):
    try:
        driver.get("https://www.instagram.com/")
        time.sleep(15)
        
        # Aceptar cookies
        try:
            allow_all_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(),'Permitir todas las cookies') or contains(text(), 'Aceptar todas')]")
            allow_all_cookies_button.click()
        except Exception as e:
            st.write("Error al aceptar cookies:", e)
        
        # Login
        driver.find_element(By.NAME, "username").send_keys(user)
        driver.find_element(By.NAME, "password").send_keys(passwd)
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        time.sleep(20)
        
        st.write("Login exitoso.")
    except Exception as e:
        st.write("Error al hacer login:", e)
        driver.quit()

def scrape_reels_page(driver):
    html_data = []
    driver.get("https://www.instagram.com/herasmedia/reels/")
    time.sleep(5)

    # Scroll y capturar HTML de la página
    last_height = ""
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        html_data.append(driver.page_source)
    
    return html_data

def extract_data_from_html(html_data):
    urls, views, likes, comments = [], [], [], []
    for page_html in html_data:
        soup = BeautifulSoup(page_html, "lxml")
        
        # Extraer URLs de las publicaciones
        urls.extend(re.findall(r"herasmedia/reel/[\S]{0,50}/", str(soup)))
        
        # Ejemplo: Extraer visualizaciones (requiere ajuste según HTML actual)
        for element in soup.find_all("a", class_="x1i10hfl xjbqb8w"):
            views.append(element.text)
        
        # Agregar lógica similar para "likes" y "comments" según clases y estructura HTML específicos
    
    return urls, views, likes, comments

# Ejecución principal
try:
    user = "ferragutarian@gmail.com"  # Tu usuario
    passwd = "03051997Leandro*"  # Tu contraseña

    login_to_instagram(driver, user, passwd)

    # Scrape Reels
    html_data = scrape_reels_page(driver)

    # Extraer datos de HTML
    urls, views, likes, comments = extract_data_from_html(html_data)

    # Crear DataFrame y mostrar en Streamlit
    data_for_dataframe = {
        "URL publicación": urls,
        "Número de visualizaciones": views,
        "Número de likes": likes,
        "Número de comentarios": comments
    }
    
    df = pd.DataFrame(data_for_dataframe)
    st.dataframe(df)

except Exception as e:
    st.write("Error en la ejecución:", e)
finally:
    driver.quit()
