# coinmover_bybit

## prerequisites:  
Bybit: Create an APIkey and make sure to activate at least: Contracts - Orders Positions  + Wallet - Account Transfer Subaccount Transfer.   

## follow all the steps below to install

## running this script on Windows:
1. Download coinmover_bybit.exe from the releases page ( https://github.com/elmontagne/coinmover_bybit/releases ).   
1a. Aternatively: Download coinmover_bybit_windows.zip.   
2. Make sure to install .net core ( https://dotnet.microsoft.com/download/dotnet-core/3.1/runtime/ ).   
![dotnet](https://user-images.githubusercontent.com/90505490/161711018-c820d2dd-2bb9-4ac9-b6ef-abf3a59a6b38.jpg)

3. Place the exe (or unzip the file if you downloaded the zip file) to the desired location   
4. go to that folder, open the config file in that directory and edit settings (you need at least to enter the API and SECRET key. You can also change the sleeptime (waiting time until next check), percentage move and discord webhook.  
5. unblock the executable (just like you did with wickhunter.exe, rightclick the executable, select properties and if it is there: select unblock).  
6. after all the steps are done, doubleclick the executable to run it.   


## running this script on Linux with Python:   
sudo apt install python3-pip  
pip install pybit  

adviced:  
apt install screen   

Copy coinmover_bybit.py and config.ini to your server OR login to you server and enter: wget https://github.com/elmontagne/coinmover_bybit/archive/refs/heads/main.zip   (after that: unzip main.zip).     

Then edit the config file (see below).  
When all configuration is done, you can run the script: python3 coinmover_bybit.py  
If your want to run the script in the backgroud while logged off, you can use 'screen'. within screen, start the script, then ctrl-a d to disconnect the screen. You can always return to this with 'screen -r'.  
First time the script is run, balance is retrieved and after the next cycle the profits will be moved.


## edit config file.  
edit config.ini , fill in:  
botname: name your bot
api key  
api secret  
percentage_move = percentage of profits to be moved to spot  
sleeptime = after how many minutes you want to run this again  
discord_webhook = your webhook if you want to use discord notifications   
maxmargin = maximum percentage of margin in use. Above this set number there won't be transferred any funds

## thanks
Special thanks to https://github.com/triat for very valuable input improving the script!

Feeling the need to support me?    
0x12469989c0f3b38F0f230F94b58e852249cFC9DD (BEP20/ERC20).   
TVvx4GE4Z9CmpshMyubBHbxizHZ2UxNi4H (TRC20).    

