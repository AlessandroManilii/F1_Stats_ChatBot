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
from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet


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
            output = "Sorry there might be a problem with the server, please try again\n"
        dispatcher.utter_message(text=output)
        return []

class ActionShowDriverStanding(Action):

    def name(self) -> Text:
        return "action_show_driver_standing"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        driver = next(tracker.get_latest_entity_values('driver'), None)
        # dispatcher.utter_message(text=driver)
        # driver = 'leclerc'
        
        r=requests.get(url='http://ergast.com/api/f1/current/driverStandings.json')

        if r.status_code == 200 :
            data = r.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])
            not_found = True
            for x in ranking:
                if x['Driver']['driverId'] == driver:
                    output = x['Driver']['givenName'] + " " + x['Driver']['familyName'] + " "
                    if x['position'] =='1':
                        output += "is leading the championship with "+ x['points'] +"\n"
                    else:
                        output += "is in position n° "+x['position'] +" with " + x['points'] + " points \n"
                    not_found = False
                    break
            if not_found:
                output = "Sorry, maybe you spelled his name wrong or he's not participating in the current season\n"
        else:
            output = "Sorry there might be a problem with the server, please try again\n"
        dispatcher.utter_message(text=output)
        return []
     
