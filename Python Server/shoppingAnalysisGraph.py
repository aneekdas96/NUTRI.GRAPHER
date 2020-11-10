import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pickle

nutrient_list = sorted(["fat", "cholesterol", "sodium", "carbs", "protein", "calcium", "iron", "vitC"])
print(nutrient_list)

nutrients_norm = {
    "calories": 1,
    "protein": 50,
    "carbs": 300,
    "sodium": 2400,
    "fat": 65,
    "cholesterol": 300,
    "vitC": 60,
    "iron": 18,
    "calcium": 1000
}

def ingredients2nutritions(ingredients):
    # {"chocolate":{"Sodium":3,"Proteins":5}, "":{}}
    f = open("ingredient_nutrients.pickle","rb")
    ing_nutrient_dict = pickle.load(f)
    f.close()

    # print(ing_nutrient_dict)

    theta = np.linspace(0,2*np.pi,len(nutrient_list)+1,endpoint=True)
    # theta += np.pi/2
    data = {}
    ##########################################################
    max_val_nutrients = {"fat":0, "cholesterol":0, "sodium":0, "carbs":0, "protein":0, "calcium":0, "iron":0, "vitC":0}
    for item in ing_nutrient_dict.keys():
        if ing_nutrient_dict[item] == None:
            continue
        nutrients_in_ingredient = ing_nutrient_dict[item]
        for nutrient in sorted(nutrients_in_ingredient.keys()):
            # print('nutrient : ', nutrient)
            if nutrient in nutrient_list:
                # print(item, nutrient, max_val_nutrients)
                if nutrients_in_ingredient[nutrient] != None and nutrients_in_ingredient[nutrient] > max_val_nutrients[nutrient]:
                    max_val_nutrients[nutrient] = nutrients_in_ingredient[nutrient]
    # print('max value list : ', max_val_nutrients)

    #########################################################
    for ingredient in ing_nutrient_dict.keys():
        if ingredient in ingredients:
            if ing_nutrient_dict[ingredient]==None:
                print(ingredient, " not present")
                continue
            nutrients_in_ingredient = ing_nutrient_dict[ingredient]
            d = []
            for nutrient in nutrient_list:
            # for nutrient in list(sorted(nutrients_in_ingredient.keys())):
            #     if nutrient in nutrient_list:
            #     print(ingredient, nutrient, nutrients_in_ingredient[nutrient])

                if nutrients_in_ingredient[nutrient] != None:
                    d.append(float(nutrients_in_ingredient[nutrient])/float(max_val_nutrients[nutrient]))
                else:
                    d.append(float(0))
            d.append(d[0])
            data[ingredient] = d
    return theta, data

def create_graph(ingredients):
    theta, data = ingredients2nutritions(ingredients)
    # print(theta, data)
    # data_ing = []
    # for item in data:
    #     data_ing.append([data])

    plt.figure(figsize=(8,8))
    ax = plt.subplot(111,polar=True)
    colors = ['r','g','y','b','k','m','purple','olive']

    # ax.set_rgrids([0.2,0.4,0.6,0.8])
    patches = []
    for d, color in zip(list(sorted(data.keys())),colors[:len(list(data.keys()))]):
        ax.plot(theta,data[d],color)
        ax.fill(theta,data[d],color,alpha=0.3)
        patch = mpatches.Patch(color=color, label=d)
        patches.append(patch)
    # ax.set_varlabels(nutrient_list)
    plt.gca().set_xticklabels(nutrient_list)
    ax.legend(handles=patches,bbox_to_anchor=(1.05, 1.1), bbox_transform=ax.transAxes)
    # plt.title("Calories: ",)
    plt.savefig("./server_assets/analysis_shopping.jpg")

    all_data = []
    for ing in data:
        all_data.append(data[ing])
    all_data = np.array(all_data)
    # print(all_data)
    # print(all_data.shape)

    empty = []
    low = []
    analysis_message = ""
    if all_data!=[]:
        for i in range(all_data.shape[1]):
            sum_ = sum(all_data[:,i])
            if sum_==0:
                empty.append(nutrient_list[i])
            elif sum_<0.005:
                low.append(nutrient_list[i])
        if len(empty)>0:
            analysis_message = "You do not have any "+ " and ".join(empty) + " nutrients in your shopping list.\n"
        if len(low)>0:
            analysis_message += " Consider buying " + " and ".join(low) + "."
    return analysis_message

if __name__ == "__main__":
    print(create_graph(["spinach"]))
    # print(create_graph(["orange","apple"]))
    # print(create_graph(["spinach","bread","eggs", "chili powder", 'thyme']))
    # print(create_graph(["chili powder"]))
