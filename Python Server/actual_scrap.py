import urllib.request
import itertools
import requests
import _thread
import urllib.parse
import json
import time
from bs4 import BeautifulSoup
import os
from os import listdir
from os.path import isfile, join

websites = ['www.food.com', 'allrecipes.com']

data = {
    'needsimage': 1,
    'kitchen': '',
    'focus':'',
    'kw':'',
    'catname':'',
    'exclude':'',
    'start': 0,
}

def getInfo(recipe_name,url):
    dict_info = {}
    cache = os.listdir('./recipes')
    print(recipe_name, url)
    if recipe_name in cache:
        files = os.listdir('./recipes/'+recipe_name)
        # files.pop(files.index('instruct.txt'))
        for file in files:
            file_c = './recipes/'+recipe_name+'/'+file
            f = open(file_c)
            dict_info[file[:-4]]=f.read()
        # print(dict_info)
        temp = dict_info['nutri'].split('\n')
        d = {}
        for _ in temp:
            if _.split(": ")[0]=="Calorie":
                d["calories"] = _.split(": ")[1]
            elif _.split(": ")[0]=="Fat":
                d["fatContent"] = _.split(": ")[1]
            elif _.split(": ")[0] == "Carbs":
                d["carbohydrateContent"] = _.split(": ")[1]
            elif _.split(": ")[0] == "Protein":
                d["proteinContent"] = _.split(": ")[1]
            elif _.split(": ")[0] == "Cholesterol":
                d["cholesterolContent"] = _.split(": ")[1]
            elif _.split(": ")[0] == "Sodium":
                d["sodiumContent"] = _.split(": ")[1]
            else:
                try:
                    d[_.split(": ")[0]] = _.split(": ")[1]
                except:
                    pass

        dict_info['nutri'] = d
        return dict_info
        # print(dict_info)
    else:
        b = get_content([recipe_name,url])
        if b:
            return getInfo(recipe_name,url)


# def get_data(inp):
#     req = urllib.request.Request(url="http://www.supercook.com/dyn/results",
#                                  data=urllib.parse.urlencode(inp).encode(),
#                                  headers={"Content-type": "application/x-www-form-urlencoded"})
#     response = urllib.request.urlopen(req)
#     the_page = json.loads(response.read().decode())
#     data = [[_['title'], _['url']] for _ in the_page['results'] if _['url'].split('/')[2] in websites][:20]
#     return data

def get_content(recipe):
    website = recipe[1].split('/')[2]
    url = recipe[1]
    if website == 'www.food.com':
        try:
            r_path = './recipes/' + recipe[0]
            if not os.path.exists(r_path):
                os.makedirs(r_path)
            else:
                return
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')
            t = json.loads(soup.find('script', type='application/ld+json').text)
            file = open(r_path+'/instruct.txt','w')
            content = t['recipeInstructions']
            if content is not None:
                file.write(content)
            file.close()
            file = open(r_path+'/nutri.txt','w')
            nut = t['nutrition']
            content = str('Calorie: ' + nut['calories'] +'\nFat: ' + nut['fatContent'] + '\nCarbs: ' + nut['carbohydrateContent'] + '\nProtein: ' + nut['proteinContent'] + '\nCholesterol: ' + nut['cholesterolContent'] + '\nSodium: ' + nut['sodiumContent'])
            if content is not None:
                file.write(content)
            file.close()
            file = open(r_path + '/link.txt', 'w')
            content = url
            if content is not None:
                file.write(content)
            file.close()
            file = open(r_path + '/rating.txt', 'w')
            if 'aggregateRating' not in t.keys():
                content = "-1"
            else:
                content = t['aggregateRating']['ratingValue'] + '~' + t['aggregateRating']['reviewCount']
            if content is not None:
                file.write(content)
            file.close()
            file = open(r_path + '/time.txt', 'w')
            content = t['totalTime']
            if content is not None:
                file.write(content.replace('PT','').lower())
            file.close()
            file = open(r_path + '/img.txt', 'w')
            content = t['image']
            if content is not None:
                file.write(content)
            file.close()
        except Exception as e:
            print('check 0',e)
            return False
    if website == 'allrecipes.com':
        try:
            nut = {}
            r_path = './recipes/' + recipe[0]
            if not os.path.exists(r_path):
                os.makedirs(r_path)
            else:
                return


            temp = urllib.request.urlopen(url)
            html = temp.read()
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf8')
            nut_link = "https://apps.allrecipes.com/v1/recipes/" + temp.geturl().split("/")[
                4] + "?fields=nutrition&isMetric=false&servings=2"

            token = [_.split('ARToken=')[1].split(';')[0] for _ in temp.info().values() if 'ARToken=' in _][0]
            req = urllib.request.Request(nut_link, None, {"Authorization":"Bearer "+token})
            temp_de = urllib.request.urlopen(req).read()
            try:
                c = json.loads(temp_de)['nutrition']
            except:
                c = json.loads(temp_de.decode())['nutrition']
            content = [_.text for _ in soup.find_all("span", class_='recipe-directions__list--item')]
            file = open(r_path + '/instruct.txt', 'w')
            if content is not None:
                file.write("".join(content))
            file.close()
            if len(c) > 0:
                nut['calories'] = str(c['calories']['displayValue'])
                nut['fatContent'] = str(c['fat']['displayValue'])
                nut['cholesterolContent'] = str(c['cholesterol']['displayValue'])
                nut['sodiumContent'] = str(c['sodium']['displayValue'])
                nut['carbohydrateContent'] = str(c['carbohydrates']['displayValue'])
                nut['proteinContent'] = str(c['protein']['displayValue'])
                nut['vitaminC'] = str(c['vitaminC']['displayValue'])
                nut['calciumContent'] = str(c['calcium']['displayValue'])
                nut['ironContent'] = str(c['iron']['displayValue'])
                file = open(r_path + '/nutri.txt', 'w')
                if content is not None:
                    for _ in nut:
                        file.write(_ + ": " + nut[_] + '\n')
                file.close()
            else:
                file = open(r_path + '/nutri.txt', 'w')
                if content is not None:
                    file.write('')
                file.close()

            content = url
            file = open(r_path + '/link.txt', 'w')
            if content is not None:
                file.write(content)
            file.close()

            t = soup.find('div', attrs={'class','rating-stars'})

            content = t['data-ratingstars']
            content = "%.1f"%float(content)
            t = soup.find('span', attrs={'class', 'review-count'})
            file = open(r_path + '/rating.txt', 'w')
            content = content + '~' + str(t.text.split()[0])
            if content is not None:
                file.write(content)
            file.close()

            content = soup.find('time', attrs={'itemprop':'totalTime'})
            file = open(r_path + '/time.txt', 'w')
            if content is not None:
                file.write(content.text.replace(" ",""))
            else:
                file.write('NA')
            file.close()
            content = soup.find('img', attrs={'class':'rec-photo'})
            # print(content)
            content = content["src"]
            file = open(r_path + '/img.txt', 'w')
            if content is not None:
                file.write(content)
            else:
                file.write('NA')
            file.close()
        except Exception as e:
            print('check 1',e)

            return False

if __name__ == "__main__":
    # getInfo("Almond Butter")

    """
    def func(recipe):
        _thread.start_new_thread(get_content,(recipe,))
        return recipe[0]
    """
    """
    ingredients = open("all_ingredients.txt").read().split(", ")
    print(ingredients)
    #recipe = ["Baked Pumpkin Donuts", 'http://www.food.com/recipe/baked-pumpkin-donuts-333831']
    recipe = ["Egg in a Boat", 'http://allrecipes.com/recipe/21145/homemade-stewed-tomatoes/']
    get_content(recipe)
    """

    """
    x = func(["Egg in a Boat", 'http://allrecipes.com/recipe/21145/homemade-stewed-tomatoes/'])
    print(x)
    time.sleep(0.1)
    out = get_data(data)
    for recipe in out:
        get_content(recipe)
    """

    """
    name_box = soup.find('td', attrs={'class': 'time'})
    time = name_box.text
    time = time.replace(" ","")
    time = time.replace("\n","")
    print(time)
    """
    websites = ['www.food.com' , 'allrecipes.com']
    ingredients = open("all_ingredients.txt").read().split(", ")
    # get_content(["Fried Boiled Eggs", "http://allrecipes.com/recipe/241866/fried-boiled-eggs/"])
    """
    for _ in itertools.combinations(ingredients, 2):
        time.sleep(0.1)
        print('_=',_)
        data['kitchen'] = _[0] + "," + _[1]
        out = get_data(data)
        print(data['kitchen'], '-' * 50)
        for recipe in out:
            website = recipe[1].split('/')[2]
            if website in websites:
                print(recipe[0], recipe[1])
                get_content(recipe)
    """