import json
from app.utils.constants import api
from app.utils.rest_client import get

def main():
    category_stats = get_result()
    json_val ={"data":category_stats}
    return json.dumps(json_val)


def get_result():
    url = api['datastore_search_sql']
    query = 'SELECT COUNT(_id), category_level1 FROM "d2334ebf-5f4b-4f38-b383-c7a75396ac0e" GROUP BY category_level1'
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    ckan_species_list_response = response['result']['records']
    return ckan_species_list_response