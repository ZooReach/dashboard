## run the script with command 'python -m scripts.create_species_metadata_map <your-github-access-token>'

from app.utils.constants import api, authorization_key, meta_data_resource_id, visual_data_map_file_path
from app.utils.rest_client import get
import requests
import json
from github import Github
import sys
import os


class MetaData():

    def __init__(self):
        pass
         

    def get_parent_metadata(self):
        response = None
        try:
            url = api.get('datastore_search_sql', '')
            query = 'select * from "' + meta_data_resource_id + '" order by id ASC'
            query_param = {"sql": query}
            response = get(url=url, queryparams=query_param)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)    
        return response
   

    def metadata_exists(self, metadata_id, metadata):
        if len(metadata) > 1:
            mid = (len(metadata))//2
            if metadata_id == int(metadata[mid]['id']):
                return True
            elif metadata_id > int(metadata[mid]['id']):
                return self.metadata_exists(metadata_id, metadata[mid+1:])
            elif metadata_id < int(metadata[mid]['id']):
                return self.metadata_exists(metadata_id, metadata[:mid])
            return False
        else:
            return False


    def get_visual_related_map(self):
        metadata_details = []
        species_data = self.get_parent_metadata()
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'visual_metadata_map.json')) as data:
            metadata = json.loads(data.read())
            for key, value in metadata.items():
                project_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
                file_exists = os.path.isfile(os.path.join(project_dir, 'app', 'static', 'js', 'visualization', key+'.js'))
                if file_exists and self.metadata_exists(value, species_data['result']['records']):
                    metadata_details.append({
                        "id":value,
                        "name":key
                    })
        return metadata_details


    def create_visual_metadata_map(self, species_data):
        visual_map = []
        for data in species_data:
            visual_map.append(
                {
                    "id":int(data.get("id", '0')),
                    "visual": data.get("name", '')
                }
            )
        return visual_map


    def commit_species_visual_metadata(self, visual_map, github_access_token):
        g = Github(github_access_token)
        for repo in g.get_user().get_repos():
            if repo.name == 'visual':
                sha_key = repo.get_file_contents(visual_data_map_file_path).sha
                commit_response = repo.update_file(path=visual_data_map_file_path, 
                                    message="Create visual metadata map for species",
                                    content = json.dumps(visual_map),
                                    sha = sha_key
                                    )
        return commit_response


if __name__ == '__main__':
    meta_data = MetaData()
    github_access_token = sys.argv[1]
    species_data = meta_data.get_visual_related_map()
    visual_map = meta_data.create_visual_metadata_map(species_data)
    response = meta_data.commit_species_visual_metadata(visual_map, github_access_token)
    print(response)
    print(dir(response))

