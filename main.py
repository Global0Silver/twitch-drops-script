import os 
import time
import webbrowser
import requests
Streamlinks = []
print ("made by Globalsl (discord @)")
while True: #input loop
    newlinks = input ("Enter the streamers page link(leave blank if you want to stop entering): \n")
    if newlinks == '' :
        break
    Streamlinks.append (newlinks)
print (Streamlinks)

input ("This will close Chrome \nPRESS ENTER TO CONTINUE")

def countdown(t): 
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1

while True:
 for x in Streamlinks: # list loop
  contents = requests.get(x).content.decode('utf-8')
  if 'isLiveBroadcast' in contents: 
    print(x + ' is live')
    webbrowser.open(x)
    countdown(int(7300)) #waits 2 hours
    os.system('taskkill /im chrome.exe /f') #kills the browser as there isnt a way to close a tab using webbrowser module
    Streamlinks.remove(x) # removes from the list as no longer needed
  else:
   print(x + ' is not live')
   if x == Streamlinks[-1]: #if the item is at the back of the list (I fucking hate this)
    countdown(int(1200))  #sleep for 20 minutes to not spam 
 if Streamlinks == []:
  break
#made by globalsl (discord @)