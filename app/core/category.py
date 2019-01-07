from .species_repository import get_home_page_data, get_category_data,get_species_data


def get_home_page():
    return get_home_page_data()


def get_category(parent_id,parent_data):
    categories_list = get_category_data(parent_id)

    if len(categories_list) == 0:
        species_data = get_species_data(parent_data)
        species_obj = []
        for species in species_data:
            species_obj.append({"name": species['species'], "genus": species['genus'], "type": {},
                                "kingdom": species['kingdom'],
                                "image": "images/placeholder.svg"})
        return species_obj

    return categories_list


