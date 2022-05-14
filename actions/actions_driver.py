# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
from pathlib import Path
from typing import Any, Text, Dict, List
import requests
import wikipedia
import fastf1 as f1
from fastf1 import plotting
import datetime
from math import isnan
import numpy
import pandas
import matplotlib.pyplot as plt
from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet

codes = {"leclerc": "LEC", "sainz": "SAI", "max_verstappen": "VER", "perez": "PER", "hamilton": "HAM", "russell": "RUS",
         "norris": "NOR", "ricciardo": "RIC", "alonso" : "ALO", "ocon" : "OCO", "gasly" : "GAS", "tsunoda" : "TSU",
         "magnussen" : "MAG", "mick_schumacher" : "MSC", "vettel" : "VET", "stroll" : "STR", "albon" : "alb", "latifi": "LAT",
         "bottas" : "BOT", "zhou" : "ZHO", "hulkenberg": "HUL"}


class ActionShowStandings(Action):

    def name(self) -> Text:
        return "action_show_standings"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/driverStandings.json')

        if r.status_code == 200 :
            data = r.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])
            rank = [] #lista contenente la classifica 
            header = "Pos.\tDrivers\t\tpoints\tConstructor \n" 
            rank.append(header)
            for x in ranking:
                tabs = "\t\t"
                if len(x['Driver']['familyName']) > 7:
                    tabs = "\t"
                temp = str("  "+x['position']+"\t"+x['Driver']['familyName']+tabs+x['points']+"\t["+x['Constructors'][0]['name'] +"]\n")
                rank.append(temp) 
            lista = ''.join(rank)  #devo trasformare la lista in stringa per poterla restituire in output
            output="The drivers standings of the current season {}: \n {}".format(season,lista)
        else:
            output = "Sorry there might be a problem with the server, please try again.\n"
        dispatcher.utter_message(text=output)
        return []
    
class ActionShowChampionshipLeader(Action):

    def name(self) -> Text:
        return "action_show_championship_leader"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/driverStandings.json')

        if r.status_code == 200 :
            data = r.json()
            season = data['MRData']['StandingsTable']['season']
            leader = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][0]
            output = leader['Driver']['givenName'] + " " + leader['Driver']['familyName'] + " "           
            output += "is leading the championship with "+ leader['points'] +" points.\n"
        else:
            output = "Sorry there might be a problem with the server, please try again.\n"
        dispatcher.utter_message(text=output)
        return [SlotSet("driver", leader["Driver"]["driverId"])]

class ActionShowDriverStanding(Action):

    def name(self) -> Text:
        return "action_show_driver_standing"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        driver = next(tracker.get_latest_entity_values('driver'), None)
        if driver is None:
            driver = tracker.get_slot('driver')
        if driver is None:
            output = "Sorry you didn't specify the driver.\n"
        else:
        
            r=requests.get(url='http://ergast.com/api/f1/current/driverStandings.json')

            if r.status_code == 200 :
                data = r.json()
                season = data['MRData']['StandingsTable']['season']
                ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])
                not_found = True
                driver = driver.lower()
                for x in ranking:
                    if x['Driver']['driverId'] == driver:
                        output = x['Driver']['givenName'] + " " + x['Driver']['familyName'] + " "
                        if x['position'] =='1':
                            output += "is leading the championship with "+ x['points'] +" points\n"
                        else:
                            output += "is in position n° "+x['position'] +" with " + x['points'] + " points \n"
                        not_found = False
                        break
                if not_found:
                    output = "Sorry, maybe you spelled his name wrong or he's not participating in the current season.\n"
            else:
                output = "Sorry there might be a problem with the server, please try again.\n"
        dispatcher.utter_message(text=output)
        return []


class ActionShowDriverInfo(Action):

    def name(self) -> Text:
        return "action_show_driver_info"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        driver = next(tracker.get_latest_entity_values('driver'), None)
        if driver is None:
            driver = tracker.get_slot('driver')
        if driver is None:
            output = "Sorry, you didn't specify the driver.\n"
        else:
            driver = driver.lower()
            r=requests.get(url='http://ergast.com/api/f1/drivers/'+driver+'.json')

            if r.status_code == 200 :
                data = r.json()
                d = data['MRData']['DriverTable']['Drivers'][0]
                wikipedia.set_lang("en")
                try:
                    xt = ""
                    if d["familyName"] == "Sainz":
                        xt=" Jr."
                    summary = wikipedia.summary(d["givenName"]+ " " +d["familyName"]+xt,auto_suggest=False, sentences = 3)
                    output = str(summary)
                except Exception as e:
                    output = str(e)+". There might be problems with wikipedia at the moment, please try later.\n"
            else:
                output = "Sorry there might be a problem with the server, please try again.\n"
        dispatcher.utter_message(text=output)
        return []

class ActionShowDriverLapTimes(Action):

    def name(self) -> Text:
        return "action_show_driver_lap_times"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        driver = next(tracker.get_latest_entity_values('driver'), None)
        if driver is None:
            driver = tracker.get_slot('driver')
        race = next(tracker.get_latest_entity_values('race_name'), None)
        if race is None:
            race = tracker.get_slot('race_name')
        stype = next(tracker.get_latest_entity_values('session_type'), None)
        if stype is None:
            # output = "Sorry, you didn't specify the session (race,qualifying,sprint,etc...).\n"
            stype = "race"
        
        if driver is None:
            output = "Sorry, you didn't specify the driver.\n"
        elif driver not in codes:
            output = "Sorry, this driver is not participating in this season.\n"
        elif race is None:
            output = "Sorry, you didn't specify a grand prix or a circuit.\n"
        else:
            now = datetime.datetime.now()
            year = int(now.date().strftime("%Y"))
            f1.Cache.enable_cache('./f1_cache')
            driver = driver.lower()
            try:
                session = f1.get_session(year, race, stype)
            except ValueError as e:
                output = "Sorry. "+ str(e) +"\n"
            else:
                if session.date > now:
                   output = "The session hasn't started yet.\n"
                else:
                    session.load(weather=False)
                    try:
                        dr = session.get_driver(codes[driver])
                    except ValueError as e:
                        output = "Sorry, there is no data for " + driver + " during '"+ session.name + "' of the " + session.event["EventName"] + ".\n"    
                    else:
                        if session.name != "Qualifying":
                            ft = session.laps.pick_driver(codes[driver]).pick_fastest()
                            if type(ft["LapTime"]) is numpy.float64 and isnan(ft["LapTime"]):
                                output = "Sorry, there is no data for " + dr["FirstName"] + " " + dr["LastName"] + " during '"+ session.name + "' of the " + session.event["EventName"] + ".\n"
                            else:
                                output = dr["FirstName"] + " " + dr["LastName"] + "'s fastest lap during '" + session.name + "' of the " + session.event["EventName"] + " is:\n"
                                lt = lap_time(ft["LapTime"])
                                output +=  lt +" with " + ft["Compound"] + " tyres on lap n° "+ str(int(ft["LapNumber"]))+ ".\n" 
                        else:
                            output = dr["FirstName"] + " " + dr["LastName"] + "'s qualifying laps of the " + session.event["EventName"] + " are:\n"
                            results = session.results
                            for i in range(1, 4):
                                data = results.loc[:,['Abbreviation', 'Q'+str(i)]]
                                time = data[data['Abbreviation'] == codes[driver]].iat[0,1]
                                if pandas.isnull(time):
                                    output += "Q"+str(i)+": no time\n"
                                else:
                                    lt = lap_time(time)
                                    output += "Q"+str(i)+": " + lt+"\n" 
        dispatcher.utter_message(text=output)
        return []



def lap_time(timedelta):
    millis = timedelta.microseconds / 1000
    minutes, seconds = divmod(timedelta.seconds, 60)
    return ("{:01}:{:02}.{:03}".format(int(minutes), int(seconds), int(millis)))


class ActionTelemetry(Action):

    def name(self) -> Text:
        return "action_telemetry"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        plotting.setup_mpl()


        now = datetime.datetime.now()
        year = int(now.date().strftime("%Y"))
        f1.Cache.enable_cache('./f1_cache')

        driver1 = tracker.get_slot('driver1t').lower()
        driver2 = tracker.get_slot('driver2t').lower()
        race_name = tracker.get_slot('race_name_t')

        race = f1.get_session(year, race_name, 'R')
        race.load()

        d1 = race.laps.pick_driver(codes[driver1])
        d2 = race.laps.pick_driver(codes[driver2])

        fig, ax = plt.subplots()
        ax.plot(lec['LapNumber'], d1['LapTime'], color='red')
        ax.plot(ham['LapNumber'], d2['LapTime'], color='cyan')
        ax.set_title("{0} vs {1}".format(driver1, driver2))
        ax.set_xlabel("Lap Number")
        ax.set_ylabel("Lap Time")
        
        plt.savefig('./img/telemetry.png')
        with open("url.txt") as file:
            init_path = file.readlines()
        path = init_path[0] +"/img/telemetry.png"  #url da cambiare ogni volta (unica limitazione)
        dispatcher.utter_message(image = path)
        return [] 

class ActionShowDriverConstructors(Action):

    def name(self) -> Text:
        return "action_show_driver_constructors"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        driver = next(tracker.get_latest_entity_values('driver'), None)
        if driver is None:
            driver = tracker.get_slot('driver')
        driver = driver.lower()
        if driver is None:
            output = "Sorry you didn't specify the driver.\n"
        elif driver not in codes:
            output = "Sorry, this driver is not participating in this season.\n"
        else:   
            # I have to specify current because in the list of all constructors the records aren't ordered
            r = requests.get(url='http://ergast.com/api/f1/current/drivers/'+driver+'/constructors.json')
            r2 = requests.get(url='http://ergast.com/api/f1/drivers/'+driver+'.json')
            r3 = requests.get(url='http://ergast.com/api/f1/drivers/'+driver+'/constructors.json')
            if r.status_code == 200 and r2.status_code == 200 and r3.status_code == 200:
                data = r.json()
                data2 = r2.json()
                data3 = r3.json()
                
                driver = data2['MRData']['DriverTable']['Drivers'][0]
                driver_name = driver["givenName"] + " " + driver["familyName"]
                total = int(data3['MRData']['total'])
                current = data['MRData']['ConstructorTable']['Constructors'][0]
                constructors = data3['MRData']['ConstructorTable']['Constructors']
                c_name = current["name"]
                output = driver_name + " is currently driving for " + current["name"] + ".\n"
                if total > 1:
                    output += "He has previously driven for:\n"
                    for i in range(0, total):
                        if constructors[i]["name"] != c_name:
                            output += constructors[i]["name"] + "\n"
            else:
                output = "Sorry there might be a problem with the server, please try again.\n"
        dispatcher.utter_message(text=output)
        return []
     
