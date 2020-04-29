The purpose of this script is to pull down the top winners and losers of stock data that day.

That is done by web scraping

This then is used to drive what stock information we are pulling, and identifying a summary of the latest stock news that is out there, as wells as analyist sentiment

We then passed that information to MsSQL, for safe keeping

Then finally, pulled this infomraiton from MsSQL all in Python


-----------------------

How to run:

One, you will need a FinnHubb API key, it is free so go to the website, insert it in the code

Next you will need MsSQL

Note, in the engine you will need to identify the vairables such as computer name, password, ports, etc.  Port usually is 1433, but you will need to active this port on your MsSQL server so that it is "open" to receive data from PyThon