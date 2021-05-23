#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium')


# In[2]:


from selenium import webdriver as wd
driver_binary = r"C:\Users\Manav\chromedriver_win32\chromedriver.exe"
driver = wd.Chrome(driver_binary)


# In[6]:


import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# The account you want to check
account = "ponmaakishan"

# Chrome executable
chrome_binary = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"   # Add your path here


def login(driver):
    username = "manavmessi252"   # Your username
    password = "Khushi@02"   # Your password

    # Load page
    driver.get("https://www.instagram.com/")
    time.sleep(5) 
    #Login
    driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
    driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
    driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
    
    time.sleep(10)
    driver.find_element_by_xpath("//button[text()='Not Now']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//button[text()='Not Now']").click()

    # Wait for the login page to load
#     WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.LINK_TEXT, "See All")))
    driver.implicitly_wait(10)

# 
def scrape_followers(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))


#     driver.find_element_by_partial_link_text("follower").click()
    follower = driver.find_element_by_xpath('//ul[@class="k9GMp "]/li[2]/a/span')
    follower.click()
    time.sleep(10)
    
    followers_count = convert_str_to_number(follower.text)
#     followers_count = int(follower.text)
    
    while True:
        driver.execute_script('''
                var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                fDialog.scrollTop = fDialog.scrollHeight
        ''')
        list_of_followers = driver.find_elements_by_xpath('//div[@class="PZuss"]/li/div/div/div[2]/div/span/a')
        list_of_followers_count = len(list_of_followers)
        
        if list_of_followers_count == followers_count:
            break
      
    new_list_of_followers = []
    for i in list_of_followers:
        new_list_of_followers.append(i.text)

    return new_list_of_followers

def scrape_following(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Following' link
#     driver.find_element_by_partial_link_text("following").click()
    following = driver.find_element_by_xpath('//ul[@class="k9GMp "]/li[3]/a/span')
    following.click()
    
    time.sleep(10)
    

    following_count = convert_str_to_number(following.text)
#     following_count = int(following.text)
    
    while True:
        driver.execute_script('''
                var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                fDialog.scrollTop = fDialog.scrollHeight
        ''')
        list_of_following = driver.find_elements_by_xpath('//div[@class="PZuss"]/li/div/div/div[2]/div/span/a')
        list_of_following_count = len(list_of_following)
        
        if list_of_following_count == following_count:
            break
      
    new_list_of_following = []
    for i in list_of_following:
        new_list_of_following.append(i.text)

    
    return new_list_of_following


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)


if __name__ == "__main__":
    options = wd.ChromeOptions()
    options.binary_location = chrome_binary # chrome.exe
    driver_binary = r"C:\Users\Manav\chromedriver_win32\chromedriver.exe"
    driver = wd.Chrome(executable_path = driver_binary, chrome_options=options)
    try:
        login(driver)
        followers = scrape_followers(driver, account)
        print("______________________________________")
        print("FOLLOWERS")
        print(followers)
        following = scrape_following(driver, account)
        print("\n______________________________________")
        print("FOLLOWING")
        print(following)
        output =[]
        for i in following:
            if i not in followers:
                output.append(i)
                
        result = {
            "followers_list" : followers,
            "following_list" : following,
            "output" : output
        }
        
        import pandas as pd
        
        df= pd.DataFrame.from_dict(result,orient='index').transpose()
        df.to_csv('instagram.csv') 

    finally:
        driver.quit()


# In[ ]:




