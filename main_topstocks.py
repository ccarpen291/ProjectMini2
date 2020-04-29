# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd



from pprint import pprint
import datetime
from datetime import date
from time import time
from time import sleep
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import scipy as stat
from sqlalchemy import *

base_url = 'https://finnhub.io/api/v1/'
api_key = "api key here"


# URL of page to be scraped
url = 'https://thestockmarketwatch.com/markets/after-hours/trading.aspx'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')

# Check to see if the website access works. Expect 200.
response

#Write the gainers table to DF. Gainers is the 2nd table.
gainers = pd.read_html(soup.prettify())[1]

#Check the DF.
gainers.head()

#Clean up the column names
gainers_clean = gainers.rename(columns={"%Chg": "percent_change", "Last":"last_price", "Symb":"symbol", "Company":"company", "Volume":"volume"})

#Fix the data in the last_price column.
gainers_clean['last_price'] = gainers_clean['last_price'].str.split(' ').str[2]

#Show the new DF.
gainers_clean
gainers_clean_df = gainers_clean

#Write the gainers table to DF. Gainers is the 3rd table.
losers = pd.read_html(soup.prettify())[2]

#Clean up the column names
losers_clean = losers.rename(columns={"%Chg": "percent_change", "Last":"last_price", "Symb":"symbol", "Company":"company", "Volume":"volume"})

#Fix the data in the last_price column.
losers_clean['last_price'] = losers_clean['last_price'].str.split(' ').str[2]

#Show the new DF.
losers_clean

loser_clean_df=losers_clean

#Check the DF.
#print(losers.head())

#Clean up the column names
losers_clean = losers.rename(columns={"%Chg": "percent_change", "Last":"last_price", "Symb":"symbol", "Company":"company", "Volume":"volume"})

#Fix the data in the last_price column.
losers_clean['last_price'] = losers_clean['last_price'].str.split(' ').str[2]

#Show the new DF.
losers_clean

# Check the raw HTML grab.
#print(soup.prettify())

# Make a list of the gainers symbols.

gainers_list = gainers_clean['symbol'].tolist()
gainers_list

# Make a list of the losers symbols.

losers_list = losers_clean['symbol'].tolist()
losers_list

################################################################################
#Start pulling FinnHubb data
#This calls several codes from the api to give a brief summary of the selected stock
names = []
quotes = []
target_H = []
target_L = []
target_A = []
target_update = []
tech_analysis_B = []
tech_analysis_S = []
tech_analysis_N = []
tech_analysis_sig = []
news_bull = []
news_bear = []
resolution = 5

counter = 0
for gain in gainers_list: 
  counter +=1
  print(f"Gainers currently gathered...{counter} of {len(gainers_list)}")
  #Price Target
  price_target = requests.get(f'{base_url}/stock/price-target?symbol={gain}&token={api_key}').json()

  #Stock Quote
  quote = requests.get(f'{base_url}/quote?symbol={gain}&token={api_key}').json()

  #Aggregate Indicators
  tech_ind = requests.get(f'{base_url}/scan/technical-indicator?symbol={gain}&resolution={resolution}&token={api_key}').json()


  news_sentiment = requests.get(f'{base_url}news-sentiment?symbol={gain}&token={api_key}').json()

  names.append(gain)
  quotes.append(quote['c'])

  target_H.append(price_target['targetHigh'])
  target_L.append(price_target['targetLow'])
  target_A.append(price_target['targetMean'])
  target_update.append(price_target['lastUpdated'][:10])


  try:
    tech_analysis_B.append(tech_ind['technicalAnalysis']['count']['buy'])
  except:
    tech_analysis_B.append("NA")  
  try:
    tech_analysis_S.append(tech_ind['technicalAnalysis']['count']['sell'])
  except:
    tech_analysis_S.append("NA")     
  try:
    tech_analysis_N.append(tech_ind['technicalAnalysis']['count']['neutral'])
  except:
    tech_analysis_N.append("NA") 
  try:
    tech_analysis_sig.append(tech_ind['technicalAnalysis']['signal'])
  except:
    tech_analysis_sig.append("NA") 

  try:
    news_bull.append(news_sentiment['sentiment']['bullishPercent'])
  except:
    news_bull.append('NA')    
  try:
    news_bear.append(news_sentiment['sentiment']['bearishPercent'])
  except:
    news_bear.append('NA')

  sleep(1)

raw_data_gain = {"Name":names,"Quote":quotes,"High Target":target_H,"Low Target":target_L,
              "Avg Target":target_A,"Target Updated":target_update,"Buy":tech_analysis_B,
              "Sell":tech_analysis_S,"Neutral":tech_analysis_N,
              "Signal":tech_analysis_sig,"News Bull%":news_bull,"News Bear%":news_bear }
loop_df_gain = pd.DataFrame(raw_data_gain) 
loop_df_gain.head(10)


resolution = 5


#Losers

#this is the resolution of the days
resolution = 5

#This calls several codes from the api to give a brief summary of the selected stock
names = []
quotes = []
target_H = []
target_L = []
target_A = []
target_update = []
tech_analysis_B = []
tech_analysis_S = []
tech_analysis_N = []
tech_analysis_sig = []
news_bull = []
news_bear = []

counter = 0
for lose in losers_list: 
  counter +=1
  print(f"Loers currently gathered...{counter} of {len(losers_list)}")
  #Price Target
  try:
      requests.get(f'{base_url}/stock/price-target?symbol={lose}&token={api_key}').json()
  except:
      pass
  try:
    price_target = requests.get(f'{base_url}/stock/price-target?symbol={lose}&token={api_key}').json()
  except:
    price_target = 0

  #Stock Quote
  try:
   quote = requests.get(f'{base_url}/quote?symbol={lose}&token={api_key}').json()
  except:
   quote = "NA"

  #Aggregate Indicators
  try:
    tech_ind = requests.get(f'{base_url}/scan/technical-indicator?symbol={lose}&resolution={resolution}&token={api_key}').json()
  except:
    tech_ind = "NA"


  try:
    news_sentiment = requests.get(f'{base_url}news-sentiment?symbol={lose}&token={api_key}').json()
  except:
    news_sentiment = "NA"
  try:
    names.append(lose)
  except:
    names.append("NA")
  try:
    quotes.append(quote['c'])
  except:
    quotes.append("NA")
  try:
    target_H.append(price_target['targetHigh'])
  except:
    target_H.append(0)
  try:
    target_L.append(price_target['targetLow'])
  except:
    target_L.append(0)
  try:
    target_A.append(price_target['targetMean'])
  except:
    target_A.append(0)
  try:
    target_update.append(price_target['lastUpdated'][:10])
  except:
    target_update.append(0)


  try:
    tech_analysis_B.append(tech_ind['technicalAnalysis']['count']['buy'])
  except:
    tech_analysis_B.append("NA")  
  try:
    tech_analysis_S.append(tech_ind['technicalAnalysis']['count']['sell'])
  except:
    tech_analysis_S.append("NA")     
  try:
    tech_analysis_N.append(tech_ind['technicalAnalysis']['count']['neutral'])
  except:
    tech_analysis_N.append("NA") 
  try:
    tech_analysis_sig.append(tech_ind['technicalAnalysis']['signal'])
  except:
    tech_analysis_sig.append("NA") 
    
  try:
    news_bull.append(news_sentiment['sentiment']['bullishPercent'])
  except:
    news_bull.append('NA')    
  try:
    news_bear.append(news_sentiment['sentiment']['bearishPercent'])
  except:
    news_bear.append('NA')

  sleep(1)

raw_data_lose = {"Name":names,"Quote":quotes,"High Target":target_H,"Low Target":target_L,
              "Avg Target":target_A,"Target Updated":target_update,"Buy":tech_analysis_B,
              "Sell":tech_analysis_S,"Neutral":tech_analysis_N,
              "Signal":tech_analysis_sig,"News Bull%":news_bull,"News Bear%":news_bear }
loop_df_lose = pd.DataFrame(raw_data_lose) 
loop_df_lose.head(10)


#########################################################
##################SQL###################################
#########################################################

################################################################################
#Fire up the engine
engine = create_engine('mssql+pymssql://Computer_Name\User_Login:User_Password@localhost:_DBS Port_/_ServerName')
#Pass the data to the SQL server
loser_clean_df.to_sql('TOP_Losers', engine, if_exists = 'append', index = False)
gainers_clean_df.to_sql('TOP_Gainers', engine, if_exists = 'append', index = False)
loop_df_gain.to_sql('Stock_Gainers', engine, if_exists = 'append', index = False)
loop_df_lose.to_sql('Stock_Losers', engine, if_exists = 'append', index = False)
#covid_df.to_sql('COVID_History', engine, if_exists = 'replace', index = False)


#Pull and print the data from the server
print(pd.read_sql_table('TOP_Losers',engine))
print(pd.read_sql_table('TOP_Gainers',engine))
print(pd.read_sql_table('Stock_Gainers',engine))
print(pd.read_sql_table('Stock_Losers',engine))

