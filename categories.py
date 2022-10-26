import requests
import json
import config


# urls_category_id_w = {
#     '2111785': 'новинки',
# }
#
# urls_category_id_m = {
#     '2113873': 'костюмы',
# }
#
# categories_by_market = {
#     'zara_w': urls_category_id_w,
#     'zara_m': urls_category_id_m
# }

def categories_by_market(market):
    session = requests.session()
    categories_ids = dict()
    response = session.get(config.url_category, headers=config.headers, params=config.params)
    json_loads = json.loads(response.text)
    section_names = json_loads['categories']
    for section_name in section_names:  # woman, man, kid, beauty, origins
        categories_list = dict()
        for category in section_name['subcategories']:
            if 'products' in category['layout'] or 'marketing' in category['layout']:
                if not category['hasSubcategories']:
                    category_name = formatting_category_name(category['name'])
                    if category.get('redirectCategoryId'):
                        category_id = category['redirectCategoryId']
                    else:
                        category_id = category['id']
                    categories_list.update({category_id: category_name})
                    continue
                for subcategory in category['subcategories']:
                    if 'products' in subcategory['layout'] or 'marketing' in subcategory['layout']:
                        if not subcategory['hasSubcategories']:
                            category_name = formatting_category_name(subcategory['name'])
                            if subcategory.get('redirectCategoryId'):
                                subcategory_id = subcategory['redirectCategoryId']
                            else:
                                subcategory_id = subcategory['id']
                            categories_list.update({subcategory_id: category_name})
                            continue
        if 'sectionName' in section_name:
            section = section_name['sectionName']
        else:
            section = section_name['name']
        categories_ids[formatting_category_name(section)] = categories_list
    if market == 'zara_w':
        return categories_ids['woman']
    elif market == 'zara_m':
        return categories_ids['woman']
    elif market == 'zara_k':
        return categories_ids['kid']
    elif market == 'zara_b':
        return categories_ids['beauty']
    elif market == 'zara_o':
        return categories_ids['origins']


def formatting_category_name(name: str):
    name = name.lower()
    if 'zara' in name:
        return name.replace('zara', '').strip()
    if '\xa0' in name:
        name = name.replace('\xa0', ' ')
    if ' | ' in name:
        return ' '.join(name.split(' | '))
    if ' ' in name:
        return name.replace(' ', '_')
    if '-' in name:
        return name.replace('-', '_')
    return name


if __name__ == '__main__':
    categories = categories_by_market('zara_w')
    print(categories)