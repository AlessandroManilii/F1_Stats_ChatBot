# This files contains custom actions related to races

import json
from pathlib import Path
from typing import Any, Text, Dict, List
import requests
import wikipedia
from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet

class ActionNextRace(Action):

    def name(self) -> Text:
        return "action_next_race"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/next.json')
        if r.status_code == 200 :
            data = r.json()
            data = data['MRData'] ['RaceTable']['Races'][0]
            season = data['season']
            round = data['round']
            name = data['raceName']
            country = data['Circuit']['Location']['country']
            city = data['Circuit']['Location']['locality']
            circuit_name = data['Circuit']['circuitName']
            schedule_header = "\t\tDate\t\tTime \n"
            output = "The next race for " + season + " season is " \
                + name + " (n° " + str(round) + ").\n" \
                + "It will be held in " + country + "," + city \
                + " at " + circuit_name + ".\n" \
                + "The following it's the official race schedule:\n" \
                + schedule_header \
                + "Race \t\t" + data['date'] + "\t" + data['time'].replace(':00Z', " (GMT)") + "\n" \
                + "First Practice \t" + data['FirstPractice']['date'] \
                    + "\t" + data['FirstPractice']['time'].replace(':00Z', " (GMT)") + "\n" \
                + "Second Practice\t" + data['SecondPractice']['date'] \
                    + "\t" + data['SecondPractice']['time'].replace(':00Z', " (GMT)") + "\n" \
                + "Qualifying \t" +  data['Qualifying']['date'] \
                    + "\t" + data['Qualifying']['time'].replace(':00Z', " (GMT)") + "\n"

            if 'Sprint' in data:
                output += "Sprint \t" +  data['Sprint']['date'] \
                    + "\t" + data['Sprint']['time'].replace(':00Z', " (GMT)")
        else:
            output = "Sorry there might be a problem with the server, please try again\n"

        dispatcher.utter_message(text=output)
        return []

class ActionNextRaceSchedule(Action):

    def name(self) -> Text:
        return "action_next_race_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/next.json')
        if r.status_code == 200 :
            data = r.json()
            data = data['MRData'] ['RaceTable']['Races'][0]
            name = data['raceName']
            schedule_header = "\t\tDate\t\tTime \n"
            output = "The following it's the official race schedule for " + name + ":\n" \
                + schedule_header \
                + "Race \t\t" + data['date'] + "\t" + data['time'].replace(':00Z', " (GMT)") + "\n" \
                + "First Practice \t" + data['FirstPractice']['date'] \
                    + "\t" + data['FirstPractice']['time'].replace(':00Z', " (GMT)") + "\n" \
                + "Second Practice\t" + data['SecondPractice']['date'] \
                    + "\t" + data['SecondPractice']['time'].replace(':00Z', " (GMT)") + "\n" \
                + "Qualifying \t" +  data['Qualifying']['date'] \
                    + "\t" + data['Qualifying']['time'].replace(':00Z', " (GMT)") + "\n"

            if 'Sprint' in data:
                output += "Sprint \t" +  data['Sprint']['date'] \
                    + "\t" + data['Sprint']['time'].replace(':00Z', " (GMT)")
        else:
            output = "Sorry there might be a problem with the server, please try again\n"

        dispatcher.utter_message(text=output)
        return []

class ActionLastRace(Action):

    def name(self) -> Text:
        return "action_last_race"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/last.json')
        if r.status_code == 200 :
            data = r.json()
            data = data['MRData'] ['RaceTable']['Races'][0]
            season = data['season']
            round = data['round']
            name = data['raceName']
            country = data['Circuit']['Location']['country']
            city = data['Circuit']['Location']['locality']
            circuit_name = data['Circuit']['circuitName']
            output = "Last race for " + season + " season has been " \
                + name + " (n° " + str(round) + ").\n" \
                + "It's been held in " + country + "," + city \
                + " at " + circuit_name
        else:
            output = "Sorry there might be a problem with the server, please try again\n"

        dispatcher.utter_message(text=output)
        return []

class ActionNthRace(Action):

    def name(self) -> Text:
        return "action_nth_race"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="race 1 stats")

        return []