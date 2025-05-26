from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

def scrape_google_maps(search_query, max_places=10):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # service = Service(executable_path='chromedriver')  
    driver = webdriver.Chrome(options=options) # , service=service)

    driver.get("https://www.google.com/maps")
    
    # Search
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(search_query)
    driver.find_element(By.ID, "searchbox-searchbutton").click()
    
    time.sleep(5)
    
    places = []
    count = 0

    while count < max_places:
        listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/place")]')
        for i in range(len(listings)):
            try:
                # Re-fetch listings each time to avoid stale elements
                listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/place")]')
                place = listings[i]
                driver.execute_script("arguments[0].click();", place)
                time.sleep(3)

                name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
                try:
                    address = driver.find_element(By.XPATH, "//button[@data-item-id='address']").text
                except:
                    address = "N/A"

                try:
                    rating = driver.find_element(By.CLASS_NAME, "F7nice").text
                except:
                    rating = "N/A"

                try:
                    phone = "N/A"
                    phone_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Phone')]")
                    for btn in phone_buttons:
                        if btn.text.strip():
                            phone = btn.text.strip()
                            break
                    if phone == "N/A":
                        import re
                        spans = driver.find_elements(By.XPATH, "//span | //div")
                        for span in spans:
                            text = span.text.strip()
                            if re.match(r"^\+?\d[\d\s\-\(\)]{7,}$", text):
                                phone = text
                                break
                except Exception as e:
                    phone = "N/A"

                places.append({
                    "Name": name,
                    "Address": address,
                    "Phone": phone,
                    "Rating": rating
                })
                count += 1
                if count >= max_places:
                    break

                # listings back
                driver.execute_script("window.history.back();")
                time.sleep(3)

            except Exception as e:
                print(f"Error: {e}")
                continue

        if count >= max_places:
            break

    driver.quit()
    df = pd.DataFrame(places)
    df.to_csv("output.csv", index=False)
    return df
