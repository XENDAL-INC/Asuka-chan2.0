import discord
from discord.ext import commands
import json

class levelsystem(commands.Cog):
  def _init_(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    inVC=False
    for roles in member.guild.roles:
      if roles.name=="inVC":
        inVC=True
        role=roles
        break

    if inVC:
      if not member.voice:
        await member.remove_roles(role)
      else:
        await member.add_roles(role)
  
  @commands.Cog.listener()
  async def on_message(self, message):
    with open('db/users.json', 'r') as f:
      users = json.load(f)
    
    await update_data(users, message.author, 5, message.channel)

    with open('db/users.json', 'w') as f:
      json.dump(users,f)

async def update_data(users, user, exp, channel):
  try:
    t = users[str(user.id)]
    users[str(user.id)]['experience'] += 5

    #lvlup
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
      await channel.send("GG, " + user.mention + " has leveled up to level " + str(lvl_end) + "!")
      users[str(user.id)]['level'] = lvl_end
  except:
    try:
      t = users[str(user.id)]
    except:
      if not user.bot:
        users[user.id]= {}
        users[user.id]['experience']= 0
        users[user.id]['level'] = 0
    

def setup(bot):
  bot.add_cog(levelsystem(bot))