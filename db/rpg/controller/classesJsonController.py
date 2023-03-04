import json


def getAllClasses():
    # Load the JSON file
    with open('db/rpg/db/classes.json', 'r') as f:
        data = json.load(f)

    # Extract the "classes" array
    classes = data['classes']
    return classes


def getClassByName(name):
    data = getAllClasses()
    for clss in data:
        if clss['name'].lower() == name.lower():
            return clss
    return None


def getClassById(id):
    data = getAllClasses()
    for clss in data['classes']:
        if clss['id'] == id:
            return clss
    return None


def getAttributeFromClass(name, attribute):
    clss = getClassByName(name)
    return clss[attribute]
