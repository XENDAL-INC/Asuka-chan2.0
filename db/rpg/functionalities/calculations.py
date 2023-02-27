import random


def calculate_damage(level, power, attack_stat, defense_stat, modifier):
    """
    Calculates the damage of an attack in the Pokemon games using the given formula.
    
    Args:
    - level (int): The level of the attacking Pokemon.
    - power (int): The base power of the attack.
    - attack_stat (int): The attacking Pokemon's attack or special attack stat.
    - defense_stat (int): The defending Pokemon's defense or special defense stat.
    - modifier (float): The modifier for the damage calculation, taking into account type matchups,
        critical hits, and other factors.
        
    Returns:
    - damage (int): The amount of damage dealt by the attack.
    """

    random_multiplier = random.uniform(
        0.85, 1.0)  # Random value between 0.85 and 1.0
    numerator = (((((
        (2 * level) / 5) + 2) * power * attack_stat) / defense_stat) / 50) + 2
    damage = int(((numerator * modifier * random_multiplier) / 100) +
                 0.5)  # Round to nearest integer

    return damage


def levelUp(lvl, exp, player_exp):

    # Calculate x value for given level
    x = ((lvl + 54) - 55) * 0.3

    # Check if enough experience points to level up
    if exp >= ((x + 0.2) * ((lvl + 54)**2) + 1) - player_exp:
        # Deduct required experience points from total exp
        exp = exp - (((x + 0.2) * ((lvl + 54)**2) + 1) - player_exp)

        # Increase level by 1
        lvl += 1

        # Check if there is remaining exp to be gained
        if exp > 0:
            # Recursively call levelUp function with remaining exp
            levelUp(lvl, exp, 0)

        # Return new level and player_exp
        return lvl, player_exp

    # If not enough exp to level up
    else:
        # Add gained exp to player_exp
        player_exp = player_exp + exp

        # Return current level and updated player_exp
        return lvl, player_exp


def ifHit(attacker_acc, defender_eva):
    # Calculate the evasion fraction based on the defender's evasion stat.
    eva_fraction = defender_eva / 100 * 3 / 4
    # Multiply the accuracy and evasion fractions to get the hit chance as a decimal.
    hit_chance = attacker_acc * eva_fraction
    # Generate a random number between 0 and 1. If it's less than or equal to the hit chance, the attack lands.
    if random.random() <= hit_chance:
        return True
    else:
        return False


def calc_accuracy(attack_acc, modifier):
    accuracy = (attack_acc / 100 * 3 / 4) * (1 + (modifier / 100))
    return min(1.0, accuracy)
