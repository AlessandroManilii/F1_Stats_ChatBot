# This files contains custom actions related to races

from typing import Any, Text, Dict, List
import requests
import urllib.request
import fastf1 as f1
from datetime import date
import re
import pandas as pd
import os

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase

if not os.path.exists('./f1_cache'):
    os.makedirs('./f1_cache')

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

        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        season_rounds = int(data['MRData']['total'])

        race_num_list = [format(x, 'd') for x in list(range(1, season_rounds + 1))]

        race_entity = next(tracker.get_latest_entity_values('race'), None)
        race_name_entity = next(tracker.get_latest_entity_values('race_name'), None)
        if race_entity is not None:
            race = race_entity
        else:
            race = race_name_entity
        if race is None:
            race_slot = tracker.get_slot('race')
            race_name_slot = tracker.get_slot('race_name')
            if race_slot is not None:
                race = race_slot
            elif race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            if race in race_num_list:
                race_num = race
            else:
                session = f1.get_session(date.today().year, race,'R')
                race_num = session.event.RoundNumber
            r=requests.get(url='http://ergast.com/api/f1/current/'+str(race_num)+'.json')
            if r.status_code == 200 :
                data = r.json()
                data = data['MRData'] ['RaceTable']['Races'][0]
                round = data['round']
                name = data['raceName']
                country = data['Circuit']['Location']['country']
                city = data['Circuit']['Location']['locality']
                circuit_name = data['Circuit']['circuitName']
                schedule_header = "\t\tDate\t\tTime \n"
                output = str(race_num) + "° race of current season is " \
                    + name + " (n° " + str(round) + ").\n" \
                    + "It's planned to be held in " + country + "," + city \
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
                    output += "Sprint \t\t" +  data['Sprint']['date'] \
                        + "\t" + data['Sprint']['time'].replace(':00Z', " (GMT)")
            else:
                output = "Sorry there might be a problem with the server, please try again\n"

        dispatcher.utter_message(text=output)
        return []

class ActionNthRaceSchedule(Action):

    def name(self) -> Text:
        return "action_nth_race_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        season_rounds = int(data['MRData']['total'])

        race_num_list = [format(x, 'd') for x in list(range(1, season_rounds + 1))]
        
        race_entity = next(tracker.get_latest_entity_values('race'), None)
        race_name_entity = next(tracker.get_latest_entity_values('race_name'), None)
        if race_entity is not None:
            race = race_entity
        else:
            race = race_name_entity
        if race is None:
            race_slot = tracker.get_slot('race')
            race_name_slot = tracker.get_slot('race_name')
            if race_slot is not None:
                race = race_slot
            elif race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            if race in race_num_list:
                race_num = race
            else:
                session = f1.get_session(date.today().year, race,'R')
                race_num = session.event.RoundNumber
            r=requests.get(url='http://ergast.com/api/f1/current/'+str(race_num)+'.json')
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

class ActionNthRaceResults(Action):

    def name(self) -> Text:
        return "action_nth_race_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        season_rounds = int(data['MRData']['total'])

        race_num_list = [format(x, 'd') for x in list(range(1, season_rounds + 1))]
        print(race_num_list)
        
        race_entity = next(tracker.get_latest_entity_values('race'), None)
        race_name_entity = next(tracker.get_latest_entity_values('race_name'), None)
        if race_entity is not None:
            race = race_entity
        else:
            race = race_name_entity
        if race is None:
            race_slot = tracker.get_slot('race')
            race_name_slot = tracker.get_slot('race_name')
            if race_slot is not None:
                race = race_slot
            elif race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            if race in race_num_list:
                race_num = race
            else:
                session = f1.get_session(date.today().year, race, 'R')
                race_num = session.event.RoundNumber
            r=requests.get(url='http://ergast.com/api/f1/current/'+str(race_num)+'/results.json')
            if r.status_code == 200 :
                data = r.json()
                data = data['MRData'] ['RaceTable']['Races']
                if len(data) == 0:
                    output = str(race_num) + "° race of current season hasn't be raced yet."
                else:
                    data = data[0]
                    name = data['raceName']
                    output = name + "🏁 race results of current season are the following:\n" 
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

class ActionNthRaceCircuit(Action):

    def name(self) -> Text:
        return "action_nth_race_circuit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        season_rounds = int(data['MRData']['total'])

        race_num_list = [format(x, 'd') for x in list(range(1, season_rounds + 1))]

        race_entity = next(tracker.get_latest_entity_values('race'), None)
        race_name_entity = next(tracker.get_latest_entity_values('race_name'), None)
        if race_entity is not None:
            race = race_entity
        else:
            race = race_name_entity
        if race is None:
            race_slot = tracker.get_slot('race')
            race_name_slot = tracker.get_slot('race_name')
            if race_slot is not None:
                race = race_slot
            elif race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            if race in race_num_list:
                race_num = race
            else:
                session = f1.get_session(date.today().year, race, 'R')
                race_num = session.event.RoundNumber
            r=requests.get(url='http://ergast.com/api/f1/current/'+str(race_num)+'/circuits.json')
            if r.status_code == 200 :
                data = r.json()
                data = data['MRData']['CircuitTable']['Circuits'][0]
                circuit = data['circuitName']
                city_country = data['Location']['locality'] + ',' + data['Location']['country']
                wiki_url = data['url']
                output = str(race_num) + "° race of current season is planned to be raced in " \
                + circuit + ", located in " + city_country \
                + ". More details on circuit can be found at " + wiki_url 
            else:
                output = "Sorry there might be a problem with the server, please try again\n"     

        dispatcher.utter_message(text=output)
        return []

class ActionHighlights(Action):

    def name(self) -> Text:
        return "action_highlights"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/last.json')
        data = r.json()
        race = data['MRData']['RaceTable']['Races'][0]['raceName']
        search_keyword="f1+"+str(date.today().year)+race.replace(" ", "")+"+highlights"
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        for i in range(1):
            output = "https://www.youtube.com/watch?v=" + video_ids[i]
            dispatcher.utter_message(text=output)
        return []

class ActionQualifyingHighlights(Action):

    def name(self) -> Text:
        return "action_qualifying_highlights"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/last.json')
        data = r.json()
        race = data['MRData']['RaceTable']['Races'][0]['raceName']
        search_keyword="f1+"+str(date.today().year)+race.replace(" ", "")+"qualifying+highlights"
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        for i in range(1):
            output = "https://www.youtube.com/watch?v=" + video_ids[i]
            dispatcher.utter_message(text=output)
        return []

class ActionNthRaceHighlights(Action):

    def name(self) -> Text:
        return "action_nth_race_highlights"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        season_rounds = int(data['MRData']['total'])

        race_num_list = [format(x, 'd') for x in list(range(1, season_rounds + 1))]
        
        race_entity = next(tracker.get_latest_entity_values('race'), None)
        race_name_entity = next(tracker.get_latest_entity_values('race_name'), None)
        if race_entity is not None:
            race = race_entity
        else:
            race = race_name_entity
        if race is None:
            race_slot = tracker.get_slot('race')
            race_name_slot = tracker.get_slot('race_name')
            if race_slot is not None:
                race = race_slot
            elif race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            if race in race_num_list:
                race_num = race
            else:
                session = f1.get_session(date.today().year, race, 'R')
                race_num = session.event.RoundNumber
            r=requests.get(url='http://ergast.com/api/f1/current/last.json')
            data = r.json()
            last_race = data['MRData']['RaceTable']['round']
            if int(race_num) > int(last_race):
                output = "Given grand prix has not be raced yet."
            else:
                r=requests.get(url='http://ergast.com/api/f1/current/'+str(race_num)+'.json')
                data = r.json()
                race = data['MRData']['RaceTable']['Races'][0]['raceName']
                search_keyword="f1+"+str(date.today().year)+race.replace(" ", "")+"highlights"
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                for i in range(1):
                    output = "https://www.youtube.com/watch?v=" + video_ids[i]
        dispatcher.utter_message(text=output)
        return []

class ActionNthRaceQualifyingHighlights(Action):

    def name(self) -> Text:
        return "action_nth_race_qualifying_highlights"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        season_rounds = int(data['MRData']['total'])

        race_num_list = [format(x, 'd') for x in list(range(1, season_rounds + 1))]
        
        race_entity = next(tracker.get_latest_entity_values('race'), None)
        race_name_entity = next(tracker.get_latest_entity_values('race_name'), None)
        if race_entity is not None:
            race = race_entity
        else:
            race = race_name_entity
        if race is None:
            race_slot = tracker.get_slot('race')
            race_name_slot = tracker.get_slot('race_name')
            if race_slot is not None:
                race = race_slot
            elif race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            if race in race_num_list:
                race_num = race
                print("no numerical race\n")
            else:
                session = f1.get_session(date.today().year, race, 'R')
                race_num = session.event.RoundNumber
                print(race_num)
            
            r=requests.get(url='http://ergast.com/api/f1/current/last.json')
            data = r.json()
            last_race = data['MRData']['RaceTable']['round']
            if int(race_num) > int(last_race):
                output = "Given grand prix has not be raced yet."
            else:
                r=requests.get(url='http://ergast.com/api/f1/current/'+str(race_num)+'.json')
                data = r.json()
                race = data['MRData']['RaceTable']['Races'][0]['raceName']
                search_keyword="f1+"+str(date.today().year)+race.replace(" ", "")+"qualifying+highlights"
                print(search_keyword)
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                for i in range(1):
                    output = "https://www.youtube.com/watch?v=" + video_ids[i]
        dispatcher.utter_message(text=output)
        return []

class ActionNextRaceOnTv(Action):

    def name(self) -> Text:
        return "action_next_race_on_tv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        r=requests.get(url='http://ergast.com/api/f1/current/next.json')
        if r.status_code == 200 :
            data = r.json()
            data = data['MRData']['RaceTable']['Races'][0]
            season = data['season']
            round = data['round']
            name = data['raceName']
            #check info TV
            df = pd.read_csv("./tv.csv", delimiter=',')
            info = df.loc[df['Index'] == int(round)]
            if info['free'].values[0] == "si":
                output = "The race of " + name + " will be broadcast free to air on TV and pay TV Sky"
            else:
                output = "The race of " + name + " will be broadcast exclusively on Sky" 
        else:
            output = "Sorry there might be a problem with the server, please try again\n"

        dispatcher.utter_message(text=output)
        return []    

class ActionRaceOnTv(Action):

    def name(self) -> Text:
        return "action_race_on_tv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data=requests.get(url='http://ergast.com/api/f1/current.json').json()
        race = next(tracker.get_latest_entity_values('race_name'), None)
        if race is None:
            race_name_slot = tracker.get_slot('race_name')
            if race_name_slot is not None:
                race = race_name_slot
            else:
                output = "Sorry you didn't specify the race.\n"
        else:
            session = f1.get_session(date.today().year, race, 'R')
            race_num = session.event.RoundNumber
            race_name_event = session.event.EventName
            #check info TV
            df = pd.read_csv("./tv.csv", delimiter=',')
            info = df.loc[df['Index'] == int(race_num)]
            if info['free'].values[0] == "si":
                output = "The " + race_name_event + " of will be broadcast free to air on TV and pay TV Sky"
            else:
                output = "The " + race_name_event + " of will be broadcast exclusively on Sky" 
    
        dispatcher.utter_message(text=output)
        return []                         