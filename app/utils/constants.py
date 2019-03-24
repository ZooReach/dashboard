environment_details = {
    'ckan': 'http://68.183.89.90'
}

api = {
    'datastore_search': environment_details['ckan'] + '/api/3/action/datastore_search',
    'datastore_search_sql': environment_details['ckan'] + '/api/3/action/datastore_search_sql',
    'datastore_create': environment_details['ckan'] + '/api/3/action/datastore_create',
    'datastore_delete': environment_details['ckan'] + '/api/3/action/datastore_delete',
}

display_details = ['phylum', 'class', 'family', 'redlist_category']

meta_data_resource_id = "2804721b-d474-4f00-8249-49dc7d996d79"

visual_meta_data_resource_id = "847896c8-ad47-4bf7-a5e0-05c2c41d0c64"

authorization_key = "223844a7-bf47-411e-bb9b-16f6eada21f4"

visual_data_map_file_path = 'app/helper/species_metadata.json'

visual_resource_id = '4c1b2e43-379f-4d9f-8a4b-0f5bc46a8778'

experts_resource_id = '315c64b1-1b26-40e2-bd7c-3818c6ccdcd6'