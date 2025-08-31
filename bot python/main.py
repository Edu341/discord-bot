import discord
from discord.ext import commands, tasks
from discord import ui, app_commands
import asyncio
import json
import datetime
import random
import re
import os
import aiohttp
import time
import sqlite3
from collections import defaultdict

# ========== UNIQUE SERVERS DATABASE ========== #
UNIQUE_SERVERS = [
    # Original list (56 servers)
    "https://discord.gg/5GE4xm9Hmx", "https://discord.gg/Fwa5nWzxjg", "https://discord.gg/teQaTUku",
    "https://discord.gg/Yskg8vcqMj", "https://discord.gg/NMEQ23khCg", "https://discord.gg/tUuzHdnVA4",
    "https://discord.gg/cAGNSQeEfq", "https://discord.gg/6uABQ2yV", "https://discord.gg/27VQkXEN",
    "https://discord.gg/obsidiann", "https://discord.gg/uSfXDAUrGE", "https://discord.com/invite/zR3mRuCCQN",
    "https://discord.gg/GQQ5Cng2", "https://discord.gg/bpatjRJsVs", "https://discord.gg/ohanami",
    "https://discord.gg/4AYSy7daNM", "https://discord.gg/vGKPfmg9X7", "https://discord.gg/RG3uyRCWaX",
    "https://discord.gg/fBmwdXWPJ9", "https://discord.gg/KvYE4fRR", "https://discord.gg/rUzfTFCzHG",
    "https://discord.gg/GhnrFYYqeB", "https://discord.gg/yTgNgtNCMR", "https://discord.gg/TMAYnwbWqb",
    "https://discord.gg/YadhG8n4AV", "https://discord.gg/FuVxGTdda3", "https://discord.gg/5ztTPry24E",
    "https://discord.gg/CuM4YFfDYg", "https://discord.gg/x2kdXFzFhj", "https://discord.gg/5D7cSaK5Px",
    "https://discord.gg/nYMNPudd9A", "https://discord.gg/58va9vm3zr", "https://discord.gg/2wk83whd",
    "https://discord.gg/oceanhub", "https://discord.gg/Xt6KgVX63q", "https://discord.gg/CMEMKw7jqq",
    "https://discord.gg/krnckFfN", "https://discord.gg/fCa5NaDWG7", "https://discord.gg/P3cZfhPuHq",
    "https://discord.gg/aXjgJe55xY", "https://discord.gg/kzMdy5ZF9A", "https://discord.gg/4Gp52nqMcy",
    "https://discord.gg/7B4p7fTB7Q", "https://discord.gg/b9Cq2gKxQT", "https://discord.gg/sS3GsxDy",
    "https://discord.gg/RxvwPC9Qq5", "https://discord.gg/aX4rfuedBM", "https://discord.gg/dT7uutYGEA",
    "https://discord.gg/zgXJ3G3Gzy", "https://discord.gg/zc7qDZHKCc", "https://discord.gg/eKBYsXxCVp",
    "https://discord.gg/hUPEzfAuG6", "https://discord.gg/ptkpEbmARZ", "https://discord.gg/h39saMKNuj",
    "https://discord.gg/k5buUP32Zp", "https://discord.gg/rPYmzNEKvG", "https://discord.gg/Pkj7SQxdkH",
    "https://discord.gg/volpix-mc", "https://discord.gg/haizen",
    # New servers added (144)
    "https://discord.gg/EEpk7apcbc", "https://discord.gg/6z4RSnJAw6", "https://discord.gg/UFabhM9YKY",
    "https://discord.gg/9Jms2JuZ5Q", "https://discord.gg/ZJSkMAmjn2", "https://discord.gg/zR85tqF67k",
    "https://discord.gg/hmv5MDdJAs", "https://discord.gg/heartlessitalia", "https://discord.gg/ZckmMgxs6Y",
    "https://discord.gg/fRApqDaMUQ", "https://discord.gg/7xKjGG4uy8", "https://discord.gg/Dxjwx9Epz7",
    "https://discord.gg/xb8XY3UFbV", "https://discord.gg/cristalmc", "https://discord.gg/Mhh2JRzX9G",
    "https://discord.gg/dY5Z5KKcyW", "https://discord.gg/DPEC89jXeX", "https://discord.gg/4NXMev3SQ5",
    "https://discord.gg/kEbWpu4dWK", "https://discord.gg/R7p7RUuDE9", "https://discord.gg/hPnFBdu9cn",
    "https://discord.gg/DYsA2srphN", "https://discord.gg/47GMzShCwC", "https://discord.gg/smuVfcUW8M",
    "https://discord.gg/GJkdu67acg", "https://discord.gg/g2bSvGzV5t", "https://discord.gg/APmuJMBh5E",
    "https://discord.gg/R7p7RUuDE9", "https://discord.gg/hPnFBdu9cn", "https://discord.gg/dT7uutYGEA",
    "https://discord.gg/qfpdmvFPrj", "https://discord.gg/U4qWQySGeg", "https://discord.gg/VHgpp3BRce",
    "https://discord.gg/XyzjZWh5AD", "https://discord.gg/k5ZQx4n3tQ", "https://discord.gg/AbJD8cuq95",
    "https://discord.gg/7J8SjQmTpg", "https://discord.gg/fyzkDBU5Df", "https://discord.gg/zgXJ3G3Gzy",
    "https://discord.com/invite/Sjs9qHVTTZ", "https://discord.gg/QzahpnwqJf", "https://discord.gg/RZmjCfymZ5",
    "https://discord.gg/ZVRCf2eu5Z", "https://discord.gg/jqKdZQjR7w", "https://discord.gg/GxYPUdZty5",
    "https://discord.gg/c33nv97dqs", "https://discord.gg/sNDE3txEkY", "https://discord.gg/uYyG74yu",
    "https://discord.gg/EYJa7CNvtN", "https://discord.gg/vjxcVmTKuz", "https://discord.gg/MXX3BDJ3xz",
    "https://discord.gg/hBYgrSg8K8", "https://discord.gg/UXsVTADnkX", "https://discord.gg/NMEQ23khCg",
    "https://discord.gg/WEeKz8yG5H", "https://discord.gg/HBNMVF86uR", "https://discord.gg/Fsj5muUMB5",
    "https://discord.gg/FzycNCq8Up", "https://discord.gg/ECkPjsGeG9", "https://discord.gg/3sx5jSQ587",
    "https://discord.gg/reccenteritaliano-767657914563035138", "https://discord.com/invite/zR3mRuCCQN", "https://discord.gg/CXsNJSgp",
    "https://discord.gg/vGKPfmg9X7", "https://discord.gg/d9dqX6zWy3", "https://discord.gg/5ztTPry24E",
    "https://discord.gg/CuM4YFfDYg", "https://discord.gg/PbVr5q5v", "https://discord.gg/6gQmWHWqa6",
    "https://discord.gg/P4ANqw28Tv", "https://discord.gg/qesBrM2JHJ", "https://discord.gg/PH5e93eRX5",
    "https://discord.gg/Y66UzmFwSV", "https://discord.gg/bpatjRJsVs", "https://discord.gg/3SnFkBfBGx",
    "https://discord.gg/xqmVa5AnEq", "https://discord.gg/xgtBNjdvQy", "https://discord.gg/FuVxGTdda3",
    "https://discord.gg/ccitaly2", "https://discord.gg/QE4jNsMapN", "https://discord.gg/REQmFgNRFT",
    "https://discord.gg/8F3AwXPeUd", "https://discord.gg/cy8veqvm66", "https://discord.gg/kgXPPMNDuc",
    "https://discord.gg/pvgCDQFKTv", "https://discord.gg/feamXExTbD", "https://discord.gg/SgDkkPvjMR",
    "https://discord.gg/zCn5xhCAJa", "https://discord.gg/jhySqrRPMW", "https://discord.gg/mAJvU4EtHp",
    "https://discord.gg/pKsNQw6Zt9", "https://discord.gg/24wPYNFPk4", "https://discord.gg/JGXqMcbBhq",
    "https://discord.gg/RG3uyRCWaX", "https://discord.gg/mvwZTCvCv6", "https://discord.gg/7FPFHaPwsV",
    "https://discord.gg/K9dXnMPBra", "https://discord.gg/oei", "https://discord.gg/xivtag",
    "https://discord.gg/EuUQBV2kB9", "https://discord.com/invite/zR3mRuCCQN", "https://discord.gg/underworld-818910678197862432",
    "https://discord.gg/romarp", "https://discord.gg/YDJQGa2hwU", "https://discord.gg/sNDE3txEkY", "https://discord.gg/MXX3BDJ3xz",
    "https://discord.gg/WEeKz8yG5H", "https://discord.gg/Fsj5muUMB5", "https://discord.gg/hpxDhzPWkF",
    "https://discord.gg/55vYFBwQRU", "https://discord.gg/UQGrMkZEUa", "https://discord.gg/8WXGkDrgf2",
    "https://discord.gg/JfDUgATMZA", "https://discord.gg/6beEA67u27", "https://discord.gg/HjtxwPFVM5",
    "https://discord.gg/Dgd8CZC3XC", "https://discord.gg/X8kTfvTQa4", "https://discord.gg/tAWtvAsqPp", "https://discord.gg/dksh3QbzDd",
    "https://discord.gg/sharmrps", "https://discord.com/invite/qkssTRsmm9", "https://discord.gg/SsmNAv44Xx", "https://discord.gg/bmw3Zpdr5P",
    "https://discord.gg/KEzP4PkjWj", "https://discord.gg/tAexWvycGk", "https://discord.gg/xwGrUJzFTG", "https://discord.com/invite/qh9YxpYQVx"
]

AUTHORIZED_ROLE_ID = None  # Will be set with /random-role-set

class ServerView(discord.ui.View):
    def __init__(self, invite_link: str):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Join Server",
            url=invite_link,
            style=discord.ButtonStyle.link,
            emoji="ðŸŽ¯"
        ))
   
# ========== TICKET CONFIGURATION ========== #
config = {
    "SUPPORT_ROLE_ID": int(os.getenv("SUPPORT_ROLE_ID", "1394357096295956580")),
    "LOG_CHANNEL_ID": int(os.getenv("LOG_CHANNEL_ID", "1408439077577031812")),
    "TICKET_CATEGORY_ID": int(os.getenv("TICKET_CATEGORY_ID", "1392745407582437448")),
    "STAFF_ROLE_ID": int(os.getenv("STAFF_APPLICATION_ROLE_ID", "1392091644299575417"))
}

REDDIT_API = os.getenv('zOOe_Usq-GG5_1NGm1v2mg', '')
IMGFLIP_USER = os.getenv('Edu8', '')
IMGFLIP_PASS = os.getenv('SjQrHZLA!!nf7b7', '')
STEAM_API = os.getenv('5BAD35621E851927AE6157D1E7AC8E95', '')
SPOTIFY_CLIENT_ID = os.getenv('bc1422e1ff4e41f9ab588bd6576a708d', '')
SPOTIFY_CLIENT_SECRET = os.getenv('98ceacb5e2c546928f435ed0889292cd', '')

try:
    import nacl
except ImportError:
    nacl = None

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

log_channel_id = 1392745544941703269
welcome_channel_id = 1392109096857239664
verification_role_id = None
gallery_channel_id = 1392062907528904748
confession_channel_id = 139206291025953179

warnings = defaultdict(list)
birthdays = {}
story_parts = []
muted_members = {}

queues = {}
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

bot.start_time = datetime.datetime.now(datetime.timezone.utc)

@bot.event
async def on_ready():
    print(f"âœ… Bot online as {bot.user.name} | {len(UNIQUE_SERVERS)} servers available")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="Edu's Community - @antoilking10"
    ))
    load_data()
    try:
        await bot.tree.sync()
        print("âœ… Commands synchronized!")
    except Exception as e:
        print(f"âŒ Error synchronizing commands: {e}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(welcome_channel_id)
    if channel:
        embed = discord.Embed(
            title="ðŸ‘‹ Welcome!",
            description=f"Hello {member.mention}, welcome to **Edu's Community**!\nIntroduce yourself and have fun with us!\n\n-# We remind you to read the Rules",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await channel.send(embed=embed)

def save_data():
    data = {
        'warnings': dict(warnings),
        'birthdays': birthdays,
        'muted_members': muted_members
    }
    with open('bot_data.json', 'w') as f:
        json.dump(data, f)

def load_data():
    global warnings, birthdays, muted_members
    try:
        with open('bot_data.json', 'r') as f:
            data = json.load(f)
            warnings.update(data.get('warnings', {}))
            birthdays.update(data.get('birthdays', {}))
            muted_members.update(data.get('muted_members', {}))
    except FileNotFoundError:
        pass

# ========== RANDOM SERVER COMMAND ========== #
@bot.tree.command(name="random-role-set", description="[ADMIN ONLY] Set the role for /random-server")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def set_role(interaction: discord.Interaction, role: discord.Role):
    global AUTHORIZED_ROLE_ID
    AUTHORIZED_ROLE_ID = role.id
    await interaction.response.send_message(
        f"âœ… Authorized role set: {role.mention}",
        ephemeral=True
    )

@bot.tree.command(name="random-server", description="Show a random partner server")
@app_commands.checks.cooldown(1, 2)
async def random_server(interaction: discord.Interaction):
    if AUTHORIZED_ROLE_ID is None:
        await interaction.response.send_message(
            "âŒ Use /random-role-set first to set an authorized role",
            ephemeral=True
        )
        return

    if not any(role.id == AUTHORIZED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message(
            "âŒ You don't have the required role for this command!",
            ephemeral=True
        )
        return

    invite = random.choice(UNIQUE_SERVERS)
    embed = discord.Embed(
        title="ðŸ” Random Partner Server",
        description="Here is a server from our network:",
        color=0x5865F2
    )
    embed.add_field(name="Invite", value=f"[Click here to join]({invite})", inline=False)
    embed.set_footer(text=f"Total servers: {len(UNIQUE_SERVERS)}")
    await interaction.response.send_message(embed=embed, view=ServerView(invite), ephemeral=True)

@set_role.error
async def role_set_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "âŒ Only ADMINS can use this command!",
            ephemeral=True
        )

# ========== PARTNERSHIP COMMAND === #
# ID of the channel to send partnerships to
PARTNER_CHANNEL_ID = 1411451850485403830
# ID of the authorized role
AUTHORIZED_ROLE_ID = 1392745984387452978

class PartnershipModal(discord.ui.Modal, title="Partnership Form"):
    description_input = discord.ui.TextInput(
        label="Server description",
        style=discord.TextStyle.paragraph,
        placeholder="Write the description of the other server here",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Get the channel to send the partnership to
        channel = bot.get_channel(PARTNER_CHANNEL_ID)
        if channel is None:
            await interaction.response.send_message("Error: channel not found.", ephemeral=True)
            return

        # Name of the user who used the command
        handler = interaction.user.name
        # Name of the server (guild) manager
        manager = interaction.guild.name if interaction.guild else "Unknown server"

        # Formatted message
        message_content = (
            f"{self.description_input.value}\n\n"
            f"**---**\n"
            f"Handler: {handler}\n"
            f"Manager: {manager}\n"
            f"**---**"
        )

        # Send the message without mentioning everyone or here
        await channel.send(message_content, allowed_mentions=discord.AllowedMentions.none())

        # Response to the user (ephemeral)
        await interaction.response.send_message("Partnership sent successfully!", ephemeral=True)

@bot.tree.command(name="partnership", description="Send a partnership")
async def partnership(interaction: discord.Interaction):
    # Check if the user has the required role
    role_ids = [role.id for role in interaction.user.roles] if isinstance(interaction.user, discord.Member) else []
    if AUTHORIZED_ROLE_ID not in role_ids:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )
        return

    # Show the modal if authorized
    modal = PartnershipModal()
    await interaction.response.send_modal(modal)

# ========== PING COMMAND ========== #
def get_uptime():
    delta = datetime.datetime.now(datetime.timezone.utc) - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m"

async def get_db_ping():
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return round((time.time() - start_time) * 1000, 2)
    except Exception:
        return None

@bot.tree.command(name="ping", description="Show latency statistics")
async def ping_slash(interaction: discord.Interaction):
    try:
        ws_latency = round(bot.latency * 1000, 2)
        api_start = time.time()
        await interaction.response.defer(ephemeral=True)
        api_ping = round((time.time() - api_start) * 1000, 2)
        db_ping = await get_db_ping()
        uptime = get_uptime()
        status = "ðŸŸ¢ Excellent" if ws_latency < 100 else "ðŸŸ¡ Medium" if ws_latency < 300 else "ðŸ”´ Critical"
        embed = discord.Embed(
            title="ðŸ“Š Connection Statistics",
            color=0x2b2d31,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.add_field(
            name="ðŸ›œ Latency",
            value=f"The Bot's **Latency** is `{status}` (`{ws_latency}ms`)",
            inline=False
        )
        embed.add_field(name="â³ Uptime", value=f"`{uptime}`", inline=True)
        embed.add_field(name="ðŸŒ API", value=f"`{api_ping}ms`", inline=True)
        embed.add_field(name="ðŸª™ Database", value=f"`{db_ping}ms`" if db_ping else "`N/A`", inline=True)
        embed.add_field(
            name="ðŸ‘€ Node",
            value=f"`Node1.SparkedHost.Germany.eu`" if interaction.guild else "`DM`",
            inline=True
        )
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        print(f"Error in /ping: {e}")
        await interaction.followup.send("âŒ An error occurred while executing the command.", ephemeral=True)

# ========== TICKET SYSTEM ========== #
async def staff_check(interaction: discord.Interaction) -> bool:
    if not any(role.id == config["STAFF_ROLE_ID"] for role in interaction.user.roles):
        await interaction.response.send_message(
            "âŒ **Permission denied**\nOnly Staff can use this command!",
            ephemeral=True
        )
        return False
    return True

@bot.tree.command(name="ticket-panel", description="Create a ticket panel (Staff Only)")
@app_commands.check(staff_check)
async def ticket_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="**EDU'S COMMUNITY TICKETS**",
        description=(
            "**Click on the most relevant category for your Ticket**\n\n"
            "**NOTE**: *Troll tickets will be closed and sanctioned.*\n\n"
            "**TICKET RULES**\n\n"
            "- Write in the Ticket immediately after opening it.\n\n"
            "- Respect the Staff and do not waste their time.\n\n"
            "- Please do not tag the Staff.\n\n"
            "- If you want to report a Bug or a Player, send all relevant evidence.\n\n"
            "- Inactive Tickets will be closed after 3 hours."
        ),
        color=0x2b2d31
    )

    select = ui.Select(
        custom_id="ticket-type",
        placeholder="Choose the most suitable category for your Ticket...",
        options=[
            discord.SelectOption(label="General Support", description="Request general assistance", value="support"),
            discord.SelectOption(label="Bug & Player Report", description="Report an issue or a player", value="bug"),
            discord.SelectOption(label="Staff Application", description="Apply to become Staff", value="staff"),
            discord.SelectOption(label="Other", description="Something related to other categories", value="other")
        ]
    )

    view = ui.View()
    view.add_item(select)
    
    await interaction.response.send_message("âœ… Panel created!", ephemeral=True, delete_after=2)
    await interaction.followup.send(embed=embed, view=view)

async def handle_ticket_creation(interaction: discord.Interaction):
    ticket_type = interaction.data["values"][0]
    user = interaction.user

    if ticket_type == "staff":
        if not any(role.id == config["STAFF_ROLE_ID"] for role in user.roles):
            await interaction.response.send_message(
                "âŒ You do not have permission to access the Staff Application!",
                ephemeral=True
            )
            return

    ticket_name = {
        "support": f"ðŸŒâ–¾supportà¼{user.name}",
        "bug": f"âš”ï¸â–¾reportà¼{user.name}",
        "staff": f"ðŸ‘‘â–¾staff-moduleà¼{user.name}",
        "other": f"â­â–¾otherà¼{user.name}"
    }.get(ticket_type, f"ticket-{ticket_type}")[:95]

    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        interaction.guild.get_role(config["SUPPORT_ROLE_ID"]): discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    if ticket_type == "staff":
        overwrites[interaction.guild.get_role(config["STAFF_ROLE_ID"])] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    try:
        ticket_channel = await interaction.guild.create_text_channel(
            name=ticket_name,
            category=interaction.guild.get_channel(config["TICKET_CATEGORY_ID"]),
            overwrites=overwrites
        )

        if ticket_type == "staff":
            staff_embed = discord.Embed(
                title="ðŸ‘‘**STAFF APPLICATION**",
                description=(
                    f"ðŸ‘¤ Welcome to the Staff Application {user.mention}\n"
                    "ðŸ“‹ You will be asked some application questions\n\n"
                    "â— **NOTE**: *Please answer honestly and in detail*"
                ),
                color=0xffa500
            )

            view = ui.View()
            view.add_item(ui.Button(label="ðŸ”§ Manage", custom_id="manage-ticket", style=discord.ButtonStyle.secondary))
            view.add_item(ui.Button(label="âŒ Close", custom_id="close-ticket", style=discord.ButtonStyle.danger))

            await ticket_channel.send(
                content=f"ðŸ‘‘ <@&{config['STAFF_ROLE_ID']}> new staff application!",
                embed=staff_embed,
                view=view
            )

            questions_embed = discord.Embed(
                title="ðŸ“‹ **STAFF QUESTIONNAIRE**",
                description=(
                    "**Answer the following questions:**\n\n"
                    "**1.** What is your name?\n**Answer:**\n\n"
                    "**2.** How old are you?\n**Answer:**\n\n"
                    "**3.** Why do you want to become Staff?\n**Answer:**\n\n"
                    "**4.** Do you want to be Staff only on Discord or also on Minecraft?\n**Answer:**\n\n"
                    "**5.** If two Staff members were arguing, what would you do?\n**Answer:**\n\n"
                    "**6.** Do you know the Rules?\n**Answer:**\n\n"
                    "**7.** For how long would you punish a person for insults or flaming?\n**Answer:**\n\n"
                    "*Based on your answers, you will be asked more questions*"
                ),
                color=0x00ff00
            )
            await ticket_channel.send(embed=questions_embed)

        else:
            embed = discord.Embed(
                title="ðŸ“–**TICKET INFO**",
                description=(
                    f"ðŸ‘¤ Welcome to the Ticket system {user.mention}\n"
                    "â˜‘ï¸ We remind you to read this short note carefully\n\n"
                    "â— **NOTE**: *We remind you not to tag Staff and to send everything in the dedicated channel*"
                ),
                color=0x2b2d31
                )

            view = ui.View()
            view.add_item(ui.Button(label="ðŸ”§ Manage", custom_id="manage-ticket", style=discord.ButtonStyle.secondary))
            view.add_item(ui.Button(label="âŒ Close", custom_id="close-ticket", style=discord.ButtonStyle.danger))

            await ticket_channel.send(
                content=f"ðŸ› ï¸ <@&{config['SUPPORT_ROLE_ID']}> a ticket has just been opened!",
                embed=embed,
                view=view
            )

        await interaction.response.send_message(
            f"âœ… Ticket created: {ticket_channel.mention}",
            ephemeral=True
        )

    except Exception as e:
        print(f"âŒ Error creating ticket: {e}")
        await interaction.response.send_message(
            "âŒ Error creating the ticket! Please try again later.",
            ephemeral=True
        )

async def handle_ticket_buttons(interaction: discord.Interaction):
    custom_id = interaction.data.get("custom_id")
    
    if custom_id == "manage-ticket":
        if not any(role.id == config["SUPPORT_ROLE_ID"] for role in interaction.user.roles):
            await interaction.response.send_message(
                "âŒ Only Staff can manage tickets!", 
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        
        try:
            channel_name = interaction.channel.name
            username_match = channel_name.split("à¼")[-1] if "à¼" in channel_name else None
            ticket_creator = discord.utils.get(interaction.guild.members, name=username_match) if username_match else None
            
            if not ticket_creator:
                return await interaction.followup.send(
                    "âŒ Could not find the ticket creator!",
                    ephemeral=True
                )

            await interaction.channel.edit(overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ticket_creator: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.guild.get_role(config["SUPPORT_ROLE_ID"]): discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=False
                )
            })

            async for msg in interaction.channel.history(limit=10):
                if msg.embeds and "TICKET INFO" in msg.embeds[0].title:
                    new_view = ui.View()
                    new_view.add_item(ui.Button(
                        label="âŒ Close",
                        custom_id="close-ticket",
                        style=discord.ButtonStyle.danger
                    ))
                    await msg.edit(view=new_view)
                    break

            manage_embed = discord.Embed(
                title="ðŸ”§ Ticket Under Management",
                description=(
                    f"{interaction.user.mention} is now managing this ticket.\n\n"
                    f"Only {interaction.user.mention} and {ticket_creator.mention} "
                    "can write in this channel."
                ),
                color=0xffa500
            )
            await interaction.channel.send(embed=manage_embed)
            
            await interaction.followup.send(
                "âœ… You have taken control of the ticket!",
                ephemeral=True
            )

        except Exception as e:
            print(f"âŒ Error managing ticket: {e}")
            await interaction.followup.send(
                "âŒ Error managing the ticket!",
                ephemeral=True
            )

    elif custom_id == "close-ticket":
        await interaction.response.defer(ephemeral=True)
        
        try:
            transcript_content = f"Transcript of: {interaction.channel.name}\n"
            transcript_content += f"Closed on: {datetime.datetime.now(datetime.timezone.utc)}\n"
            transcript_content += f"Closed by: {interaction.user}\n\n"
            transcript_content += "="*50 + "\n"
            
            async for msg in interaction.channel.history(limit=200, oldest_first=True):
                transcript_content += f"{msg.created_at} - {msg.author}: {msg.content}\n"
                if msg.attachments:
                    transcript_content += f"Attachments: {', '.join([a.url for a in msg.attachments])}\n"
                transcript_content += "-"*50 + "\n"
            
            filename = f"transcript_{interaction.channel.id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript_content)

            log_channel = interaction.guild.get_channel(config["LOG_CHANNEL_ID"])
            if log_channel:
                log_embed = discord.Embed(
                    title="ðŸŽŸï¸ Ticket Closed",
                    description=f"**Closed by**: {interaction.user.mention}",
                    color=0xff0000
                )
                
                log_embed.add_field(
                    name="ðŸ“„ Transcript",
                    value="`See attached file`",
                    inline=False
                )
                
                log_embed.add_field(
                    name="ðŸ”– Channel",
                    value=f"#{interaction.channel.name}",
                    inline=True
                )
                
                log_embed.add_field(
                    name="â±ï¸ Closed on",
                    value=discord.utils.format_dt(discord.utils.utcnow(), style="f"),
                    inline=True
                )

                await log_channel.send(
                    embed=log_embed,
                    file=discord.File(filename)
                )

            await interaction.followup.send("âœ… Ticket closed with transcript!", ephemeral=True)
            await interaction.channel.delete()

        except Exception as e:
            print(f"âŒ Error closing ticket: {e}")
            await interaction.followup.send(
                "âŒ Error closing the ticket!",
                ephemeral=True
            )

# ========== LISTENER FOR TICKET INTERACTIONS ==========

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data.get("custom_id") == "ticket-type":
            await handle_ticket_creation(interaction)
        elif interaction.data.get("custom_id") in ["manage-ticket", "close-ticket"]:
            await handle_ticket_buttons(interaction)

# ========== FUNCTIONS FOR MEMES ==========

async def get_reddit_meme():
    headers = {'User-Agent': 'EduDiscordBot/1.0'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/memes/top.json?limit=50', headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = data['data']['children']
                    images = [p['data'] for p in posts if p['data'].get('post_hint') == 'image']
                    if images:
                        post = random.choice(images)
                        return {
                            'title': post['title'],
                            'url': post['url'],
                            'permalink': f"https://reddit.com{post['permalink']}",
                            'upvotes': post['ups']
                        }
    except Exception as e:
        print(f"Error fetching Reddit meme: {e}")
    return None

async def get_imgflip_meme():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.imgflip.com/get_memes') as response:
                if response.status == 200:
                    data = await response.json()
                    memes = data['data']['memes']
                    meme = random.choice(memes)
                    return {
                        'title': meme['name'],
                        'url': meme['url'],
                        'upvotes': meme.get('box_count', 0)
                    }
    except Exception as e:
        print(f"Error fetching Imgflip meme: {e}")
    return None

async def get_random_meme():
    meme = await get_reddit_meme()
    if meme:
        return meme
    meme = await get_imgflip_meme()
    if meme:
        return meme
    local_memes = [
        {"title": "ðŸ˜‚ Funny Meme", "url": "https://i.imgur.com/8WjJY9J.jpg"},
        {"title": "ðŸŽ® Gaming Meme", "url": "https://i.imgur.com/3JZ3Q3X.jpg"},
        {"title": "ðŸ’» Programmer Meme", "url": "https://i.imgur.com/5ZQ2W9J.jpg"},
        {"title": "ðŸ± Cat Meme", "url": "https://i.imgur.com/7XZ3Q3X.jpg"},
        {"title": "ðŸŽ­ Drama Meme", "url": "https://i.imgur.com/9YJ3Q3X.jpg"}
    ]
    return random.choice(local_memes)

# ========== ALIAS SYSTEM FOR COMMANDS (! AND /) ==========
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
    if message.content.startswith('/'):
        modified_content = '!' + message.content[1:]
        ctx = await bot.get_context(message)
        ctx.message.content = modified_content
        await bot.invoke(ctx)

# ========== SLASH COMMANDS ==========
@bot.tree.command(name="help", description="Show all available commands")
async def help_slash(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ðŸŽ® Bot Commands - Edu's Community",
        description="Here are all the available commands:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="ðŸ›¡ï¸ MODERATION (Staff Only)",
        value="â€¢ `/ban @user [reason]` - Ban a user\n"
              "â€¢ `/kick @user [reason]` - Kick a user\n"
              "â€¢ `/mute @user [duration]` - Mute a user\n"
              "â€¢ `/warn @user [reason]` - Give a warning\n"
              "â€¢ `/warnings [@user]` - View warnings",
        inline=False
    )
    embed.add_field(
        name="â„¹ï¸ UTILITY",
        value="â€¢ `/info` - Info about the server\n"
              "â€¢ `/userinfo [@user]` - Info about a user\n"
              "â€¢ `/poll [question]` - Create a poll\n"
              "â€¢ `/birthday [DD/MM]` - Register birthday\n"
              "â€¢ `/help` - This message",
        inline=False
    )
    embed.add_field(
        name="ðŸŽµ MUSIC (YouTube Links Only)",
        value="â€¢ `/play [youtube-url]` - Play music\n"
              "â€¢ `/stop` - Stop the music\n"
              "â€¢ `/skip` - Skip the song\n"
              "â€¢ `/pause` - Pause playback\n"
              "â€¢ `/resume` - Resume playback\n"
              "â€¢ `/queue` - Show the queue",
        inline=False
    )
    embed.add_field(
        name="ðŸŽ‰ FUN",
        value="â€¢ `/joke` - A joke\n"
              "â€¢ `/meme` - A random meme\n"
              "â€¢ `/joker` - A Joker quote\n"
              "â€¢ `/8ball [question]` - Magic 8-ball\n"
              "â€¢ `/rps [rock/paper/scissors]` - Rock paper scissors",
        inline=False
    )
    embed.set_footer(text="Use ! or / before each command!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="ban", description="Ban a user from the server")
async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("âŒ Only administrators can use this command.", ephemeral=True)
        return
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"âœ… {member.mention} has been banned.\nReason: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"âŒ Error during ban: {str(e)}")

@bot.tree.command(name="kick", description="Kick a user from the server")
async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("âŒ Only administrators can use this command.", ephemeral=True)
        return
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"âœ… {member.mention} has been kicked.\nReason: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"âŒ Error during kick: {str(e)}")

@bot.tree.command(name="mute", description="Mute a user for a certain time (in minutes)")
async def mute_slash(interaction: discord.Interaction, member: discord.Member, duration: int = 10):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("âŒ Only administrators can use this command.", ephemeral=True)
        return
    try:
        mute_role = discord.utils.get(interaction.guild.roles, id=verification_role_id)
        if mute_role:
            await member.add_roles(mute_role)
            muted_members[str(member.id)] = (datetime.datetime.now().isoformat(), duration)
            save_data()
            await interaction.response.send_message(f"ðŸ”‡ {member.mention} has been muted for {duration} minutes.")
            await asyncio.sleep(duration * 60)
            await member.remove_roles(mute_role)
            muted_members.pop(str(member.id), None)
            save_data()
        else:
            await interaction.response.send_message("âŒ Mute role not found.")
    except Exception as e:
        await interaction.response.send_message(f"âŒ Error during mute: {str(e)}")

@bot.tree.command(name="warn", description="Give a warning to a user")
async def warn_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("âŒ Only administrators can use this command.", ephemeral=True)
        return
    try:
        warnings[str(member.id)].append(reason)
        save_data()
        await interaction.response.send_message(f"âš ï¸ {member.mention} has received a warning.\nReason: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"âŒ Error during warn: {str(e)}")

@bot.tree.command(name="warnings", description="View a user's warnings")
async def warnings_slash(interaction: discord.Interaction, member: discord.Member = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("âŒ Only administrators can use this command.", ephemeral=True)
        return
    member = member or interaction.user
    user_warnings = warnings.get(str(member.id), [])
    if user_warnings:
        embed = discord.Embed(
            title=f"âš ï¸ Warnings for {member.display_name}",
            description="\n".join([f"{i+1}. {w}" for i, w in enumerate(user_warnings)]),
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"{member.mention} has no warnings.")

@bot.tree.command(name="meme", description="Show a random meme from Reddit or other sites")
async def meme_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    meme_data = await get_random_meme()
    embed = discord.Embed(title=meme_data['title'], color=discord.Color.gold())
    embed.set_image(url=meme_data['url'])
    if 'upvotes' in meme_data:
        embed.set_footer(text=f"ðŸ‘ {meme_data['upvotes']} upvotes â€¢ r/memes")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="joker", description="A Joker quote")
async def joker_slash(interaction: discord.Interaction):
    joker_quotes = [
        "Why so serious?",
        "I believe whatever doesn't kill you simply makes you... stranger.",
        "Madness is like gravity. All it takes is a little push.",
        "I'm not a monster. I'm just ahead of the curve.",
        "If you're good at something, never do it for free.",
        "Introduce a little anarchy. Upset the established order, and everything becomes chaos.",
        "This town deserves a better class of criminal.",
        "I think you and I are destined to do this forever."
    ]
    embed = discord.Embed(title="ðŸƒ The Joker", description=f"*{random.choice(joker_quotes)}*", color=discord.Color.purple())
    embed.set_thumbnail(url="https://i.imgur.com/9YJ3Q3X.jpg")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="play", description="Play music from YouTube (URL only)")
async def play_slash(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    if not nacl:
        await interaction.followup.send("âŒ PyNaCl is not installed! Install with `pip install pynacl` to use music.")
        return
    if not interaction.user.voice:
        await interaction.followup.send("âŒ You must be in a voice channel!")
        return
    if not url.startswith(('https://www.youtube.com/', 'https://youtube.com/', 'https://youtu.be/')):
        await interaction.followup.send("âŒ Please enter a valid YouTube URL!")
        return
    voice_channel = interaction.user.voice.channel
    try:
        voice_client = interaction.guild.voice_client
        if not voice_client:
            voice_client = await voice_channel.connect()
        if voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
        if interaction.guild.id not in queues:
            queues[interaction.guild.id] = []
        queues[interaction.guild.id].append(url)
        if not voice_client.is_playing():
            await play_next(interaction.guild, voice_client, interaction)
        else:
            await interaction.followup.send(f"ðŸŽµ Added to queue: {url}")
    except Exception as e:
        await interaction.followup.send(f"âŒ Error: {str(e)}")

@bot.tree.command(name="stop", description="Stop music playback")
async def stop_slash(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        if interaction.guild.id in queues:
            queues[interaction.guild.id] = []
        await interaction.response.send_message("â¹ï¸ Music stopped")
    else:
        await interaction.response.send_message("âŒ I'm not playing anything")

@bot.tree.command(name="skip", description="Skip the current song")
async def skip_slash(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("â­ï¸ Song skipped")
    else:
        await interaction.response.send_message("âŒ I'm not playing anything")

@bot.tree.command(name="pause", description="Pause playback")
async def pause_slash(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("â¸ï¸ Music paused")
    else:
        await interaction.response.send_message("âŒ I'm not playing anything")

@bot.tree.command(name="resume", description="Resume playback")
async def resume_slash(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("â–¶ï¸ Playback resumed")
    else:
        await interaction.response.send_message("âŒ The music is not paused")

@bot.tree.command(name="queue", description="Show the song queue")
async def queue_slash(interaction: discord.Interaction):
    if interaction.guild.id in queues and queues[interaction.guild.id]:
        queue_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(queues[interaction.guild.id][:10])])
        embed = discord.Embed(title="ðŸŽµ Playback Queue", description=queue_list, color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("ðŸ“­ The queue is empty")

async def play_next(guild, voice_client, interaction=None):
    if guild.id in queues and queues[guild.id]:
        try:
            url = queues[guild.id].pop(0)
            voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
            if interaction:
                embed = discord.Embed(title="ðŸŽµ Now Playing", description=url, color=discord.Color.green())
                embed.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/linecons-free-vector-icons-pack/32/music-512.png")
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Playback error: {e}")
            if interaction:
                await interaction.followup.send(f"âŒ Error during playback: {str(e)}")
            await play_next(guild, voice_client)
    else:
        await asyncio.sleep(60)
        if voice_client and not voice_client.is_playing():
            await voice_client.disconnect()

@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question")
async def eightball_slash(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes â€“ definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    embed = discord.Embed(
        title="ðŸŽ± The Magic 8-Ball",
        color=discord.Color.dark_blue(),
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name="â“ Question", value=question, inline=False)
    embed.add_field(name="ðŸŽ± Answer", value=random.choice(responses), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rps", description="Rock, paper, or scissors against the bot")
async def rps_slash(interaction: discord.Interaction, choice: str):
    choice = choice.lower()
    options = ["rock", "paper", "scissors"]
    if choice not in options:
        await interaction.response.send_message("Choose between: rock, paper, scissors")
        return
    bot_choice = random.choice(options)
    result = ""
    if choice == bot_choice:
        result = "It's a tie!"
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "You win!"
    else:
        result = "You lose!"
    embed = discord.Embed(
        title="ðŸª¨ Rock Paper Scissors",
        description=f"You: **{choice}**\nBot: **{bot_choice}**\n\n**{result}**",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="joke", description="Get a random joke")
async def joke_slash(interaction: discord.Interaction):
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "What does a programmer order at a bar? A Java!",
        "Why did the chicken cross the road? To get to the other side.",
        "What's the worst thing for a computer scientist? Having connection problems in love.",
        "What do you call a cat that programs? A c++-purr!"
    ]
    embed = discord.Embed(
        title="ðŸ˜‚ Joke",
        description=random.choice(jokes),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.command()
async def eightball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes â€“ definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    embed = discord.Embed(
        title="ðŸŽ± The Magic 8-Ball",
        color=discord.Color.dark_blue(),
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name="â“ Question", value=question, inline=False)
    embed.add_field(name="ðŸŽ± Answer", value=random.choice(responses), inline=False)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    TOKEN = os.getenv('ED1_TOKEN')
    if not TOKEN:
        print("Error: Bot token not found.")
        print("Make sure to set the ED1_TOKEN environment variable")
        exit(1)
    bot.run(TOKEN)
