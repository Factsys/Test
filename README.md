import discord
from discord.ext import commands
import datetime
import os
import asyncio

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Event when bot is ready
@bot.event
async def on_ready():
    print("Bot launched and ready!")


# COMMANDS

@bot.command()
async def embed(ctx):
    embedmsg = discord.Embed(
        title="Skibdid yea",
        description="hell naw",
        color=discord.Color.random()
    )
    embedmsg.set_thumbnail(url=ctx.author.avatar.url)
    embedmsg.add_field(
        name=f"{bot.user.name}'s Ping:",
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


# Run the bot using the environment variable from Render
if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT")
    if not token:
        raise RuntimeError("DISCORD_BOT environment variable not set")

    asyncio.run(bot.start(token))
