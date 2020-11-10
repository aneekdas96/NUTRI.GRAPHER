import urllib.request
import urllib.parse
import json

def scrape(ingredients):
    data = {
        'needsimage': 1,
        'kitchen': '',
        'focus': '',
        'kw': '',
        'catname': ',',
        'exclude': '',
        'start': 0,
    }

    websites = ['www.food.com', 'allrecipes.com']

    ingredients_str = ""
    for i in ingredients:
        ingredients_str += i +","
    data["kitchen"] = ingredients_str
    req = urllib.request.Request(url="http://www.supercook.com/dyn/results",
                                 data=urllib.parse.urlencode(data).encode(),
                                 headers={"Content-type": "application/x-www-form-urlencoded"})
    response = urllib.request.urlopen(req)
    the_page = json.loads(response.read().decode())
    data = [[_['title'] + "~=~" + _['url'] + "~=~" +",".join(_['needs'])]
            for _ in the_page['results'] if _['url'].split('/')[2] in websites][:35]

    recipe_link = ""
    for i in data:
        recipe_link += i[0] + "~<>~"

    return recipe_link

if __name__ == "__main__":
    print(scrape(["tomato","egg"]))