import nextcord
from nextcord.ext import commands
from nextcord.ui import Button
#from nextcord_components import DiscordComponents, Button, ButtonStyle
from nextcord import Embed


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
    return embed, buttons
