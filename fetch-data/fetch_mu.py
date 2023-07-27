'''Fetches posts and alignments from automated games on Mafia Universe'''

import argparse
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BOT_NAME = "Mafia Host"

def scrape(opt):
    driver = webdriver.Chrome()
    driver.get("https://www.mafiauniverse.com/forums/")
    
    window1 = driver.current_window_handle
    
    log_in = driver.find_element(By.CLASS_NAME, "login-window")
    log_in.click()
    
    username_box = driver.find_element(By.NAME, "vb_login_username")
    username_box.send_keys(opt.username)
    
    password_box = driver.find_element(By.NAME, "vb_login_password")
    password_focus = driver.find_element(By.NAME, "vb_login_password_hint")
    password_focus.click()
    password_box.send_keys(opt.password)
    
    log_in_button = driver.find_element(By.CLASS_NAME, "loginbutton")
    log_in_button.click()
    
    # wait for redirect
    time.sleep(5)
    
    profile_button = driver.find_element(By.CLASS_NAME, "welcomelink").find_element(By.TAG_NAME, "a")
    profile_button.click()
    
    driver.switch_to.new_window("tab")
    driver.get("https://www.mafiauniverse.com/forums/forums/6-Automated-Games")
    
    window2 = driver.current_window_handle

    threads = driver.find_elements(By.CLASS_NAME, "title")
    df = pd.DataFrame(columns=["text", "label"])

    for i in range(len(threads)):
        thread = threads[i]
        thread.click()
        
        try:
            element_present = EC.presence_of_element_located((By.ID, 'postlist'))
            WebDriverWait(driver, 3).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            quit()
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
        try:
            element_present = EC.presence_of_element_located((By.ID, 'threadlist'))
            WebDriverWait(driver, 3).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            quit()
        threads = driver.find_elements(By.CLASS_NAME, "title")
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-username", default=None)
    parser.add_argument("-password", default=None)
    
    opt = parser.parse_args()
    
    if not all([opt.username, opt.password]):
        print("[ERROR] username and password are required arguments")
        quit()
    
    scrape(opt)
    
if __name__ == '__main__':
    main()