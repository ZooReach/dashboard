## run this file with command 'python -m app.scripts.visual_metadata_db_dump' ##

from ..utils.constants import api, authorization_key, visual_meta_data_resource_id
from ..utils.rest_client import post
import requests
import sys
import json

class VisualMetaData():

    def __init__(self, species_list):
        self.species_list = species_list


    def delete_visual_metadata(self):
        
        url = api.get('datastore_delete', '')
        headers = {
            'Authorization': authorization_key,
            'Content-Type':'application/json'
        }
        body = {

            "resource_id": visual_meta_data_resource_id,
            "force":"True",
            "primary_key":["id"]
        }
        try:
            response = post(url, headers, body)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)  


    def get_species_data(self):
        records = []
        for index, metadata in enumerate(self.species_list, start=1):
            entry = {
                "id":index,
                "metadata_id":metadata.get("id", ''),
                "visual":metadata.get("visual", '')
            }
            records.append(entry)
        return records
            

    def insert_visual_metadata(self):

        url = api.get('datastore_create', '')
        headers = {
            'Authorization': authorization_key,
            'Content-Type':'application/json'
        }
        body =  {

            "resource_id": visual_meta_data_resource_id,
            "method":"upsert",
            "force":"True",
            "primary_key":["id"],
            "fields":[{"id":"id"},{"id":"metadata_id"},{"id":"visual"}],
            "records":self.get_species_data()
        }
        try:
            response = post(url, headers, body)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)    


def read_visual_metadat_map(meta_url):

    response = None
    try:
        response = requests.get(meta_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)    
    return response.text


if __name__ == '__main__':
    meta_url = 'https://raw.githubusercontent.com/ZooReach/visual/master/app/helper/species_metadata.json'
    species_list =  read_visual_metadat_map(meta_url)
    if species_list:
        visual_metadat_obj =  VisualMetaData(json.loads(species_list))
        visual_metadat_obj.delete_visual_metadata()
        visual_metadat_obj.insert_visual_metadata()

