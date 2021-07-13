# RAT-Telegram-Bot
Windows Remote Admitistrations Tool for fully remote computer control via Telegram

## Installation
* Clone this repo
* Create a new telegram bot via @BotFather and copy its **API**
* Find @ShowJsonBot to get your **id**. message -> from -> id
* Paste your bot **API** and **id** into config.py file
* Download [Python](https://www.python.org/downloads/) (**add to path**)
* Download [OpenHardwareMonitor](https://openhardwaremonitor.org/downloads/)
* We need only OpenHardwareMonitorLib.dll from it. Place it into your main folder
* Install necessary requirements using `pip install -r requirements.txt`
* Create .exe file using `pyinstaller -w -F bot.py` (dist/bot.exe)
* Place bot.exe in root folder
* Well done! Run bot.exe

### Notice
* Run bot.exe as an administrator to get full list of hardware temperatures

## Features
* Power management: shutdown, restart (also using delay)
* Execution of any cmd-commands
* Tracking hardware temperature
* Screenshot
* Shows PC and user info (Username, PC name, IP)

## Commands
```
/start
/shut - shotdown menu
/restart - restart menu
/temperature - temperature menu
/spec - user info
/screenshot - make a screenshot
/help - installation guide
```

## TODO
* Add english
* Track other hardware info
* Add more functions
* Add screenshots
