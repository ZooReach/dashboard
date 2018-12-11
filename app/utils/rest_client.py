import requests


def get(url, headers={}, queryparams={}):
    result = requests.get(url, headers=headers, params=queryparams)
    return result.json()



