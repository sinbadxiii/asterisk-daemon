#!/usr/bin/python3

import time
from settings import login, connection, redisConf

from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction

import redis

ENDPOINT_EVENT = 'EndpointList'
CORE_SHOW_EVENT = 'CoreShowChannel'
REDIS_CACHE_ENDPOINT = 'corp:asterisk:endpointlist'
REDIS_CACHE_CORE_SHOW_CHANNEL = 'corp:asterisk:core-show-channel'
ZHENKIN_SIP = 107

r = redis.StrictRedis(**redisConf)
status = {}
active = {}

def event_notification(source, event):
    print (event)

client = AMIClient(**connection)
future = client.login(**login)
if future.response.is_error():
    raise Exception(str(future.response))

action = SimpleAction(
        'Originate',
        Channel='PJSIP/101',
        Exten=ZHENKIN_SIP,
        Priority=1,
        Context='default',
        CallerID='python',
    )
client.send_action(action)

client.add_event_listener(event_notification)

try:
    while True:
        time.sleep(3)
except (KeyboardInterrupt, SystemExit):
    client.logoff()