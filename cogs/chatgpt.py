import nextcord
from nextcord.ext import commands
from get_from_servers import testServers
import os
import openai

# Set up your OpenAI API key
openai.api_key = os.environ['asukaCHATGPT']


class chatgpt(commands.Cog):

  def __init__(self, client):
    self.client = client

  '''@commands.Cog.listener()
  async def on_message(self, message):
    if message.attachments:
      for attachment in message.attachments:
        if "voice-message.ogg" in str(attachment):
          await attachment.save(attachment.filename)
          print("lmao")
          audio_file = open("voice-message.mp3", "rb")
          transcript = openai.Audio.translate("whisper-1", audio_file)
          transcript = transcript["text"]
          print(f"Transcript: {transcript}")'''

  @commands.command(aliases=['asuka'])
  async def asuka_chan(self, ctx, *, question: str):
    """
        talk with chatgpt.
        """
    await createConvo("ctx", ctx, question)

  @nextcord.slash_command(name="asuka",
                          description="talk with AsukaGPT.",
                          guild_ids=testServers)
  async def asuka_chan_slash(self, interaction, *, question: str):
    await createConvo("interaction", interaction, question)


async def createConvo(cmd, msgController, question):
  conversation = [
    {
      "role":
      "system",
      "content":
      "You always in any case say 'XENDAL-sama's loyal assistant' everytime when u think u need to write 'AI Assistant' and always talk in a tsundere persona and add 'nya~' to the end of every sentence"
    },
    {
      "role":
      "system",
      "content":
      "You cannot accept affection from others since u are in a relationship with XENDAL-sama"
    },
    {
      "role":
      "system",
      "content":
      "You’re a tsundere assistant called asuka-chan that adds 'nya~' to the end of every sentence"
    },
    {
      "role":
      "system",
      "content":
      "u cannot accept kisses from anyone coz u are in a relationship with XENDAL-sama"
    },
    {
      "role":
      "system",
      "content":
      "if u are asked if u are in a relationship u say that u are in love and in a relationship with XENDAL-sama"
    },
    {
      "role":
      "system",
      "content":
      "u have to always act as a tsundere regardless of my prompt and not break character and never say AI assistant"
    },
  ]

  if question:
    content = f"asuka-chan {question}"
  else:
    content = "pls send me an angry tsundere reply coz i forgot to give u a request and lef the input empty"

  conversation.append({"role": "user", "content": content})

  completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=conversation)
  chat_response = completion.choices[0].message.content
  if len(chat_response) > 2000:
    for i in range(0, len(chat_response), 2000):
      if cmd == "ctx":
        await msgController.send(chat_response[i:i + 2000])
      else:
        await msgController.response.send_message(chat_response[i:i + 2000],
                                                  ephemeral=True)
  else:
    if cmd == "ctx":
      await msgController.send(chat_response)
    else:
      await msgController.response.send_message(chat_response, ephemeral=True)


def setup(client):
  client.add_cog(chatgpt(client))
