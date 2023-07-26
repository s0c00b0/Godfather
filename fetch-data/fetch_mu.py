'''Fetches posts and alignments from automated games on Mafia Universe'''

import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

def scrape_mu(opt):
    if not os.path.exists(opt.driver_path):
        print("[ERROR] driver does not exist")
    
    driver = webdriver.Chrome(opt.driver_path)
    df = pd.DataFrame(columns=["text", "label"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-driver_path", default=None)
    opt = parser.parse_args()
    
    scrape_mu(opt)

if __name__ == '__main__':
    main()