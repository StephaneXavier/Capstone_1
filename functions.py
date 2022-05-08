
from models import User
from flask import session
import requests
from API_key import app_id,api_key
from app import next_trips_url
from datetime import datetime
from models import Submitted_Data




def get_username():
    if session['user_id']:
        user = User.query.get(session['user_id'])
        return user.username
    return None


def calculate_time(arr):
    t=0
    for e in arr:
        t +=e.delay
    return t


class Validator():


    def __init__(self):
        self.errors = []
    

    def validate_busNo_stopNo(self, busNo, stopNo):
        res = requests.get(f'{next_trips_url}', params={'appID':app_id, 'apiKey':api_key, 'stopNo':stopNo,'routeNo':busNo}).json()
        try:
            res['GetNextTripsForStopResult']['Route']['RouteDirection']['Trips']['Trip']
            return True
        except:
           self.errors.append("Bus/stop combination wrong OR bus/stop numbers don't exist")
           return False


    def validate_schedule_time(self,scheduled_time):
        ct = datetime.now().time()
        if scheduled_time:
                if ct > scheduled_time:
                    return True
                
                else:
                    self.errors.append("Can't report bus ahead of it's scheduled arrival time")
                    return False 
        else:
            return True



def get_search_query_data(user_param):
# Take the immutable dict, turn it into dic. Delete the cfrs toke, then make a new
# dict where any key-pair entry is deleted if the value is None
# then spread that dict of search values into search query
    search_param = dict(user_param)
    del search_param['csrf_token']
    search_param = {key: value for (key, value) in search_param.items()
               if value}

    return Submitted_Data.query.filter_by(**search_param).all()
    


def extract_search_query_data(sqlalch_data, busNo, stopNo):
    
    if busNo and not stopNo:
        resp = {f'busNo_{busNo}_info':{'delay':0,'noShow':0}}
        for e in sqlalch_data:
            
            if not e.noShow:
                resp[f'busNo_{busNo}_info']['delay'] += e.delay
            else:
                resp[f'busNo_{busNo}_info']['noShow'] += 1
    
    if stopNo and not busNo:
        resp = {f'stopNo_{stopNo}_info':{'delay':0,'noShow':0}}
        for e in sqlalch_data:
            if e.delay:
                resp[f'stopNo_{stopNo}_info']['delay'] += e.delay
            else:
                resp[f'stopNo_{stopNo}_info']['noShow'] += 1

    return resp
    
