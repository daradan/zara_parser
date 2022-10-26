import requests
import json
import config


categories_ids = {}


def process_category(category_obj):
    for subcategory in category_obj['subcategories']:
        if 'products' in subcategory['layout'] or 'marketing' in subcategory['layout']:
            process_category(subcategory)
    else:
        category_id = category_obj.get('redirectCategoryId', category_obj['id'])
        category_name = formatting_category_name(category_obj['name'])
        categories_ids[category_id] = category_name


def categories_by_market(market):
    global categories_ids
    categories_ids = {}
    session = requests.session()
    response = session.get(config.url_category, headers=config.headers, params=config.params)
    json_loads = json.loads(response.text)
    sections = json_loads['categories']
    for section in sections:  # woman, man, kid, beauty, origins
        section_name = section.get('sectionName', section['name'])
        if market == 'zara_w' and section_name == 'WOMAN':
            process_category(section)
        if market == 'zara_m' and section_name == 'MAN':
            process_category(section)
        if market == 'zara_k' and section_name == 'KID':
            process_category(section)
        if market == 'zara_b' and section_name == 'BEAUTY':
            process_category(section)
        if market == 'zara_o' and section_name == 'ZARA ORIGINS':
            process_category(section)
    return categories_ids


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
    res = categories_by_market('zara_w')
    print(res)
