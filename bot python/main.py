import asyncio
import threading
import requests
import time

# Funzione keep-alive per Render
def run_keep_alive():
    while True:
        try:
            requests.get("https://ecbot-i4ny.onrender.com")
            time.sleep(240)  # 4 minuti (meno di 5)
        except Exception as e:
            print(f"Keep-alive error: {e}")
            time.sleep(240)

# Avvia keep-alive in thread separato
keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
keep_alive_thread.start()

# ID dei ruoli da assegnare in base al numero di warn
WARN_ROLE_IDS = {
    1: 1403679881333706823,  # 1 warn
    2: 1403679930885345310, # 2 warn
    3: 1403679970886291497  # 3 warn
}
import discord
from discord.ext import commands
from discord import app_commands, ui
import os
import asyncio
from gtts import gTTS
import yt_dlp
from collections import defaultdict
import random
import time
import sqlite3
import platform
from datetime import datetime, timedelta
from dotenv import load_dotenv
import hashlib
import requests
from flask import Flask
import threading
import time
import requests
import os

# --- FUN & SOCIAL COMMANDS ---
@app_commands.command(name="meme", description="Send a random meme from Reddit")
async def meme(interaction: discord.Interaction):
    r = requests.get("https://meme-api.com/gimme")
    data = r.json()
    embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color)
    embed.set_image(url=data['url'])
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="joke", description="Random joke")
async def joke(interaction: discord.Interaction):
    r = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
    data = r.json()
    if data['type'] == 'single':
        text = data['joke']
    else:
        text = f"{data['setup']}\n{data['delivery']}"
    embed = discord.Embed(title="Joke", description=text, color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="8ball", description="Magic 8ball answers your questions")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    responses = ["Yes", "No", "Maybe", "Ask later", "Absolutely yes", "Absolutely not", "Cannot answer now"]
    embed = discord.Embed(title="🎱 8ball", description=f"Question: {question}\nAnswer: {random.choice(responses)}", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="gif", description="Search for a gif")
@app_commands.describe(query="Keyword for the gif")
async def gif(interaction: discord.Interaction, query: str):
    api_key = "dc6zaTOxFJmzC"  # Giphy public beta key
    r = requests.get(f"https://api.giphy.com/v1/gifs/search?q={query}&api_key={api_key}&limit=1")
    data = r.json()
    if data['data']:
        url = data['data'][0]['images']['original']['url']
        embed = discord.Embed(title=f"Gif: {query}", color=discord.Color.orange())
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No gif found.")

@app_commands.command(name="quiz", description="Simple quiz")
async def quiz(interaction: discord.Interaction):
    questions = [
        ("What is the capital of Italy?", "Rome"),
        ("2+2?", "4"),
        ("Color of the sky?", "blue")
    ]
    q, a = random.choice(questions)
    await interaction.response.send_message(f"Question: {q}")
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.lower() == a.lower():
            await interaction.channel.send("Correct answer!")
        else:
            await interaction.channel.send(f"Wrong answer! It was: {a}")
    except:
        await interaction.channel.send("Time's up!")

@app_commands.command(name="rps", description="Rock paper scissors against the bot")
@app_commands.describe(choice="Rock, paper or scissors")
async def rps(interaction: discord.Interaction, choice: str):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)
    if choice == bot_choice:
        result = "Draw!"
    elif (choice == "rock" and bot_choice == "scissors") or (choice == "paper" and bot_choice == "rock") or (choice == "scissors" and bot_choice == "paper"):
        result = "You win!"
    else:
        result = "You lose!"
    await interaction.response.send_message(f"You: {choice}\nBot: {bot_choice}\n{result}")

@app_commands.command(name="trivia", description="Random trivia question")
async def trivia(interaction: discord.Interaction):
    r = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
    data = r.json()['results'][0]
    question = data['question']
    correct = data['correct_answer']
    options = data['incorrect_answers'] + [correct]
    random.shuffle(options)
    embed = discord.Embed(title="Trivia", description=question, color=discord.Color.magenta())
    for i, opt in enumerate(options):
        embed.add_field(name=f"Option {i+1}", value=opt, inline=False)
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="ship", description="Ship two users")
@app_commands.describe(user1="First user", user2="Second user")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    percent = random.randint(0, 100)
    embed = discord.Embed(title="💖 Ship", description=f"{user1.mention} + {user2.mention} = {percent}% compatibility!", color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="gallery", description="Show the photo gallery from the dedicated channel")
async def gallery(interaction: discord.Interaction):
    channel_id = 1234567890123456997  # Replace with gallery channel ID
    channel = interaction.guild.get_channel(channel_id)
    if channel:
        photos = []
        async for msg in channel.history(limit=50):
            for att in msg.attachments:
                if att.content_type and att.content_type.startswith("image"):
                    photos.append(att.url)
        if photos:
            embed = discord.Embed(title="Gallery", color=discord.Color.gold())
            for url in photos[:5]:
                embed.set_image(url=url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No photos found.")
    else:
        await interaction.response.send_message("Gallery channel not found.")

@app_commands.command(name="shoutout", description="Send a nice message to a member")
@app_commands.describe(user="User to thank", message="Message")
async def shoutout(interaction: discord.Interaction, user: discord.Member, message: str):
    embed = discord.Embed(title="Shoutout!", description=f"{user.mention}: {message}", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

# --- MODERATION & UTILITY COMMANDS ---
LOG_CHANNEL_ID = 1408439077577031812  # Replace with your log channel ID
WARNINGS = {}

@app_commands.command(name="ban", description="Ban a user from the server")
@app_commands.describe(user="User to ban", reason="Reason for ban")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(title="User banned", description=f"{user.mention} has been banned.\nReason: {reason}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Ban error: {e}", ephemeral=True)

@app_commands.command(name="kick", description="Kick a user from the server")
@app_commands.describe(user="User to kick", reason="Reason for kick")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(title="User kicked", description=f"{user.mention} has been kicked.\nReason: {reason}", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Kick error: {e}", ephemeral=True)

@app_commands.command(name="mute", description="Mute a user for a specific time (minutes)")
@app_commands.describe(user="User to mute", duration="Mute duration in minutes")
async def mute(interaction: discord.Interaction, user: discord.Member, duration: int = 5):
    try:
        timeout_until = datetime.utcnow() + timedelta(minutes=duration)
        await user.edit(timeout=timeout_until, reason="Mute command")
        embed = discord.Embed(title="User muted", description=f"{user.mention} has been muted for {duration} minutes.", color=discord.Color.dark_grey())
        await interaction.response.send_message(embed=embed)
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Mute error: {e}", ephemeral=True)

@app_commands.command(name="warn", description="Warn a user (warning counter)")
@app_commands.describe(user="User to warn", reason="Reason for warning")
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    WARNINGS.setdefault(user.id, 0)
    WARNINGS[user.id] += 1
    warn_count = WARNINGS[user.id]
    embed = discord.Embed(title="Warning", description=f"{user.mention} has received a warning.\nReason: {reason}\nTotal warnings: {warn_count}", color=discord.Color.yellow())
    # Assegna il ruolo in base al numero di warn
    role_id = WARN_ROLE_IDS.get(warn_count)
    if role_id:
        warn_role = interaction.guild.get_role(role_id)
        if warn_role and warn_role not in user.roles:
            try:
                await user.add_roles(warn_role, reason=f"Warned {warn_count} times by bot")
            except Exception as e:
                await interaction.response.send_message(f"Warning given, but failed to assign role: {e}", ephemeral=True)
    await interaction.response.send_message(embed=embed)
    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)

@app_commands.command(name="info", description="Show server info")
async def info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"Server info: {guild.name}", color=discord.Color.blue())
    embed.add_field(name="Members", value=str(guild.member_count))
    embed.add_field(name="Created on", value=guild.created_at.strftime('%d/%m/%Y'))
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "N/A")
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="userinfo", description="Show info about a user")
@app_commands.describe(user="User to show")
async def userinfo(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"User info: {user.display_name}", color=discord.Color.green())
    embed.add_field(name="ID", value=str(user.id))
    embed.add_field(name="Roles", value=", ".join([r.name for r in user.roles if r.name != "@everyone"]))
    embed.add_field(name="Joined on", value=user.joined_at.strftime('%d/%m/%Y') if user.joined_at else "N/A")
    embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="poll", description="Create a poll with reactions")
@app_commands.describe(question="Poll question")
async def poll(interaction: discord.Interaction, question: str):
    embed = discord.Embed(title="Poll", description=question, color=discord.Color.purple())
    msg = await interaction.channel.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await interaction.response.send_message("Poll created!", ephemeral=True)

@app_commands.command(name="translate", description="Translate text to a language")
@app_commands.describe(text="Text to translate", lang="Target language (ex: en, it, fr)")
async def translate(interaction: discord.Interaction, text: str, lang: str):
    try:
        r = requests.post("https://libretranslate.de/translate", data={"q": text, "source": "auto", "target": lang})
        result = r.json()
        translated = result.get("translatedText", "Translation error")
        embed = discord.Embed(title="Translation", description=translated, color=discord.Color.teal())
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Translation error: {e}", ephemeral=True)

# --- BOT DEFINITION & COMMAND REGISTRATION ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print('TOKEN:', TOKEN)
if not TOKEN or TOKEN.strip() == '' or TOKEN == 'None':
    print('[ERRORE] Il token Discord non è stato trovato. Controlla il file .env e la variabile DISCORD_TOKEN.')
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Register all slash commands after bot is defined
bot.tree.add_command(meme)
bot.tree.add_command(joke)
bot.tree.add_command(eightball)
bot.tree.add_command(gif)
bot.tree.add_command(quiz)
bot.tree.add_command(rps)
bot.tree.add_command(trivia)
bot.tree.add_command(ship)
bot.tree.add_command(gallery)
bot.tree.add_command(shoutout)
bot.tree.add_command(ban)
bot.tree.add_command(kick)
bot.tree.add_command(mute)
bot.tree.add_command(warn)
bot.tree.add_command(info)
bot.tree.add_command(userinfo)
bot.tree.add_command(poll)
bot.tree.add_command(translate)

# Invite tracking
invite_tracker = defaultdict(int)
invite_cache = {}

# Define roles based on invite counts (example: adjust role names as needed)
INVITE_ROLES = {
    1: 1392731553221578843,    # 1 invito
    3: 1392731553624363058,    # 3 inviti
    5: 1392731554362425445,    # 5 inviti
    10: 1392731555188969613,   # 10 inviti
    50: 1392731615632818286,   # 50 inviti
    100: 1392731616060772424   # 100+ inviti
}

TRANSCRIPT_CHANNEL_ID = 123456789012345680  # Inserisci qui l'ID del canale transcript
SUPPORT_ROLE_ID = 1392746082588557383  # Ruolo support aggiornato
PARTNERSHIP_CHANNEL_ID = 1408163064326656060  # ID aggiornato del canale partnership
ANTIRAID_LOG_CHANNEL_ID = 1408439077577031812  # ID aggiornato del canale log antiraid/antinuke
ANTINUKE_LOG_CHANNEL_ID = 1408439077577031812  # ID aggiornato del canale log antinuke (usa lo stesso di antiraid o specifica uno diverso)

# Variabili globali per automod, antinuke, antiraid

NUKE_THRESHOLD = 3
RAID_LINK_THRESHOLD = 5
RAID_LINK_WORDS = ['discord.gg/', 'spamlink.com']
nuke_actions = {}
raid_links = {}
spam_tracker = {}
BLACKLISTED_WORDS = [
    'diocane', 'dio cane', 'porco dio', 'discord.gg/', 'troia', 'negra'  # aggiungi qui le parole da bloccare
]
BLACKLIST_MUTE_DURATION = 60  # secondi (1min), puoi mettere 300 per 5min
IGNORED_CATEGORY_ID = 1234567890123456998  # Sostituisci con l'ID della categoria da ignorare
SPAM_MSG_THRESHOLD = 3  # Numero di messaggi per considerare spam
SPAM_TIME_WINDOW = 60   # Secondi (1 minuto)

# Whitelist utenti/bot che possono bypassare automod/antispam
WHITELISTED_USER_IDS = set()

antinuke_enabled = True
antiraid_enabled = False
join_times = {}

class TicketView(discord.ui.View):
    def __init__(self, opener):
        super().__init__(timeout=None)
        self.opener = opener
        self.claimed_by = None
    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.claimed_by is None:
            self.claimed_by = interaction.user
            await interaction.response.send_message(f"Ticket claimed by {interaction.user.mention}", ephemeral=False)
        else:
            await interaction.response.send_message(f"Ticket already claimed by {self.claimed_by.mention}", ephemeral=True)
    @discord.ui.button(label="Reclaim", style=discord.ButtonStyle.secondary)
    async def reclaim(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.claimed_by = interaction.user
        await interaction.response.send_message(f"Ticket reclaimed by {interaction.user.mention}", ephemeral=False)
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CloseReasonModal(self.opener, self.claimed_by)
        await interaction.response.send_modal(modal)

class OpenTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.success)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = TicketReasonModal()
        await interaction.response.send_modal(modal)

class CloseReasonModal(discord.ui.Modal, title="Close Ticket"):
    reason = discord.ui.TextInput(label="Reason for closing the ticket", style=discord.TextStyle.paragraph, required=True)
    def __init__(self, opener, closer):
        super().__init__()
        self.opener = opener
        self.closer = closer
    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.channel
        # Transcript
        transcript = ""
        async for msg in channel.history(limit=None, oldest_first=True):
            transcript += f"[{msg.created_at.strftime('%Y-%m-%d %H:%M')}] {msg.author.display_name}: {msg.content}\n"
        # Send transcript to user
        try:
            await self.opener.send(f"Transcript of your ticket:\n```{transcript}```")
        except Exception:
            pass
        # Send transcript to staff channel
        staff_channel = interaction.guild.get_channel(1392745544941703269)
        if staff_channel:
            embed = discord.Embed(
                title="Ticket Closed",
                description=f"Ticket opened by {self.opener.mention} and closed by {self.closer.mention if self.closer else interaction.user.mention}.\nReason: {self.reason.value}",
                color=discord.Color.red()
            )
            await staff_channel.send(embed=embed)
            await staff_channel.send(f"Transcript:\n```{transcript}```")
        await interaction.response.send_message("Ticket closed and transcript sent.", ephemeral=True)
        await channel.delete()

class TicketReasonModal(discord.ui.Modal, title="Open a Ticket"):
    reason = discord.ui.TextInput(label="Reason for your ticket", style=discord.TextStyle.paragraph, required=True)
    async def on_submit(self, interaction: discord.Interaction):
        support_role = interaction.guild.get_role(SUPPORT_ROLE_ID)
        # Create ticket channel
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
        channel_name = f"ticket-of-{interaction.user.name}"
        ticket_channel = await interaction.guild.create_text_channel(channel_name, overwrites=overwrites, reason="Ticket opened")
        mention = support_role.mention if support_role else "@Support"
        user_mention = interaction.user.mention
        # Tag user + support role fuori dall'embed
        await ticket_channel.send(f"{mention} {user_mention}")
        embed = discord.Embed(
            title="Please wait for a staff reply",
            description=f"Your ticket has been created. Reason: {self.reason.value}\nA staff member will reply as soon as possible.",
            color=discord.Color.green()
        )
        await ticket_channel.send(embed=embed, view=TicketView(interaction.user))
        await interaction.response.send_message(f"Your ticket channel has been created: {ticket_channel.mention}", ephemeral=True)

TICKET_CHANNEL_ID = 1392745580484231260  # Ticket channel ID aggiornato
PARTNERSHIP_MANAGER_ROLE_ID = 123456789012345682  # Sostituisci con l'ID del ruolo staff che può gestire le partnership

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

    # Messaggio di stato ON/OFF
    STATUS_CHANNEL_ID = 1234567890123456999  # Sostituisci con l'ID del canale dove vuoi il messaggio di stato
    for guild in bot.guilds:
        status_channel = guild.get_channel(STATUS_CHANNEL_ID)
        if status_channel:
            await status_channel.send(f"✅ Il bot è ON! ({bot.user.display_name})")

    if not TOKEN or TOKEN.strip() == "" or TOKEN == "None":
        print("[ERRORE] Il token Discord non è stato trovato. Controlla il file .env e la variabile DISCORD_TOKEN.")
    else:
        print("TOKEN caricato correttamente.")

    # Cache invites for all guilds
    for guild in bot.guilds:
        invites = await guild.invites()
        invite_cache[guild.id] = {invite.code: invite.uses for invite in invites}

    # Eklubs: elimina i messaggi precedenti e invia nuovo embed
    channel_id = 1402978154284453908  # Sostituisci con l'ID del canale desiderato
    for guild in bot.guilds:
        channel = guild.get_channel(channel_id)
        if channel:
            # Elimina ultimi 20 messaggi
            try:
                async for msg in channel.history(limit=20):
                    await msg.delete()
            except Exception as e:
                print(f"Errore cancellando messaggi: {e}")
            embed = discord.Embed(
                title="🎤 Klubs!",
                description=(
                    "**What are they?**\n"
                    "• Klubs are private voice rooms where you decide who can join!\n\n"
                    "**What permissions do I need to create one?**\n"
                    "• Click the button below to see the roles allowed to create a klub.\n\n"
                    "**Commands:**\n"
                    ">create [name]\n"
                    ">edit [name]\n"
                    ">lock (only trusted & creator can join)\n"
                    ">unlock (everyone can join)\n"
                    ">trust [user] (allow access)\n"
                    ">delete (remove klub)\n"
                ),
                color=discord.Color.dark_purple()
            )
            embed.set_footer(text="Allowed Roles")
            await channel.send(embed=embed)

    # Ticket: elimina i messaggi precedenti e invia nuovo messaggio ticket
    for guild in bot.guilds:
        channel = guild.get_channel(1392745580484231260)
        if channel:
            try:
                async for msg in channel.history(limit=20):
                    await msg.delete()
            except Exception as e:
                print(f"Error deleting ticket messages: {e}")
            embed = discord.Embed(
                title="🎫 Open a Ticket",
                description="Need help or want a partnership? Click a button below to open a ticket or request a partnership with our staff.",
                color=discord.Color.blue()
            )
            await channel.send(embed=embed, view=OpenTicketView())

    # Sincronizza i comandi slash
    try:
        synced = await bot.tree.sync()
        print(f'Slash commands sincronizzati: {len(synced)}')
        for cmd in synced:
            print(f"Comando registrato: /{cmd.name}")
    except Exception as e:
        print(f'Errore sync slash commands: {e}')
    # Conferma sync playvid
    if any(cmd.name == "playvid" for cmd in await bot.tree.fetch_commands()):
        print("Comando /playvid registrato e pronto!")
    else:
        print("ATTENZIONE: /playvid NON registrato!")

@bot.command()
async def ping(ctx):
	latency = round(bot.latency * 1000)  # ms
	embed = discord.Embed(
		title="Pong!",
		description=f"Bot latency: {latency} ms",
		color=discord.Color.green()
	)
	await ctx.send(embed=embed)

# !say <messaggio>
@bot.command()
async def say(ctx, *, message: str):
	await ctx.send(message)

# Update roles when a member joins
@bot.event
async def on_member_join(member):
    guild = member.guild
    # --- INVITE TRACKER LOGIC ---
    before = invite_cache.get(guild.id, {})
    invites = await guild.invites()
    after = {invite.code: invite.uses for invite in invites}
    used_code = None
    for code in after:
        if after[code] > before.get(code, 0):
            used_code = code
            break
    invite_cache[guild.id] = after
    if used_code:
        inviter = None
        for invite in invites:
            if invite.code == used_code:
                inviter = invite.inviter
                break
        if inviter:
            invite_tracker[inviter.id] += 1
            await update_invite_roles(inviter, guild)
    # --- ANTIRAID LOGIC ---
    now = time.time()
    join_times.setdefault(guild.id, []).append(now)
    if antiraid_enabled:
        recent_joins = [t for t in join_times[guild.id] if now - t < 60]
        if len(recent_joins) >= 5:
            log_channel = guild.get_channel(ANTIRAID_LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(f"[ANTIRAID] Possibile raid rilevato: {len(recent_joins)} join in 1 minuto!")

# Update roles when a member leaves
@bot.event
async def on_member_remove(member):
    guild = member.guild
    # --- INVITE TRACKER LOGIC ---
    for inviter_id in invite_tracker:
        if invite_tracker[inviter_id] > 0:
            invite_tracker[inviter_id] -= 1
            inviter = guild.get_member(inviter_id)
            if inviter:
                await update_invite_roles(inviter, guild)
    # --- ANTINUKE LOGIC ---
    log_channel = guild.get_channel(ANTIRAID_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f"[ANTINUKE] Membro rimosso: {member.display_name} (ID: {member.id})")

# Function to update roles based on invites
async def update_invite_roles(member, guild):
	invites = invite_tracker.get(member.id, 0)
	for count, role_name in INVITE_ROLES.items():
		role = discord.utils.get(guild.roles, name=role_name)
		if role:
			if invites >= count:
				if role not in member.roles:
					await member.add_roles(role)
			else:
				if role in member.roles:
					await member.remove_roles(role)
    
# !jointts
@bot.command()
async def jointts(ctx):
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)
    await ctx.send("TTS mode enabled. I will read messages in this channel.")

    tts_queue = asyncio.Queue()
    reading = True

    async def tts_reader():
        while reading:
            msg = await tts_queue.get()
            tts = gTTS(text=msg.content, lang='en')
            tts.save('tts.mp3')
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            ctx.voice_client.play(discord.FFmpegPCMAudio('tts.mp3', executable="C:/Users/Edu/Desktop/ffmpeg/bin/ffmpeg.exe"))
            while ctx.voice_client.is_playing():
                await asyncio.sleep(0.5)

    bot.loop.create_task(tts_reader())

    def check(m):
        return m.channel == ctx.channel and m.author != bot.user

    while reading:
        try:
            msg = await bot.wait_for('message', check=check, timeout=300)
            await tts_queue.put(msg)
        except asyncio.TimeoutError:
            reading = False
            break

# !leaderboard (placeholder)
@bot.command()
async def leaderboard(ctx):
	await ctx.send('Leaderboard non ancora implementata.')

# !partner (placeholder)
@bot.command()
async def partner(ctx):
	await ctx.send('Partner non ancora implementato.')


# !giveaway (placeholder)
@bot.command()
async def giveaway(ctx):
	await ctx.send('Giveaway non ancora implementato.')

# !restart (placeholder)
@bot.command()
async def restart(ctx):
	await ctx.send('Restart non ancora implementato.')

# !role <utente> <ruolo>
@bot.command()
async def role(ctx, member: discord.Member, *, role_name: str):
	role = discord.utils.get(ctx.guild.roles, name=role_name)
	if role:
		await member.add_roles(role)
		await ctx.send(f'Ruolo "{role_name}" aggiunto a {member.mention}!')
	else:
		await ctx.send('Ruolo non trovato.')


# !ekblus (placeholder)

@bot.tree.command(name="eklubs", description="Info about Eklubs")
async def eklubs(interaction: discord.Interaction):
    # Ottieni i ruoli che possono creare un klub
    allowed_roles = []
    for count, role_name in INVITE_ROLES.items():
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role:
            allowed_roles.append(role.mention)
    allowed_roles_str = '\n'.join(allowed_roles) if allowed_roles else 'Nessun ruolo trovato.'
    class AuthorizedRolesView(ui.View):
        @ui.button(label="Authorized roles", style=discord.ButtonStyle.primary)
        async def show_roles(self, interaction2: discord.Interaction, button: ui.Button):
            role_ids = list(INVITE_ROLES.values())
            await interaction2.response.send_message(f"Authorized role IDs: {', '.join(str(rid) for rid in role_ids)}", ephemeral=True)

    embed = discord.Embed(
        title="What are Eklubs?",
        description=(
            "Eklubs are private rooms in Edu's Community where you decide who can enter!\n\n"
            "**What permissions do I need to create one?**\n"
            f"Authorized Roles:\n{allowed_roles_str}\n\n"
            "**Commands:**\n"
            ">create [name]\n"
            ">modify [name]\n"
            ">unlock (access for everyone)\n"
            ">trust [user] (grant access)\n"
            ">delete (remove eklubs)\n"
        ),
        color=discord.Color.purple()
    )
    embed.set_footer(text="Authorized Roles")
    channel_id = 1402978154284453908
    channel = interaction.guild.get_channel(channel_id)
    if channel:
        await channel.send(embed=embed, view=AuthorizedRolesView())
        await interaction.response.send_message(f"Embed sent to {channel.mention}", ephemeral=True)
    else:
        await interaction.response.send_message("Channel not found.", ephemeral=True)

# !shutdown
@bot.command()
async def shutdown(ctx):
	await ctx.send('Bot in spegnimento...')
	await bot.close()

# Coda globale per ogni server
music_queues = {}

async def play_next_song(interaction, guild_id):
    """Plays the next song in the queue for the given guild, with loop support and music embed UI."""
    queue = music_queues.get(guild_id, [])
    if not queue:
        await interaction.channel.send("The queue is empty.")
        return
    song = queue.pop(0)
    vc = interaction.guild.voice_client
    if not vc:
        await interaction.channel.send("Not connected to any voice channel.")
        return
    if vc.is_playing():
        vc.stop()
    # Scarica il file audio, riproduci, poi elimina
    import hashlib
    try:
        # Scarica da YouTube o SoundCloud
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': 'temp_song_%(id)s.%(ext)s',
            'noplaylist': True,
            'extract_flat': False,
        }
        file_path = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song['url'], download=True)
                file_path = ydl.prepare_filename(info)
        except Exception as yt_error:
            await interaction.channel.send(f"[yt-dlp] Errore YouTube: {yt_error}")
            # Prova con SoundCloud
            ydl_opts_sc = ydl_opts.copy()
            ydl_opts_sc['default_search'] = 'scsearch'
            try:
                with yt_dlp.YoutubeDL(ydl_opts_sc) as ydl:
                    info = ydl.extract_info(song['title'], download=True)
                    file_path = ydl.prepare_filename(info)
            except Exception as sc_error:
                await interaction.channel.send(f"[yt-dlp] Errore SoundCloud: {sc_error}")
                return
        # Riproduci il file scaricato
        try:
            audio_source = discord.FFmpegPCMAudio(file_path, executable="C:/Users/Edu/Desktop/ffmpeg/bin/ffmpeg.exe")
            vc.play(audio_source)
            for _ in range(10):
                await asyncio.sleep(0.5)
                if vc.is_playing():
                    break
            if not vc.is_playing():
                await interaction.channel.send(f"Playback failed to start. FFmpeg non ha riprodotto l'audio.")
                await interaction.channel.send(f"File usato: {file_path}")
                await vc.disconnect()
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                return
        except Exception as ffmpeg_error:
            await interaction.channel.send(f"[FFmpeg] Errore: {ffmpeg_error}")
            await interaction.channel.send(f"File usato: {file_path}")
            await vc.disconnect()
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            return
    except Exception as e:
        await interaction.channel.send(f"Error streaming audio: {e}")
        return
    except Exception as e:
        await interaction.channel.send(f"Error streaming audio: {e}")
        return
    # Invia embed e controlli PRIMA di avviare la riproduzione
    queue_str = "\n".join([f"{i+1}. {s['title']} (by {s['requester']})" for i, s in enumerate(music_queues.get(guild_id, []))]) or "No songs in queue."
    embed = discord.Embed(
        title=f"🎶 Now playing: {song['title']}",
        description=f"Author: {song['author']}\nDuration: {timedelta(seconds=song['duration'])}\nRequested by: {song['requester']}",
        color=discord.Color.purple()
    )
    embed.add_field(name="Queue", value=queue_str, inline=False)
    if song['thumbnail']:
        embed.set_thumbnail(url=song['thumbnail'])
    controls_view = MusicControls()
    await interaction.channel.send(embed=embed, view=controls_view)
    try:
        while vc.is_playing():
            await asyncio.sleep(1)
    except Exception as e:
        await interaction.channel.send(f"Playback error: {e}")
    # Dopo la riproduzione elimina il file
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as del_error:
            await interaction.channel.send(f"Errore eliminando file audio: {del_error}")
    # Log: fine riproduzione
    await interaction.channel.send("Playback finished. Checking queue and voice client...")
    # Check voice client and queue before next song
    vc = interaction.guild.voice_client
    if not vc or not vc.is_connected():
        await interaction.channel.send("Voice client disconnected. Music stopped.")
        return
    if hasattr(controls_view, 'is_looping') and controls_view.is_looping:
        music_queues.setdefault(guild_id, []).insert(0, song)
        await play_next_song(interaction, guild_id)
    elif music_queues.get(guild_id):
        await play_next_song(interaction, guild_id)
    else:
        await interaction.channel.send("Queue finished. Bot will stay in the voice channel.")
        # Non disconnettere il bot, resta nel canale vocale
        # await vc.disconnect()  # Commentato per far restare il bot

# !play <song>
@bot.tree.command(name="play", description="Search and play a song from YouTube")
@app_commands.describe(query="Search for a song or paste a YouTube link")
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    guild_id = interaction.guild.id
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.followup.send("You must be in a voice channel to use this command.")
        return
    channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        await channel.connect()
    elif interaction.guild.voice_client.channel != channel:
        await interaction.guild.voice_client.move_to(channel)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'outtmpl': 'song.%(ext)s',
        'playlistend': 30,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        entries = info['entries'] if 'entries' in info else [info]
        results = entries[:30]

    if not results or all(not s.get('title') for s in results):
        await interaction.followup.send(embed=discord.Embed(
            title="No results found",
            description="Nessuna canzone trovata per la tua ricerca.",
            color=discord.Color.red()
        ))
        return

    class SongPaginator(ui.View):
        def __init__(self, results):
            super().__init__(timeout=120)
            self.results = results
            self.page = 0
            self.max_page = (len(results) - 1) // 10
            self.update_buttons()

        def update_buttons(self):
            self.clear_items()
            start = self.page * 10
            end = start + 10
            for i, song in enumerate(self.results[start:end]):
                button = ui.Button(label=song.get('title', f'Song {start+i+1}'), style=discord.ButtonStyle.primary)
                button.callback = self.make_callback(start + i)
                self.add_item(button)
            if self.page > 0:
                self.add_item(ui.Button(label="⬅ Indietro", style=discord.ButtonStyle.secondary, custom_id="prev", row=4, callback=self.prev_page))
            if self.page < self.max_page:
                self.add_item(ui.Button(label="➡ Avanti", style=discord.ButtonStyle.secondary, custom_id="next", row=4, callback=self.next_page))

        async def prev_page(self, interaction2: discord.Interaction):
            self.page -= 1
            self.update_buttons()
            await interaction2.response.edit_message(embed=self.get_embed(), view=self)

        async def next_page(self, interaction2: discord.Interaction):
            self.page += 1
            self.update_buttons()
            await interaction2.response.edit_message(embed=self.get_embed(), view=self)

        def make_callback(self, idx):
            async def callback(interaction2: discord.Interaction):
                await interaction2.response.defer()
                song = self.results[idx]
                url = song['webpage_url']
                title = song.get('title', 'Unknown')
                author = song.get('uploader', 'Unknown')
                ext = song.get('ext', 'webm')
                duration = song.get('duration', 0)
                thumbnail = song.get('thumbnail', None)
                # Usa hash dell'url per nome file unico
                file_hash = hashlib.md5(url.encode()).hexdigest()
                unique_name = f"song_{file_hash}.{ext}"
                # Controlla se il file esiste già
                if not os.path.exists(unique_name):
                    ydl_opts_play = {
                        'format': 'bestaudio/best',
                        'noplaylist': True,
                        'quiet': True,
                        'outtmpl': unique_name,
                    }
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts_play) as ydl:
                            info = ydl.extract_info(url, download=True)
                            duration = info.get('duration', duration)
                            thumbnail = info.get('thumbnail', thumbnail)
                    except Exception as e:
                        await interaction2.edit_original_response(content=f"Error downloading: {e}")
                        return
                queue = music_queues.setdefault(interaction2.guild.id, [])
                queue.append({
                    'file': unique_name,
                    'title': title,
                    'author': author,
                    'duration': duration,
                    'thumbnail': thumbnail,
                    'url': url,
                    'requester': interaction2.user.mention
                })
                # Define MusicControls view for music control buttons
                class MusicControls(ui.View):
                    def __init__(self):
                        super().__init__(timeout=120)
                        self.add_item(ui.Button(label="⏸ Pausa", style=discord.ButtonStyle.secondary, custom_id="pause"))
                        self.add_item(ui.Button(label="▶ Riprendi", style=discord.ButtonStyle.secondary, custom_id="resume"))
                        self.add_item(ui.Button(label="⏹ Ferma", style=discord.ButtonStyle.danger, custom_id="stop"))
                        self.add_item(ui.Button(label="⏭ Salta", style=discord.ButtonStyle.primary, custom_id="skip"))
                        self.add_item(ui.Button(label="🔁 Loop", style=discord.ButtonStyle.success, custom_id="loop"))
                        self.is_looping = False

                    @ui.button(label="⏸ Pausa", style=discord.ButtonStyle.secondary)
                    async def pause(self, interaction: discord.Interaction, button: ui.Button):
                        vc = interaction.guild.voice_client
                        if vc and vc.is_playing():
                            vc.pause()
                            await interaction.response.send_message("Playback paused.", ephemeral=True)
                        else:
                            await interaction.response.send_message("Nothing is playing.", ephemeral=True)

                    @ui.button(label="▶ Riprendi", style=discord.ButtonStyle.secondary)
                    async def resume(self, interaction: discord.Interaction, button: ui.Button):
                        vc = interaction.guild.voice_client
                        if vc and vc.is_paused():
                            vc.resume()
                            await interaction.response.send_message("Playback resumed.", ephemeral=True)
                        else:
                            await interaction.response.send_message("Nothing is paused.", ephemeral=True)

                    @ui.button(label="⏹ Ferma", style=discord.ButtonStyle.danger)
                    async def stop(self, interaction: discord.Interaction, button: ui.Button):
                        vc = interaction.guild.voice_client
                        if vc and (vc.is_playing() or vc.is_paused()):
                            vc.stop()
                            await interaction.response.send_message("Playback stopped.", ephemeral=True)
                        else:
                            await interaction.response.send_message("Nothing to stop.", ephemeral=True)

                    @ui.button(label="⏭ Salta", style=discord.ButtonStyle.primary)
                    async def skip(self, interaction: discord.Interaction, button: ui.Button):
                        vc = interaction.guild.voice_client
                        if vc and vc.is_playing():
                            vc.stop()
                            await interaction.response.send_message("Song skipped.", ephemeral=True)
                        else:
                            await interaction.response.send_message("Nothing to skip.", ephemeral=True)

                    @ui.button(label="🔁 Loop", style=discord.ButtonStyle.success)
                    async def loop(self, interaction: discord.Interaction, button: ui.Button):
                        self.is_looping = not self.is_looping
                        status = "enabled" if self.is_looping else "disabled"
                        await interaction.response.send_message(f"Loop {status} for current song.", ephemeral=True)

                controls_view = MusicControls()
                await interaction2.channel.send(content=f"Controlli musica per **{title}**:", view=controls_view)
                vc = interaction2.guild.voice_client
                if not vc.is_playing():
                    await play_next_song(interaction2, interaction2.guild.id)
                else:
                    await interaction2.edit_original_response(content=f"Aggiunta in coda: {title}")
            return callback

        def get_embed(self):
            embed = discord.Embed(title=f"Seleziona una canzone (pagina {self.page+1}/{self.max_page+1})", color=discord.Color.green())
            start = self.page * 10
            end = start + 10
            for i, song in enumerate(self.results[start:end]):
                embed.add_field(name=f"{start+i+1}. {song.get('title', 'Unknown')}", value=song.get('uploader', 'Unknown'), inline=False)
            return embed

    paginator = SongPaginator(results)
    await interaction.followup.send(embed=paginator.get_embed(), view=paginator)

class VideoView(discord.ui.View):
    def __init__(self, video_url):
        super().__init__(timeout=None)
        self.video_url = video_url
    @discord.ui.button(label="Guarda Video", style=discord.ButtonStyle.primary)
    async def watch_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Ecco il video: {self.video_url}", ephemeral=True)

@app_commands.command(name="playvid", description="Cerca e mostra un video YouTube nella chat")
@app_commands.describe(video="Titolo o link del video da cercare")
async def playvid(interaction: discord.Interaction, video: str):
    await interaction.response.defer()
    # Cerca il video su YouTube
    import yt_dlp
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo+bestaudio/best',
        'default_search': 'ytsearch1',
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video, download=False)
        if 'entries' in info:
            info = info['entries'][0]
    video_url = f"https://www.youtube.com/watch?v={info['id']}"
    embed = discord.Embed(
        title=f"📹 {info.get('title', 'Video')}",
        description=f"{info.get('uploader', '')}\nDurata: {timedelta(seconds=info.get('duration', 0))}",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=info.get('thumbnail', ''))
    embed.add_field(name="Guarda il video", value=f"[Clicca qui]({video_url})", inline=False)
    view = VideoView(video_url)
    await interaction.followup.send(embed=embed, view=view)

# Registrazione comando
bot.tree.add_command(playvid)

def get_uptime():
    """Calcola l'uptime in formato giorni, ore, minuti"""
    delta = datetime.utcnow() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return f"{days}g {hours}h {minutes}m"

async def get_db_ping():
    """Calcola la latenza del database locale"""
    try:
        conn = sqlite3.connect(':memory:')  # Test su DB temporaneo
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return round((time.time() - start_time) * 1000, 2)
    except Exception:
        return None

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    try:
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Slash commands sincronizzati per questo server: {len(synced)}')
    except Exception as e:
        await ctx.send(f'Errore sync slash commands: {e}')

class MusicControls(ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(ui.Button(label="⏸ Pause", style=discord.ButtonStyle.secondary, custom_id="pause"))
        self.add_item(ui.Button(label="▶ Resume", style=discord.ButtonStyle.secondary, custom_id="resume"))
        self.add_item(ui.Button(label="⏹ Stop", style=discord.ButtonStyle.danger, custom_id="stop"))
        self.add_item(ui.Button(label="⏭ Skip", style=discord.ButtonStyle.primary, custom_id="skip"))
        self.add_item(ui.Button(label="🔁 Loop", style=discord.ButtonStyle.success, custom_id="loop"))
        self.is_looping = False

    @ui.button(label="⏸ Pause", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, button: ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("Playback paused.", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing is playing.", ephemeral=True)

    @ui.button(label="▶ Riprendi", style=discord.ButtonStyle.secondary)
    async def resume(self, interaction: discord.Interaction, button: ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("Playback resumed.", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing is paused.", ephemeral=True)

    @ui.button(label="⏹ Ferma", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: ui.Button):
        vc = interaction.guild.voice_client
        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
            await interaction.response.send_message("Playback stopped.", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing to stop.", ephemeral=True)

    @ui.button(label="⏭ Salta", style=discord.ButtonStyle.primary)
    async def skip(self, interaction: discord.Interaction, button: ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.response.send_message("Song skipped.", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing to skip.", ephemeral=True)

    @ui.button(label="🔁 Loop", style=discord.ButtonStyle.success)
    async def loop(self, interaction: discord.Interaction, button: ui.Button):
        self.is_looping = not self.is_looping
        status = "enabled" if self.is_looping else "disabled"
        await interaction.response.send_message(f"Loop {status} for current song.", ephemeral=True)

# Nuovi comandi per lingua TTS
@bot.command(name="jointts_ita")
async def jointts_ita(ctx):
    await jointts_lang(ctx, 'it')

@bot.command(name="jointts_eng")
async def jointts_eng(ctx):
    await jointts_lang(ctx, 'en')

# TTS attivo solo dopo !jointts_ita o !jointts_eng, e solo dal canale testuale associato
tts_active = {}
tts_lang = {}

async def jointts_lang(ctx, lang):
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)
    guild_id = ctx.guild.id
    tts_active[guild_id] = True
    tts_lang[guild_id] = lang
    await ctx.send(f"TTS mode enabled. Scrivi nel canale testuale con lo stesso nome della vocale per far parlare il bot in {lang.upper()}.")

## partner_add command removed. Use only PartnershipManager group for /partner commands.

# Nuovo gruppo di comandi slash /partner (add, delete, edit)
PARTNERSHIP_MANAGER_ROLE_ID = 123456789012345682  # Sostituisci con l'ID del ruolo staff che può gestire le partnership

class PartnershipManager(app_commands.Group):
    def __init__(self):
        super().__init__(name="partner", description="Gestisci le partnership")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
            role = interaction.guild.get_role(PARTNERSHIP_MANAGER_ROLE_ID)
            member = interaction.guild.get_member(interaction.user.id)
            debug_msg = f"[DEBUG] User: {interaction.user.display_name} (ID: {interaction.user.id})\n"
            debug_msg += f"Role to check: {role.name if role else 'None'} (ID: {PARTNERSHIP_MANAGER_ROLE_ID})\n"
            if member:
                debug_msg += f"Member found. Roles: {', '.join([r.name for r in member.roles])}\n"
                debug_msg += f"Role present in member.roles: {'Yes' if role and role in member.roles else 'No'}\n"
            else:
                debug_msg += "Member NOT found in guild.\n"
            await interaction.response.send_message(debug_msg, ephemeral=True)
            if member and role and role in member.roles:
                return True
            # Always send a followup error message for clarity
            await interaction.followup.send(f"Non hai i permessi per gestire le partnership. (Cerca ruolo: {role.name if role else 'None'})", ephemeral=True)
            return False

    @app_commands.command(name="add", description="Aggiungi una partnership")
    async def add(self, interaction: discord.Interaction, name: str, description: str, invite_url: str):
        embed = discord.Embed(
            title=f"🤝 Partnership: {name} | {invite_url}",
            description=description,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Added by {interaction.user.display_name}")
        channel = interaction.guild.get_channel(PARTNERSHIP_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Partnership aggiunta in {channel.mention}", ephemeral=True)
            # Salva partnership nel database
            try:
                conn = sqlite3.connect('partnerships.db')
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS partnerships (
                        name TEXT PRIMARY KEY,
                        description TEXT,
                        invite_url TEXT,
                        added_by TEXT,
                        added_at TEXT
                    )
                """)
                cursor.execute("""
                    INSERT OR REPLACE INTO partnerships (name, description, invite_url, added_by, added_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, description, invite_url, interaction.user.display_name, datetime.utcnow().isoformat()))
                conn.commit()
                conn.close()
            except Exception as db_error:
                await interaction.channel.send(f"[DB] Errore salvataggio partnership: {db_error}")
        else:
            await interaction.response.send_message("Partnership channel not found.", ephemeral=True)

    @app_commands.command(name="delete", description="Elimina una partnership")
    async def delete(self, interaction: discord.Interaction, name: str):
        # Chiede il nome della partnership (già come argomento)
        channel = interaction.guild.get_channel(PARTNERSHIP_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message("Partnership channel not found.", ephemeral=True)
            return
        found = False
        async for msg in channel.history(limit=100):
            if msg.embeds:
                embed = msg.embeds[0]
                if embed.title and name.lower() in embed.title.lower():
                    await msg.delete()
                    found = True
                    break
        # Elimina dal database
        try:
            conn = sqlite3.connect('partnerships.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM partnerships WHERE name = ?", (name,))
            conn.commit()
            conn.close()
        except Exception as db_error:
            await interaction.channel.send(f"[DB] Errore eliminazione partnership: {db_error}")
        if found:
            await interaction.response.send_message(f"Partnership '{name}' eliminata.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Nessuna partnership trovata con nome '{name}'.", ephemeral=True)

    @app_commands.command(name="edit", description="Modifica una partnership")
    async def edit(self, interaction: discord.Interaction, name: str, new_description: str = None, new_invite_url: str = None):
        # Chiede il nome della partnership (già come argomento)
        channel = interaction.guild.get_channel(PARTNERSHIP_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message("Partnership channel not found.", ephemeral=True)
            return
        found = False
        async for msg in channel.history(limit=100):
            if msg.embeds:
                embed = msg.embeds[0]
                if embed.title and name.lower() in embed.title.lower():
                    if new_description:
                        embed.description = new_description
                    if new_invite_url:
                        parts = embed.title.split('|')
                        embed.title = f"{parts[0].strip()} | {new_invite_url}"
                    await msg.edit(embed=embed)
                    found = True
                    break
        # Aggiorna nel database
        try:
            conn = sqlite3.connect('partnerships.db')
            cursor = conn.cursor()
            if new_description:
                cursor.execute("UPDATE partnerships SET description = ? WHERE name = ?", (new_description, name))
            if new_invite_url:
                cursor.execute("UPDATE partnerships SET invite_url = ? WHERE name = ?", (new_invite_url, name))
            conn.commit()
            conn.close()
        except Exception as db_error:
            await interaction.channel.send(f"[DB] Errore modifica partnership: {db_error}")
        if found:
            await interaction.response.send_message(f"Partnership '{name}' modificata.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Nessuna partnership trovata con nome '{name}'.", ephemeral=True)

bot.tree.add_command(PartnershipManager())

# Nuovo evento on_message: ripete ogni messaggio in chat dicendo chi lo ha scritto
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Ignora utenti/bot whitelistati
    if message.author.id in WHITELISTED_USER_IDS:
        await bot.process_commands(message)
        return
    # Automod: ignora la categoria (solo se il canale ha la categoria)
    if hasattr(message.channel, 'category') and message.channel.category and message.channel.category.id == IGNORED_CATEGORY_ID:
        await bot.process_commands(message)
        return

    # Automod: elimina e mette timeout chi scrive parole blacklistate, tranne ticket/partnership staff
    is_ticket = message.channel.id == TICKET_CHANNEL_ID or message.channel.name.startswith('ticket-of-')
    staff_role = discord.utils.get(message.guild.roles, id=PARTNERSHIP_MANAGER_ROLE_ID)
    is_staff = staff_role in message.author.roles if staff_role else False
    is_partnership = message.channel.id == PARTNERSHIP_CHANNEL_ID
    if not is_ticket and not (is_partnership and is_staff):
        # Blacklist check (case-insensitive)
        msg_content = message.content.lower()
        if any(word.lower() in msg_content for word in BLACKLISTED_WORDS):
            log_channel = message.guild.get_channel(ANTINUKE_LOG_CHANNEL_ID)
            member = message.guild.get_member(message.author.id)
            if not member:
                member = message.author  # fallback
            # Elimina il messaggio
            try:
                await message.delete()
            except Exception as e:
                if log_channel:
                    await log_channel.send(f"[AUTOMOD] Error deleting message: {e}")
            # Prova a mettere timeout
            try:
                timeout_until = datetime.utcnow() + timedelta(minutes=5)
                if hasattr(member, 'edit'):
                    await member.edit(timeout=timeout_until, reason="Automod blacklist word")
                    await message.channel.send(f"{member.mention} è stato messo in timeout per 5 minuti per linguaggio vietato.", delete_after=5)
                    if log_channel:
                        await log_channel.send(f"[AUTOMOD] {member.mention} ({getattr(member, 'display_name', member.name)}, ID: {member.id}) ha usato una parola blacklistata ed è stato messo in timeout per 5 min.")
                else:
                    await message.channel.send(f"{member.mention}, il tuo messaggio è stato eliminato per linguaggio vietato.", delete_after=5)
                    if log_channel:
                        await log_channel.send(f"[AUTOMOD] {member.mention} ({getattr(member, 'display_name', member.name)}, ID: {member.id}) ha usato una parola blacklistata. Messaggio eliminato.")
            except Exception as e:
                if log_channel:
                    await log_channel.send(f"[AUTOMOD] Errore timeout: {e}")
            return



    # Elimina i messaggi nei canali klub dopo 5 secondi
    KLUB_CHANNEL_IDS = [1234567890123456789]  # Sostituisci con gli ID dei canali klub
    if message.channel.id in KLUB_CHANNEL_IDS and not message.author.bot:
        try:
            await message.delete(delay=5)
        except Exception:
            pass

    # Crea un canale klub se il messaggio è '>create (name)'
    if message.content.startswith('>create '):
        name = message.content[len('>create '):].strip()
        guild = message.guild
        # Sostituisci con la logica per autorizzare solo ruoli specifici
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            message.author: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        try:
            new_channel = await guild.create_text_channel(name, overwrites=overwrites)
            await message.channel.send(f"Klub '{name}' created!", delete_after=5)
        except Exception as e:
            await message.channel.send(f"Error creating klub: {e}", delete_after=5)
    guild_id = message.guild.id if message.guild else None
    if guild_id and tts_active.get(guild_id):
        vc = message.guild.voice_client
        voice_channel = vc.channel if vc else None
        if voice_channel and message.channel.name == voice_channel.name:
            lang = tts_lang.get(guild_id, 'it')
            tts = gTTS(text=message.content, lang=lang)
            tts.save('tts.mp3')
            if vc.is_playing():
                vc.stop()
            vc.play(discord.FFmpegPCMAudio('tts.mp3', executable="C:/Users/Edu/Desktop/ffmpeg/bin/ffmpeg.exe"))
    await bot.process_commands(message)


# ID del canale dove il bot manda messaggi automatici
AUTO_MESSAGE_CHANNEL_ID = 1392062910259531797  # Canale auto messages

# Klub management in on_message
async def on_message(message):
    # ...existing code...
    # Klub commands
    if message.content.startswith('>modify '):
        name = message.content[len('>modify '):].strip()
        # Modifica il canale klub (esempio: cambia topic)
        channel = discord.utils.get(message.guild.channels, name=name)
        if channel:
            await channel.edit(topic=f"Modified by {message.author.display_name}")
            await message.channel.send(f"Klub '{name}' modified!", delete_after=5)
        else:
            await message.channel.send(f"Klub '{name}' not found.", delete_after=5)

    elif message.content.startswith('>unlock'):
        # Rende il canale accessibile a tutti
        channel = message.channel
        await channel.set_permissions(message.guild.default_role, view_channel=True, send_messages=True)
        await channel.send("Klub unlocked for everyone!", delete_after=5)

    elif message.content.startswith('>trust '):
        user_mention = message.content[len('>trust '):].strip()
        user = None
        if user_mention.startswith('<@') and user_mention.endswith('>'):
            user_id = int(user_mention[2:-1])
            user = message.guild.get_member(user_id)
        if user:
            await message.channel.set_permissions(user, view_channel=True, send_messages=True)
            await message.channel.send(f"{user.mention} can now access this klub!", delete_after=5)
        else:
            await message.channel.send("User not found.", delete_after=5)

    elif message.content.startswith('>delete'):
        channel = message.channel
        await channel.send("Klub will be deleted in 5 seconds.", delete_after=5)
        await asyncio.sleep(5)
        await channel.delete()

    # Messaggi automatici del bot
    if AUTO_MESSAGE_CHANNEL_ID:
        auto_channel = message.guild.get_channel(AUTO_MESSAGE_CHANNEL_ID)
        if auto_channel and not message.author.bot:
            await auto_channel.send(f"Automatic message: {message.content}")

    # ...existing code...

if __name__ == "__main__":
    print("Starting Discord bot and keep-alive...")
    bot.run(TOKEN)





