import json


def getAllAttackTypes():
    with open('attacks.json', 'r') as f:
        data = json.load(f)

    attack_types = []
    for t in data['types']:
        attack_types.append({
            'id': t['id'],
            'name': t['name'],
            'attacks': t['attacks']
        })

    return attack_types


def getAttacksByType(type_name):
    all_attack_types = getAllAttackTypes()
    for attack_type in all_attack_types:
        if attack_type['name'] == type_name:
            return attack_type['attacks']
    return []


def get_attack_by_name(attack_name):
    with open('attacks.json', 'r') as f:
        data = json.load(f)

    for attack_type in data['types']:
        for attack in attack_type['attacks']:
            if attack['name'] == attack_name:
                return attack

    return None