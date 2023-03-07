import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
#import nextcord_components
#from nextcord_components import DiscordComponents, Button, ButtonStyle
from nextcord import Embed
import asyncio
import sys
import random

sys.path.append('db/rpg/functionalities/')
sys.path.append('db/rpg/controller/')

# Import the Python file
import calculations as calc
import combat as combat
import interactiveMessages as intMsg
import playerJsonController as playerCont
import monsterJsonController as monsterCont
import classesJsonController as classCont
import attacksJsonController as attacksCont


class RPGCommands(commands.Cog):

  def __init__(self, client):
    self.client = client
    #self.player = None
    #self.newMonster = None
    #self.playerHpBar = None
    #self.monsterHpBar = None
    #self.playerDmg = None
    #self.monsterDmg = None
    #self.monsterLvl = None
    self.encounters = {}

  @commands.command()
  async def createChar(self, ctx):
    user = ctx.author.name
    id = ctx.author.id
    avatar = ctx.author.display_avatar
    await ctx.send('What is your Name?')
    name = "John Doe"

    def check(message):
      return message.author == ctx.author and message.channel == ctx.channel

    try:
      response = await self.client.wait_for('message', check=check, timeout=30)
      await ctx.send(
        '```Hi ' + str(response.content) +
        '! Welcome to the world of Eryndor, a realm of magic and adventure where the five elements reign supreme. Whether you seek the power of fire, thunder, ice, wind, or dark, there is a path for you to follow and a destiny to fulfill.\n\nIn Eryndor, magic is everything. It flows through the land, the sea, and the very air we breathe. It is the key to power and the gateway to adventure. Those who master the five elements can shape the world to their will, becoming the greatest heroes or villains of their age.\n\nSo come, adventurer, and explore the wonders of Eryndor. Unleash the fury of the elements, brave perilous dungeons and treacherous terrain, and discover the secrets that lie hidden in the deepest, darkest corners of this enchanted land. The journey will be long and dangerous, but the rewards are beyond measure. Will you rise to the challenge and become a legend of Eryndor?```'
      )
      name = str(response.content)
    except asyncio.TimeoutError:
      await ctx.send('You took too long to respond.')
      return

    class_name = "Fire"
    await ctx.send(
      'What Element do u want to master? u have to choose from one of the following:'
    )
    await ctx.send(
      '```Fire: Those who master the element of fire are known for their fierce determination and their ability to unleash devastating attacks upon their enemies. Their raw power allows them to deal massive amounts of damage, but they lack the defensive capabilities of other adventurers. At critical situations increase their damage output.\n\nThunder: are lightning-fast and quick-witted, using their speed and agility to outmaneuver their foes. They are versatile fighters, capable of dealing moderate damage while still maintaining their mobility. However, they have slightly less health than other adventurers, making them vulnerable to sustained attacks. At critical health, they have a chance to attack twice\n\nIce: known for their durability and their ability to withstand even the most punishing attacks. They have a high base health pool and a slight boost to their defense, allowing them to shrug off damage while they close in on their enemies. However, their offensive capabilities are slightly weaker. At critical situations, they create an ice armor to protect themselves  and take less damage from attacks.\n\nWind:  are the masters of evasion, using their speed and agility to dodge attacks and strike from unexpected angles. They have a high base evasion stat and a slight boost to their speed, making them difficult to hit in combat. However, they have slightly less health than other adventurers, making them vulnerable to sustained attacks. In critical situations, they will use their mastery of the wind to evade incoming attacks.\n\nDark: Those who master the element of darkness are shrouded in mystery, able to hide in the shadows and strike with deadly accuracy. They have base stats across the board, but their attacks have a higher chance to hit their target. They are versatile fighters, capable of adapting to any situation and outmaneuvering their foes. In critical situations they can instill fear in their enemies, causing them to hesitate in combat.```'
    )

    try:
      response = await self.client.wait_for('message', check=check, timeout=30)
      #await ctx.send('hi')
      class_name = str(response.content)
    except asyncio.TimeoutError:
      await ctx.send('You took too long to respond.')
      return

    clss = classCont.getClassByName(class_name)
    hp = calc.calc_hp(clss['hp'], 1)
    atk = calc.calc_stat(clss['atk'], 1)
    defense = calc.calc_stat(clss['defense'], 1)
    speed = calc.calc_stat(clss['speed'], 1)
    evasion = calc.calc_stat(clss['evasion'], 1)
    accuracy = calc.calc_stat(clss['accuracy'], 1)
    attacks = []
    targetAttacks = attacksCont.getAllAttacksByTypeAndLevel(clss['name'], 0)
    for attack in targetAttacks.values():
      attacks.append(attack['name'])
    playerCont.createNewPlayerDB(id, user, class_name, name, hp, atk, defense,
                                 speed, evasion, accuracy, attacks)
    player = playerCont.getPlayersById(id)
    embed = intMsg.showRPGChar(user, player, avatar)
    await ctx.send(embed=embed)

  @commands.command()
  async def showChar(self, ctx):
    user = ctx.author.name
    id = ctx.author.id
    avatar = ctx.author.display_avatar
    self.player = playerCont.getPlayersById(id)

    embed = intMsg.showRPGChar(user, self.player, avatar)
    await ctx.send(embed=embed)

  @commands.command()
  async def encounter(self, ctx):
    user = ctx.author.name
    id = ctx.author.id
    if str(id) not in self.encounters:
      self.encounters[str(id)] = {
        'player': None,
        'newMonster': None,
        'playerHpBar': None,
        'monsterHpBar': None,
        'playerDmg': None,
        'monsterDmg': None,
        'monsterLvl': None,
      }
      #print(self.encounters)
    else:
      await ctx.send("u are already in an encounter")
      return
    avatar = ctx.author.display_avatar
    player = playerCont.getPlayersById(id)

    randomLvlRange = random.randint(-2, 1)
    monsterLvl = player['lvl'] + randomLvlRange
    if monsterLvl <= 0:
      monsterLvl = player['lvl']

    randomMonsterId = random.randint(0, len(monsterCont.getAllMonsters()) - 1)

    newMonster = monsterCont.getMonsterById(str(randomMonsterId))
    newMonster['MaxHp'] = calc.calc_hp(newMonster['MaxHp'], monsterLvl)
    newMonster['CurrentHp'] = newMonster['MaxHp']
    newMonster['atk'] = calc.calc_stat(newMonster['atk'], monsterLvl)
    newMonster['defense'] = calc.calc_stat(newMonster['defense'], monsterLvl)
    newMonster['speed'] = calc.calc_stat(newMonster['speed'], monsterLvl)

    playerHpBar = combat.health_bar(player["CurrentHp"], player["MaxHp"])
    monsterHpBar = combat.health_bar(newMonster["CurrentHp"],
                                     newMonster["MaxHp"])
    embed, buttons = intMsg.showRPGEncounter(user, player, newMonster, avatar,
                                             playerHpBar, monsterHpBar,
                                             monsterLvl)

    self.encounters[str(id)]['player'] = player
    self.encounters[str(id)]['newMonster'] = newMonster
    self.encounters[str(id)]['playerHpBar'] = playerHpBar
    self.encounters[str(id)]['monsterHpBar'] = monsterHpBar
    self.encounters[str(id)]['monsterLvl'] = monsterLvl

    async def callback(interaction: nextcord.Interaction):
      if id != interaction.user.id:
        await interaction.response.send_message(
          f"{interaction.user.mention} you can't interact with somebody else's encounter b-baka!"
        )
        return
      custom_id = interaction.data['custom_id']
      for button_item in buttons:
        if button_item.custom_id == custom_id:
          player = self.encounters[str(interaction.user.id)]['player']
          newMonster = self.encounters[str(interaction.user.id)]['newMonster']
          playerHpBar = self.encounters[str(
            interaction.user.id)]['playerHpBar']
          monsterHpBar = self.encounters[str(
            interaction.user.id)]['monsterHpBar']
          playerDmg = self.encounters[str(interaction.user.id)]['playerDmg']
          monsterDmg = self.encounters[str(interaction.user.id)]['monsterDmg']
          monsterLvl = self.encounters[str(interaction.user.id)]['monsterLvl']

          player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, gameOver, loser, winner = combat.simpleEncounter(
            player, newMonster, button_item.label, monsterLvl)


          msgContent = intMsg.encounterOutcome(player['name'],
                                               button_item.label, playerDmg,
                                               newMonster['name'],
                                               monsterAtkName, monsterDmg,
                                               gameOver, loser, winner)

          embed, new_buttons = intMsg.showRPGEncounter(user, player,
                                                       newMonster, avatar,
                                                       playerHpBar,
                                                       monsterHpBar,
                                                       monsterLvl)

          if gameOver:
            del self.encounters[str(id)]
            await interaction.response.edit_message(content=msgContent,
                                                    embed=embed,
                                                    view=None)
            if player['CurrentHp'] <= 0:
              player['CurrentHp'] = player['MaxHp']
            else:
              startLvl = player['lvl']
              player['lvl'], player['exp'] = calc.levelUp(
                player['lvl'], newMonster['exp'], player['exp'])
              if startLvl < player['lvl']:
                clss = classCont.getClassByName(player['class'])
                player['MaxHp'] = calc.calc_hp(clss['hp'], player['lvl'])
                player['CurrentHp'] = player['MaxHp']
                player['atk'] = calc.calc_stat(clss['atk'], player['lvl'])
                player['defense'] = calc.calc_stat(clss['defense'],
                                                   player['lvl'])
                player['speed'] = calc.calc_stat(clss['speed'], player['lvl'])

            playerCont.updateSinglePlayerInfo(player, id)

            return
          self.encounters[str(interaction.user.id)]['player'] = player
          self.encounters[str(interaction.user.id)]['newMonster'] = newMonster
          self.encounters[str(
            interaction.user.id)]['playerHpBar'] = playerHpBar
          self.encounters[str(
            interaction.user.id)]['monsterHpBar'] = monsterHpBar
          self.encounters[str(interaction.user.id)]['playerDmg'] = playerDmg
          self.encounters[str(interaction.user.id)]['monsterDmg'] = monsterDmg
          self.encounters[str(interaction.user.id)]['monsterLvl'] = monsterLvl
          await interaction.response.edit_message(content=msgContent,
                                                  embed=embed)
          break

    view = View()
    for button_item in buttons:
      view.add_item(button_item)
      button_item.callback = callback

    message = await ctx.send(embed=embed, view=view)

  @commands.command()
  async def lmao(self, ctx):
    attacks = attacksCont.getAllAttacksByTypeAndLevel("Fire", 0)


def setup(client):
  client.add_cog(RPGCommands(client))
