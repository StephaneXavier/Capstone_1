from models import User
from flask import session
import requests
# from API_key import app_id,api_key
# from app import next_trips_url
from datetime import date, timedelta, datetime
from models import Submitted_Data, db
import os

app_id = os.environ.get('app_id')
api_key = os.environ.get('api_key')
next_trips_url = 'https://api.octranspo1.com/v2.0/GetNextTripsForStop'

def get_username():
    if session.get('user_id'):
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
# Take the immutable dict of what user search params were, turn it into dic. Delete the cfrs token.
# Chain the search parameters that are not empty. Return a list of all the sqlalch obj.

    search_param = dict(user_param)
    # del search_param['csrf_token']
    
    temp = None

    if search_param['to_date']  != '':
        temp = Submitted_Data.query.filter(Submitted_Data.date_submitted <= search_param['to_date'])

    if search_param['from_date'] != '':
        if search_param['to_date']  == '':
            temp = Submitted_Data.query.filter(Submitted_Data.date_submitted >= search_param['from_date'] )
        else:
            temp = temp.filter(Submitted_Data.date_submitted >= search_param['from_date'])
    
    if search_param['busNo'] != '':
        if search_param['from_date']  == '':
            temp = Submitted_Data.query.filter(Submitted_Data.busNo == search_param['busNo'] )
        else:
            temp = temp.filter(Submitted_Data.busNo == search_param['busNo'])

    if search_param['stopNo'] != '':
        if search_param['busNo'] =='':
            temp = Submitted_Data.query.filter(Submitted_Data.stopNo == search_param['stopNo'] )
        else:    
            temp = temp.filter(Submitted_Data.stopNo == search_param['stopNo'])

    return temp.all()


def extract_search_query_data(sqlalch_data, user_param):
    """ Take the list of sql obj from the get_search_query_data and the user search
    parameters. Return an object that gives you the search parameters from the user
    as well as the delay and noShow data for that search"""
    resp = {'search_param': {'busNo':0, 'stopNo':0, 'from_date':0, 'to_date':0}, 'data':{'delay':0,'noShow':0}}

    for e in sqlalch_data:
        resp['search_param']['busNo'] = user_param['busNo']
        resp['search_param']['stopNo'] = user_param['stopNo']
        resp['search_param']['from_date'] = user_param['from_date']
        resp['search_param']['to_date'] = user_param['to_date']
        if not e.noShow:
            resp['data']['delay'] += e.delay
        else:
            resp['data']['noShow'] += 1
    return resp

    
    
def nav_totals():

    datapoints = len(Submitted_Data.query.all())
    no_shows_amount = len(Submitted_Data.query.filter_by(noShow=True).all())
    delays_arr = Submitted_Data.query.filter_by(noShow=False).all()
    total_delay_time = calculate_time(delays_arr)

    return {'datapoints':datapoints, 'no_shows_amount':no_shows_amount, 'total_delay_time':total_delay_time}    