import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import base64
import io

nutrients_norm = {
    "calories": 1,
    "proteinContent": 50,
    "carbohydrateContent": 300,
    "sodiumContent": 2400,
    "fatContent": 65,
    "cholesterolContent": 300,
    "vitaminC": 60,
    "ironContent": 18,
    "calciumContent": 1000
}

keys2name = {
    "calories": "Calories",
    "proteinContent": "Proteins",
    "carbohydrateContent": "Carbohydrates",
    "sodiumContent": "Sodium",
    "fatContent": "Fats",
    "cholesterolContent": "Cholesterol",
    "vitaminC": "VitaminC",
    "ironContent": "Iron",
    "calciumContent": "Calcium"
}


def img_base64(graph_fname):
    with open(graph_fname,"rb") as f:
        encoded_im = base64.b64encode(f.read())
    return encoded_im.decode('utf-8')

def normalize_nutrients(nutrients):
    for i in nutrients.keys():
        if '<' in nutrients[i]:
            nutrients[i] = nutrients[i].replace('<', '')
        if float(nutrients[i])>nutrients_norm[i]:
            nutrients[i] = nutrients_norm[i]-0.01
        nutrients[i] = float(nutrients[i])/nutrients_norm[i]
    return nutrients

def saveRose(nutrients):
    nutrients = normalize_nutrients(nutrients)
    calories = float(nutrients["calories"])
    del nutrients["calories"]
    n_keys = sorted(list(nutrients.keys()))
    n_keys_name = []
    n_values = []
    n_values_norm = []
    for i in n_keys:
        n_values.append(nutrients[i])
        n_values_norm.append(nutrients_norm[i])
        n_keys_name.append(keys2name[i])

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_axes([0.01, 0.1, 0.8, 0.8], polar=True)
    # ax.grid(False)
    ax.set_rlabel_position(30)

    # ax.set_ylim(0,5)
    # ax.set_yticks(np.arange(0,5,0.5))
    # ax.set_xlim(1,len(nutrients.keys())+1)
    ax.set_xticks(np.arange(0, len(nutrients.keys()) + 1, 2 * np.pi / len(nutrients.keys())))

    xlabels = n_keys_name
    plt.gca().set_xticklabels(xlabels)

    N = len(nutrients.keys())
    theta = np.arange(0.0, 2 * np.pi, 2 * np.pi / N)
    # theta = np.linspace(0.0, 2*np.pi, N)
    # theta = [0,1,2,3,4,5]
    # theta = np.arange(N)
    radii = 10 * np.random.rand(N)  # the values of nutrients
    radii = n_values  # the values of nutrients
    width = np.pi / 4 * np.random.rand(N)  # the width of each arc
    width = [1] * N  # the width of each arc
    bars = ax.bar(theta, radii, width=width, bottom=0.0)

    patches = []
    for i, r, bar in zip(np.arange(N), radii, bars):
        if r == 0:
            r = 0.1
        bar.set_facecolor(cm.CMRmap(r))
        patch = mpatches.Patch(color=cm.CMRmap(r),
                               label=n_keys_name[i] + ": " + "%.1f" % (n_values[i] * n_values_norm[i]))
        patches.append(patch)
        # bar.set_alpha(0.5)

    ax.set_rmax(1)

    # max_wind_circle = plt.Circle((0, 0), 0.2, transform=ax.transData._b, fill=False, edgecolor='gray',
    #                              linewidth=1, alpha=1, zorder=9)
    # fig.gca().add_artist(max_wind_circle)
    # max_wind_circle = plt.Circle((0, 0), 0.4, transform=ax.transData._b, fill=False, edgecolor='gray',
    #                              linewidth=1, alpha=1, zorder=9)
    # fig.gca().add_artist(max_wind_circle)
    max_wind_circle = plt.Circle((0, 0), 0.5, transform=ax.transData._b, fill=False, edgecolor='blue',
                                 linewidth=1, alpha=1, zorder=9)
    fig.gca().add_artist(max_wind_circle)
    # max_wind_circle = plt.Circle((0, 0), 0.6, transform=ax.transData._b, fill=False, edgecolor='gray',
    #                              linewidth=1, alpha=1, zorder=9)
    # fig.gca().add_artist(max_wind_circle)
    # max_wind_circle = plt.Circle((0, 0), 0.8, transform=ax.transData._b, fill=False, edgecolor='gray',
    #                              linewidth=1, alpha=1, zorder=9)
    # fig.gca().add_artist(max_wind_circle)

    ax.legend(handles=patches, bbox_to_anchor=(1.25, 1.1), bbox_transform=ax.transAxes)

    plt.title("Calories: %.1f Kcal" % calories)
    plt.savefig("./server_assets/graph.jpg")
    # plt.show()


def give_colour(nutrients):
    nutrients_colour = {
        "proteinContent": 'red',
        "carbohydrateContent": 'magenta',
        "sodiumContent": 'blue',
        "fatContent": 'brown',
        "cholesterolContent": 'yellow',
        "vitaminC": 'green',
        "ironContent": 'black',
        "calciumContent": 'gray'
    }

    n_keys = list(sorted(nutrients.keys()))
    n_keys.remove('calories')
    print(n_keys)
    n_values = []
    for i in n_keys:
        if i!="calories":
            n_values.append(float(nutrients[i])/float(nutrients_norm[i]))
    print(n_values)
    index = np.argmax(n_values)
    print(index)
    return nutrients_colour[n_keys[index]]



if __name__ == "__main__":
    # saveRose({
    #     "calories": 40,
    #     "proteinContent": 15 / 100,
    #     "carbohydrateContent": 56 / 100,
    #     "sodiumContent": 87 / 100,
    #     "fatContent": 56 / 100,
    #     "cholesterolContent": 54 / 100
    # })
    #
    print(give_colour({
        "calories": 67,
        "proteinContent": 34 / 100,
        "carbohydrateContent": 23 / 100,
        "sodiumContent": 67 / 100,
        "fatContent": 67 / 100,
        "cholesterolContent": 43 / 100,
        "vitaminC": 56 / 100,
        "iron": 45 / 100,
        "calcium": 12 / 100,

    }))

