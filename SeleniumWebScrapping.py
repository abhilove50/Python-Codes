from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd


timeout = 10
chrome_path = r"chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
page = driver.get("https://euipo.europa.eu/eSearch/#advanced/representatives")
element = driver.find_element(By.XPATH, ('//*[@id="advancedPage"]/div/div/div/div[2]/div[1]/div[1]/div/span[2]/select/option[3]'))
Country_option = Select(driver.find_element(By.XPATH, ('//*[@id="advancedPage"]/div/div/div/div[2]/div[1]/div[1]/div/span[2]/select')))
Country_option.select_by_value("RepresentativeIncorporationCountryCode")
driver.find_element(By.XPATH, ('//*[@id="advancedPage"]/div/div/div/div[1]/div[2]/ul/li[2]/a[contains(.,"Country")]')).click()
element_country_name = driver.find_element(By.XPATH, ('//*[@id="row_c133"]/span[4]/select/option[11]'))
Country_Type = Select(driver.find_element(By.XPATH, ('//*[@id="row_c133"]/span[4]/select')))
Country_Type.select_by_value("FI")
driver.find_element(By.XPATH, ('//*[@id="advancedPage"]/div/div/div/div[2]/nav/ul/li[3]/a[contains(.,"Search")]')).click()
try:
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="advancedPage"]/div/div/div/div[4]/div[3]/div/div[1]/div/div/dl[2]/dd'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print(element.text)
    print(element_country_name.text)
    Addresses = []
    for i in range(1, 51):
        Addresses.append((driver.find_element_by_xpath('//*[@id="advancedPage"]/div/div/div/div[4]/div[3]/div/div['+str(i)+']/div/div/dl[2]/dd')).text)
    print(Addresses)
    print(Addresses[0])
    result_file = open("output.csv", "w")
    wr = csv.writer(result_file, delimiter=' ')
    new_list = []
    for elem in Addresses:
        new_list.append(elem.splitlines())

    print(new_list)
    print(new_list[0][0].upper())
    converted_list = []
    for i in range(0, 50):
        driver.get("http://translate.google.com/m?")
        inputElement = driver.find_element(By.NAME, "q")
        inputElement.send_keys(new_list[i][0].upper())
        inputElement.send_keys(Keys.ENTER)
        text_converted = driver.find_element(By.XPATH, "/html/body/div[3]")
        converted_list.append(text_converted.text.upper())
    list_combined = []
    for i in range(0, len(Addresses)):
        list_combined.append([Addresses[i], converted_list[i]])
        # wr.writerow([list_combined[i]])

    df = pd.DataFrame(list_combined)
    df.to_csv("output.csv", index=False, header=False)
    driver.quit()
