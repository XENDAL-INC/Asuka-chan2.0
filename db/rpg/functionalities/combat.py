import random
import sys

sys.path.append('db/rpg/functionalities/')
sys.path.append('db/rpg/controller/')

import calculations as calc
import attacksJsonController as attacksCont
import classesJsonController as classCont


def health_bar(health, max_health):
  """
    This function returns an ASCII health bar for the given health and maximum health.

    Parameters:
    health (int): The current health value.
    max_health (int): The maximum health value.

    Returns:
    str: The ASCII health bar.
    """
  if health <= 0:
    health = 0
  health_percentage = health / max_health
  filled_blocks = int(health_percentage * 15)
  empty_blocks = 15 - filled_blocks
  health_bar = "[" + "█" * filled_blocks + "░" * empty_blocks + "]"
  health_bar += "\n" + str(health) + "/" + str(max_health)
  return health_bar


def simpleEncounter(player, newMonster, attack_used, monsterLvl):

  #userAttack
  atkClass = classCont.getClassByName(player['class'])
  dmgModifier = calc.checkAdvantage(atkClass, newMonster['class'])
  defModifier = 1
  evasionModifier = 0
  statusInflict = None

  passiveCheck = calc.checkPassive(player['CurrentHp'], player['MaxHp'],
                                   player['class'])
  if passiveCheck is not None:
    passive, passiveValue = passiveCheck
    if passive == "dmgModifier":
      dmgModifier *= passiveValue
    elif passive == "defModifier":
      defModifier = passiveValue
    elif passive == "evade":
      evasionModifier += passiveValue
    elif passive == "status":
      statusInflict = passiveValue

  attack_used = attacksCont.getAttacksByName(attack_used)
  attack_power = attack_used['power']
  playerDmg = calc.calculate_damage(player['lvl'], attack_power, player['atk'],
                                    newMonster['defense'], dmgModifier)
  newMonster['CurrentHp'] -= playerDmg
  monsterHpBar = health_bar(newMonster["CurrentHp"], newMonster["MaxHp"])

  if newMonster['CurrentHp'] <= 0:
    playerHpBar = health_bar(player["CurrentHp"], player["MaxHp"])
    return player, newMonster, playerHpBar, monsterHpBar, playerDmg, None, None, True, newMonster[
      'name'], player['name']

  #monsterAttack

  monsterRandomAttack = random.choice(newMonster["attacks"])
  monsterAtkUsed = attacksCont.getAttacksByName(monsterRandomAttack)
  attack_power = monsterAtkUsed['power']

  atkClass = classCont.getClassByName(newMonster['class'])
  dmgModifier = calc.checkAdvantage(atkClass, player['class'])
  dmgModifier *= defModifier

  monsterDmg = calc.calculate_damage(monsterLvl, attack_power,
                                     newMonster['atk'], player['defense'],
                                     dmgModifier)
  player['CurrentHp'] -= monsterDmg
  playerHpBar = health_bar(player["CurrentHp"], player["MaxHp"])
  if player['CurrentHp'] <= 0:
    return player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkUsed[
      'name'], True, player['name'], newMonster['name']

  return player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkUsed[
    'name'], False, None, None


def combatVSPc(player_dmg,
               computer_dmg,
               playerTurn,
               player_health,
               computer_health,
               isWin=False,
               isLoss=False):
  if playerTurn:
    print("Player's turn:")
    #input("Press Enter to attack...")
    print("You attacked the computer and dealt", player_dmg, "damage.")
    computer_health -= player_dmg
    print("Computer's health is now", computer_health)
    if computer_health <= 0:
      isWin = True
      return playerTurn, player_health, computer_health, isWin, isLoss
    playerTurn = False

  if not playerTurn:
    # Computer's turn
    print("Computer's turn:")
    print("The computer attacked you and dealt", computer_dmg, "damage.")
    player_health -= computer_dmg
    if player_health <= 0:
      isLoss = True
      return playerTurn, player_health, computer_health, isWin, isLoss
    playerTurn = True
