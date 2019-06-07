def preprocess(contents):
    '''
    Prepprocessin scrape data

    Parameters
    ----------
    contents: list of dicts
    - A list of dict scraped from allrecipes.com

    Returns
    contents: list of dicts
    '''
    
    assert isinstance(contents, list)
    assert all([isinstance(x, dict) for x in contents])
    
    for content in contents:

        # Removed unnecessary attributes 
        content.pop('reviews', None)
        content.pop('link', None)
        content.pop('catagories', None)
        content.pop('title', None)
        content.pop('num_servings', None)

        # Split ingredients
        content['ingredients'] = [word for x in content['ingredients'] for word in x.split()]
        content['num_directions'] = len(content['directions'])
        content['num_ingredients'] = len(content['ingredients'])
        
        # Convert nutrition facts to float format
        float_list = ['calories', 'carbohydrate', 'cholesterol', 'fat', 'protein', 'sodium', 'preptime', 'cooktime']
        for attr in float_list:
            if content[attr] == None:
                content[attr] = float('NaN')
                continue
            items = content[attr].strip().split()
            content[attr] = float('NaN')
            for item in items:
                try:
                    content[attr] = float(item)
                    break
                except ValueError:
                    pass  
            
        # Change the unit of 'readyin_time' to mins
        if (content['readyin_time'] == None):
            content['readyin_time'] = float('NaN')
            continue

        time_list = content['readyin_time'].split()
        num = 0.0
        for i in range(0, len(time_list), 2):
            if time_list[i + 1] == 'd':
                num += float(time_list[i]) * 24 * 60
            elif time_list[i + 1] == 'h':
                num += float(time_list[i]) * 60
            else:
                num += float(time_list[i])
        content['readyin_time'] = num

    return contents
