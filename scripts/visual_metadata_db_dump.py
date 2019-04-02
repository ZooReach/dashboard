## run this file with command 'python -m scripts.visual_metadata_db_dump' from dashboard folder##

from app.utils.constants import api, authorization_key, visual_resource_id
from app.utils.rest_client import post
import requests
import sys
import json

class VisualMetaData():

    def __init__(self, species_list):
        self.species_list = species_list


    def delete_visual_metadata(self):
        
        response = None
        url = api.get('datastore_delete', '')
        headers = {
            'Authorization': authorization_key,
            'Content-Type':'application/json'
        }
        body = {

            "resource_id": visual_resource_id,
            "force":"True",                                      
            "primary_key":["id"]
        }
        try:
            response = post(url, headers, body)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)  
        return response


    def get_species_data(self):
        records = [{"id":1, "metadata_id":0, "visual":"test"}]
        for index, metadata in enumerate(self.species_list, start=2):
            entry = {
                "id":index,
                "metadata_id":metadata.get("id", ''),
                "visual":metadata.get("visual", '')
            }
            records.append(entry)
        return records
            

    def insert_visual_metadata(self):

        response = None
        url = api.get('datastore_create', '')
        headers = {
            'Authorization': authorization_key,
            'Content-Type':'application/json'
        }
        body =  {

            "resource_id": visual_resource_id,
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
        return response    


def read_visual_metadata_map(meta_url):

    response = None
    try:
        response = requests.get(meta_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)    
    return response


if __name__ == '__main__':
    meta_url = 'https://raw.githubusercontent.com/ZooReach/visual/master/app/helper/species_metadata.json'
    species_list =  read_visual_metadata_map(meta_url)
    if species_list:
        visual_metadat_obj =  VisualMetaData(json.loads(species_list.text))
        delete_status = visual_metadat_obj.delete_visual_metadata()
        insertion_status = visual_metadat_obj.insert_visual_metadata()

