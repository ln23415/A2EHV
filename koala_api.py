import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ipdb


RESET = False
 
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")
driver = Chrome(options=chrome_options)

if RESET:
    driver.get("https://chat.lmsys.org/")
input_box = driver.find_element(By.XPATH, '/html/body/gradio-app/div/div/div/div/div/div[1]/div[2]/div/div[4]/div[1]/div/div/label/textarea')


sendButton = driver.find_element(By.XPATH, '/html/body/gradio-app/div/div/div/div/div/div[1]/div[2]/div/div[4]/div[2]/button')

chatArea = driver.find_element(By.XPATH, '/html/body/gradio-app/div/div/div/div/div/div[1]/div[2]/div/div[3]/div[2]/div')

clearButton = driver.find_element(By.XPATH, '/html/body/gradio-app/div/div/div/div/div/div[1]/div[2]/div/div[5]/button[5]')

def clearHistory(stime = 5):
    driver.implicitly_wait(1)

    clearButton.click()

    time.sleep(stime)



def send_message(text):
    input_box.send_keys(text)
    input_box.send_keys(Keys.ENTER)



def send_and_get_respose(inp):
    # last_message_timestamp = None
    send_message(inp)
    # ipdb.set_trace()
    time.sleep(20)
    new_msg = ''
    while True:
        try:
            new_msg = chatArea.find_elements(By.CLASS_NAME, 'bot')[-1].text
            if (new_msg[-1] not in ['.', '?', '!', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']) or (new_msg[-1] == '') or (new_msg[-1] == ' '):
                print('Still waiting generating...')
                time.sleep(15)
                continue
        except:
            print('Still waiting generating...')
            time.sleep(15)
        break
    # if response:
    #     last_message_timestamp = response['ts']
    # ipdb.set_trace()
    # new_message = get_new_messages(dm_channel_id, last_message_timestamp)
    return new_msg



