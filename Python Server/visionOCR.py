from google.cloud import vision
from google.cloud.vision import types
import io

def getIngredients(picName, client):
    ingredients = []

    with io.open(picName,"rb") as f:
        img_content = f.read()

    image = types.Image(content=img_content)

    response = client.text_detection(image=image)
    text = response.text_annotations

    # print(text)
    if len(text)>0:
        ocrResult = text[0].description
        print("found: ")
        # try:
        #     print(ocrResult)
        # except:
        #     pass

        for i in ocrResult.split("\n"):
            if i != '':
                ingredients.append(i.lstrip().rstrip().lower())

    return ingredients
