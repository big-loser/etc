#!/usr/bin/python3

import requests
import json

import time
import hmac
import hashlib
import base64
import urllib.parse
import sys
from datetime import datetime

def sign():
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC9caccf7336b4056d8c778'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    #print(timestamp)
    #print(sign)
    return(timestamp, sign)

def req(host, data):
    header = {'Content-Type': 'application/json'}
    r = requests.post(host, headers=header, data=json.dumps(data))
    print(r.text)

def handle_alert():
    '''
    # handle_alert method which is called from Ambari
    # :param definitionName: the alert definition unique ID
    # :param definitionLabel: the human readable alert definition label
    # :param serviceName: the service that the alert definition belongs to
    # :param alertState: the state of the alert (OK, WARNING, etc)
    # :param alertText: the text of the alert
    # :param alertTimestamp: the timestamp the alert went off - Added in AMBARI-20291
    # :param hostname: the hostname the alert fired off for - Added in AMBARI-20291
    '''

    definitionName = sys.argv[1]
    definitionLabel = sys.argv[2]
    serviceName = sys.argv[3]
    alertState = sys.argv[4]
    alertText = sys.argv[5]
    # AMBARI-20291
    if len(sys.argv) == 8:
        alertTimestamp = sys.argv[6]
        hostname = sys.argv[7]
    else:
        alertTimestamp = 'N/A'
        hostname = 'N/A'

    # Generate a timestamp for when this script was called
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add custom logic here to handle the alert

    context = 'definitionName\ndefinitionLabel\nserviceName\nalertState\nalertText\nalertTimestamp\nhostname'

    data = { "msgtype": "text","text": {"content": context} }

    ts, sg = sign()
    host = 'https://oapi.dingtalk.com/robot/send?access_token=1bd86df82e4da81&timestamp=%s&sign=%s' %(ts, sg)
    req(host, data)

if __name__ == '__main__':
    if len(sys.argv) >= 6:
        handle_alert()
    else:
        print("Incorrect number of arguments")
        sys.exit(1)
