from app.core.file_operations import get_json_file, get_json_file_path_from_data


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


def get_species_from_path(category_type, path):
    species_str = ''
    for idx, name in enumerate(path):
        if 'type' in category_type:
            category_type = category_type['type'][name]
        else:
            species_str = path[idx:]
    return species_str


def get_resource_id(category_path):
    category_type = get_json_file(get_json_file_path_from_data(category_path[0]))
    return category_type['type'][category_path[0]]['resource_id']