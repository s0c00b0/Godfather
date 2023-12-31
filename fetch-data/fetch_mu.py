'''Fetches posts and alignments from automated games on Mafia Universe'''

import argparse
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert

BOT_NAME = "Mafia Host"

def scrape(opt):
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=op)
    driver.get("https://www.mafiauniverse.com/forums/")
    
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
    
    link = "https://www.mafiauniverse.com/forums/forums/6-Automated-Games"
    driver.get(link)

    threads = driver.find_elements(By.CLASS_NAME, "title")

    if not os.path.exists(opt.save_path):
        os.makedirs(opt.save_path)
        
    file = open(os.path.join(opt.save_path, "data.txt"), "w", encoding="utf-8")

    for i in range(len(threads)):
        thread = threads[i]
        thread.click()
        
        try:
            element_present = EC.presence_of_element_located((By.ID, 'postlist'))
            WebDriverWait(driver, 3).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            quit()
        
        locked = driver.find_element(By.CLASS_NAME, "newcontent_textcontrol")
        if locked.text.strip() == "Closed Thread":
            driver.get(link)
            time.sleep(1)
            try:
                element_present = EC.presence_of_element_located((By.ID, 'threadlist'))
                WebDriverWait(driver, 3).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
                quit()
            threads = driver.find_elements(By.CLASS_NAME, "title")
            print("[INFO] game " + str(i + 1) + " is locked, skipped")
            continue
        
        status = driver.find_element(By.CLASS_NAME, "richPrefix")
        if not status.text == "Completed":
            driver.get(link)
            time.sleep(1)
            try:
                element_present = EC.presence_of_element_located((By.ID, 'threadlist'))
                WebDriverWait(driver, 3).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
                quit()
            threads = driver.find_elements(By.CLASS_NAME, "title")
            print("[INFO] game " + str(i + 1) + " is in-progress, skipped")
            continue
        
        mod_name = driver.find_element(By.CLASS_NAME, "postbitlegacy").find_element(By.CLASS_NAME, "username").text
            
        page = 1
        end_page = int(driver.find_element(By.CLASS_NAME, "pagination_top").find_element(By.CLASS_NAME, "popupctrl").text[10:])
        base_url = driver.current_url

        while page <= end_page:
            time.sleep(1)
            posts = driver.find_elements(By.CLASS_NAME, "postbitlegacy")
            for post in posts:
                if post.get_attribute("data-postnumber") == None:
                    continue
                username = post.find_element(By.CLASS_NAME, "username").text
                if username == mod_name:
                    continue
                elif username == BOT_NAME:
                    title = post.find_element(By.CLASS_NAME, "bbc_title").text
                    if title == "Game Over":
                        post.find_element(By.CLASS_NAME, "newreply").click()
                        time.sleep(0.25)
                        textbox = driver.find_element(By.ID, "quick_reply").find_element(By.CLASS_NAME, "cke_source")
                        data = textbox.get_attribute("value")
                        file.write(data)
                        file.write("--END_QUOTE_SEPARATOR--\n")
                        page = end_page
                        print("[INFO] game " + str(i + 1) + " complete")
                        break
                else:
                    post.find_element(By.CLASS_NAME, "newreply").click()
                    time.sleep(0.25)
                    textbox = driver.find_element(By.ID, "quick_reply").find_element(By.CLASS_NAME, "cke_source")
                    data = textbox.get_attribute("value")
                    file.write(data)
                    file.write("--END_QUOTE_SEPARATOR--\n")
                    
            page += 1
            prev_next = driver.find_element(By.ID, "pagination_top").find_elements(By.CLASS_NAME, "prev_next")
            
            if len(prev_next) == 2:
                prev_next[1].click()
            elif len(prev_next) == 1:
                prev_next[0].click()
            
        driver.get(link)
        time.sleep(1)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'threadlist'))
            WebDriverWait(driver, 3).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            quit()
        threads = driver.find_elements(By.CLASS_NAME, "title")
    file.close()
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-username", default=None)
    parser.add_argument("-password", default=None)
    parser.add_argument("-save_path", default=".")
    
    opt = parser.parse_args()
    
    if not all([opt.username, opt.password]):
        print("[ERROR] username and password are required arguments")
        quit()
    
    if not opt.save_path:
        print("[INFO] save_path not specified, saving to data.txt in current directory")
    
    scrape(opt)
    
if __name__ == '__main__':
    main()