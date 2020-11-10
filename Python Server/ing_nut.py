from nutritionix.nutritionix import NutritionixClient

nutritionix = NutritionixClient(
    application_id="6842cc73",
    api_key="182622a1734bc424ace8f216b995094e"
    # debug=True, # defaults to False
)

print(nutritionix.search(q='rice', limit=10, offset=0, search_nutrient='calories'))
