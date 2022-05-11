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
import string
from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet

class ActionShowStandingYear(Action):

    def name(self) -> Text:
        return "action_show_standings_year"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        year = str(tracker.get_slot('season'))
        r_d=requests.get(url='https://ergast.com/api/f1/'+  year +'/last/driverStandings.json')
        flag_d = False
        r_c =requests.get(url='https://ergast.com/api/f1/'+ year +'/last/ConstructorStandings.json')
        flag_c = False
        output1 = ""
        output2 = ""

        if r_d.status_code == 200 :
            data = r_d.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])
            rank = []
            header = "Pos. \t Driver \t points \n"
            rank.append(header)
            for x in ranking:
                if x['position'] == '1':
                    winner = str(x['Driver']['givenName']+" "+x['Driver']['familyName'])
                    winnercar = str(x['Constructors'][0]['name']) 
                temp = str("  "+x['position']+"\t"+x['Driver']['givenName']+" "+x['Driver']['familyName']+"\t"+x['points']+" \n")
                rank.append(temp)
            lista = ''.join(rank)
            output1="The driver who won the championship in {} was {} with {}. \n The drivers standings of the season {}: \n {}".format(season,winner,winnercar,season,lista)
        else:
            flag_d = True
        
        if r_c.status_code == 200 :
            data = r_c.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'])
            rank = []
            header = "Pos. \t Constructor \t points \n"
            rank.append(header)
            for x in ranking:
                if x['position'] == '1':
                    winnercar = str(x['Constructor']['name'])
                temp = str("  "+x['position']+"\t"+x['Constructor']['name']+"\t"+x['points']+" \n")
                rank.append(temp)
            lista = ''.join(rank)
            output2="\n The Constructor who won the championship in {} was {}. \n The Constructor standings of the season {}: \n {}".format(season,winnercar,season,lista)
        else:
            flag_c = True

        if flag_c and flag_d: 
            output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
        
        output = output1+output2
        dispatcher.utter_message(text=output)
        return []

class ActionChampionshipWikipedia(Action):

    def name(self) -> Text:
        return "action_championship_wikipedia"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        season = str(tracker.get_slot('season'))
        wikipedia.set_lang("en")
        try:
            search = season + "_Formula_One_World_Championship"
            summary = wikipedia.summary(search, sentences = 12)
            output = str(summary)
        except:
            output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
        dispatcher.utter_message(text=output)
        return []

class ActionShowWinnerYear(Action):

    def name(self) -> Text:
        return "action_show_winner_year"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        year = str(tracker.get_slot('season'))
        r_d=requests.get(url='https://ergast.com/api/f1/'+  year +'/last/driverStandings.json')


        if r_d.status_code == 200 :
            data = r_d.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])
            for x in ranking:
                if x['position'] == '1':
                    winner = str(x['Driver']['givenName']+" "+x['Driver']['familyName'])
                    winnercar = str(x['Constructors'][0]['name']) 
                    break
            output="The driver who won the championship in {} was {} with {}. \n".format(season,winner,winnercar)
        else:
            output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
        
        dispatcher.utter_message(text=output)
        return []        