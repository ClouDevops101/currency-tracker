
<a href="http://bitly.com/2grT54q"><img src="https://cdn.codementor.io/badges/i_am_a_codementor_dark.svg" alt="I am a codementor" style="max-width:100%"/></a><a href="http://bitly.com/2grT54q"><img src="Currency_Exchange.svg" height="50"> 
 [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WX4EKLLLV49WG)

# currency-tracker

Description : A currency exchange tracker based on Boursorama Website. 
1) The idea is to gather information is order to feed a dataset in a first step.
2) Detect and study the algorithme that lead to influence each currency
3) Produce a model.

HOW It WORKS
================
The exchange dict store the revelent value and condition to trigger a notification, ex when a currency is higher or lower than a certain value (bestrate)
```python
exchange = [
    {'devise': 'EUR-MAD', 'condition': '>=', 'bestrate': '10.97', 'weight': 0},
    {'devise': 'EUR-USD', 'condition': '>=', 'bestrate': '1.1944', 'weight': 0},
     {'devise':'USD-MAD','condition':'<=','bestrate':'9.3529','weight':0},
      {'devise':'JPY-EUR','condition':'<', 'bestrate':'0.75166','weight':0},
      {'devise':'CNY-EUR','condition':'>', 'bestrate':'0.12832','weight':0}
]
```

Rotation : Random but the last one :
====================================
This algorithme avoid to check the same currency twice, so the idea is to rotate over other currency randomly.
```python
        while index == last:
            index = random.randint(0, len(exchange) - 1)
```

The configuration is inside the python script : 

Sleep between checks :
====================================
In order to do a clean check and not subcharge the server side, we do a sleep between every check the value is the modulo the variation, as the variation could be negative then the higher the shorter the sleep is , long when the variation is negative. 
```python
        while index == last:
            index = random.randint(0, len(exchange) - 1)
```

The configuration is inside the python script : 
Requierements
================
This code could be run on a linux machine : 

this is systemD configuration to set it up as a deamon :
```
#####/etc/systemd/system/currency-tracker.service 
[Unit]
Description=Currency Tracker
Documentation=http://currency-0000----XXXXXXX.io/
After=network.target

[Service]
Type=simple
User=centos
Group=centos
WorkingDirectory=/home/centos/
ExecStart=/bin/python /home/centos/currency-tracker-v0.1.py

TimeoutStopSec=180
Restart=no

[Install]
WantedBy=multi-user.target
```
it also can be run on a docker container a aws lambda serverless or Amazon azure function

