#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import datetime
import time
from tqdm import tqdm
import pandas as pd


# In[4]:


class flighttrack:
    def __init__(self, apikey) -> None:
        self.apikey = apikey
    def apiget(self,url,params):
        headers = {
            "X-RapidAPI-Key": self.apikey,
            "X-RapidAPI-Host": "flightera-flight-data.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()


# In[5]:


def getFlightInfo(self, flightNumber, date = None, outputToConsole = True):
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            params = {"flnr":flightNumber,"date":date}
        else:
            params = {"flnr":flightNumber}
        result = self.apiget("https://flightera-flight-data.p.rapidapi.com/flight/info",params)
        if 'Error' in result:
            print(result['Error'].replace('this flight number', flightNumber).replace('this date', date))
            return None
        if 'message' in result:
            print(result['message'])
            return None
        info_dict = {}
        info_dict["Flight Number"] = result[0].get("flnr",'N/A')
        info_dict["Status"] = result[0].get('status','N/A')
        info_dict["Airline Name"] = result[0].get('airline_name','N/A')
        info_dict["Departure"] = result[0].get("departure_name",'N/A')
        info_dict["Departure City"] = result[0].get("departure_city",'N/A')
        info_dict["Scheduled Departure"] = result[0].get("scheduled_departure_utc",'N/A')
        info_dict["Actual Departure"] = result[0].get("actual_departure_utc",'N/A')
        info_dict["Departure Terminal"] = result[0].get("departure_terminal",'N/A')
        info_dict["Departure Gate"] = result[0].get("departure_gate",'N/A')
        info_dict["Arrival"] = result[0].get("arrival_name",'N/A')
        info_dict["Arrival City"] = result[0].get("arrival_city",'N/A')
        info_dict["Scheduled Arrival"] = result[0].get("scheduled_arrival_utc",'N/A')
        info_dict["Actual Arrival"] = result[0].get("actual_arrival_utc",'N/A')
        info_dict["Arrival Terminal"] = result[0].get("arrival_terminal",'N/A')
        info_dict["Arrival Gate"] = result[0].get("arrival_gate",'N/A')
        if outputToConsole:
            for key,value in info_dict.items():
                print("{:>20}:\t{}".format(key,value))
            return
        return info_dict


# In[6]:


def getTravelInfo(self,departure,arrival,date,airline,resultCnt = 10):
        select_date = date
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        params = {"name":airline}
        result = self.apiget("https://flightera-flight-data.p.rapidapi.com/airline/search",params)
        if len(result)==0:
            print("Cannot find the airline '{}', please check your input!".format(airline))
            return
        if len(result)>1:
            print("Found {} airlines match {}, please choose one: ".format(len(result),airline),end='')
            for a in result:
                print(a['name'],end=' ')
            print("")
            return
        ident = result[0]['ident']
        flights = []
        while (date.strftime('%Y-%m-%d')==select_date):
            params = {"time":date.strftime('%Y-%m-%d %H:%M:%S'),"ident":ident}
            result = self.apiget("https://flightera-flight-data.p.rapidapi.com/airline/flights",params)
            time.sleep(0.5)
            for flight in result['flights']:
                if datetime.datetime.strptime(flight['date'],'%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d') == select_date:
                    flights.append(flight['flnr'])
                    if len(flights)>resultCnt:
                        break
            if len(flights)>resultCnt:
                break
            date = datetime.datetime.strptime(result['next_time'],'%Y-%m-%dT%H:%M:%SZ')
            print("\rGot {} flights".format(len(flights)))
        if len(flights) == 0:
            print("Couldn't find the flight.")
            return
        available = []
        for i in tqdm(range(len(flights)),desc='Getting flight info'):
            info = self.getFlightInfo(flights[i],outputToConsole=False)
            if info['Departure City'].lower() == departure.lower() and info['Arrival City'].lower() == arrival.lower():
                available.append(info)
            time.sleep(0.6)
        if len(available) == 0:
            print("Couldn't find the flight.")
            return
        return pd.DataFrame.from_dict(available)
        


# In[1]:


jupyter nbconvert --to script flight_track.ipynb


# In[ ]:




