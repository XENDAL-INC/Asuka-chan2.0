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
import messagesJsonController as msgCont


class RPGCommands(commands.Cog):

  def __init__(self, client):
    self.client = client
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

    embedCt = 0

    try:
      response = await self.client.wait_for('message', check=check, timeout=30)
      msg = msgCont.getMessageByName("welcome")
      embed = intMsg.createChar(user, avatar,
                                f'Hi {str(response.content)}! {msg}')
      embedMessage = await ctx.send(embed=embed)
      asuka = embedMessage.author
      await embedMessage.add_reaction("▶️")

      name = str(response.content)
    except asyncio.TimeoutError:
      await ctx.send('You took too long to respond.')
      return

    class_name = "Fire"

    def checkReaction(reaction, user):
      global userReact
      if reaction.message == embedMessage and user.id == id:
        if user == asuka:
          userReact = ctx.author
        else:
          userReact = user
          return True

    try:
      #reaction.emoji == "▶️"
      emoji = "▶️"
      emojiConfirm = "✅"
      while await self.client.wait_for('reaction_add',
                                       check=checkReaction,
                                       timeout=60):

        embedCt += 1
        await embedMessage.remove_reaction(emoji, userReact)
        if embedCt == 1:
          fireEmbed = intMsg.classChoice(
            user, avatar, "Fire",
            f'Fire: {classCont.getAttributeFromClass("Fire", "description")}')
          await embedMessage.edit(embed=fireEmbed)
          await embedMessage.add_reaction("✅")

        elif embedCt == 2:
          thunderEmbed = intMsg.classChoice(
            user, avatar, "Thunder",
            f'Thunder: {classCont.getAttributeFromClass("Thunder", "description")}'
          )
          await embedMessage.edit(embed=thunderEmbed)
        elif embedCt == 3:
          iceEmbed = intMsg.classChoice(
            user, avatar, "Ice",
            f'Ice: {classCont.getAttributeFromClass("Ice", "description")}')
          await embedMessage.edit(embed=iceEmbed)
        elif embedCt == 4:
          windEmbed = intMsg.classChoice(
            user, avatar, "Wind",
            f'Thunder: {classCont.getAttributeFromClass("Wind", "description")}'
          )
          await embedMessage.edit(embed=windEmbed)
        elif embedCt == 5:
          darkEmbed = intMsg.classChoice(
            user, avatar, "Dark",
            f'Dark: {classCont.getAttributeFromClass("Dark", "description")}')
          await embedMessage.edit(embed=darkEmbed)
        else:
          embedCt = 0
          await embedMessage.edit(embed=embed)
          await embedMessage.remove_reaction(emojiConfirm, asuka)

    except asyncio.TimeoutError:
      await embedMessage.remove_reaction(emoji, asuka)
      return

    try:
      response = await self.client.wait_for('message', check=check, timeout=30)
      #await ctx.send('hi')
      if str(response.content) in ["Fire", "Ice", "Thunder", "Wind", "Dark"]:
        class_name = str(response.content)
      else:
        await ctx.send(
          'You gave an invalid response, pls try (Fire, Ice, Thunder, Wind or Dark)'
        )
        return
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

          player, newMonster, playerHpBar, monsterHpBar, playerDmg, monsterDmg, monsterAtkName, gameOver, loser, winner, statusInflict, statusDmg = combat.simpleEncounter(
            player, newMonster, button_item.label, monsterLvl)

          msgContent = intMsg.encounterOutcome(player['name'],
                                               button_item.label, playerDmg,
                                               newMonster['name'],
                                               monsterAtkName, monsterDmg,
                                               gameOver, loser, winner,
                                               statusInflict, statusDmg)

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
