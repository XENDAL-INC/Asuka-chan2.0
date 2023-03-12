import nextcord
from nextcord.ext import commands
from nextcord.ui import Button
#from nextcord_components import DiscordComponents, Button, ButtonStyle
from nextcord import Embed


def createChar(user, avatar, wlcmMsg):
  embed = Embed()
  embed.set_thumbnail(url=avatar)
  embed.color = 0x4887c6
  embed.title = f"{user}'s Character Creation"
  embed.description = wlcmMsg
  emojis = ["▶️", "✅"]
  buttons = [
    Button(style=nextcord.ButtonStyle.secondary, label=emoji)
    for emoji in emojis
  ]
  return embed, buttons


def classChoice(user, avatar, clssName, description):
  embed = Embed()
  embed.set_thumbnail(url=avatar)
  embed.color = 0x4887c6
  embed.title = "What Element do u want to master? u have to choose by clicking the buttons!"
  embed.description = description
  return embed


def showRPGChar(user, player, avatar):
  embed = Embed()
  embed.set_thumbnail(url=avatar)
  embed.color = 0x4887c6
  embed.title = user + "'s Character"
  fields = [("Name", str(player["name"]), False),
            ("Class", str(player["class"]), True),
            ("Lvl", str(player["lvl"]), True),
            ("Exp", str(player["exp"]), True),
            ("HP", str(player["MaxHp"]), True),
            ("ATK", str(player["atk"]), True),
            ("DEF", str(player["defense"]), True),
            ("SPD", str(player["speed"]), True),
            ("EVA", str(player["evasion"]), True),
            ("ACC", str(player["accuracy"]), True),
            ("Attacks", str(player["attacks"]), False)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)
  #embed.set_footer(text="Requested by " + author.name)
  return embed


def showAttack(attack, avatar):
  embed = Embed()
  embed.set_thumbnail(url=avatar)
  embed.color = 0x4887c6
  embed.title = "Attack Info"
  fields = [("Attack Name", str(attack['name']), True),
            ("Type", str(attack['type']), True),
            ("Lvl", str(attack['lvl']), True),
            ("Power", str(attack["power"]), False),
            ("Accuracy", str(attack["accuracy"]), True),
            ("Status", str(attack["status"]), False),
            ("Description", str(attack['description']), False)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)

  return embed


def showRPGEncounter(user, player, monster, avatar, playerHpBar, monsterHpBar,
                     monsterLvl):
  embed = Embed()
  embed.set_thumbnail(url=avatar)
  embed.color = 0x4887c6
  embed.title = user + "'s Encounter"
  fields = [("Monster Name", str(monster["name"]), True),
            ("Lvl", str(monsterLvl), True), (monsterHpBar, "", False),
            (user + "'s Character", str(player["name"]), True),
            ("Lvl", str(player["lvl"]), True),
            ("EXP", str(player["exp"]), True), (playerHpBar, "", False),
            ("Attacks", "", True)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)
  # Adding buttons to the embed

  buttons = [
    Button(style=nextcord.ButtonStyle.primary, label=attack)
    for attack in player["attacks"]
  ]
  buttons.append(Button(style=nextcord.ButtonStyle.danger, label="Escape"))
  return embed, buttons


def encounterOutcome(playerName, playerAtk, playerDmg, monsterName, monsterAtk,
                     monsterDmg, gameOver, loser, winner, statusInflict,
                     statusDmg, healModifier):
  if not gameOver:
    if statusInflict is None:
      msg = f"{playerName} used {playerAtk} and dealt {playerDmg}!"
      msg += f"\n{monsterName} used {monsterAtk} and dealt {monsterDmg}!"
    else:
      msg = f"{playerName} used {playerAtk} and dealt {playerDmg}! ... WOW {playerName} also applied {statusInflict}!"
      if statusDmg > 0:
        if statusInflict == "Leech":
          msg += f"\n{playerName} absorbed {statusDmg} HP from {monsterName}!"
        else:
          msg += f"\n{monsterName} received extra {statusDmg} dmg from {statusInflict}!"
        msg += f"\n{monsterName} used {monsterAtk} and dealt {monsterDmg}!"
      else:
        msg += f"\n{monsterName} couldn't attack due to {statusInflict}!"

    if healModifier > 0:
      msg += f"\n{playerName} regained {int(healModifier*(playerDmg + statusDmg))} from the dmg caused!"

  else:
    msg = f"{winner} has defeated {loser}!"

  return msg


def showRPGPvp(user1, user2, player1, player2, avatar, player1HpBar,
               player2HpBar, turn):

  embed = Embed()
  embed.set_thumbnail(url=avatar)
  embed.color = 0x4887c6
  embed.title = f"{user1} vs. {user2}!"
  buttons = [
    Button(style=nextcord.ButtonStyle.primary, label=attack)
    for attack in player1["attacks"]
  ]
  fields = [(f"{user1}'s Turn", "", False)]

  if turn == 1:
    buttons = [
      Button(style=nextcord.ButtonStyle.primary, label=attack)
      for attack in player2["attacks"]
    ]
    fields = [(f"{user2}'s Turn", "", False)]

  fields.extend([(f"{user2}'s Character", str(player2["name"]), True),
                 ("Lvl", str(player2["lvl"]), True),
                 ("EXP", str(player2["exp"]), True), (player2HpBar, "", False),
                 (f"{user1}'s Character", str(player1["name"]), True),
                 ("Lvl", str(player1["lvl"]), True),
                 ("EXP", str(player1["exp"]), True), (player1HpBar, "", False),
                 ("Attacks", "", True)])
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)

  buttons.append(Button(style=nextcord.ButtonStyle.danger, label="Surrender"))

  return embed, buttons


def pvpOutcome(attackerName, attack_used, playerDmg, defenderName, gameOver,
               statusInflict, statusDmg, healModifier):
  if not gameOver:
    msg = f"{attackerName} used {attack_used} and dealt {playerDmg}!"
    if statusInflict is not None:
      msg += f"... WOW {attackerName} also applied {statusInflict}!"
      if statusDmg > 0:
        if statusInflict == "Leech":
          msg += f"\n{attackerName} absorbed {statusDmg} HP from {defenderName}!"
        else:
          msg += f"\n{defenderName} received extra {statusDmg} dmg from {statusInflict}!"
      else:
        msg += f"\n{defenderName} couldn't attack due to {statusInflict}!"

    if healModifier > 0:
      msg += f"\n{attackerName} regained {int(healModifier*(playerDmg + statusDmg))} from the dmg caused!"

  else:
    msg = f"{attackerName} has defeated {defenderName}!"

  return msg
