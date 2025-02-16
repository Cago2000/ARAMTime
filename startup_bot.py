import discord
from datetime import datetime
import json

with open("params.json", "r") as params_json:
    params = json.load(params_json)

YOUR_USER_ID = params["your_discord_user_id"]
USER_IDS = params["discord_user_ids"]
BOT_TOKEN = params["bot_token"]
GAME_NAME = params["game_name"]

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_presence_update(before, after):

    if USER_IDS is None or len(USER_IDS) == 0:
        return
    if after.id in USER_IDS:
        if after.activity is None:
            return
        if after.activity.details == GAME_NAME and before.activity.details != GAME_NAME and after.activity.session_id is not None:
            print(before, before.activity)
            print(after, after.activity)
            user = await client.fetch_user(YOUR_USER_ID)
            if user is None:
                return
            print(f'{after.name} is now playing {after.activity.name}!')
            current_time = datetime.now().strftime("%H:%M")
            await user.send(f"🔔 {after.name} started playing {GAME_NAME}! ({current_time})")

client.run(BOT_TOKEN)
