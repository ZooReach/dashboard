environment_details = {
    'ckan': 'http://139.59.66.4'
}

api = {
    'datastore_search' : environment_details['ckan']+'/api/3/action/datastore_search',
    'datastore_search_sql' : environment_details['ckan']+'/api/3/action/datastore_search_sql',

}

display_details = ['phylum', 'class', 'family', 'redlist_category']
