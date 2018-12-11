def get_category(path, json_data):
    for name in path:
        json_data = json_data['type'][name]
        for key in json_data['type']:
            if 'type' not in json_data['type'][key]:
                ckan_species_list_response = {
                    "result": [
                        {
                            "Name": "ambassis",
                            "image": "images/placeholder.svg"
                        },
                        {
                            "Name": "species2",
                            "image": "images/placeholder.svg"
                        }]
                }
                species_obj = {species['Name']: species for species in ckan_species_list_response['result']}
                json_data['type'][key]['type'] = species_obj
    return json_data
