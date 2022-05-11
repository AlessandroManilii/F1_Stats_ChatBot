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


class ActionShowConstructorStandings(Action):

    def name(self) -> Text:
        return "action_show_constructor_standings"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/constructorStandings.json')

        if r.status_code == 200 :
            data = r.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'])
            rank = [] #lista contenente la classifica 
            header = "Pos. \t Constructor \t points \n" 
            rank.append(header)
            for x in ranking: 
                temp = str("  "+x['position']+"\t"+x['Constructor']['name']+"\t"+x['points']+" \n")
                rank.append(temp) 
            lista = ''.join(rank)  #devo trasformare la lista in stringa per poterla restituire in output
            output="The Constructor standings of the current season {}: \n {}".format(season,lista)
        else:
            output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
        dispatcher.utter_message(text=output)
        return []

        
class ActionConstructorWikipedia(Action):

    def name(self) -> Text:
        return "action_constructor_wikipedia"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        team = next(tracker.get_latest_entity_values('constructor_name'), None)
        if team is None:
            team = tracker.get_slot('constructor_name')
        if team is None:
            output = "Sorry you didn't specify the team.\n"
        else:
            wikipedia.set_lang("en")
            teams = team.replace(" ", "_")
            teams = string.capwords(teams)
            #Api ergast per cercare la pagina wikipedia, poichè le scuderie hanno nomi diversi su wikipedia
            r=requests.get(url='http://ergast.com/api/f1/constructors/'+teams+'.json')


            if r.status_code == 200 :
                data = r.json()
                wiki_url = data['MRData']['ConstructorTable']['Constructors'][0]['url']
                split_str = wiki_url.split("/")
                team = split_str[4]

                if team == "McLaren": #è un bug, se si cerca MClaren esce mc lauren usando il comando dell'else( non so il perchè) 
                    try:
                        p = wikipedia.WikipediaPage(team)
                        output = p.summary 
                    except:
                        output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
                else:
                    try:
                        summary = wikipedia.summary(team, sentences=10)
                        output = summary
                    except:
                        output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"    
            else:
                output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
            
            dispatcher.utter_message(text=output)
            return []

class ActionListConstructors(Action):

    def name(self) -> Text:
        return "action_list_constructors"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/constructorStandings.json')

        if r.status_code == 200 :
            data = r.json()
            season = data['MRData']['StandingsTable']['season']
            ranking = list(data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'])
            rank = [] #lista contenente la classifica 
            for x in ranking: 
                temp = str("  "+x['Constructor']['name']+ "\n")
                rank.append(temp) 
            lista = ''.join(rank)  #devo trasformare la lista in stringa per poterla restituire in output
            output="The Constructor of the current season {}: \n {}".format(season,lista)
        else:
            output = "I do not know anything about, what a mistery!? Are you sure it is correctly spelled?"
        dispatcher.utter_message(text=output)
        return []    

