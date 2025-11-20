from rqst_scrapping import *


def get_links_cat() -> str:
    driver = driver_open()
    try:
        driver.get("https://www.primevideo.com/help")
        wait = WebDriverWait(driver, 20)
        box_categories = wait.until(EC.visibility_of_element_located((By.ID, "links-contain")))
        categories = box_categories.find_elements(By.CLASS_NAME, "accordionItem" )
        results = []
        for category in categories:
            main_title = category.find_element(By.CSS_SELECTOR, "a.accordionItemHeading h3").text
            sub_categories = category.find_elements(By.CSS_SELECTOR, "li a")
            for sub in sub_categories:
                sub_title = sub.get_attribute('innerText').strip()
                link = sub.get_attribute("href")
                results.append([main_title, sub_title, link])
        
        
    except Exception as e:
        return f"Error: {e}"

    finally:
        driver.quit()
    
    return results

def get_info_sub_cat(sub_cats: list):
    i = 0
    info = []
    for sub_cat in sub_cats:
        link = sub_cat[2]
        print(i, "/", len(sub_cats))
        driver = driver_open()
        try:
            driver.get(link)
            wait = WebDriverWait(driver, 20)
            info =wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "help-content")))
           
            paragraphs = info.find_elements(By.TAG_NAME, 'p')
            paragraph_texts = " ".join([p.text for p in paragraphs if p.text])
            ordered_lists = info.find_elements(By.TAG_NAME, 'ol')
            
            for ol in ordered_lists:
                items = ol.find_elements(By.TAG_NAME, 'li')
                paragraph_texts+= " ".join([li.text for li in items if li.text])

            if not paragraph_texts.strip():
                paragraph_texts = "No info"

            sub_cat.insert(2, paragraph_texts)
            sub_cats[i] = sub_cat

        except Exception as e:
            
            sub_cat.insert(2, "No info")
            sub_cats[i] = sub_cat
        finally:
            driver.quit()
        i+=1
    return sub_cats
       
            
if __name__ == "__main__":
    links = get_links_cat()
    links = get_info_sub_cat(links)
    #Converts and saves to .csv all the info collected in the folder "/processed_data"
    csv_help_prime = pd.DataFrame(links, columns=['Category','Sub Section','Info', 'Link'])
    csv_help_prime.to_csv("data/processed_data/prime_help.csv", index=False)
    