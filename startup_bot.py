import os
import sys
import discord
from datetime import datetime
import json

def load_json(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def get_base_path():
    if getattr(sys, 'frozen', False): #Running as an EXE
        return os.path.dirname(sys.executable)
    else: #Running as a .py script
        return os.path.dirname(os.path.abspath(__file__))

base_path = get_base_path()
bot_token_path = os.path.join(base_path, "bot_token.json")
token = load_json(bot_token_path)
BOT_TOKEN = token["bot_token"]


intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_presence_update(before, after):
    params = load_json(os.path.join(base_path, "params.json"))
    user_ids = params["discord_user_ids"]
    your_user_id = params["your_discord_user_id"]
    game_name = params["game_name"]

    if user_ids is None or after.id not in user_ids:
        return

    print(f'before: {before}. {before.activity}')
    print(f'after: {after}. {after.activity}')
    print("---------------------------------------")

    if after.activity is None or after.activity.details != game_name:
        return

    if before is None or before.activity.details == game_name:
        return

    user = await client.fetch_user(your_user_id)
    if not user:
        return

    current_time = datetime.now().strftime("%H:%M")
    await user.send(f"🔔 {after.name} started playing {game_name}! ({current_time})")

client.run(BOT_TOKEN)
