import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import configparser
import os

config = configparser.ConfigParser(allow_no_value=True)

config.read("config.ini")
try:
   config_data = config["SETTINGS"]
except:#writes default settings if they are missing
   config['SETTINGS'] ={'//leave token blank to be asked for it during runtime': None,
                     'Secret token':'',
                     'Watch time': '3800',
                     'Live check cooldown': '360',
                     'Check if drops are enabled': '1',
                     '//leave type blank for all drops': None,
                     'Type of drop': 'Rust'}
   print("settings not found, attempting to create")
   config_data = config["SETTINGS"]
   with open('config.ini', 'w') as configfile:
        config.write(configfile)

#get config 
secret = config_data['secret token']
check_drop = int(config_data['check if drops are enabled'])
drop_type = config_data['type of drop']
watch_time = int(config_data['watch time'])
live_check_cooldown = int(config_data['Live check cooldown'])

if secret == '':
 secret = input("enter your twitch auth token: ")
 os.system('cls' if os.name == 'nt' else 'clear')
driver = webdriver.Chrome()
driver.get("https://www.twitch.tv")
driver.add_cookie({"name" : "auth-token", "value" : secret})

def countdown(t): 
 while t: 
  mins, secs = divmod(t, 60)
  hours, mins = divmod(mins, 60)
  timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs) 
  print(timer, end="\r") 
  time.sleep(1) 
  t -= 1

def check_if_live(twitch_streamers):
 contents = requests.get(twitch_streamers).content.decode('utf-8')
 if 'isLiveBroadcast' in contents: 
    print(twitch_streamers + ' is live')
    return True
 else:
    print(twitch_streamers + ' is not live')
    return  False
    
 
def watch_stream(twitch_stream,watch_time):
 driver.get(twitch_stream)
 time.sleep(5)#loading time
 try: 
     button=driver.find_element(By.XPATH,'//*[@id="channel-player-gate"]/div/div/div[4]/div/button/div/div')
     button.click()
     print("clicked start watching") 
 except NoSuchElementException: 
     print("No need to click start watching")   
 if check_drop_status(check_drop,drop_type) == False:#checks if drops are enabled
    driver.get("data:, waiting for someone to go live")#opens a blank page
    return False
 countdown(watch_time)
 return True    
 
 
def check_drop_status(check_drop,drop_type):
 if check_drop == 0:
   return True
 try: #CSS selecttors
    driver.find_element(By.CSS_SELECTOR,'#live-page-chat > div > div > div.Layout-sc-1xcs6mc-0.iTiPMO.chat-shell.chat-shell__expanded > div > div > section > div > div:nth-child(3) > div.InjectLayout-sc-1i43xsx-0.dUREKt > div > div.Layout-sc-1xcs6mc-0 > div > div.simplebar-scroll-content.community-highlight-stack__scroll-area--disable > div > div > div.ScTransitionBase-sc-hx4quq-0.kHfhAq.tw-transition > div > div > div > div > div > div > div.highlight__click-target > div > div > div.Layout-sc-1xcs6mc-0.cVwZw > button').click()
    time.sleep(1)
    dropsenabled=driver.find_element(By.CSS_SELECTOR,'#live-page-chat > div > div > div.Layout-sc-1xcs6mc-0.iTiPMO.chat-shell.chat-shell__expanded > div > div > section > div > div:nth-child(3) > div.InjectLayout-sc-1i43xsx-0.dUREKt > div > div.Layout-sc-1xcs6mc-0.eKDZrJ > div.community-highlight-stack__scroll-area--disable.scrollable-area.scrollable-area--suppress-scroll-x > div.simplebar-scroll-content.community-highlight-stack__scroll-area--disable > div > div > div.ScTransitionBase-sc-hx4quq-0.kHfhAq.tw-transition > div > div > div:nth-child(1) > div > div > div > div > div > div.ScTransitionBase-sc-hx4quq-0.dtAmne.tw-transition > div > div.Layout-sc-1xcs6mc-0.iCNEPM > div > div:nth-child(1) > p')
    print(dropsenabled.text) 
 except NoSuchElementException:#trys to find if drops are enabled for rust
    print("drops are disabled/already been claimed")
    return False    
 if drop_type in dropsenabled.text or drop_type == '':
    print(drop_type ,'drops are enabled')
    return True
 else:
    print(drop_type ,'drops are disabled')
    return False


with open('streamer_list.txt', 'r') as ins:#loads from txt to list
    twitch_streamers = [[n for n in line.split()] for line in ins]

while True:# if if if if
 all_equal = all(x == twitch_streamers[0] for x in twitch_streamers)
 if all_equal == True:
    print("Done")
    break
 print ("---------")
 #print (twitch_streamers)
 for i in range(len(twitch_streamers)):

        for j in range(len(twitch_streamers[i])):
            if twitch_streamers[i] == "0":#ignores
                break
            if check_if_live(twitch_streamers[i][j]) == True:  
                print ("watching",twitch_streamers[i][j])
                if watch_stream(twitch_streamers[i][j],watch_time) == True:
                    twitch_streamers[i] = "0"#marks as completed
                    print("Done watching")
                    break
        if twitch_streamers[i] == twitch_streamers[-1]:#reduces request spam
             print("checked everyone. Sleeping to prevent spam")
             countdown(live_check_cooldown)
