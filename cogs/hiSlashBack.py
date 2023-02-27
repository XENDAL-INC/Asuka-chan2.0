import nextcord
from nextcord import Interaction

serverTest=[720672074070360064, 826068702017486868, 812977201598955522, 675483399519076399]

@nextcord.slash_command(name="hi", description="Say hi to Asuka-chan!", guild_ids=serverTest)
async def testmain(self, interaction: Interaction):
  global honorifics
  honorifics=" Sempai"
  author=interaction.user

  if author.id==380016239310929931:
    honorifics="-Sama"
  
  if author.id==319617215391465472:
    await interaction.response.send_message("**HENTAI! LOLICON!**")
  elif author.id==265181840288120833:
    await interaction.response.send_message("**SHUT THE FUCK UP MONKEY**")
  else:
    await interaction.response.send_message("Ohayo" + author.mention + honorifics + " :heart:")

