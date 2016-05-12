import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_events(urlname):
    
    events_url = BASE_URL + '/' + urlname + '/events'
    params = {'sign':'true','key': API_KEY, 'status': 'past'}
    response = requests.get(events_url, params = params)
    events = response.json()
    
    return events

urlname = 'DE-ProD-SF'
get_events(urlname)

# get events
urlname = 'DS-ProD-SF'

events_url = BASE_URL + '/' + urlname + '/events'
params = {'sign':'true','key': API_KEY, 'status': 'past'}
response = requests.get(events_url, params = params)
events = response.json()

len(events)
event_ids = []
event_desc_raw= []

for event in events:
    event_ids.append(event['id'])
    event_desc_raw.append(event['description'])

event_description = []
for i in xrange(len(event_ids)):
    soup = BeautifulSoup(event_desc_raw[i], 'html.parser')
    event_description.append(soup.get_text())
    
df_events= pd.DataFrame([event_ids, event_description]).T
df_events.columns = ['event_id', 'event_description']
df_events

member_id = []
event_id = []

for i in event_ids:
    rsvps_url = BASE_URL + '/' + urlname +'/events/' + i + '/rsvps'
    params = {'sign':'true','key': API_KEY}
    response = requests.get(rsvps_url, params = params)
    rsvps = response.json()
    
    for rsvp in rsvps:
        member_id.append(rsvp['member']['id'])
        event_id.append(rsvp['event']['id'])
               
df_rsvps = pd.DataFrame([member_id, event_id]).T
df_rsvps.columns = ['member_id', 'event_id']
df_rsvps

df = pd.merge(df_events, df_rsvps, on = 'event_id')