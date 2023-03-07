import random


def calculate_damage(level, power, attack_stat, defense_stat, modifier):

  random_multiplier = random.uniform(0.85,
                                     1.0)  # Random value between 0.85 and 1.0
  numerator = (((((
    (25 * level)) + 2) * power * attack_stat) / defense_stat)) + 2
  damage = int(((numerator) / 100 * modifier * random_multiplier) +
               0.5)  # Round to nearest integer

  return damage


def levelUp(lvlStart, exp, player_exp):
  lvl = lvlStart
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


def checkAdvantage(atkClass, defType):
  if atkClass['strong'].lower() == defType.lower():
    return 1.50
  elif atkClass['weak'].lower() == defType.lower():
    return 0.50
  else:
    return 1


def checkPassive(currentHp, MaxHp, type):
  if currentHp / MaxHp <= 0.30:
    if type.lower() == "fire":
      return "dmgModifier", 1.30
    elif type.lower() == "ice":
      return "defModifier", 0.50
    elif type.lower() == "thunder":
      if random.random() < 0.3:
        return "dmgModifier", 2
      else:
        return "dmgModifier", 1
    elif type.lower() == "wind":
      return "evade", 0.30
    elif type.lower() == "dark":
      return "status", "Fear"
  else:
    return None


def checkIfStatus(status, chance):
  if random.random() < (chance / 100):
    return status
  return None


def checkStatus(status, maxHp, currentHp):
  if status is not None:
    if status in ["Burn", "Bleed"]:
      currentHp -= (maxHp * 0.05)
      return currentHp, (maxHp * 0.05), False
    elif status in ["Stun", "Freeze", "Fear"]:
      return currentHp, 0, True
  return None


def calc_accuracy(attack_acc, modifier):
  accuracy = (attack_acc / 100 * 3 / 4) * (1 + (modifier / 100))
  return min(1.0, accuracy)


def calc_hp(base_hp, lvl):
  new_hp = (0.01 * (2 * 66) * 0.25 * (base_hp * 6) * lvl) + lvl + 10
  return int(new_hp)


def calc_stat(base_stat, lvl):
  new_stat = (0.01 * (2 * 66) * 0.25 * (base_stat * 6) * lvl) + 5
  return int(new_stat)
