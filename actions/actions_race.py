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

class ActionLastRaceResults(Action):

    def name(self) -> Text:
        return "action_last_race_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/last/results.json')
        if r.status_code == 200 :
            data = r.json()
            data = data['MRData'] ['RaceTable']['Races'][0]
            name = data['raceName']
            output = "Results for " + name + " are the following:\n" 
            results_header = "N.\tPilot\t\tConstructor\tTime\t\tFastest Lap\tPoints\n"
            output += results_header
            results = data['Results']
            for record in results:
                row = []
                row.append(record['position'])
                row.append(record['Driver']['familyName'])
                row.append(record['Constructor']['name'])
                if 'Time' in record:
                    row.append(record['Time']['time'])
                else: 
                    row.append("-------")
                if 'FastestLap' in record:
                    row.append(record['FastestLap']['Time']['time'])
                else: 
                    row.append("-------")
                row.append(record['points'])

                output += row[0] + "\t"
                for el in row[1:]:
                    if len(el)>7:
                        output += el + "\t" 
                    else: 
                        output += el + "\t\t"
                output +=  "\n"
        else:
            output = "Sorry there might be a problem with the server, please try again\n"

        dispatcher.utter_message(text=output)
        return []

class ActionLastRaceQualifyingInfo(Action):

    def name(self) -> Text:
        return "action_last_race_qualifying_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        r=requests.get(url='http://ergast.com/api/f1/current/last/qualifying.json')
        if r.status_code == 200 :
            data = r.json()
            data = data['MRData'] ['RaceTable']['Races'][0]
            name = data['raceName']
            output = "Qualifying results for " + name + " are the following:\n" 
            results_header = "Grid\tPilot\t\tConstructor\tQ1\t\tQ2\t\tQ3\n"
            output += results_header
            results = data['QualifyingResults']
            for record in results:
                row = []
                row.append(record['position'])
                row.append(record['Driver']['familyName'])
                row.append(record['Constructor']['name'])
                if 'Q1' in record:
                    row.append(record['Q1'])
                else: 
                    row.append("---")
                if 'Q2' in record:
                    row.append(record['Q2'])
                else: 
                    row.append("---")
                if 'Q3' in record:
                    row.append(record['Q3'])
                else: 
                    row.append("---")

                output += row[0] + "\t"
                for el in row[1:]:
                    if len(el)>7:
                        output += el + "\t" 
                    else: 
                        output += el + "\t\t"
                output +=  "\n"
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

class ActionNthRaceSchedule(Action):

    def name(self) -> Text:
        return "action_nth_race_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nth = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8,
            "nineth": 9,
            "tenth": 10,
            "eleventh": 11,
            "twelth": 12,
            "thirteenth": 13,
            "fourteenth": 14,
            "fifteenth": 15,
            "sixteenth": 16,
            "seventeenth": 17,
            "eighteenth": 18,
            "nineteenth": 19,
            "twentieth": 20,
            "twentieth-first": 21,
            "twentieth-second": 22,
            "twentieth-third": 23,
            "twentieth-fourth": 24,
            "twentieth-fifth": 25 
        }
        
        race = next(tracker.get_latest_entity_values('race'), None)
        if race is None:
            race = tracker.get_slot('race')
        if race is None:
            output = "Sorry you didn't specify the race.\n"
        else:
            if race in nth.keys():
                race = nth[str(race)]
            if race not in range(1,25):
                output = "Sorry you didn't specify a correct race number.\n"
            r=requests.get(url='http://ergast.com/api/f1/current/'+str(race)+'.json')
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



