import discord
from discord.ext import commands
import datetime
import os
import asyncio
import threading
from flask import Flask

# Initialize bot with minimal intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Flask app for web service
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Bot is running!"

@app.route('/status')
def status():
    if bot.is_ready():
        return {"status": "online", "bot_name": bot.user.name if bot.user else "Unknown"}
    return {"status": "offline"}

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Event when bot is ready
@bot.event
async def on_ready():
    print("Bot launched and ready!")
    if bot.user:
        print(f"Logged in as {bot.user.name}")
        print(f"Bot ID: {bot.user.id}")
    else:
        print("Bot user not available")

# COMMANDS
@bot.command()
async def embed(ctx):
    embedmsg = discord.Embed(
        title="Skibdid yea",
        description="hell naw",
        color=discord.Color.random()
    )
    embedmsg.set_thumbnail(url=ctx.author.avatar.url)
    bot_name = bot.user.name if bot.user else "Bot"
    embedmsg.add_field(
        name=f"{bot_name}'s Ping:",
        value=f"{round(bot.latency * 1000)}ms",
        inline=False
    )
    embedmsg.set_footer(text="fake", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embedmsg)

@bot.command()
async def read(ctx):
    await ctx.send(f"{ctx.author.mention} read here: https://www.wikihow.com/Teach-Yourself-to-Read")

@bot.command()
async def timestamps(ctx):
    now = int(datetime.datetime.now().timestamp())
    await ctx.send(f"Current time is: {now}")

@bot.command()
async def dateonly(ctx):
    date = datetime.datetime.utcnow().date()
    await ctx.send(f"Today's date: `{date}`")

@bot.command()
async def time(ctx):
    now = datetime.datetime.utcnow()
    timestamp = int(now.timestamp())
    await ctx.send(f"Current time: <t:{timestamp}:F>")

# Run the bot
if __name__ == "__main__":
    # Check for Discord token in environment variables (multiple possible names)
    token = (os.getenv("DISCORD_TOKEN") or 
             os.getenv("DISCORD_BOT") or 
             os.getenv("DISCORD_BOT_TOKEN") or
             os.getenv("BOT_TOKEN"))
    
    if not token:
        print("Error: No Discord bot token found!")
        print("Available environment variables:")
        for key, value in os.environ.items():
            if 'DISCORD' in key.upper() or 'BOT' in key.upper() or 'TOKEN' in key.upper():
                print(f"  {key}: {'***' if value else 'None'}")
        print("Please set one of: DISCORD_TOKEN, DISCORD_BOT, DISCORD_BOT_TOKEN, or BOT_TOKEN")
        exit(1)
    
    print(f"Found token with length: {len(token)}")
    
    # Start Flask web server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print("Web server started on port 5000")
    
    try:
        # Run the Discord bot
        print("Starting Discord bot...")
        bot.run(token)
    except discord.LoginFailure:
        print("Error: Invalid Discord bot token!")
        print("Please check your token in the Discord Developer Portal")
        exit(1)
    except Exception as e:
        print(f"Error starting bot: {e}")
        exit(1)
