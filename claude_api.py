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
    driver.get("<ENTER_YOUR_SLACK_URL>")
input_box = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[5]/div[2]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]')


sendButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[5]/div[2]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div/div/div[3]/div[3]/span/button[1]')

chatArea = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[5]/div[2]/div/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div/div')

def clearHistory(stime = 5):
    driver.implicitly_wait(1)
    # sendMessage('/reset')
    # input_box.send_keys('/reset')
    driver.execute_script("arguments[0].setHTML('/reset')", input_box)
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    # sendButton.click()
    time.sleep(stime)



SLACK_USER_TOKEN = '<ENTER_YOUR_SLACK_USER_TOKEN>'

client = WebClient(token=SLACK_USER_TOKEN)
BOT_USER_ID = "<ENTER_YOUR_BOT_USER_ID>"


def send_message(channel, text):
    try:
        return client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        print(f"Error sending message: {e}")

def fetch_messages(channel, last_message_timestamp):
    response = client.conversations_history(channel=channel, oldest=last_message_timestamp)
    return [msg['text'] for msg in response['messages'] if msg['user'] == BOT_USER_ID]

def get_new_messages(channel, last_message_timestamp):
    while True:
        messages = fetch_messages(channel, last_message_timestamp)
        if messages and not messages[-1].endswith('Typing…_'):
            return messages[-1]
        time.sleep(5)

def find_direct_message_channel(user_id):
    try:
        response = client.conversations_open(users=user_id)
        return response['channel']['id']
    except SlackApiError as e:
        print(f"Error opening DM channel: {e}")

dm_channel_id = find_direct_message_channel(BOT_USER_ID)

def send_and_get_respose(inp):
    # last_message_timestamp = None
    response = send_message(dm_channel_id, inp)
    if response:
        last_message_timestamp = response['ts']
    new_message = get_new_messages(dm_channel_id, last_message_timestamp)
    return new_message



