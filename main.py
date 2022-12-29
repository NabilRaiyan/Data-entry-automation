import customtkinter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time

FONT = ('serif', 10, 'bold')
BG_COLOR = "#753a88"

window = customtkinter.CTk()
window.title("Shopping Bot")

window.geometry("400x400")
window.config(bg=BG_COLOR, padx=30)

item_list = []


def run():
    shop_link_input = shop_link.get()
    shop_link.delete(0, customtkinter.END)
    response = requests.get(shop_link_input)
    website = response.text

    soup = BeautifulSoup(website, 'html.parser')
    google_form_link = 'https://forms.gle/WhwbJ9jRKKeiYgXy7'

    # Beautiful Soup path
    link_list = []

    products = soup.find_all(name="h3", class_="wd-entities-title")
    prices = soup.find_all(name='span', class_="price")
    links = soup.find_all(name='h3', class_="wd-entities-title")
    for link in links:
        link_name = link.find_all('a')
        for href in link_name:
            link_list.append(href.get('href'))

    name_list = [name.get_text() for name in products]
    price_list = [price.get_text().split('\xa0')[0] for price in prices]

    print(name_list)
    print(price_list)
    print(link_list)

    # Selenium part

    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)

    driver_path = "your chrome driver path"
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=option)

    for i in range(len(name_list)):
        driver.get(google_form_link)
        time.sleep(2)

        name = driver.find_element(By.XPATH,
                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        name.click()
        name.send_keys(name_list[i])
        time.sleep(2)

        price = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price.click()
        price.send_keys(price_list[i])
        time.sleep(2)

        link = driver.find_element(By.XPATH,
                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link.click()
        link.send_keys(link_list[i])
        time.sleep(2)

        submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit.click()
        time.sleep(2)


frame = customtkinter.CTkFrame(master=window, height=400, width=450, fg_color="#2c3e50")
frame.grid(column=0, row=0, padx=65, pady=20, sticky="news")

title_label = customtkinter.CTkLabel(master=frame, text_font=FONT, text="Shopping Bot", text_color="white",
                                     corner_radius=8)
title_label.grid(column=0, row=0, padx=5, pady=5)

shop_link = customtkinter.CTkEntry(master=frame, placeholder_text="Enter Shop link", text_font=FONT, corner_radius=8,
                                   border_width=0, placeholder_text_color="black", width=200)
shop_link.grid(column=0, row=1, padx=15, pady=10)

run_button = customtkinter.CTkButton(master=frame, fg_color="white", text_font=FONT, text_color="black",
                                     text="Run", corner_radius=8, width=40, bg_color="#2c3e50", border_width=0,
                                     hover_color="#ffb88c",
                                     border_color="black", command=run)
run_button.grid(column=0, row=4, padx=10, pady=8)

window.mainloop()
