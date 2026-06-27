from typing import Any
import requests

refiner_recipes = requests.get("https://raw.githubusercontent.com/AssistantNMS/App/refs/heads/main/assets/json/en/Refinery.lang.json").json()
raw_materials = requests.get("https://raw.githubusercontent.com/AssistantNMS/App/refs/heads/main/assets/json/en/RawMaterials.lang.json").json()
products = requests.get("https://raw.githubusercontent.com/AssistantNMS/App/refs/heads/main/assets/json/en/Products.lang.json").json()
curiosities = requests.get("https://raw.githubusercontent.com/AssistantNMS/App/refs/heads/main/assets/json/en/Curiosity.lang.json").json()

def get_item_from_name(name: str) -> dict[str, Any]:
    raw_material = [
        raw for raw in raw_materials
        if raw["Name"] == name
    ]

    product = [
        product for product in products
        if product["Name"] == name
    ]

    curiosity = [
        curiosity for curiosity in curiosities
        if curiosity["Name"] == name
    ]

    if len(raw_material) > 0:
        return raw_material[0]
    elif len(product) > 0:
        return product[0]
    elif len(curiosity) > 0:
        return curiosity[0]
    else:
        return {}

def get_possible_items_from_name(name: str) -> list[dict[str, Any]]:
    possible_items: list[dict[str, Any]] = []

    raw_material = [
        raw for raw in raw_materials
        if name.lower() in raw["Name"].lower()
    ]

    product = [
        p for p in products
        if name.lower() in p["Name"].lower()
    ]

    curiosity = [
        curiosity for curiosity in curiosities
        if name.lower() in curiosity["Name"].lower()
    ]

    possible_items.extend(raw_material)
    possible_items.extend(product)
    possible_items.extend(curiosity)

    return possible_items

def get_item_from_id(id: str) -> dict[str, Any]:
    raw_material = [
        raw for raw in raw_materials
        if raw["Id"] == id
    ]

    product = [
        product for product in products
        if product["Id"] == id
    ]

    curiosity = [
        curiosity for curiosity in curiosities
        if curiosity["Id"] == id
    ]

    if len(raw_material) > 0:
        return raw_material[0]
    elif len(product) > 0:
        return product[0]
    elif len(curiosity) > 0:
        return curiosity[0]
    else:
        return {}
    

def get_refiner_recipes_for_item_name(name: str) -> list[Any]:
    item = get_item_from_name(name)
    
    item_id = item["Id"]

    recipes = [
        recipe for recipe in refiner_recipes
        if item_id == recipe["Output"]["Id"]
    ]

    return recipes

def get_refiner_recipes_for_possible_item_name(name: str) -> list[Any]:
    items = get_possible_items_from_name(name)

    recipes: list[Any] = []

    for i in range(len(items)):
        recipe = get_refiner_recipes_for_item_name(items[i]["Name"])
        recipes.extend(recipe)
    
    return recipes

def format_recipe(recipe: Any) -> dict[str, Any]:
    result = {}

    inputs = recipe["Inputs"]

    format_inputs = []
    for i in range(len(inputs)):
        item = get_item_from_id(inputs[i]["Id"])
        format_inputs.append({
            "Name": item["Name"],
            "Quantity": recipe["Inputs"][i]["Quantity"]
        })
    result["Inputs"] = format_inputs

    item = get_item_from_id(recipe["Output"]["Id"])
    result["Output"] = {
        "Name": item["Name"],
        "Quantity": recipe["Output"]["Quantity"]
    }

    result["Time"] = recipe["Time"]

    return result

def print_recipe(recipe: Any):
    print("inputs: ", end="")
    for i in recipe["Inputs"]:
        print(f"{i["Quantity"]} {i["Name"]}", end=", ")
    print(f"output: {recipe["Output"]["Quantity"]} {recipe["Output"]["Name"]}")

name = input("What item do you want as an end product of your refinement?: ")
recipes = get_refiner_recipes_for_possible_item_name(name)

format_recipes: list[dict[str, Any]] = []

for r in recipes:
    format_recipes.append(format_recipe(r))

for i in range(len(format_recipes)):
    print(f"idx: {i} ",end="")
    print_recipe(format_recipes[i])

if format_recipes == 1:
    recipe_option = 0
else:
    recipe_option = int(input("Out of all of these sets of inputs per recipe available for the output material, which one do you want to use?\n" \
                              f"Please type a number that can be used to index from 0 to {len(format_recipes)-1} of the list: "))

chosen_recipe = format_recipes[recipe_option]

required_inputs = chosen_recipe["Inputs"]

inventory_available: list[dict[str, Any]] = []

for i in range(len(required_inputs)):
    i_name = required_inputs[i]["Name"]

    i_available = int(input(f"How much {i_name} do you have (or wish) to spend?: "))
    inventory_available.append({
        "Name": i_name,
        "Available": i_available,
    })

num_refineries = int(input("How many refineries do you plan to use to refine this recipe?: "))

# required_inputs must contain "Name" and "Available"
# returns dict containing "Name" and "Available"
def get_restricted_input(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    least_input = inventory[0]["Available"] * required_inputs[0]["Quantity"]
    least_input_available = inventory[0]["Available"]
    least_input_name = inventory[0]["Name"]

    for i in range(1, len(inventory)):
        input_num = inventory[i]["Available"] * required_inputs[i]["Quantity"]
        if input_num < least_input:
            least_input = input_num
            least_input_available = inventory[i]["Available"]
            least_input_name = inventory[i]["Name"]
    
    return {
        "Name": least_input_name,
        "Available": least_input_available
    }

restricted_input = get_restricted_input(inventory_available)

max_total = (restricted_input["Available"] * chosen_recipe["Output"]["Quantity"])

total_time = (float(chosen_recipe["Time"]) * max_total) / chosen_recipe["Output"]["Quantity"]

print(f"You can make a total of {max_total} {chosen_recipe["Output"]["Name"]} using {num_refineries} by putting")

for i in range(len(chosen_recipe["Inputs"])):
    print(f"{(restricted_input["Available"] * chosen_recipe["Inputs"][i]["Quantity"]) / num_refineries} {chosen_recipe["Inputs"][i]["Name"]}")

print(f"in each refinery, taking a total of {total_time / num_refineries} seconds")