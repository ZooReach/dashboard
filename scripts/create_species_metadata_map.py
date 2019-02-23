from app.utils.constants import api, authorization_key, meta_data_resource_id
from app.utils.rest_client import get
import requests
import json
import sys

class MetaData():

    def __init__(self):
        pass
         
    def get_parent_metadata(self):
        response = None
        try:
            url = api.get('datastore_search_sql', '')
            query = 'select * from "' + meta_data_resource_id + '" WHERE parent_id=' + str(0)
            query_param = {"sql": query}
            response = get(url=url, queryparams=query_param)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)    
        return response


    def create_visual_metadata_map(self):
        pass    


if __name__ == '__main__':
    meta_data = MetaData()
    meta_data.get_parent_metadata()
