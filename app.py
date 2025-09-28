import discord
import aiohttp
import asyncio
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = 'token'
CHANNEL_ID = id  # Replace with your channel ID

# Custom animated emojis (ensure your bot is in the server where these exist)
ONLINE_EMOJI = "<a:online:854428384171655208>"
OFFLINE_EMOJI = "<a:offline:854428383232786492>"

SERVICES = {
    "General 📡": {
        "Main Website": "https://neonhost.shop",
        "User Panel": "https://panel.neonhost.shop/"
    },
    "☁-Web": {
        "Panel Web": "http://163.5.143.4/",
        "Node WEB-1": "http://163.5.143.4/"
    },
    "🖥-VPS": {
        "Panel VPS": "http://163.5.159.84/",
        "Node VPS-1": "http://163.5.159.84/"
    },
    "🎮-Game Servers": {
        "Game Panel": "https://dashboard.neonhost.shop/",
        "Game Node 01": "https://dashboard.neonhost.shop/"
    },
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def ping_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            start = asyncio.get_event_loop().time()
            async with session.get(url, timeout=5) as resp:
                await resp.text()
            end = asyncio.get_event_loop().time()
            latency = round((end - start) * 1000)
            return ONLINE_EMOJI, latency
    except Exception:
        return OFFLINE_EMOJI, 0

async def build_embed():
    embed = discord.Embed(
        title="🌐 Service Status Monitor",
        color=discord.Color(0x9b59b6)  # Your custom color here
    )
    for category, services in SERVICES.items():
        status_lines = []
        for name, url in services.items():
            emoji, latency = await ping_url(url)
            status_lines.append(f"{name}: {emoji} ({latency}ms)")
        embed.add_field(name=category, value="\n".join(status_lines), inline=False)

    now = datetime.now(tz=ZoneInfo("Europe/Athens"))
    local_time = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    embed.set_footer(text=f"Last updated: {local_time}")

    return embed

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    embed = await build_embed()
    message = await channel.send(embed=embed)

    while True:
        await asyncio.sleep(60)
        updated_embed = await build_embed()
        await message.edit(embed=updated_embed)

bot.run(TOKEN)
