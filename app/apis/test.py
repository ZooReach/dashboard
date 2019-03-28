import json
from app.utils.constants import api
from app.utils.rest_client import get


def main():
    category_stats = get_result()
    json_val ={"data":category_stats}
    return json.dumps(json_val)


def get_result():
    url = api['datastore_search_sql']
    query = 'SELECT parent.id, parent.name, COUNT(child.id) AS count FROM "2804721b-d474-4f00-8249-49dc7d996d79" parent INNER JOIN "2804721b-d474-4f00-8249-49dc7d996d79" child ON child.parent_id = parent.id  WHERE parent.parent_id = 0 GROUP BY parent.id, parent.name'
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    ckan_species_list_response = response['result']['records']
    return ckan_species_list_response