Python script
Only checks if the given streamer is live 
watches the stream for 1 hours. Very basic.<br/>
Logs in to twitch via auth token(cookie)<br/>
# V2
* Complete rewrite
* use of selenium
* checks if streamer has twitch drops enabled or you have already claimed it
* multidimentional list(basically means that you can group streamers(1 item - 2 streamers that drop it)
* configurable
* simple to use
## V2.1
* added firefox support
* added headless mode support
* disabled image loading for performance
## Requirements
```
pip install selenium
```
python >= 3.8
 
## streamer_list.txt
How it works:
```
https://www.twitch.tv/streamer1 https://www.twitch.tv/streamer2 --> 1 drop, but 2 streamers can drop it
https://www.twitch.tv/streamer3                                 --> 1 drop, and only 1 streamer can drop it
https://www.twitch.tv/streamer4
https://www.twitch.tv/streamer5 https://www.twitch.tv/streamer6  
``` 
Basically 1 line = 1 drop
## config.ini
type of drop = ''<br/>
![image](https://github.com/user-attachments/assets/1b212ccf-7a9c-4afb-be32-e1977b0050d3)<br/>
will detect the type of drop by the words in the large red circle<br/>
the drop down menu will not apear if you have claimed the drop or if drops are disabled
### Screenshot
![image](https://github.com/user-attachments/assets/da3411d2-9015-44ad-9160-ef56e775275f)
