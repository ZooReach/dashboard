import requests
import json


def get(url, headers={}, queryparams={}):
    result = requests.get(url, headers=headers, params=queryparams)
    return result.json()

def post(url, headers={}, data=None):
    result = requests.post(url, headers=headers, data=json.dumps(data))
    return result