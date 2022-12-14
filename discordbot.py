# here be dragons!

import config
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from functionsReq import *
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# help
@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help", url="https://letmegooglethat.com/?q=help",
        description="This is a bot that can respond to your prompts using OpenAI API",
        color=0x9440b6 )
    embed.add_field(name="/completion", value="Text completion\n**prompt** = question that will be passed to AI\n**token** = number of characters that will be returned, (min 6, max 4000), (1 token = 4 characters)\n**temp** = temperature of the response, AKA creativity of the bot (min 0, max 1)",
                    inline=False)
    embed.add_field(name="/img", value="Image generation\n**prompt** = text used to generate the image\n**size** = size of the image in pixels, 256 or 512 or 1024",
                    inline=False)
    embed.add_field(name="help", value="Show this message",
                    inline=False)
    embed.set_footer(text=randomFooter())

    await interaction.response.send_message(embed=embed)


# ping
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")


# completion
@bot.tree.command(name="completion")
@app_commands.describe(prompt = "Prompt to pass to AI")
@app_commands.describe(token = "Number of token in the response (more token = longer answer) (max 3900, min 3)")
@app_commands.describe(temp = "Temperature of the response (max 1, min 0)")
async def completion(interaction: discord.Interaction, prompt: str, token: int, temp: float):
    try:
        await interaction.response.defer()
        payload = formatPayload(prompt, temp, token)
        header = formatHeader()
        answer = sendIT(payload, header)
        answerFinal = formatAnswer(answer)
        # await interaction.response.send_message(f"Prompt: {prompt}/n Response: {answerFinal}")
        await interaction.followup.send(f"Prompt: {prompt}\nResponse: {answerFinal}")
    except Exception as exception:
        print(exception)

# img
@bot.tree.command(name="img")
@app_commands.describe(prompt = "Prompt to pass to AI")
@app_commands.describe(size = "Size of generated image, 256/512/1024")
async def img(interaction: discord.Interaction, prompt: str, size: int):
    try:
        await interaction.response.defer()
        payload = formatImgPayload(prompt, size)
        header = formatHeader()
        answer = sendITImg(payload, header)
        answerFinal = formatImg(answer)
        # await interaction.response.send_message(f"Prompt: {prompt}/n Response: {answerFinal}")
        await interaction.followup.send(f"Prompt: {prompt}\nResponse: [link]({answerFinal})")
    except Exception as exception:
        print(exception)



bot.run(config.TOKEN)
