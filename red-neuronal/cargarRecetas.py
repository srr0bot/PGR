import json

class RecipeDataLoader:
    def load_data(self, filepath):
        with open(filepath) as file:
            data = json.load(file)
        return data

    def parse_data(self, data):
        ingredients = [recipe['ingredientes'] for recipe in data.values()]
        procedures = [recipe['procedimiento'] for recipe in data.values()]
        return ingredients, procedures
