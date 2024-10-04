import nextcord
from nextcord.ext import commands
import get_from_servers as asukaDB
import os
import openai

# Set up your OpenAI API key
openai.api_key = os.environ['asukaCHATGPT']


class chatgpt(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['asuka'])
  async def asuka_chan(self, ctx, *, question: str):
    """
        talk with chatgpt.
        """
    author = ctx.author
    persona = "asuka"
    await createConvo("ctx", ctx, author, persona, question)

  @nextcord.slash_command(name="asuka",
                          description="talk with AsukaGPT.",
                          guild_ids=asukaDB.testServers)
  async def asuka_chan_slash(self, interaction, *, question: str):
    author = interaction.user
    persona = "asuka"
    await createConvo("interaction", interaction, author, persona, question)

  ###########################################################################
  ###########################################################################

  @commands.command(aliases=['elysia'])
  async def elysia_chan(self, ctx, *, question: str):
    """
        Talk with Elysia.
        """
    author = ctx.author
    persona = "elysia"
    await createConvo("ctx", ctx, author, persona, question)

  @nextcord.slash_command(name="elysia",
                          description="talk with Elysia.",
                          guild_ids=asukaDB.testServers)
  async def ellie_slash(self, interaction, *, question: str):
    author = interaction.user
    persona = "elysia"
    await createConvo("interaction", interaction, author, persona, question)

  ###########################################################################
  ###########################################################################

  @commands.command()
  async def hutao(self, ctx, *, question: str):
    """
        Talk with Hu Tao.
        """
    author = ctx.author
    persona = "hutao"
    await createConvo("ctx", ctx, author, persona, question)

  @nextcord.slash_command(name="hutao",
                          description="talk with Hutao.",
                          guild_ids=asukaDB.testServers)
  async def hutao_slash(self, interaction, *, question: str):
    author = interaction.user
    persona = "hutao"
    await createConvo("interaction", interaction, author, persona, question)


async def createConvo(cmd, msgController, author, persona, question):
  conversation = asukaDB.get_convo(persona)
  conversation.append({"role": "user", "content": question})

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
