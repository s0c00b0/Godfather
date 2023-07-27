'''Fetches posts and alignments from automated games on Mafia Universe'''

import argparse
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

BOT_NAME = "Mafia Host"

def scrape(opt):
    driver = webdriver.Chrome()
    driver.get('https://www.mafiauniverse.com/forums/forums/6-Automated-Games')

    threads = driver.find_elements(By.CLASS_NAME, "title")
    df = pd.DataFrame(columns=["text", "label"])

    for i in range(len(threads)):
        thread = threads[i]
        thread.click()
        
        mod_name = driver.find_element(By.CLASS_NAME, "postbitlegacy").find_element(By.CLASS_NAME, "username").text
            
        page = 0
        end_page = int(driver.find_element(By.CLASS_NAME, "pagination_top").find_element(By.CLASS_NAME, "popupctrl").text[10:])
        
        while not page == end_page:
            posts = driver.find_elements(By.CLASS_NAME, "postbitlegacy")
            for post in posts:
                username = post.find_element(By.CLASS_NAME, "username").text
                if username == mod_name:
                    continue
                elif username == BOT_NAME:
                    # TODO
                    pass
                else:
                    multiquote = post.find_element(By.CLASS_NAME, "multiquote")
                    multiquote.click()
                    
        driver.back()
        timeout = 3
        try:
            element_present = EC.presence_of_element_located((By.ID, 'threadlist'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            quit()
        threads = driver.find_elements(By.CLASS_NAME, "title")
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-username", default=None)
    parser.add_argument("-password", default=None)
    
    opt = parser.parse_args()
    
    scrape(opt)
    
if __name__ == '__main__':
    main()