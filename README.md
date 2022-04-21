<p align="center">
   <a href="https://github.com/vckyou/GeezProjects"><img src="https://telegra.ph/file/8e256cb133087b060e288.png" alt="Geez Projects" width=240px></a>
   <br>
   <br>
</p>

## INFORMASI

```
Saya tidak bertanggung jawab atas penyalahgunaan bot ini.
Bot ini dimaksudkan untuk bersenang-senang sekaligus membantu Anda
mengelola grup secara efisien dan mengotomatiskan beberapa hal yang membosankan.
Gunakan bot ini dengan risiko Anda sendiri, dan gunakan dengan bijak.

Selamat Menikmati :D
```

## GeezProjects Bot

[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

|Deploy Via Bot|  Deploy Via Web|
|--|--|
| [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://telegram.dog/XTZ_HerokuBot?start=dmNreW91L0dlZXpQcm9qZWN0cyBtYXN0ZXI) | [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://geezram.now.sh) |


### Create String Session

[![Run on Repl.it](https://repl.it/badge/github/jasonalantolbert/replit-badger)](https://repl.it/@vckyou/String)



### DeepSource


[![DeepSource](https://deepsource.io/gh/vckyou/GeezProjects.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/vckyou/GeezProjects/?ref=repository-badge)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![DeepSource](https://deepsource.io/gh/vckyou/GeezProjects.svg/?label=resolved+issues&show_trend=true)](https://deepsource.io/gh/vckyou/GeezProjects/?ref=repository-badge)


### Tutorial Deploy To VPS

-  ( `git clone https://github.com/vckyou/GeezProjects` )
-  ( `cd GeezProjects` )
-  ( `pip3 install -r requirements.txt` )
-  ( `mv sample_config.env config.env` )
-  edit config.env Anda dan isi VARS menggunakan ( `nano config.env` ) `CTRL + S ` untuk menyimpan VARS Anda, gunakan `CTRL + X` untuk keluar dan kembali ke direktori GeezProjects
-  Buka SCRREN di VPS Anda ( `screen -S GeezProjects` )
-  Kemudian gunakan perintah ini untuk menyebarkan GeezProjects ( `python3 -m userbot` ) Atau ( `bash start` )


### Example Plugin

  ```python
from  datetime  import  datetime
from userbot import bot
from userbot.utils import edit_or_reply, geez_cmd

@geez_cmd(pattern="ping")
async def ping(event):
	start  =  datetime.now()
	await edit_or_reply(event, "Pong!")
	end  =  datetime.now()
	ms  = (end  -  start).microseconds  /  1000
	await edit_or_reply(event, "Pong!\n`{}`".format(ms))
```

### My inspiration 🍂
*   [AdekMaulana](https://github.com/adekmaulana) : ProjectBish
*   [RaphielGang](https://github.com/RaphielGang) : Paperplane
*   [TeamUltroid](https://github.com/TeamUltroid/Ultroid) :  UltroidUserbot
*   [BianSepang](https://github.com/BianSepang/WeebProject) : WeebProject
*   [Sandy1709](https://github.com/sandy1709/catuserbot) : CatUserbot
*   [VICKY](https://github.com/vckyou/GeezProjects) :  GeezProjects
*   [Risman](https://github.com/mrismanaziz/Man-Userbot) :  Man-Userbot
*   [Alvin](https://github.com/Zora24/Lord-Userbot) : Lord-Userbot
*   [X_ImFine](https://github.com/ximfine) :  XBot-REMIX

### Credits
* [![TeamGeez](https://img.shields.io/static/v1?label=GeezProjects&message=contributions&color=critical)](https://github.com/vckyou/GeezProjects/graphs/contributors)
* [Lonami](https://github.com/LonamiWebs/) for [Telethon.](https://github.com/LonamiWebs/Telethon)
* [Laky](https://github.com/Laky-64) for [PyTgCalls.](https://github.com/pytgcalls/pytgcalls)


### License ⚠️
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
GeezProjects is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.
