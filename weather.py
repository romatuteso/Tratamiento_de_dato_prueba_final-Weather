import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from mongodb import MongoConnection

db_client = MongoConnection().client
db = db_client.get_database('Weather')
col = db.get_collection('Time')

start_urls = ['https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947',
              'https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846',
              'https://www.accuweather.com/es/ec/cuenca/127442/weather-forecast/127442']


def extra_clima():
    driver = webdriver.Chrome()

    for url in start_urls:
        driver.get(url)

        time.sleep(4)

        weather = driver.find_elements(By.CLASS_NAME, "cluster-container")
        for driver in weather:
            ciudad = driver.find_element(by=By.TAG_NAME, value='//h1').text
            current = driver.find_element(by=By.CSS_SELECTOR, value='//a[contains(@class, "cur-con-weather-card")]'
                                                           '//div[@class="temp"]').text
            real_feel = driver.find_element(by=By.CSS_SELECTOR, value='//a[contains(@class, "cur-con-weather-card")]'
                                                             '//div[@class="real-feel"]').text

            real_feel = real_feel.replace(__old='RealFeel®', __new='').replace(__old='°', __new='').replace(__old='\n', __new='').replace(__old='\t', __new='').replace('\r', '').strip()
            current = current.replace(__old='°', __new='').replace(__old='\n', __new='').replace(__old='\t', __new='').replace(__old='\r', __new='').strip()

            f = open("datos-clima.csv", "a")
            f.write(f"{ciudad},{current},{real_feel}\n")
            f.close()

            document = {
                "City": ciudad,
                "Current": current,
                "Real Feel": real_feel
                }

            col.insert_one(document=document)

            print(ciudad)
            print(current)
            print(real_feel)
            print("\n")

        driver.close()


schedule.every(1).minute.do(extra_clima)

extra_clima()

while True:
    schedule.run_pending()
    time.sleep(1)
