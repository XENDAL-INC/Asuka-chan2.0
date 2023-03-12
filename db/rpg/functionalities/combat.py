import random
import sys

sys.path.append('db/rpg/functionalities/')
sys.path.append('db/rpg/controller/')

import calculations as calc
import attacksJsonController as attacksCont
import classesJsonController as classCont
import statusesJsonController as statusCont


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


def playerPVPCalc(playerAttacking, playerDefending, attack_used):
  attack_used = attacksCont.getAttacksByName(attack_used)
  atkClass = classCont.getClassByName(attack_used['type'])
  dmgModifier = calc.checkAdvantage(atkClass, playerDefending['class'])
  defModifier = 1
  evasionModifier = 0
  healModifier = 0
  statusInflict = None

  passiveCheck1 = calc.checkPassive(playerAttacking['CurrentHp'],
                                    playerAttacking['MaxHp'],
                                    playerAttacking['class'])
  passiveCheck2 = calc.checkPassive(playerDefending['CurrentHp'],
                                    playerDefending['MaxHp'],
                                    playerDefending['class'])

  if passiveCheck1 is not None:  #check player1 passive
    passive, passiveValue = passiveCheck1
    if passive == "dmgModifier":
      dmgModifier *= passiveValue
    elif passive == "healModifier":
      healModifier = passiveValue
    elif passive == "status":
      statusInflict = passiveValue

  if passiveCheck2 is not None:  #check playerDefending passive
    passive2, passiveValue2 = passiveCheck2
    if passive2 == "defModifier":
      dmgModifier *= passiveValue2
    elif passive2 == "evade":
      evasionModifier = passiveValue2

  attack_power = attack_used['power']
  playerDmg = calc.calculate_damage(playerAttacking['lvl'], attack_power,
                                    playerAttacking['atk'],
                                    playerDefending['defense'], dmgModifier)

  statusInflict = calc.checkIfStatus(attack_used, statusInflict)
  statusDmg = 0
  statusInhibit = False

  statusInfo = calc.checkStatus(statusInflict, playerDefending['MaxHp'])
  if statusInfo is not None:
    statusDmg, statusInhibit = statusInfo

  playerDefending['CurrentHp'] -= (playerDmg + statusDmg) * defModifier
  playerAttacking['CurrentHp'] += int((playerDmg + statusDmg) * healModifier)
  if statusInflict == "Leech":
    playerAttacking['CurrentHp'] += statusDmg

  playerDefendingHpBar = health_bar(playerDefending["CurrentHp"],
                                    playerDefending["MaxHp"])

  playerAttackingHpBar = health_bar(playerAttacking["CurrentHp"],
                                    playerAttacking["MaxHp"])

  #if Game Over
  if playerDefending['CurrentHp'] <= 0:

    return playerAttacking, playerDefending, playerAttackingHpBar, playerDefendingHpBar, playerDmg, True, statusInflict, statusDmg, statusInhibit, healModifier

  #not Game Over
  playerDefending['status'] = statusInflict
  return playerAttacking, playerDefending, playerAttackingHpBar, playerDefendingHpBar, playerDmg, False, statusInflict, statusDmg, statusInhibit, healModifier


def playerEncounterCalc(player, newMonster, attack_used, monsterLvl,
                        monsterDmg, monsterAtkName):
  attack_used = attacksCont.getAttacksByName(attack_used)
  atkClass = classCont.getClassByName(attack_used['type'])
  dmgModifier = calc.checkAdvantage(atkClass, newMonster['class'])
  defModifier = 1
  evasionModifier = 0
  healModifier = 0
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
    elif passive == "healModifier":
      healModifier = passiveValue

  attack_power = attack_used['power']
  playerDmg = calc.calculate_damage(player['lvl'], attack_power, player['atk'],
                                    newMonster['defense'], dmgModifier)

  statusInflict = calc.checkIfStatus(attack_used, statusInflict)
  statusDmg = 0
  statusInhibit = False

  statusInfo = calc.checkStatus(statusInflict, newMonster['MaxHp'])
  if statusInfo is not None:
    statusDmg, statusInhibit = statusInfo

  newMonster['CurrentHp'] -= playerDmg + statusDmg
  monsterHpBar = health_bar(newMonster["CurrentHp"], newMonster["MaxHp"])
  player['CurrentHp'] += int((playerDmg + statusDmg) * healModifier)
  if statusInflict == "Leech":
    player['CurrentHp'] += statusDmg

  #if Game Over
  if newMonster['CurrentHp'] <= 0:
    playerHpBar = health_bar(player["CurrentHp"], player["MaxHp"])
    return player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, True, newMonster[
      'name'], player[
        'name'], statusInflict, statusDmg, statusInhibit, defModifier, healModifier

  #not Game Over
  newMonster['status'] = statusInflict
  playerHpBar = health_bar(player["CurrentHp"], player["MaxHp"])
  return player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, False, None, None, statusInflict, statusDmg, statusInhibit, defModifier, healModifier


def monsterEncounterCalc(player, newMonster, monsterLvl, monsterHpBar,
                         playerHpBar, defModifier):

  monsterAtkName = ""
  monsterDmg = ""
  #check if stunned
  statusInhibit = False
  if newMonster['status'] is not None:
    statusInhibit = statusCont.checkIfInhibit(newMonster['status'])
  if not statusInhibit:
    monsterRandomAttack = random.choice(newMonster["attacks"])
    monsterAtkUsed = attacksCont.getAttacksByName(monsterRandomAttack)
    monsterAtkName = monsterAtkUsed['name']
    attack_power = monsterAtkUsed['power']

    atkClass = classCont.getClassByName(monsterAtkUsed['type'])
    dmgModifier = calc.checkAdvantage(atkClass, player['class'])
    dmgModifier *= defModifier

    monsterDmg = calc.calculate_damage(monsterLvl, attack_power,
                                       newMonster['atk'], player['defense'],
                                       dmgModifier)
    player['CurrentHp'] -= monsterDmg
  playerHpBar = health_bar(player["CurrentHp"], player["MaxHp"])
  monsterHpBar = health_bar(newMonster["CurrentHp"], newMonster["MaxHp"])

  if player['CurrentHp'] <= 0:  #if Game Over
    return player, newMonster, playerHpBar, monsterHpBar, monsterDmg, monsterAtkName, True, player[
      'name'], newMonster['name'], statusInhibit

  #if stunned
  newMonster['status'] = None
  statusInhibit = None
  return player, newMonster, playerHpBar, monsterHpBar, monsterDmg, monsterAtkName, False, None, None, statusInhibit


def simpleEncounter(player, newMonster, attack_used, monsterLvl):
  monsterDmg = ""
  monsterAtkName = ""
  playerDmg = 0
  statusInflict = None
  statusDmg = 0

  if player['speed'] >= newMonster['speed']:  #if Player faster
    #userAttack
    player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, isGameOver, loser, winner, statusInflict, statusDmg, statusInhibit, defModifier, healModifier = playerEncounterCalc(
      player, newMonster, attack_used, monsterLvl, monsterDmg, monsterAtkName)

    if not isGameOver:
      #monsterAttack
      player, newMonster, playerHpBar, monsterHpBar, monsterDmg, monsterAtkName, isGameOver, loser, winner, statusInhibit = monsterEncounterCalc(
        player, newMonster, monsterLvl, monsterHpBar, playerHpBar, defModifier)

  else:  #ifPlayerSlower
    #check Player evasion and resistance passives
    defModifier = 1
    evasionModifier = 0
    passiveCheck = calc.checkPassive(player['CurrentHp'], player['MaxHp'],
                                     player['class'])
    if passiveCheck is not None:
      passive, passiveValue = passiveCheck
      if passive == "defModifier":
        defModifier = passiveValue
      elif passive == "evade":
        evasionModifier += passiveValue
    #monsterAttack
    player, newMonster, playerHpBar, monsterHpBar, monsterDmg, monsterAtkName, isGameOver, loser, winner, statusInhibit = monsterEncounterCalc(
      player, newMonster, monsterLvl, None, None, defModifier)

    if not isGameOver:
      #playerAttack
      player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, isGameOver, loser, winner, statusInflict, statusDmg, statusInhibit, defModifier, healModifier = playerEncounterCalc(
        player, newMonster, attack_used, monsterLvl, monsterDmg,
        monsterAtkName)

  return player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, isGameOver, loser, winner, statusInflict, statusDmg, healModifier


def pvp(player1, player2, attack_used, turn):
  playerDmg = 0
  statusInflict = None
  statusDmg = 0
  healModifier = 0

  if turn == 0:  #Player1 turn
    #player1Attack
    player1, player2, player1HpBar, player2HpBar, playerDmg, isGameOver, statusInflict, statusDmg, statusInhibit, healModifier = playerPVPCalc(
      player1, player2, attack_used)

    return player1, player2, player1HpBar, player2HpBar, playerDmg, isGameOver, statusInflict, statusDmg, statusInhibit, healModifier

  else:
    #player2Attack
    player2, player1, player2HpBar, player1HpBar, playerDmg, isGameOver, statusInflict, statusDmg, statusInhibit, healModifer = playerPVPCalc(
      player2, player1, attack_used)

    return player1, player2, player1HpBar, player2HpBar, playerDmg, isGameOver, statusInflict, statusDmg, statusInhibit, healModifier
