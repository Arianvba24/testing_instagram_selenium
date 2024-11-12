import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options,
    )

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument('--disable-extensions')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--ignore-ssl-errors')

user = "ferragutarian@gmail.com"
passwd = "03051997Leandro*"



# chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=options)


# with open(r"C:\Users\Cash\Proyectos\092024\Instagram bot\cookies.json") as j:
#     cookie_instagram = json.load(j)

# # cookie = {value["name"] : value["value"] for value in cookie_instagram}





# # time.sleep(2)
# # driver.add_cookie(cookie)


# for cookie in cookie_instagram:
#     try:

#         driver.add_cookie(cookie)
#     except Exception as e:
#         print(f"Error al agregar la cookie {cookie}: {e}") 
 

driver.get("https://www.instagram.com/")

try:

# "_a9-- _ap36 _a9_0"
    time.sleep(10)

    allow_all_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(),'Permitir todas las cookies') or contains(text(), 'Aceptar todas')]")
    allow_all_cookies_button.click()
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(passwd)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()

    # data_cookies = driver.get_cookies()

    # with open(r"C:\Users\Cash\Proyectos\092024\Instagram bot\cookies.json","w") as j:
    #     json.dump(data_cookies,j)

    time.sleep(15)


    driver.get(r"https://www.instagram.com/herasmedia/reels/")

    time.sleep(10)
    html_data = []

    html_data.append(driver.page_source)
    # for i in range(20):
    last_height = ""
    while True:
        try:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break  # Si la altura no cambia, significa que se ha llegado al final de la página

            last_height = new_height  # Actualiza la altura para la siguiente comparación
            html_data.append(driver.page_source)
        except:
            pass
        


    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html_data.append(driver.page_source)
    # driver.execute_script("window.scrollTo(0, 0);")
    
    # driver.execute_script("""
    # var elements = document.querySelectorAll('.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1');
    # elements.forEach(function(el) {
    #     el.style.position = 'static';  // Desactiva 'position: relative' o 'absolute'
    #     el.style.display = 'block';  // Asegura que esté visible
    #     el.style.visibility = 'visible';  // Asegura visibilidad
    # });
    # """)
    
    time.sleep(10)
    html_data.append(driver.page_source)
    # data = driver.page_source

# -------------------------------------------------------
    # for i,data in enumerate(html_data):

    #     with open(fr"C:\Users\Cash\Proyectos\092024\Instagram bot\data{i}.txt","w",encoding="UTF-8") as f:
    #         f.write(data)
# -------------------------------------------------------
 
    driver.close()

    driver.quit()

    value_x = []
    html_values = []


# -------------------------------------------------------
    # for i in range(71):

    #     with open(fr"C:\Users\Cash\Proyectos\092024\Instagram bot\data{i}.txt","r",encoding="UTF-8") as f:
    #         text_data = f.read()
    

# -------------------------------------------------------
    for i in html_data:

        
        soup = BeautifulSoup(i,"lxml")
        x_data = [i for i in soup.find_all("a",class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd")]
        html_values.extend(x_data)



        value_x.extend(re.findall(r"herasmedia/reel/[\S]{0,50}/",str(i)))



    xp = set()


    for i in value_x:
        xp.add(i)



    urls = list(xp)

    urls_for_dataframe = urls.copy()




    definitive_html = []


    def buscar(data):
        if len(urls) > 0:
            for n,i in enumerate(urls):
                if i in str(data):
                    print(i)
                    definitive_html.append(data)
                    url_added = urls.pop(n)
                    # urls_added.append(url_added)
                    return True





    for data in html_values:
        buscar(data)



    # ---------------------------------------------------------------------------------------------------------
    numbers_x = []

    for i in definitive_html:
        # i = i.replace()
        data = re.findall(r"(.{0,20})(\sM|mil)",str(i))
        print(data)
        if data:

            value = data[-1][0].split(">")
            if "mil" in data[-1][-1] and "," in value[1]:
                k_number = float(value[1].replace(",","")) * 100
                numbers_x.append(k_number)

            elif "mil" in data[-1][-1] and "," not in value[1]:
                k_number = float(value[1].replace(",","")) * 1000
                numbers_x.append(k_number)

            elif "M" in data[-1][-1] and "," in value[1]:
                m_number = float(value[1].replace(",","")) * 100000
                numbers_x.append(m_number)

            elif "M" in data[-1][-1] and "," not in value[1]:
                m_number = float(value[1].replace(",","")) * 1000000
                numbers_x.append(m_number)

        else:
            numbers_x.append("No hay valores")


    # --------------------------------------------------------------------------------

    likes = []

    for i in definitive_html:
        datos = i.find("span",class_="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs").text
        if "mil" in datos:
            value = datos.split()[0]
            value = value.replace(",","")
            data = float(value) * 1000
            likes.append(data)
        elif "mil" not in datos and len(datos) > 0:
            likes.append(datos)

        else:
            likes.append("No hay me gustas")


    # -----------------------------------------------------------------------------------

    comentarios = []

    for i in definitive_html:
        data = i.find("ul",class_="x6s0dn4 x972fbf xcfux6l x1qhh985 xm0m39n x78zum5 xa5j0wu xln7xf2 xk390pu x5yr21d xl56j7k xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3")
        children = data.find_all(recursive=False)

        if len(children) > 1:
            # Obtener el segundo hijo (index 1)
            segundo_hijo = children[1].text
            if "mil" in segundo_hijo:
                value = segundo_hijo.split()[0]
                value = value.replace(",","")
                data = float(value) * 1000
                comentarios.append(data)
            elif "mil" not in segundo_hijo and len(segundo_hijo) > 0:
                comentarios.append(segundo_hijo)

            else:
                comentarios.append("No hay comentarios")
            
            # print(segundo_hijo.text)

        else:
            comentarios.append(children.text)


    data_for_dataframe = {
        "URL publicación" : urls_for_dataframe,
        "Número de visualizaciones" : numbers_x,
        "Número de comentarios" : comentarios,
        "Número de likes" : likes
        
    }


    df = pd.DataFrame(data_for_dataframe)
    st.dataframe(df)
    # print(df)
    # df.to_excel(r"C:\Users\Cash\Proyectos\092024\Victor heras project\Instagram bot\dataframe.xlsx",index=False)
    

except:
    driver.close()
    driver.quit()
