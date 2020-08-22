# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
import numpy as np
import pandas as pd 
import requests
import json
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import credentials_http


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
        print(SR)
        print(type(SR))
       
        excel_file = 'C:/Users/Monalisa/Documents/Rasaproject/SRDetails.xlsx'
        df = pd.read_excel(excel_file)
        print(df)
#         print(df['Update'].where(df['SRNumber'] == SR)
        update = df['Update'].where(df['SRNumber'] == SR)
       
        ETA = df['ETA'].where(df['SRNumber'] == SR)
        for SRN in df['SRNumber']:
            if SRN==str(SR):
                print('Yes')
                print(type(SRN))
                print(type(SR))
            else:
                print(type(SRN))
                print(type(SR))
                print("No")
        line = update.dropna()
        print(df['SRNumber'])
        res = df.isin([SR]).any().any() 
        print("___"+str(res))
        if str(SR) in df.values :
            print("\nThis value exists in Dataframe") 
        exists = SR in df['SRNumber']
        print("Exists - "+str(exists))
        lastitem = df['Update'].iloc[-1]
        lastitem2 = df['ETA'].iloc[-1]
        print("____"+lastitem)
        print(update.dropna())
#         print(type(update))
        message = "Last update : "+str(lastitem)
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
        print("servicenow_user "+credentials_http.servicenow_user)
        print("servicenow_pwd "+credentials_http.servicenow_pwd)
#         user = 'admin'
#         pwd = 'ServiceNow1996'
        ticket = (tracker.latest_message)['text'] #captures the incident description as entered by the user
        
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        print(ticket)
        desc = tracker.get_slot("desc")
        response = requests.post(url, auth=(credentials_http.servicenow_user, credentials_http.servicenow_pwd), headers=headers ,data='{"short_description":"' + ticket + '"}')
        
        print("Action is running incident create")
        print("___"+str(response.status_code))
        
#         if response.status_code != 200:
#             print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
#         exit()

        data = response.json()

        print(type(data))
        print(data['result']['task_effective_number']) #fetches the incident number
#         message = "{} is the inc details".format(desc)
        message = "I have created Incident "+data['result']['task_effective_number']+" on your query. Our team will reach out to you soon on         this"
        dispatcher.utter_message(text=message)
        return []