##Recipe object
import json


class Recipe:

    def __init__(self):
        self.name = "temp"
        self.time = list()
        self.ingredients = list
        self.recipeInstructions = list()

    def prettyPrint(self):
        print(self.name)
        for t in self.time:
            print(t)
        for i in self.ingredients:
            print(i)
        for r in self.recipeInstructions:
            print(r)


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

