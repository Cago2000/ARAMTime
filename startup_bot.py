import os
import sys
import discord
from datetime import datetime
import json

def load_json(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

if getattr(sys, 'frozen', False):  # Running as an EXE
    base_path = os.path.dirname(sys.executable)
else:  # Running as a .py script
    base_path = os.path.dirname(os.path.abspath(__file__))
bot_token_path = os.path.join(base_path, "bot_token.json")
print(bot_token_path)
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
    if user_ids is None or len(user_ids) == 0:
        return
    if after.id in user_ids:
        if after.activity is None:
            return
        game_match = True if before.activity is None else before.activity.details == game_name
        if after.activity.details == game_name and game_match and after.activity.session_id is not None:
            print(before, before.activity)
            print(after, after.activity)
            user = await client.fetch_user(your_user_id)
            if user is None:
                return
            print(f'{after.name} is now playing {after.activity.name}!')
            current_time = datetime.now().strftime("%H:%M")
            await user.send(f"🔔 {after.name} started playing {game_name}! ({current_time})")

client.run(BOT_TOKEN)
