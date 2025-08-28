import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bearertokendobby = os.getenv('bearertokendobby')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Ready!')

@bot.command(name="book")
async def summarize_book(ctx, *, book_title: str):
    prompt = f"""
      You are a helpful literature guide. 
        For the book "{book_title}", provide:
        1. A raw, 2–3 sentence summary of the plot in your own words. 
        2. 2–3 main themes or ideas with common word
        3. A blunt note on why this book matters. 
        Make it witty, fun, and conversational.
   """

    payload = {
      "model": "accounts/sentientfoundation-serverless/models/dobby-mini-unhinged-plus-llama-3-1-8b",
      "max_tokens": 1085,
      "top_p": 1,
      "top_k": 40,
      "presence_penalty": 0,
      "frequency_penalty": 0,
      "temperature": 0.6,
      "messages": [  {
                    "role": "user",
                    "content": prompt
                }]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearertokendobby}"
    }

    response = requests.post("https://api.fireworks.ai/inference/v1/chat/completions", 
                             headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        answer = data.get('choices', [{}])[0].get('message', {}).get('content', '❌ No response from AI')
        await ctx.reply(f"📖 **{book_title}**\n{answer}")
    else:
        await ctx.reply(f"⚠️ Error {response.status_code}: {response.text}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
