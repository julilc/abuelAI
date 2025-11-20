from rqst_scrapping import *

def get_links_cat() -> str:
    driver = driver_open()
    try:
        driver.get("https://help.max.com/es-es/Home/Index")
        wait = WebDriverWait(driver, 20)
        link_element = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.ViewAll")))
        titles = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "h2.cat-heading")))
        titles = [t.text for t in titles]
        links = []
        i = 0
        for link in link_element:
            href = link.get_attribute("href")
            links.append([titles[i],href])
            i +=1
        return links

    except Exception as e:
        return f"Error: {e}"

    finally:
        driver.quit()

def get_link_sections(link)->list[list]:
    driver = driver_open()
    links_sections =[]
    try:
        driver.get(link)
        wait = WebDriverWait(driver, 10)

        # Localizar las secciones principales
        info_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.CategorySection"))
        )
        
        for section in info_elements:
            main_title = section.find_element(By.CSS_SELECTOR, "h2.CategorySectionTitle")
            main_title = main_title.text
            # Buscar subsecciones dentro de la sección
            subsecs = section.find_elements(By.CSS_SELECTOR, "div.CategorySectionAnswer")
            for subs in subsecs:
                try:
                    # Buscar enlaces en la subsección
                    link_element = subs.find_element(By.TAG_NAME, "a")
                    href = link_element.get_attribute("href")
                    sub_title = link_element.get_attribute('innerText').strip()
                    links_sections.append([main_title, sub_title, href])
                except:
                    print("enlace no encontrado")
                    continue  


    finally:
        driver.quit()

    return links_sections


def get_info_subsection(link)->str:
    driver = driver_open()
    try:
        driver.get(link)
        wait = WebDriverWait(driver, 10)

        info_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section#AnswerBody")))
        info_section = info_section.get_attribute('innerText')
    

    finally:
        driver.quit()
    
    return info_section




# Ejecutar el script
if __name__ == "__main__":
    
    #Searchs for help categories
    categories = get_links_cat()
    
    print(f"Enlace encontrado: {categories}")
    lista_info = []
    for cat in categories:
        cat_title = cat[0]
        lista_cat = []

        #Searchs for each subcategory / section
        links_sections = get_link_sections(cat[1])
        for sec in links_sections:

            sec_title = sec[0]
            subsec_title = sec[1]

            #Gets the info for each subcategory
            info_section = get_info_subsection(sec[2])
            
            #Saves category title, subcategor title, info and source link
            lista_cat.append([cat_title,sec_title,subsec_title, info_section, sec[2]])
            print(f"Category: {cat_title}")
            print(f"Secction: {sec_title}")
            print(f"Subsection: {subsec_title}")
            print(f"Info section: {info_section}")
            lista_info.extend(lista_cat)
            print(len(lista_cat))

    #Converts and saves to .csv all the info collected in the folder "/processed_data"
    csv_help_max = pd.DataFrame(lista_info, columns=['Category','Section','Sub Section','Info', 'Link'])
    csv_help_max.to_csv("data/processed_data/max_help.csv")
        