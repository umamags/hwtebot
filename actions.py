# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
import numpy as np
import pandas as pd 
import requests
import json
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# class ActionNewTravelCard(Action):
#     def name(self) -> Text:
#         return "action_newtravelcard"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Please go to www.google.com to open the instruction document to apply new card")

#         return []
    
# class ActionStatusCard(Action):
#     def name(self) -> Text:
#         return "action_statuscard"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Please provide the SR ticket #")

#         return []

class ActionIncidentTable(Action):
    def name(self) -> Text:
        return "action_Incident"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Please provide your query in detail")

        return []

class SRUpdate(Action):
    def name(self) -> Text:
        return "action_SR_Update"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        SR = tracker.get_slot("SR")
        excel_file = 'C:/Users/Monalisa/Documents/Git/Project/SRDetails.xlsx'
        df = pd.read_excel(excel_file)
        print(df)
#         print(df['Update'].where(df['SRNumber'] == SR)
        update = df['Update'].where(df['SRNumber'] == SR)
        ETA = df['ETA'].where(df['SRNumber'] == SR)
        line = update.dropna()
        lastitem = df['Update'].iloc[-1]
        lastitem2 = df['ETA'].iloc[-1]
        print("____"+lastitem)
        print(update.dropna())
#         print(type(update))
        message = "Last update on "+SR+": "+lastitem
        message1  = "ETA: "+str(lastitem2)
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text=message1)
        return []

class ActionCreateIncident(Action):
    def name(self) -> Text:
        return "action_createIncident"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = 'https://dev51095.service-now.com/api/now/table/incident'
        user = 'admin'
        pwd = 'ServiceNow1996'
        
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        
        desc = tracker.get_slot("desc")
        response = requests.post(url, auth=(user, pwd), headers=headers ,data='{"short_description":"' + desc + '"}')
        
        print("Action is running incident create")
        print("___"+str(response.status_code))
        
#         if response.status_code != 200:
#             print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
#         exit()

        data = response.json()

        print(type(data))
        print(data['result']['task_effective_number'])
#         message = "{} is the inc details".format(desc)
        message = "I have created Incident "+data['result']['task_effective_number']+" on your query. Our team will reach out to you soon on         this"
        dispatcher.utter_message(text=message)
        return []