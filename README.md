## • Note

* This is a edited version of https://github.com/termuxprofessor/TeleGram-Scraper-Adder
* I have added error handlers and fixed colours in adder.py
* You can contact me on <a href="t.me/Halto_Tha">Telegram</a>

## • API Setup
* Go to http://my.telegram.org  and log in.
* Click on API development tools and fill the required fields.
* put app name you want & select other in platform Example :
* copy "api_id" & "api_hash" after clicking create app ( will be used in setup.py )

## • How To Install and Use In Termux

`$ pkg up -y`

`$ pkg install python -y`

`$ pkg install git`

`$ git clone https://github.com/DeveloperJayu/TGAdder`

`$ cd TGAdder`

* Install requierments & Setup Configuration File. ( apiID, apiHash )

`$ python setup.py`

* To Scrape members from group.

`$ python scraper.py`

* Add Scrapped members to your group. 

`$ python adder.py`
