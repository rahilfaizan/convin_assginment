from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
import requests
import json
from .models import *

# Create your views here.


def home(request):
    params = {
        "grant_type": "password",
        "client_id": "",
        "client_secret": "",
        "username": "rahil4088@gmail.com",
        "password": "",
    }

    url = "https://login.salesforce.com/services/oauth2/token"

    r1 = requests.post(url, params=params)
    access_token = r1.json().get("access_token")
    instance_url = r1.json().get("instance_url")

    def sf_api_call(action, parameters={}, method='get', data={}):

        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % access_token
        }
        if method == 'get':
            r = requests.request(method, instance_url+action,
                                 headers=headers, params=parameters, timeout=30)
        elif method in ['post', 'patch']:
            r = requests.request(method, instance_url+action,
                                 headers=headers, json=data, params=parameters, timeout=10)
        else:
            raise ValueError('Method should be get or post or patch.')
        print('Debug: API %s call: %s' % (method, r.url))
        if r.status_code < 300:
            if method == 'patch':
                return None
            else:
                return r.json()
        else:
            raise Exception('API error when calling %s : %s' %
                            (r.url, r.content))

    account_call = sf_api_call('/services/data/v40.0/sobjects/Account')
    account_data = json.dumps(account_call, indent=2)
    account_data_json = json.loads(account_data)
    for i in range(len(account_data_json)):
        name = account_data_json["recentItems"][i]["Name"]
        accounts(Name=name).save()

    user_call = sf_api_call('/services/data/v40.0/sobjects/User')
    user_data = json.dumps(user_call, indent=2)
    user_data_json = json.loads(user_data)
    for i in range(len(user_data_json)):
        name = user_data_json["recentItems"][i]["Name"]
        users(Name=name).save()

    contact_call = sf_api_call('/services/data/v40.0/sobjects/Contact')
    contact_data = json.dumps(contact_call, indent=2)
    contact_data_json = json.loads(contact_data)
    for i in range(len(contact_data_json)):
        name = contact_data_json["recentItems"][i]["Name"]
        contacts(Name=name).save()

    return HttpResponse("Success")