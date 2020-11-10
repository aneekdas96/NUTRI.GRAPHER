import nltk
from nltk import word_tokenize

def fetch_ingredients():
    f = open('all_ingredients.txt', 'r')
    ingredients = f.read()
    # ingredient_list = word_tokenize(ingredients)
    # for index, item in enumerate(ingredient_list):
    #     if item == ',':
    #         ingredient_list.pop(index)
    # return ingredient_list
    ingredient_list = ingredients.split(',')
    for index, item in enumerate(ingredient_list):
        item = item.strip(' ')
        ingredient_list[index] = item
    return ingredient_list

def levenshtein_distance(ingredient1, ingredient2):
    if len(ingredient1) < len(ingredient2):
        return levenshtein_distance(ingredient2, ingredient1)

    if len(ingredient2) == 0:
        return len(ingredient1)

    previous_val = range(len(ingredient2) + 1)
    for i, c1 in enumerate(ingredient1):
        current_val = [i + 1]
        for j, c2 in enumerate(ingredient2):
            insertions = previous_val[j + 1] + 1
            deletions = current_val[j] + 1
            substitutions = previous_val[j] + (c1 != c2)
            current_val.append(min(insertions, deletions, substitutions))
        previous_val = current_val

    return previous_val[-1]


def nearest_word(word_to_check):
    neighbors_and_scores = []
    ingredient_list = fetch_ingredients()
    for word in ingredient_list:
        score = levenshtein_distance(word_to_check, word)
        neighbors_and_scores.append([word, score])
    sorted_list = sorted(neighbors_and_scores, key=lambda item: item[1])
    return sorted_list[0][0]

def correct_spellings(ingredients):
    corrected_ingredients = []
    for i in ingredients:
        corrected_ingredients.append(nearest_word(i))
    return corrected_ingredients

if __name__ == "__main__":
    nearest_match = nearest_word('e gg')
    nearest_match = correct_spellings(["e gg","hamato","aneek"])
    print(nearest_match)
