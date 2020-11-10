from flask import Flask, request, jsonify
from google.cloud import vision
import shoppingAnalysisGraph
import recipeScraping
import actual_scrap
import spell_check
import visionOCR
import plotRose
import doc2vec

app = Flask(__name__)

client = vision.ImageAnnotatorClient()

print("Started flask")

@app.route("/fetchRecipeNames",methods=['GET','POST'])
def getPicSendNames():
    # receive pic, ocr -> ingredients, fetch recipes' names, send names
    print("fetchRecipeNames")
    fname = "./server_assets/pic.png"
    file = request.files.get('file','')
    f = open(fname,"wb")
    f.write(file.read())
    f.close()
    ingredients = visionOCR.getIngredients(fname,client)
    try:
        print("Ingredients Detected: ", ingredients)
    except:
        pass
    ingredients = spell_check.correct_spellings(ingredients)
    try:
        print("Ingredients Detected: ", ingredients)
    except:
        pass
    recipes_names = recipeScraping.scrape(ingredients)
    # print(recipes_names)
    print("Recipes fetched")
    return recipes_names

@app.route("/fetchRecipeCoor",methods=['GET','POST'])
def getNameSendCoor():
    # receive recipe name, send it's coordinate from doc2vec
    data = request.form['text']
    recipeName, recipeLink = data.split("~=~")
    recipeName = recipeName.replace("/","")
    print("fetchRecipeCoor : ",recipeName)
    recipeInfo = actual_scrap.getInfo(recipeName, recipeLink)
    nutrient_colour = plotRose.give_colour(recipeInfo['nutri'])

    if recipeInfo is not None:
        coor = doc2vec.fetch_coor(recipeInfo["instruct"])
        coordinates = ""
        for i in coor:
            coordinates += str(i) +","
        return coordinates[:-1]+"~=~"+nutrient_colour
    else:
        return "null"

@app.route("/fetchRecipeInfo",methods=['GET','POST'])
def getNamesendInfo():
    # receive recipe name, send it's info from cache
    data = request.form['text']
    recipeName, recipeLink = data.split("~=~")
    recipeName = recipeName.replace("/","")
    print("fetchRecipeInfo : ",recipeName)
    recipeInfo = actual_scrap.getInfo(recipeName,recipeLink)
    if recipeInfo is not None:
        nutrition_dict = recipeInfo["nutri"]
        if nutrition_dict != {}:
            plotRose.saveRose(nutrition_dict)
            graph_base64 = plotRose.img_base64("./server_assets/graph.jpg")
            recipeInfo["graph_base64"] = graph_base64
        # print(recipeInfo)
        return jsonify(recipeInfo)
    else:
        return "null"

@app.route("/analyzeList",methods=['GET','POST'])
def analyzeShoppingList():
    print("analyzeList")
    fname = "./server_assets/pic.png"
    file = request.files.get('file', '')
    f = open(fname, "wb")
    f.write(file.read())
    f.close()
    ingredients = visionOCR.getIngredients(fname, client)
    try:
        print("Ingredients Detected: ", ingredients)
    except:
        pass
    ingredients = spell_check.correct_spellings(ingredients)
    try:
        print("Ingredients Detected: ", ingredients)
    except:
        pass
    analysis_message = shoppingAnalysisGraph.create_graph(ingredients)
    return plotRose.img_base64("./server_assets/analysis_shopping.jpg")+";~**~**~&&~;"+analysis_message

if __name__ == "__main__":
    app.run(host="0.0.0.0")

