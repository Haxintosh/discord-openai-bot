
# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from discord import app_commands
from functionsReq import *
TOKEN = open('bot.txt', 'r')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping")
async def completion(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

@bot.tree.command(name="completion")
@app_commands.describe(prompt = "Prompt to pass to AI")
@app_commands.describe(token = "Number of token in the response (more token = longer answer) (max 3900, min 3)")
@app_commands.describe(temp = "Temperature of the response (max 1, min 0)")
async def completion(interaction: discord.Interaction, prompt: str, token: int, temp: float):
    try:
        await interaction.response.defer()
        payload = formatPayload(prompt, temp, token)
        header = formatHeader("key.txt")
        answer = sendIT(payload, header)
        answerFinal = formatAnswer(answer)
        # await interaction.response.send_message(f"Prompt: {prompt}/n Response: {answerFinal}")
        await interaction.followup.send(f"Prompt: {prompt}\nResponse: {answerFinal}")
    except Exception as exception:
        print(exception)
bot.run(TOKEN.read())
