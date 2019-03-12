#!/usr/bin/python3

import time
from config import login, connection, redisConf

from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction

import redis
import json

ENDPOINT_EVENT = 'EndpointList'
CORE_SHOW_EVENT = 'CoreShowChannel'
REDIS_CACHE_ENDPOINT = 'corp:asterisk:endpointlist'
REDIS_CACHE_CORE_SHOW_CHANNEL = 'corp:asterisk:core-show-channel'

r = redis.StrictRedis(**redisConf)
status = {}
active = {}

def event_notification(source, event):

    if event.name == ENDPOINT_EVENT:
        global status
        if event.keys['Aor'] in status.keys():
            r.set(REDIS_CACHE_ENDPOINT, json.dumps(status))
            status = {}
        status[event.keys['Aor']] = event.keys

    if event.name == CORE_SHOW_EVENT:
        global active
        if event.keys['CallerIDNum'] in active.keys():
            r.setex(REDIS_CACHE_CORE_SHOW_CHANNEL, 5, json.dumps(active))
            active = {}
        active[event.keys['CallerIDNum']] = event.keys

def run(client):
    action = SimpleAction(
        'PJSIPShowEndpoints'
    )

    client.send_action(action)

    action = SimpleAction(
        'CoreShowChannels'
    )
    client.send_action(action)

client = AMIClient(**connection)
result = client.login(**login)
if result.response.is_error():
    raise Exception(str(result.response))

client.add_event_listener(event_notification, white_list=[
    'EndpointList',
    'CoreShowChannel'
])

try:
    while True:
        run(client)
        time.sleep(3)
except (KeyboardInterrupt, SystemExit):
    client.logoff()