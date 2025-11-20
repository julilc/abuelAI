from rqst_scrapping import *

            # sub_categories = category.find_elements(By.CSS_SELECTOR, "li a")
            # for sub in sub_categories:
            #     sub_title = sub.get_attribute('innerText').strip()
            #     link = sub.get_attribute("href")
            #     results.append([main_title, sub_title, link])
        
def get_help_sections():
    driver = driver_open()
    driver.get("https://help.disneyplus.com/es-AR/")
    wait = WebDriverWait(driver, 20)
    try:
        wrapper = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.plus-topics-wrap"))
        )
        categories = wrapper.find_elements(By.CSS_SELECTOR, "a.plus-topic-card")
        results = []
        for category in categories:
            title = category.find_element(By.CSS_SELECTOR, "div.plus-text-subtitle").text
            print(title)
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        driver.quit()


get_help_sections()


