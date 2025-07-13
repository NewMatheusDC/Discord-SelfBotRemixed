import discord
from discord.ext import commands
import ctypes
import json
import os
import random
import requests
import asyncio
import string
import time
import datetime
from colorama import Fore
import platform
import itertools
from gtts import gTTS
import io
import qrcode
import pyfiglet
import aiohttp
import socket
import base64
import discord
import discord
from discord.ext import commands

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

__version__ = "4.5"

start_time = datetime.datetime.now(datetime.timezone.utc)

with open("config/config.json", "r") as file:
    config = json.load(file)
    token = config.get("token")
    prefix = config.get("prefix")
    message_generator = itertools.cycle(config["autoreply"]["messages"])

def save_config(config):
    with open("config/config.json", "w") as file:
        json.dump(config, file, indent=4)

def selfbot_menu(bot):
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    print(f"""\n{Fore.RESET}
                            ██████╗ ████████╗██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
                           ██╔═══██╗╚══██╔══╝██║██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
                           ██║██╗██║   ██║   ██║██║   ██║       ██║   ██║   ██║██║   ██║██║     
                           ██║██║██║   ██║   ██║██║   ██║       ██║   ██║   ██║██║   ██║██║     
                           ╚█║████╔╝   ██║   ██║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
                            ╚╝╚═══╝    ╚═╝   ╚═╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n""".replace('█', f'{b}█{y}'))
    print(f"""{y}------------------------------------------------------------------------------------------------------------------------
{w}raadev {b}|{w} https://github.com/AstraaDev {b}|{w} https://github.com/AstraaDev {b}|{w} https://github.com/AstraaDev {b}|{w} https://github.com
{y}------------------------------------------------------------------------------------------------------------------------\n""")
    print(f"""{y}[{b}+{y}]{w} SelfBot Information:\n
\t{y}[{w}#{y}]{w} Version: v{__version__}
\t{y}[{w}#{y}]{w} Logged in as: {bot.user} ({bot.user.id})
\t{y}[{w}#{y}]{w} Cached Users: {len(bot.users)}
\t{y}[{w}#{y}]{w} Guilds Connected: {len(bot.guilds)}\n\n
{y}[{b}+{y}]{w} Settings Overview:\n
\t{y}[{w}#{y}]{w} SelfBot Prefix: {prefix}
\t{y}[{w}#{y}]{w} Remote Users Configured:""")
    if config["remote-users"]:
        for i, user_id in enumerate(config["remote-users"], start=1):
            print(f"\t\t{y}[{w}{i}{y}]{w} User ID: {user_id}")
    else:
        print(f"\t\t{y}[{w}-{y}]{w} No remote users configured.")
    print(f"""
\t{y}[{w}#{y}]{w} Active Autoreply Channels: {len(config["autoreply"]["channels"])}
\t{y}[{w}#{y}]{w} Active Autoreply Users: {len(config["autoreply"]["users"])}\n
\t{y}[{w}#{y}]{w} AFK Status: {'Enabled' if config["afk"]["enabled"] else 'Disabled'}
\t{y}[{w}#{y}]{w} AFK Message: "{config["afk"]["message"]}"\n
\t{y}[{w}#{y}]{w} Total Commands Loaded: 63\n\n
{y}[{Fore.GREEN}!{y}]{w} SelfBot is now online and ready!""")

bot = commands.Bot(
    command_prefix=prefix,
    description='not a selfbot', 
    self_bot=True,
    help_command=None
)

@bot.event
async def on_ready():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"SelfBot v{__version__} - Made By a5traa")
        os.system('cls')
    else:
        os.system('clear')
    selfbot_menu(bot)

@bot.event
async def on_message(message):
    # Handle copycat functionality first
    if message.author.id in config["copycat"]["users"]:
        if message.content.startswith(config['prefix']):
            response_message = message.content[len(config['prefix']):]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    # Handle AFK responses - moved this before command processing
@bot.event
async def on_message(message):
    # Handle copycat functionality first
    if message.author.id in config["copycat"]["users"]:
        if message.content.startswith(config['prefix']):
            response_message = message.content[len(config['prefix']):]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    # Handle AFK responses - moved this before command processing
    if config["afk"]["enabled"] and message.author != bot.user:
        # Check if it's a DM
        if isinstance(message.channel, discord.DMChannel):
            await message.reply(config["afk"]["message"])
            return

    # Handle autoreply
    if message.author != bot.user:
        if str(message.author.id) in config["autoreply"]["users"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
        elif str(message.channel.id) in config["autoreply"]["channels"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
            
        # Check if it's a DM
        elif isinstance(message.channel, discord.DMChannel):
            await message.reply(config["afk"]["message"])
            return

    # Handle autoreply
    if message.author != bot.user:
        if str(message.author.id) in config["autoreply"]["users"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
        elif str(message.channel.id) in config["autoreply"]["channels"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
    
    # Rest of your on_message handler...
    # (Block commands in specific guild, autoreact, etc.)
    
    # Process commands - allow from bot owner or remote users
    if (message.author == bot.user or 
        str(message.author.id) in config["remote-users"] or
        message.content.startswith(config['prefix'])):
        await bot.process_commands(message)
    
    # Block commands in specific guild
    if message.guild and message.guild.id == 1279905004181917808 and message.content.startswith(config['prefix']):
        await message.delete()
        await message.channel.send("> SelfBot commands are not allowed here. Thanks.", delete_after=5)
        return

    # Handle autoreact
    if config["autoreact"]["enabled"] and message.guild:
        if not config["autoreact"]["react_to_own"] and message.author == bot.user:
            pass
        elif str(message.author.id) not in config["autoreact"]["blacklist"]:
            for target in config["autoreact"]["targets"]:
                channel_match = str(message.channel.id) == target["channel_id"]
                server_match = target.get("server_id") is None or str(message.guild.id) == target["server_id"]
                
                if channel_match and server_match:
                    try:
                        emoji = target["emoji"]
                        if emoji.isdigit():
                            emoji = bot.get_emoji(int(emoji))
                        await message.add_reaction(emoji)
                    except Exception:
                        pass

    # Process commands - allow from bot owner or remote users
    if (message.author == bot.user or 
        str(message.author.id) in config["remote-users"] or
        message.content.startswith(config['prefix'])):
        await bot.process_commands(message)

@bot.command(aliases=['h'])
async def help(ctx, *, category=None):
    await ctx.message.delete()

    if not category:
        # Main help menu
        main_help = f"""```ansi
🌟 DiscordSelfZ v{__version__} | Prefix: {prefix} 🌟

📋 Available Categories:

{prefix}help main      - Main & Essential Commands
{prefix}help user      - User Management Commands  
{prefix}help server    - Server Management Commands
{prefix}help message   - Message Related Commands
{prefix}help utility   - Utility & Tools Commands
{prefix}help autoreact - Auto React Commands
{prefix}help fun       - Fun & Entertainment Commands
{prefix}help status    - Status & Activity Commands
{prefix}help webhook   - Webhook Management Commands
{prefix}help stealth   - Stealth & Hidden Commands
{prefix}help autocount - AutoNumber & AutoCount Commands

📊 Quick Stats:
Total Commands: 63
Guilds Connected: {len(bot.guilds)}
Cached Users: {len(bot.users)}
```

Use `{prefix}help <category>` to view specific commands."""

        await ctx.send(main_help)
        return

    # Category commands
    categories = {
        "main": {
            "title": "Main & Essential Commands",
            "commands": [
                f"{prefix}astraa - Show my social networks",
                f"{prefix}changeprefix <prefix> - Change bot prefix",
                f"{prefix}shutdown - Stop the selfbot",
                f"{prefix}uptime - Show how long the bot has been running",
                f"{prefix}ping - Return bot latency",
                f"{prefix}remoteuser <@user> - Authorize a user to execute commands remotely",
                f"{prefix}restart - restart the program (beta)"
            ]
        },
        "user": {
            "title": "User Management Commands",
            "commands": [
                f"{prefix}usericon <@user> - User's avatar",
                f"{prefix}tokeninfo <token> - Detailed token information",
                f"{prefix}hypesquad <house> - Change your HypeSquad badge",
                f"{prefix}cleardm <amount> - Clear your DM messages",
                f"{prefix}copycat <ON|OFF> <@user> - Copy user messages"
                f"{prefix}autonumber <channel-id> (server-id) (up/down) (on/false) - Configure autonumber",
                f"{prefix}autonumber here <on/off> (up/down) - Configure for current channel",
                f"{prefix}autonumber add (channel-id) (server-id) (up/down) - Add target",
                f"{prefix}autonumber remove <channel-id> (server-id) - Remove target",
                f"{prefix}autonumber list - List all targets",
                f"{prefix}autonumber config - Show configuration",
                f"{prefix}autonumber panic confirm - Reset all settings"
            ]
        },
        "server": {
            "title": "Server Management Commands",
            "commands": [
                f"{prefix}guildinfo - Detailed server information",
                f"{prefix}guildicon - Current server icon",
                f"{prefix}guildbanner - Current server banner",
                f"{prefix}guildrename <name> - Rename the server",
                f"{prefix}fetchmembers - List all server members",
                f"{prefix}firstmessage - Link to first message in channel",
                f"{prefix}copyserver <server-id> - copy the server",
                f"{prefix}mcserverinfo <server-ip> <port> - sends information about the server"
            ]
        },
        "message": {
            "title": "Message Related Commands",
            "commands": [
                f"{prefix}purge <amount> - Delete specific messages",
                f"{prefix}clear - Clear chat with spaces",
                f"{prefix}msgclr <amount> - Safely delete your own messages (max: 50)",
                f"{prefix}spam <amount> <message> - Spam messages (max: 9)",
                f"{prefix}quickdelete <message> - Send and delete after 2 seconds",
                f"{prefix}dmall <message> - DM all members",
                f"{prefix}sendall <message> - Message in all channels",
                f"{prefix}autoreply <ON|OFF> - Auto-reply in channels/users",
                f"{prefix}autocmd <bot-id> <command> <delay> - autocmd (NOT YET COMPLETED)",
                f"{prefix}stopautocmd - stop autocmd",
                f"{prefix}listautocmd - list of activated autocmds",
                f"{prefix}autolog (on/off) (souce-channel-id) (target-channel-id) - resend deleted messages",
                f"{prefix}autolog LIST - list of activated autologgers"
            ]
        },
        "utility": {
            "title": "Utility & Tools Commands",
            "commands": [
                f"{prefix}pingweb <url> - Test website status",
                f"{prefix}geoip <ip> - Geolocate an IP address",
                f"{prefix}tts <text> - Convert text to audio (.wav)",
                f"{prefix}qr <text> - Generate QR code with provided text",
                f"{prefix}gentoken - Generate fake token with correct pattern",
                f"{prefix}ascii <message> - Convert message to ASCII art",
                f"{prefix}reverse <message> - Reverse message letters",
                f"{prefix}leetspeak <message> - Convert text to l33t sp34k"
            ]
        },
        "autoreact": {
            "title": "Auto React Commands",
            "commands": [
                f"{prefix}autoreact <channel> <emoji> - Auto-react in specific channel",
                f"{prefix}areact <true|false> - Enable/disable auto-react",
                f"{prefix}ablacklist <list|add|remove> <@user> - Manage auto-react blacklist",
                f"{prefix}aconfig - Auto-react configuration",
                f"{prefix}panicreact - Remove all auto-react configurations",
                f"{prefix}reactservers - List all auto-react targets",
                f"{prefix}myignore <true|false> - React to own messages"
            ]
        },
        "fun": {
            "title": "Fun & Entertainment Commands",
            "commands": [
                f"{prefix}dick <@user> - Show user's 'size'",
                f"{prefix}minesweeper <size> - Customizable Minesweeper game",
                f"{prefix}airplane - ⚠️ 9/11 animation (use responsibly)",
                f"{prefix}nitro - Generate fake Nitro code"
            ]
        },
        "status": {
            "title": "Status & Activity Commands",
            "commands": [
                f"{prefix}playing <status> - Set 'Playing' status",
                f"{prefix}watching <status> - Set 'Watching' status",
                f"{prefix}streaming <status> - Set 'Streaming' status",
                f"{prefix}stopactivity - Remove activity status",
                f"{prefix}afk <ON|OFF> <message> - AFK mode with custom message"
            ]
        },
        "webhook": {
            "title": "Webhook Management Commands",
            "commands": [
                f"{prefix}webhook <name> [avatar] - Create new webhook in channel",
                f"{prefix}webhooks - List webhooks in current channel",
                f"{prefix}whserverlist - List all server webhooks",
                f"{prefix}webhooksend <url> <message> - Send message via webhook",
                f"{prefix}whjson <url> <file.json> - Send JSON via webhook",
                f"{prefix}webhookedit <url> [name] [avatar] - Edit existing webhook",
                f"{prefix}whremove <url> - Remove a webhook"
            ]
        },
        "stealth": {
            "title": "Stealth & Hidden Commands",
            "commands": [
                f"{prefix}hidemention <message> - Hide messages inside others",
                f"{prefix}edit <message> - Move edited tag position"
            ]
        },
        "autocount": {
            "title": "AutoNumber & AutoCount Commands",
            "commands": [
            f"{prefix}autonumber <channel-id> (server-id) (up/down) (on/false) - Configure autonumber",
            f"{prefix}autonumber here <on/off> (up/down) - Configure for current channel",
            f"{prefix}autonumber add (channel-id) (server-id) (up/down) - Add target",
            f"{prefix}autonumber remove <channel-id> (server-id) - Remove target",
            f"{prefix}autonumber list - List all targets",
            f"{prefix}autonumber config - Show configuration",
            f"{prefix}autonumber panic confirm - Reset all settings",
            f"{prefix}count <number> to <number2> - Start counting in current channel",
            f"{prefix}stopcount - Stop counting in current channel",
            f"{prefix}count2 <channel-id> <server-id> (up/down) (on/off) - Remote counting",
            f"{prefix}stopcount2 - Stop remote counting"
        ]
    }
}
    
    if category.lower() in categories:
        cat_data = categories[category.lower()]
        
        category_help = f"```ansi\n🌟 {cat_data['title']} 🌟\n\n"
        
        for i, command in enumerate(cat_data['commands'], 1):
            category_help += f"{i:2}. {command}\n"
        
        category_help += f"\nUse {prefix}help to return to main menu```"
        
        await ctx.send(category_help)
    else:
        await ctx.send(f"> **❌ Category not found!**\n> Use `{prefix}help` to see all available categories.", delete_after=10)

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."

    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    await ctx.send(uptime_stamp)

@bot.command()
async def ping(ctx):
    await ctx.message.delete()

    before = time.monotonic()
    message_to_send = await ctx.send("Pinging...")

    await message_to_send.edit(content=f"`{int((time.monotonic() - before) * 1000)} ms`")

@bot.command(aliases=['astra'])
async def astraa(ctx):
    await ctx.message.delete()

    embed = f"""**MY SOCIAL NETWORKS | Prefix: `{prefix}`**\n
    > :pager: `Discord Server`\n*https://discord.gg/PKR7nM9j9U*
    > :computer: `GitHub Page`\n*https://github.com/AstraaDev*
    > :robot: `SelfBot Project`\n*https://github.com/AstraaDev/Discord-SelfBot*"""

    await ctx.send(embed)

@bot.command()
async def geoip(ctx, ip: str=None):
    await ctx.message.delete()

    if not ip:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `geoip <ip>`", delete_after=5)
        return

    try:
        r = requests.get(f'http://ip-api.com/json/{ip}')
        geo = r.json()
        embed = f"""**GEOLOCATE IP | Prefix: `{prefix}`**\n
        > :pushpin: `IP`\n*{geo['query']}*
        > :globe_with_meridians: `Country-Region`\n*{geo['country']} - {geo['regionName']}*
        > :department_store: `City`\n*{geo['city']} ({geo['zip']})*
        > :map: `Latitute-Longitude`\n*{geo['lat']} - {geo['lon']}*
        > :satellite: `ISP`\n*{geo['isp']}*
        > :robot: `Org`\n*{geo['org']}*
        > :alarm_clock: `Timezone`\n*{geo['timezone']}*
        > :electric_plug: `As`\n*{geo['as']}*"""
        await ctx.send(embed, file=discord.File("img/astraa.gif"))
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to geolocate ip\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def tts(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `tts <message>`", delete_after=5)
        return

    content = content.strip()

    tts = gTTS(text=content, lang="en")
    
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)

    await ctx.send(file=discord.File(f, f"{content[:10]}.wav"))

@bot.command(aliases=['qrcode'])
async def qr(ctx, *, text: str="https://discord.gg/PKR7nM9j9U"):
    qr = qrcode.make(text)
    
    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr)
    img_byte_arr.seek(0)

    await ctx.send(file=discord.File(img_byte_arr, "qr_code.png"))

@bot.command()
async def pingweb(ctx, website_url: str=None):
    await ctx.message.delete()

    if not website_url:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `pingweb <url>`", delete_after=5)
        return

    try:
        r = requests.get(website_url).status_code
        if r == 404:
            await ctx.send(f'> Website **down** *({r})*')
        else:
            await ctx.send(f'> Website **operational** *({r})*')
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to ping website\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def gentoken(ctx, user: str=None):
    await ctx.message.delete()

    code = "ODA"+random.choice(string.ascii_letters)+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))+"."+random.choice(string.ascii_letters).upper()+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))+"."+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    
    if not user:
        await ctx.send(''.join(code))
    else:
        await ctx.send(f"> {user}'s token is: ||{''.join(code)}||")

@bot.command()
async def quickdelete(ctx, *, message: str=None):
    await ctx.message.delete()

    if not message:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `quickdelete <message>`', delete_after=2)
        return
    
    await ctx.send(message, delete_after=2)

@bot.command(aliases=['uicon'])
async def usericon(ctx, user: discord.User = None):
    await ctx.message.delete()

    if not user:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `usericon <@user>`', delete_after=5)
        return
    
    # Get the best available avatar URL
    if user.avatar:
        avatar_url = user.avatar.url
    elif hasattr(user, 'guild_avatar') and user.guild_avatar:  # For server-specific avatars
        avatar_url = user.guild_avatar.url
    else:
        avatar_url = user.display_avatar.url  # This works for both users and bots
    
    await ctx.send(f"> {user.mention}'s avatar:\n{avatar_url}")

@bot.command(aliases=['tinfo'])
async def tokeninfo(ctx, usertoken: str=None):
    await ctx.message.delete()

    if not usertoken:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `tokeninfo <token>`', delete_after=5)
        return

    headers = {'Authorization': usertoken, 'Content-Type': 'application/json'}
    languages = {
        'da': 'Danish, Denmark',
        'de': 'German, Germany',
        'en-GB': 'English, United Kingdom',
        'en-US': 'English, United States',
        'es-ES': 'Spanish, Spain',
        'fr': 'French, France',
        'hr': 'Croatian, Croatia',
        'lt': 'Lithuanian, Lithuania',
        'hu': 'Hungarian, Hungary',
        'nl': 'Dutch, Netherlands',
        'no': 'Norwegian, Norway',
        'pl': 'Polish, Poland',
        'pt-BR': 'Portuguese, Brazilian, Brazil',
        'ro': 'Romanian, Romania',
        'fi': 'Finnish, Finland',
        'sv-SE': 'Swedish, Sweden',
        'vi': 'Vietnamese, Vietnam',
        'tr': 'Turkish, Turkey',
        'cs': 'Czech, Czechia, Czech Republic',
        'el': 'Greek, Greece',
        'bg': 'Bulgarian, Bulgaria',
        'ru': 'Russian, Russia',
        'uk': 'Ukrainian, Ukraine',
        'th': 'Thai, Thailand',
        'zh-CN': 'Chinese, China',
        'ja': 'Japanese',
        'zh-TW': 'Chinese, Taiwan',
        'ko': 'Korean, Korea'
    }

    try:
        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: An error occurred while sending request\n> __Error__: `{str(e)}`', delete_after=5)
        return

    if res.status_code == 200:
        res_json = res.json()
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_id = res_json['id']
        avatar_id = res_json['avatar']
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
        phone_number = res_json['phone']
        email = res_json['email']
        mfa_enabled = res_json['mfa_enabled']
        flags = res_json['flags']
        locale = res_json['locale']
        verified = res_json['verified']
        days_left = ""
        language = languages.get(locale)
        creation_date = datetime.datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
        has_nitro = False

        try:
            nitro_res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
            nitro_res.raise_for_status()
            nitro_data = nitro_res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                d2 = datetime.datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                days_left = abs((d2 - d1).days)
        except requests.exceptions.RequestException as e:
            pass

        try:
            embed = f"""**TOKEN INFORMATIONS | Prefix: `{prefix}`**\n
        > :dividers: __Basic Information__\n\tUsername: `{user_name}`\n\tUser ID: `{user_id}`\n\tCreation Date: `{creation_date}`\n\tAvatar URL: `{avatar_url if avatar_id else "None"}`
        > :crystal_ball: __Nitro Information__\n\tNitro Status: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`
        > :incoming_envelope: __Contact Information__\n\tPhone Number: `{phone_number if phone_number else "None"}`\n\tEmail: `{email if email else "None"}`
        > :shield: __Account Security__\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tFlags: `{flags}`
        > :paperclip: __Other__\n\tLocale: `{locale} ({language})`\n\tEmail Verified: `{verified}`"""

            await ctx.send(embed, file=discord.File("img/astraa.gif"))
        except Exception as e:
            await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: `{str(e)}`', delete_after=5)
    else:
        await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: Invalid token', delete_after=5)

@bot.command()
async def cleardm(ctx, amount: str="1"):
    await ctx.message.delete()

    if not amount.isdigit():
        await ctx.send(f'> **[**ERROR**]**: Invalid amount specified. It must be a number.\n> __Command__: `{config["prefix"]}cleardm <amount>`', delete_after=5)
        return

    amount = int(amount)

    if amount <= 0 or amount > 100:
        await ctx.send(f'> **[**ERROR**]**: Amount must be between 1 and 100.', delete_after=5)
        return

    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in DMs.', delete_after=5)
        return

    deleted_count = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == bot.user:
            try:
                await message.delete()
                deleted_count += 1
            except discord.Forbidden:
                await ctx.send(f'> **[**ERROR**]**: Missing permissions to delete messages.', delete_after=5)
                return
            except discord.HTTPException as e:
                await ctx.send(f'> **[**ERROR**]**: An error occurred while deleting messages: {str(e)}', delete_after=5)
                return

    await ctx.send(f'> **Cleared {deleted_count} messages in DMs.**', delete_after=5)

@bot.command()
async def msgclr(ctx, amount: str="10"):
    await ctx.message.delete()

    if not amount.isdigit():
        await ctx.send(f'> **[**ERROR**]**: Invalid amount specified. It must be a number.\n> __Command__: `{config["prefix"]}msgclr <amount>`', delete_after=5)
        return

    amount = int(amount)

    if amount <= 0:
        await ctx.send(f'> **[**ERROR**]**: Amount must be greater than 0.', delete_after=5)
        return

    # Limite máximo para evitar detecção - máximo 50 mensagens por vez
    if amount > 50:
        await ctx.send(f'> **[**ERROR**]**: Maximum amount is 50 to avoid detection.', delete_after=5)
        return

    deleted_count = 0
    errors = 0
    
    # Status message para mostrar progresso
    status_msg = await ctx.send(f'> **Starting message cleanup...** Target: {amount} messages')

    try:
        async for message in ctx.channel.history(limit=200):  # Busca mais mensagens para encontrar as suas
            if message.author == bot.user and message.id != status_msg.id:
                try:
                    await message.delete()
                    deleted_count += 1
                    
                    # Atualiza status a cada 5 mensagens deletadas
                    if deleted_count % 5 == 0:
                        await status_msg.edit(content=f'> **Deleting messages...** Progress: {deleted_count}/{amount}')
                    
                    # Delay entre deletions para evitar rate limit (1-2 segundos)
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    
                    if deleted_count >= amount:
                        break
                        
                except discord.Forbidden:
                    errors += 1
                    continue
                except discord.HTTPException:
                    errors += 1
                    # Increase delay if hitting rate limits
                    await asyncio.sleep(random.uniform(3.0, 5.0))
                    continue
                except discord.NotFound:
                    # Message already deleted
                    continue

        # Final status
        await status_msg.edit(content=f'> **Cleanup completed!** Deleted: {deleted_count} messages | Errors: {errors}')
        await asyncio.sleep(3)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit(content=f'> **[**ERROR**]**: An error occurred: {str(e)}')
        await asyncio.sleep(5)
        await status_msg.delete()


@bot.command(aliases=['hs'])
async def hypesquad(ctx, house: str=None):
    await ctx.message.delete()

    if not house:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `hypesquad <house>`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json'}

    try:
        r = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Invalid status code\n> __Error__: `{str(e)}`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
    payload = {}
    if house == "bravery":
        payload = {'house_id': 1}
    elif house == "brilliance":
        payload = {'house_id': 2}
    elif house == "balance":
        payload = {'house_id': 3}
    else:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Error__: Hypesquad house must be one of the following: `bravery`, `brilliance`, `balance`', delete_after=5)
        return

    try:
        r = requests.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        r.raise_for_status()

        if r.status_code == 204:
            await ctx.send(f'> Hypesquad House changed to `{house}`!')

    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to change Hypesquad house\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['ginfo'])
async def guildinfo(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    date_format = "%a, %d %b %Y %I:%M %p"
    embed = f"""> **GUILD INFORMATIONS | Prefix: `{prefix}`**
:dividers: __Basic Information__
Server Name: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nCreation Date: `{ctx.guild.created_at.strftime(date_format)}`\nServer Icon: `{ctx.guild.icon.url if ctx.guild.icon.url else 'None'}`\nServer Owner: `{ctx.guild.owner}`
:page_facing_up: __Other Information__
`{len(ctx.guild.members)}` Members\n`{len(ctx.guild.roles)}` Roles\n`{len(ctx.guild.text_channels) if ctx.guild.text_channels else 'None'}` Text-Channels\n`{len(ctx.guild.voice_channels) if ctx.guild.voice_channels else 'None'}` Voice-Channels\n`{len(ctx.guild.categories) if ctx.guild.categories else 'None'}` Categories"""
    
    await ctx.send(embed)

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()

    await ctx.send(f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}")

@bot.command()
async def whremove(ctx, webhook: str=None):
    await ctx.message.delete()

    if not webhook:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}whremove <webhook>`', delete_after=5)
        return
    
    try:
        requests.delete(webhook.rstrip())
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to delete webhook\n> __Error__: `{str(e)}`', delete_after=5)
        return
    
    await ctx.send(f'> Webhook has been deleted!')

@bot.command(aliases=['whcreate'])
async def webhook(ctx, name: str=None, avatar_url: str=None):
    await ctx.message.delete()

    if not name:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}webhook <name> [avatar_url]`', delete_after=5)
        return

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_webhooks:
        await ctx.send("> **[**ERROR**]**: You do not have permission to manage webhooks", delete_after=5)
        return

    try:
        if avatar_url:
            avatar_response = requests.get(avatar_url)
            avatar_data = avatar_response.content if avatar_response.status_code == 200 else None
        else:
            avatar_data = None

        webhook = await ctx.channel.create_webhook(name=name, avatar=avatar_data)
        await ctx.send(f'> **Webhook created successfully!**\n> Name: `{webhook.name}`\n> URL: `{webhook.url}`')
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to create webhook\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['whlist'])
async def webhooks(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_webhooks:
        await ctx.send("> **[**ERROR**]**: You do not have permission to view webhooks", delete_after=5)
        return

    try:
        webhooks = await ctx.channel.webhooks()
        
        if not webhooks:
            await ctx.send("> **No webhooks found in this channel**", delete_after=5)
            return

        webhook_list = f"**WEBHOOKS IN #{ctx.channel.name} | Prefix: `{prefix}`**\n\n"
        
        for i, webhook in enumerate(webhooks, 1):
            webhook_list += f"> **{i}.** `{webhook.name}`\n"
            webhook_list += f"    ID: `{webhook.id}`\n"
            webhook_list += f"    URL: `{webhook.url}`\n"
            webhook_list += f"    Created by: `{webhook.user.name if webhook.user else 'Unknown'}`\n\n"

        await ctx.send(webhook_list)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to list webhooks\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['whsend'])
async def webhooksend(ctx, webhook_url: str=None, *, message: str=None):
    await ctx.message.delete()

    if not webhook_url or not message:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}webhooksend <webhook_url> <message>`', delete_after=5)
        return

    try:
        data = {
            "content": message,
            "username": bot.user.name,
            "avatar_url": str(bot.user.avatar.url) if bot.user.avatar else None
        }
        
        response = requests.post(webhook_url, json=data)
        
        if response.status_code == 204:
            await ctx.send("> **Message sent successfully via webhook!**", delete_after=5)
        else:
            await ctx.send(f'> **[**ERROR**]**: Failed to send message\n> __Status Code__: `{response.status_code}`', delete_after=5)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to send webhook message\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['whedit'])
async def webhookedit(ctx, webhook_url: str=None, name: str=None, avatar_url: str=None):
    await ctx.message.delete()

    if not webhook_url:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}webhookedit <webhook_url> [name] [avatar_url]`', delete_after=5)
        return

    if not name and not avatar_url:
        await ctx.send(f'> **[**ERROR**]**: You must provide either a name or avatar URL to edit', delete_after=5)
        return

    try:
        data = {}
        
        if name:
            data["name"] = name
        
        if avatar_url:
            avatar_response = requests.get(avatar_url)
            if avatar_response.status_code == 200:
                import base64
                avatar_b64 = base64.b64encode(avatar_response.content).decode('utf-8')
                data["avatar"] = f"data:image/png;base64,{avatar_b64}"
        
        response = requests.patch(webhook_url, json=data)
        
        if response.status_code == 200:
            await ctx.send("> **Webhook edited successfully!**", delete_after=5)
        else:
            await ctx.send(f'> **[**ERROR**]**: Failed to edit webhook\n> __Status Code__: `{response.status_code}`', delete_after=5)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to edit webhook\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['whslist'])
async def whserverlist(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_webhooks:
        await ctx.send("> **[**ERROR**]**: You do not have permission to view webhooks", delete_after=5)
        return

    try:
        all_webhooks = []
        total_webhooks = 0
        
        for channel in ctx.guild.text_channels:
            try:
                webhooks = await channel.webhooks()
                if webhooks:
                    all_webhooks.append((channel, webhooks))
                    total_webhooks += len(webhooks)
            except Exception:
                pass

        if total_webhooks == 0:
            await ctx.send("> **No webhooks found in this server**", delete_after=5)
            return

        webhook_list = f"**ALL WEBHOOKS IN {ctx.guild.name} | Total: {total_webhooks} | Prefix: `{prefix}`**\n\n"
        
        for channel, webhooks in all_webhooks:
            webhook_list += f"**#{channel.name}** ({len(webhooks)} webhook{'s' if len(webhooks) > 1 else ''})\n"
            
            for i, webhook in enumerate(webhooks, 1):
                webhook_list += f"    **{i}.** `{webhook.name}`\n"
                webhook_list += f"        ID: `{webhook.id}`\n"
                webhook_list += f"        URL: `{webhook.url}`\n"
                webhook_list += f"        Created by: `{webhook.user.name if webhook.user else 'Unknown'}`\n"
            
            webhook_list += "\n"

        # Split message if too long
        if len(webhook_list) > 2000:
            parts = []
            current_part = ""
            for line in webhook_list.split('\n'):
                if len(current_part + line + '\n') > 1950:
                    parts.append(current_part)
                    current_part = line + '\n'
                else:
                    current_part += line + '\n'
            if current_part:
                parts.append(current_part)
            
            for part in parts:
                await ctx.send(part)
        else:
            await ctx.send(webhook_list)

    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to list server webhooks\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def whjson(ctx, webhook_url: str=None, json_file: str=None):
    await ctx.message.delete()

    if not webhook_url or not json_file:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}whjson <webhook_url> <file.json>`', delete_after=5)
        return

    if not json_file.endswith('.json'):
        await ctx.send(f'> **[**ERROR**]**: File must be a .json file', delete_after=5)
        return

    try:
        # Check if file exists
        if not os.path.exists(json_file):
            await ctx.send(f'> **[**ERROR**]**: File `{json_file}` not found', delete_after=5)
            return

        # Read and parse JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Send the JSON data to webhook
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(webhook_url, json=json_data, headers=headers)
        
        if response.status_code == 204:
            await ctx.send(f"> **JSON message sent successfully via webhook!**\n> File: `{json_file}`", delete_after=5)
        else:
            await ctx.send(f'> **[**ERROR**]**: Failed to send JSON message\n> __Status Code__: `{response.status_code}`\n> __Response__: `{response.text}`', delete_after=5)

    except json.JSONDecodeError as e:
        await ctx.send(f'> **[**ERROR**]**: Invalid JSON format in file\n> __Error__: `{str(e)}`', delete_after=5)
    except FileNotFoundError:
        await ctx.send(f'> **[**ERROR**]**: File `{json_file}` not found', delete_after=5)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to send JSON webhook message\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['hide'])
async def hidemention(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}hidemention <message>`', delete_after=5)
        return
    
    await ctx.send(content + ('||\u200b||' * 200) + '@everyone')

@bot.command()
async def edit(ctx, *, content: str=None):
    await ctx.message.delete()
    
    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}edit <message>`', delete_after=5)
        return
    
    text = await ctx.send(content)

    await text.edit(content=f"\u202b{content}")

@bot.command(aliases=['911'])
async def airplane(ctx):
    await ctx.message.delete()

    frames = [
        f''':man_wearing_turban::airplane:\t\t\t\t:office:''',
        f''':man_wearing_turban:\t:airplane:\t\t\t:office:''',
        f''':man_wearing_turban:\t\t::airplane:\t\t:office:''',
        f''':man_wearing_turban:\t\t\t:airplane:\t:office:''',
        f''':man_wearing_turban:\t\t\t\t:airplane::office:''',
        ''':boom::boom::boom:''']
    
    sent_message = await ctx.send(frames[0])

    for frame in frames[1:]:
        await asyncio.sleep(0.5)
        await sent_message.edit(content=frame)

@bot.command(aliases=['mine'])
async def minesweeper(ctx, size: int=5):
    await ctx.message.delete()

    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for _ in range(size - 1)]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
    m_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    message_to_send = "**Click to play**:\n"

    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offsets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message_to_send += tile
        message_to_send += "\n"

    await ctx.send(message_to_send)

@bot.command(aliases=['leet'])
async def leetspeak(ctx, *, content: str):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `leetspeak <message>`", delete_after=5)
        return

    content = content.replace('a', '4').replace('A', '4').replace('e', '3').replace('E', '3').replace('i', '1').replace('I', '1').replace('o', '0').replace('O', '0').replace('t', '7').replace('T', '7').replace('b', '8').replace('B', '8')
    await ctx.send(content)

@bot.command()
async def dick(ctx, user: str=None):
    await ctx.message.delete()

    if not user:
        user = ctx.author.display_name

    size = random.randint(1, 15)
    dong = "=" * size

    await ctx.send(f"> **{user}**'s Dick size\n8{dong}D")

@bot.command()
async def reverse(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `reverse <message>`", delete_after=5)
        return

    content = content[::-1]
    await ctx.send(content)

@bot.command(aliases=['fetch'])
async def fetchmembers(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in a server.', delete_after=5)
        return
    
    members = ctx.guild.members
    member_data = []

    for member in members:
        member_info = {
            "name": member.name,
            "id": str(member.id),
            "avatar_url": str(member.avatar.url) if member.avatar else str(member.default_avatar.url),
            "discriminator": member.discriminator,
            "status": str(member.status),
            "joined_at": str(member.joined_at)
        }
        member_data.append(member_info)

    with open("members_list.json", "w", encoding="utf-8") as f:
        json.dump(member_data, f, indent=4)

    await ctx.send("> List of members:", file=discord.File("members_list.json"))

    os.remove("members_list.json")

@bot.command()
async def spam(ctx, amount: int=1, *, message_to_send: str="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    try:
        if amount <= 0 or amount > 9:
            await ctx.send("> **[**ERROR**]**: Amount must be between 1 and 9", delete_after=5)
            return
        for _ in range(amount):
            await ctx.send(message_to_send)
    except ValueError:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `spam <amount> <message>`', delete_after=5)

@bot.command(aliases=['gicon'])
async def guildicon(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} icon :**\n{ctx.guild.icon.url if ctx.guild.icon else '*NO ICON*'}")

@bot.command(aliases=['gbanner'])
async def guildbanner(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} banner :**\n{ctx.guild.banner.url if ctx.guild.banner else '*NO BANNER*'}")

@bot.command(aliases=['grename'])
async def guildrename(ctx, *, name: str=None):
    await ctx.message.delete()

    if not name:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `guildrename <name>`", delete_after=5)
        return

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.guild.me.guild_permissions.manage_guild:
        await ctx.send(f'> **[**ERROR**]**: Missing permissions', delete_after=5)
        return
    
    try:
        await ctx.guild.edit(name=name)
        await ctx.send(f"> Server renamed to '{name}'")
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to rename the server\n> __Error__: `{str(e)}`, delete_after=5')

@bot.command()
async def purge(ctx, num_messages: int=1):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("> **[**ERROR**]**: You do not have permission to delete messages", delete_after=5)
        return
    
    if 1 <= num_messages <= 100:
        deleted_messages = await ctx.channel.purge(limit=num_messages)
        await ctx.send(f"> **{len(deleted_messages)}** messages have been deleted", delete_after=5)
    else:
        await ctx.send("> **[**ERROR**]**: The number must be between 1 and 100", delete_after=5)

@bot.command(aliases=['autor'])
async def autoreply(ctx, command: str, user: discord.User=None):
    await ctx.message.delete()

    if command not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid input. Use `ON` or `OFF`.\n> __Command__: `autoreply ON|OFF [@user]`", delete_after=5)
        return

    if command.upper() == "ON":
        if user:
            if str(user.id) not in config["autoreply"]["users"]:
                config["autoreply"]["users"].append(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply enabled for user {user.mention}.**", delete_after=5)
        else:
            if str(ctx.channel.id) not in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].append(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been enabled in this channel**", delete_after=5)
    elif command.upper() == "OFF":
        if user:
            if str(user.id) in config["autoreply"]["users"]:
                config["autoreply"]["users"].remove(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply disabled for user {user.mention}**", delete_after=5)
        else:
            if str(ctx.channel.id) in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].remove(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been disabled in this channel**", delete_after=5)

@bot.command(aliases=['remote'])
async def remoteuser(ctx, action: str=None, user: discord.User=None):
    await ctx.message.delete()
    
    if not action or action.upper() not in ["ADD", "REMOVE"]:
        await ctx.send(
            f"> **[ERROR]**: Invalid action. Use `ADD` or `REMOVE`.\n"
            f"> __Command__: `{prefix}remoteuser ADD|REMOVE <@user>`",
            delete_after=5
        )
        return
    
    if not user:
        await ctx.send(
            f"> **[ERROR]**: Please specify a user.\n"
            f"> __Command__: `{prefix}remoteuser ADD|REMOVE <@user>`",
            delete_after=5
        )
        return
    
    if action.upper() == "ADD":
        if str(user.id) not in config["remote-users"]:
            config["remote-users"].append(str(user.id))
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> Added {user.mention} to remote users.", delete_after=5)
        else:
            await ctx.send(f"> {user.mention} is already a remote user.", delete_after=5)
    
    elif action.upper() == "REMOVE":
        if str(user.id) in config["remote-users"]:
            config["remote-users"].remove(str(user.id))
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> Removed {user.mention} from remote users.", delete_after=5)
        else:
            await ctx.send(f"> {user.mention} is not a remote user.", delete_after=5)

@bot.command()
async def afk(ctx, status: str, *, message: str=None):
    await ctx.message.delete()

    if status not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `afk ON|OFF <message>`", delete_after=5)
        return

    if status.upper() == "ON":
        if not config["afk"]["enabled"]:
            config["afk"]["enabled"] = True
            if message:
                config["afk"]["message"] = message
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> **AFK mode enabled.** Message: `{config['afk']['message']}`", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is already enabled", delete_after=5)
    elif status.upper() == "OFF":
        if config["afk"]["enabled"]:
            config["afk"]["enabled"] = False
            save_config(config)
            selfbot_menu(bot)
            await ctx.send("> **AFK mode disabled.** Welcome back!", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is not currently enabled", delete_after=5)

@bot.command(aliases=["prefix"])
async def changeprefix(ctx, *, new_prefix: str=None):
    await ctx.message.delete()

    if not new_prefix:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `changeprefix <prefix>`", delete_after=5)
        return
    
    config['prefix'] = new_prefix
    save_config(config)
    selfbot_menu(bot)
    
    bot.command_prefix = new_prefix

    await ctx.send(f"> Prefix updated to `{new_prefix}`", delete_after=5)

@bot.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()

    msg = await ctx.send("> Shutting down...")
    await asyncio.sleep(2)

    await msg.delete()
    await bot.close()

@bot.command()
async def clear(ctx):
    await ctx.message.delete()

    await ctx.send('ﾠﾠ' + '\n' * 200 + 'ﾠﾠ')

@bot.command()
async def sendall(ctx, *, message="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return
    
    channels = ctx.guild.text_channels
    success_count = 0
    failure_count = 0
    
    try:        
        for channel in channels:
            try:
                await channel.send(message)
                success_count += 1
            except Exception as e:
                failure_count += 1
        await ctx.send(f"> {success_count} message(s) sent successfully, {failure_count} failed to send", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[**ERROR**]**: An error occurred: `{e}`", delete_after=5)

@bot.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, action: str=None, user: discord.User=None):
    await ctx.message.delete()
    
    if action not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return
    
    if not user:
        await ctx.send(f"> **[**ERROR**]**: Please specify a user to copy.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return
    
    if action == "ON":
        if user.id not in config['copycat']['users']:
            config['copycat']['users'].append(user.id)
            save_config(config)
            await ctx.send(f"> Now copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` is already being copied.", delete_after=5)
    
    elif action == "OFF":
        if user.id in config['copycat']['users']:
            config['copycat']['users'].remove(user.id)
            save_config(config)
            await ctx.send(f"> Stopped copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` was not being copied.", delete_after=5)

@bot.command()
async def firstmessage(ctx):
    await ctx.message.delete()
    
    try:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}"
            await ctx.send(f"> Here is the link to the first message: {link}", delete_after=5)
            break
        else:
            await ctx.send("> **[ERROR]**: No messages found in this channel.", delete_after=5)
    
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while fetching the first message. `{e}`", delete_after=5)

@bot.command()
async def ascii(ctx, *, message=None):
    await ctx.message.delete()
    
    if not message:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `ascii <message>`", delete_after=5)
        return
    
    try:
        ascii_art = pyfiglet.figlet_format(message)
        await ctx.send(f"```\n{ascii_art}\n```", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while generating the ASCII art. `{e}`", delete_after=5)

@bot.command()
async def autoreact(ctx, channel_id: str=None, server_id: str=None, emoji: str=None):
    await ctx.message.delete()
    
    if not channel_id or not emoji:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `autoreact <channel_id> [server_id] <emoji>`", delete_after=5)
        return
    
    if not channel_id.isdigit():
        await ctx.send(f"> **[**ERROR**]**: Channel ID must be a number", delete_after=5)
        return
    
    if server_id and not server_id.isdigit():
        if emoji is None:
            emoji = server_id
            server_id = None
        else:
            await ctx.send(f"> **[**ERROR**]**: Server ID must be a number", delete_after=5)
            return
    
    # Get channel and server names for display
    try:
        channel = bot.get_channel(int(channel_id))
        channel_name = channel.name if channel else f"Unknown Channel ({channel_id})"
        
        if server_id:
            guild = bot.get_guild(int(server_id))
            server_name = guild.name if guild else f"Unknown Server ({server_id})"
            server_text = f" in server **{server_name}**"
        else:
            if channel and channel.guild:
                server_name = channel.guild.name
                server_text = f" in server **{server_name}**"
            else:
                server_text = ""
    except:
        channel_name = f"Unknown Channel ({channel_id})"
        server_text = f" in server {server_id}" if server_id else ""
    
    target = {
        "channel_id": channel_id,
        "server_id": server_id,
        "emoji": emoji
    }
    
    if target not in config["autoreact"]["targets"]:
        config["autoreact"]["targets"].append(target)
        save_config(config)
        await ctx.send(f"> **Added autoreact target**: Channel **#{channel_name}**{server_text} with emoji {emoji}", delete_after=5)
    else:
        await ctx.send(f"> **Target already exists**", delete_after=5)

@bot.command()
async def areact(ctx, status: str=None):
    await ctx.message.delete()
    
    if status not in ["true", "false"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid status. Use `true` or `false`.\n> __Command__: `areact <true/false>`", delete_after=5)
        return
    
    config["autoreact"]["enabled"] = status == "true"
    save_config(config)
    
    status_text = "enabled" if config["autoreact"]["enabled"] else "disabled"
    await ctx.send(f"> **Autoreact {status_text}**", delete_after=5)

@bot.command()
async def ablacklist(ctx, action: str=None, user: str=None):
    await ctx.message.delete()
    
    if action not in ["list", "add", "remove"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `list`, `add`, or `remove`.\n> __Command__: `ablacklist <list/add/remove> [@user/user-id/user-nickname]`", delete_after=5)
        return
    
    if action == "list":
        if not config["autoreact"]["blacklist"]:
            await ctx.send(f"> **Autoreact blacklist is empty**", delete_after=5)
        else:
            blacklist_text = "\n".join([f"• {user_id}" for user_id in config["autoreact"]["blacklist"]])
            await ctx.send(f"> **Autoreact blacklist**:\n{blacklist_text}", delete_after=10)
        return
    
    if not user:
        await ctx.send(f"> **[**ERROR**]**: Please specify a user", delete_after=5)
        return
    
    # Extract user ID from mention or use as is
    user_id = user.strip("<@!>")
    
    if action == "add":
        if user_id not in config["autoreact"]["blacklist"]:
            config["autoreact"]["blacklist"].append(user_id)
            save_config(config)
            await ctx.send(f"> **Added {user_id} to autoreact blacklist**", delete_after=5)
        else:
            await ctx.send(f"> **User already in blacklist**", delete_after=5)
    
    elif action == "remove":
        if user_id in config["autoreact"]["blacklist"]:
            config["autoreact"]["blacklist"].remove(user_id)
            save_config(config)
            await ctx.send(f"> **Removed {user_id} from autoreact blacklist**", delete_after=5)
        else:
            await ctx.send(f"> **User not in blacklist**", delete_after=5)

@bot.command()
async def aconfig(ctx):
    await ctx.message.delete()
    
    status = "Enabled" if config["autoreact"]["enabled"] else "Disabled"
    targets_count = len(config["autoreact"]["targets"])
    blacklist_count = len(config["autoreact"]["blacklist"])
    react_own = "Yes" if config["autoreact"]["react_to_own"] else "No"
    
    # Build targets list with server and channel names
    targets_text = ""
    if config["autoreact"]["targets"]:
        targets_text = "\n"
        for i, target in enumerate(config["autoreact"]["targets"], 1):
            try:
                channel = bot.get_channel(int(target['channel_id']))
                channel_name = channel.name if channel else f"Unknown Channel"
                
                if target.get("server_id"):
                    guild = bot.get_guild(int(target['server_id']))
                    server_name = guild.name if guild else f"Unknown Server"
                    server_text = f" in {server_name}"
                else:
                    if channel and channel.guild:
                        server_name = channel.guild.name
                        server_text = f" in {server_name}"
                    else:
                        server_text = " (Any Server)"
            except:
                channel_name = f"Unknown Channel"
                server_text = f" (Server ID: {target.get('server_id', 'Any')})"
            
            targets_text += f"    • #{channel_name}{server_text} - {target['emoji']}\n"
    
    config_text = f"""**AUTOREACT CONFIGURATION | Prefix: `{prefix}`**

> :gear: __Status__: `{status}`
> :dart: __Active Targets__ (`{targets_count}`): {targets_text if targets_text else "`None`"}
> :no_entry_sign: __Blacklisted Users__: `{blacklist_count}`
> :mirror: __React to Own Messages__: `{react_own}`"""
    
    await ctx.send(config_text, delete_after=15)

@bot.command()
async def panicreact(ctx):
    await ctx.message.delete()
    
    config["autoreact"]["enabled"] = False
    config["autoreact"]["targets"] = []
    config["autoreact"]["blacklist"] = []
    config["autoreact"]["react_to_own"] = False
    save_config(config)
    
    await ctx.send(f"> **PANIC MODE**: All autoreact configurations cleared!", delete_after=5)

@bot.command()
async def reactservers(ctx):
    await ctx.message.delete()
    
    if not config["autoreact"]["targets"]:
        await ctx.send(f"> **No autoreact targets configured**", delete_after=5)
        return
    
    targets_text = ""
    for i, target in enumerate(config["autoreact"]["targets"], 1):
        try:
            channel = bot.get_channel(int(target['channel_id']))
            channel_name = channel.name if channel else f"Unknown Channel"
            
            if target.get("server_id"):
                guild = bot.get_guild(int(target['server_id']))
                server_name = guild.name if guild else f"Unknown Server"
                server_text = f" in {server_name}"
            else:
                if channel and channel.guild:
                    server_name = channel.guild.name
                    server_text = f" in {server_name}"
                else:
                    server_text = " (Any Server)"
        except:
            channel_name = f"Unknown Channel"
            server_text = f" (Server ID: {target.get('server_id', 'Any')})"
        
        targets_text += f"{i}. #{channel_name}{server_text} - {target['emoji']}\n"
    
    await ctx.send(f"**AUTOREACT TARGETS**:\n```{targets_text}```", delete_after=10)

@bot.command()
async def myignore(ctx, status: str=None):
    await ctx.message.delete()
    
    if status not in ["true", "false"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid status. Use `true` or `false`.\n> __Command__: `myignore <true/false>`", delete_after=5)
        return
    
    config["autoreact"]["react_to_own"] = status == "true"
    save_config(config)
    
    status_text = "will" if config["autoreact"]["react_to_own"] else "will not"
    await ctx.send(f"> **Your own messages {status_text} be reacted to**", delete_after=5)

@bot.command()
async def playing(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `playing <status>`", delete_after=5)
        return
    
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"> Successfully set the game status to `{status}`", delete_after=5)
    
@bot.command()
async def watching(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `watching <status>`", delete_after=5)
        return
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
    await ctx.send(f"> Successfully set the watching status to `{status}`", delete_after=5)    
    
@bot.command()
async def streaming(ctx, status: str=None, url: str="https://twitch.tv/"):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `streaming <status> [url]`", delete_after=5)
        return
    
    # Create a button that links to the stream
    stream_button = f"[Watch Stream]({url})"
    
    # Set the streaming activity
    await bot.change_presence(
        activity=discord.Streaming(
            name=status,
            url=url
        )
    )
    
    # Send a message with the stream info and button
    await ctx.send(
        f"> **Now streaming**: {status}\n"
        f"> **Stream URL**: {url}\n"
        f"> {stream_button}",
        delete_after=10
    )
    
@bot.command(aliases=["stopstreaming", "stopstatus", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()

    await bot.change_presence(activity=None, status=discord.Status.dnd)

@bot.command()
async def dmall(ctx, *, message: str="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    members = [m for m in ctx.guild.members if not m.bot]
    total_members = len(members)
    estimated_time = round(total_members * 4.5)

    await ctx.send(f">Starting DM process for `{total_members}` members.\n> Estimated time: `{estimated_time} seconds` (~{round(estimated_time / 60, 2)} minutes)", delete_after=10)

    success_count = 0
    fail_count = 0

    for member in members:
        try:
            await member.send(message)
            success_count += 1
        except Exception:
            fail_count += 1

        await asyncio.sleep(random.uniform(3, 6))

    await ctx.send(f"> **[**INFO**]**: DM process completed.\n> Successfully sent: `{success_count}`\n> Failed: `{fail_count}`", delete_after=10)

@bot.command()
async def autocmd(ctx, bot_id: str=None, command: str=None, delay: str=None, *, args: str=None):
    await ctx.message.delete()
    
    if not bot_id or not command or not delay:
        await ctx.send(
            f"> **[ERROR]**: Invalid command.\n"
            f"> __Usage__: `{prefix}autocmd <bot-id> <command> <delay_seconds> [args]`\n"
            f"> Example: `{prefix}autocmd 123456789 ping 5` (sends `</ping:123456789>` every 5 seconds)\n"
            f"> Example: `{prefix}autocmd 987654321 say 10 Hello!` (sends `</say:987654321> Hello!` every 10 sec)",
            delete_after=10
        )
        return
    
    try:
        delay = float(delay)
        if delay <= 0:
            raise ValueError("Delay must be greater than 0")
    except ValueError:
        await ctx.send(f"> **[ERROR]**: Invalid delay. Must be a number > 0.", delete_after=5)
        return
    
    # Store autocmd tasks (now with bot_id tracking)
    if not hasattr(bot, 'autocmd_tasks'):
        bot.autocmd_tasks = {}
    
    # Cancel existing task for this channel
    task_key = f"{ctx.channel.id}-{bot_id}"
    if task_key in bot.autocmd_tasks:
        bot.autocmd_tasks[task_key].cancel()
    
    # Create new task
    async def autocmd_task():
        try:
            while True:
                # Create proper slash command syntax with bot ID
                slash_cmd = f"</{command}:{bot_id}>"
                if args:
                    slash_cmd += f" {args}"
                
                # Send the command
                await ctx.channel.send(slash_cmd)
                
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            pass  # Task was cancelled
        except Exception as e:
            await ctx.send(f"> **[ERROR]**: Autocmd failed: `{str(e)}`", delete_after=5)
    
    task = bot.loop.create_task(autocmd_task())
    bot.autocmd_tasks[task_key] = task
    
    await ctx.send(
        f"> **Autocmd started**:\n"
        f"> Bot: `<@{bot_id}>`\n"
        f"> Command: `</{command}:{bot_id}>{' ' + args if args else ''}`\n"
        f"> Interval: `{delay}` seconds\n"
        f"> Use `{prefix}stopautocmd {bot_id}` to cancel",
        delete_after=10
    )

@bot.command()
async def stopautocmd(ctx, bot_id: str=None):
    await ctx.message.delete()
    
    if not bot_id:
        await ctx.send(
            f"> **[ERROR]**: Please specify which bot to stop\n"
            f"> __Usage__: `{prefix}stopautocmd <bot-id>`\n"
            f"> Use `{prefix}listautocmd` to see running commands",
            delete_after=10
        )
        return
    
    task_key = f"{ctx.channel.id}-{bot_id}"
    
    if not hasattr(bot, 'autocmd_tasks') or task_key not in bot.autocmd_tasks:
        await ctx.send(f"> **[ERROR]**: No autocmd running for bot `<@{bot_id}>` in this channel", delete_after=5)
        return
    
    bot.autocmd_tasks[task_key].cancel()
    del bot.autocmd_tasks[task_key]
    
    await ctx.send(f"> **Stopped autocmd** for bot `<@{bot_id}>`", delete_after=5)

@bot.command()
async def listautocmd(ctx):
    await ctx.message.delete()
    
    if not hasattr(bot, 'autocmd_tasks') or not bot.autocmd_tasks:
        await ctx.send("> No active autocmd tasks running", delete_after=5)
        return
    
    message = "> **Active Autocmd Tasks**:\n"
    
    for task_key in bot.autocmd_tasks:
        channel_id, bot_id = task_key.split("-")
        if int(channel_id) == ctx.channel.id:
            message += f"- Bot: `<@{bot_id}>` (in this channel)\n"
    
    if message == "> **Active Autocmd Tasks**:\n":
        message = "> No active autocmd tasks in this channel"
    
    await ctx.send(message, delete_after=10)
    

# Automod protection
@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)
    
    # Automod protection
    if message.author.id == bot.user.id:
        return
    
    # Check if message is targeting our autocmd bots
    if hasattr(bot, 'autocmd_tasks'):
        for task_key in list(bot.autocmd_tasks.keys()):
            _, bot_id = task_key.split("-")
            if f"<@{bot_id}>" in message.content or f"</" in message.content:
                # Add your automod logic here
                if "stop" in message.content.lower() or "cancel" in message.content.lower():
                    await message.delete()
                    warning = await message.channel.send(
                        f"> {message.author.mention} Don't interfere with autocmd processes!",
                        delete_after=5
                    )
                    await asyncio.sleep(5)
                    await warning.delete()                    
                  
import aiohttp
import io
from PIL import Image  # For image handling if needed

@bot.command(aliases=['servercopy'])
async def copyserver(ctx, server_id: int = None):
    try:
        await ctx.message.delete()
    except:
        pass
    
    if not server_id:
        return await ctx.send(f"> **[ERROR]**: Please specify a server ID.\n> __Command__: `{prefix}copyserver <server-id>`", delete_after=10)
    
    progress_msg = None
    try:
        progress_msg = await ctx.send("> Starting server copy process...")
        
        # Get target server
        target_guild = bot.get_guild(server_id)
        if not target_guild:
            return await progress_msg.edit(content="> **[ERROR]**: Server not found or bot is not in that server.")
        
        # Download server icon
        icon_bytes = None
        if target_guild.icon:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(target_guild.icon.with_format('png').url)) as resp:
                        if resp.status == 200:
                            icon_bytes = await resp.read()
            except Exception as e:
                await ctx.send(f"> [WARNING] Failed to download server icon: {str(e)}", delete_after=5)
        
        # Create new server
        new_guild_name = f"Copy of {target_guild.name}"[:32]  # Max 32 characters
        await progress_msg.edit(content=f"> Creating new server: `{new_guild_name}`...")
        
        try:
            if icon_bytes:
                new_guild = await bot.create_guild(new_guild_name, icon=icon_bytes)
                await progress_msg.edit(content=f"> Created server with icon: `{new_guild.name}`")
            else:
                new_guild = await bot.create_guild(new_guild_name)
                await progress_msg.edit(content=f"> Created server without icon: `{new_guild.name}`")
        except Exception as e:
            return await progress_msg.edit(content=f"> **[ERROR]**: Failed to create server: {str(e)}")
        
        # Copy server settings
        await progress_msg.edit(content="> Copying server settings...")
        try:
            await new_guild.edit(
                verification_level=target_guild.verification_level,
                explicit_content_filter=target_guild.explicit_content_filter,
                afk_timeout=target_guild.afk_timeout,
                system_channel_flags=target_guild.system_channel_flags
            )
        except Exception as e:
            await ctx.send(f"> [WARNING] Failed to copy some settings: {str(e)}", delete_after=5)
        
        # Initialize counters for the report
        roles_created = 0
        text_channels_created = 0
        voice_channels_created = 0
        
        # Copy roles (skip @everyone)
        await progress_msg.edit(content="> Copying roles...")
        for role in sorted(target_guild.roles, key=lambda r: r.position, reverse=True):
            if role.name == "@everyone":
                continue
                
            try:
                await new_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                roles_created += 1
                await asyncio.sleep(1)  # Delay to prevent rate limits
            except Exception as e:
                await ctx.send(f"> [WARNING] Failed to create role {role.name}: {str(e)}", delete_after=5)
        
        # Copy channels with delays
        await progress_msg.edit(content="> Copying channels (this may take a while due to rate limits)...")
        for category in target_guild.categories:
            try:
                new_category = await new_guild.create_category_channel(
                    name=category.name,
                    position=category.position,
                    overwrites=category.overwrites
                )
                await asyncio.sleep(2)  # Delay after creating a category
                
                for channel in category.channels:
                    try:
                        if isinstance(channel, discord.TextChannel):
                            await new_guild.create_text_channel(
                                name=channel.name,
                                position=channel.position,
                                topic=channel.topic,
                                slowmode_delay=channel.slowmode_delay,
                                nsfw=channel.nsfw,
                                category=new_category,
                                overwrites=channel.overwrites
                            )
                            text_channels_created += 1
                        elif isinstance(channel, discord.VoiceChannel):
                            await new_guild.create_voice_channel(
                                name=channel.name,
                                position=channel.position,
                                bitrate=channel.bitrate,
                                user_limit=channel.user_limit,
                                category=new_category,
                                overwrites=channel.overwrites
                            )
                            voice_channels_created += 1
                        await asyncio.sleep(1)  # Delay between channel creations
                    except Exception as e:
                        await ctx.send(f"> [WARNING] Failed to create channel {channel.name}: {str(e)}", delete_after=5)
            except Exception as e:
                await ctx.send(f"> [WARNING] Failed to create category {category.name}: {str(e)}", delete_after=5)
        
        # Create invite
        invite_url = "Failed to create"
        try:
            invite = await new_guild.text_channels[0].create_invite(max_age=0, max_uses=0)
            invite_url = str(invite)
        except Exception as e:
            await ctx.send(f"> [WARNING] Failed to create invite: {str(e)}", delete_after=5)
        
        # Final report
        report = f"""**SERVER COPY COMPLETE**
> Original: {target_guild.name} ({target_guild.id})
> New: {new_guild.name} ({new_guild.id})
> 
> **Copied Elements:**
> - Server icon: {'✅' if icon_bytes else '❌'}
> - Server settings: ✅
> - Roles: {roles_created}/{len(target_guild.roles)-1}
> - Channels: {text_channels_created + voice_channels_created}/{len(target_guild.channels)}
> 
> Invite: {invite_url if invite_url else 'Failed to create'}"""
        
        await progress_msg.edit(content=report)
        
    except Exception as e:
        if progress_msg:
            await progress_msg.edit(content=f"> **[ERROR]**: Server copy failed: {str(e)}")
        else:
            await ctx.send(f"> **[ERROR]**: Server copy failed: {str(e)}", delete_after=10)
            
@bot.command()
async def autolog(ctx, action: str=None, source_channel: str=None, target_channel: str=None):
    await ctx.message.delete()
    
    if not action or action.upper() not in ["ON", "OFF", "LIST"]:
        await ctx.send(
            f"> **[ERROR]**: Invalid command.\n"
            f"> __Usage__:\n"
            f"> `{prefix}autolog ON <source-channel-id> <target-channel-id>` - Enable logging\n"
            f"> `{prefix}autolog OFF <source-channel-id>` - Disable logging\n"
            f"> `{prefix}autolog LIST` - Show active loggers",
            delete_after=10
        )
        return
    
    if action.upper() == "LIST":
        if not config["autolog"]["log_pairs"]:
            await ctx.send("> No active message loggers configured", delete_after=5)
            return
        
        log_list = "> **Active Message Loggers**:\n"
        for pair in config["autolog"]["log_pairs"]:
            source_ch = bot.get_channel(int(pair["source"]))
            target_ch = bot.get_channel(int(pair["target"]))
            
            source_name = f"#{source_ch.name}" if source_ch else f"Unknown Channel ({pair['source']})"
            target_name = f"#{target_ch.name}" if target_ch else f"Unknown Channel ({pair['target']})"
            
            log_list += f"- From {source_name} to {target_name}\n"
        
        await ctx.send(log_list, delete_after=15)
        return
    
    if not source_channel or not source_channel.isdigit():
        await ctx.send(f"> **[ERROR]**: Invalid source channel ID", delete_after=5)
        return
    
    if action.upper() == "ON":
        if not target_channel or not target_channel.isdigit():
            await ctx.send(f"> **[ERROR]**: Invalid target channel ID", delete_after=5)
            return
        
        # Check if this source is already being logged
        for pair in config["autolog"]["log_pairs"]:
            if pair["source"] == source_channel:
                await ctx.send(f"> **[ERROR]**: This channel is already being logged", delete_after=5)
                return
        
        # Add new log pair
        config["autolog"]["log_pairs"].append({
            "source": source_channel,
            "target": target_channel
        })
        
        # Enable autolog if not already enabled
        if not config["autolog"]["enabled"]:
            config["autolog"]["enabled"] = True
        
        save_config(config)
        
        source_ch = bot.get_channel(int(source_channel))
        target_ch = bot.get_channel(int(target_channel))
        
        source_name = f"#{source_ch.name}" if source_ch else f"Channel {source_channel}"
        target_name = f"#{target_ch.name}" if target_ch else f"Channel {target_channel}"
        
        await ctx.send(
            f"> **Message logging enabled**\n"
            f"> From: {source_name}\n"
            f"> To: {target_name}",
            delete_after=10
        )
    
    elif action.upper() == "OFF":
        # Remove all pairs with this source channel
        removed = False
        config["autolog"]["log_pairs"] = [
            pair for pair in config["autolog"]["log_pairs"] 
            if pair["source"] != source_channel
        ]
        
        # Disable autolog if no more pairs exist
        if not config["autolog"]["log_pairs"]:
            config["autolog"]["enabled"] = False
        
        save_config(config)
        
        source_ch = bot.get_channel(int(source_channel))
        source_name = f"#{source_ch.name}" if source_ch else f"Channel {source_channel}"
        
        await ctx.send(
            f"> **Message logging disabled** for {source_name}",
            delete_after=10
        )

@bot.event
async def on_message_delete(message):
    if not config["autolog"]["enabled"] or message.author.bot:
        return
    
    # Find if this channel is being logged
    for pair in config["autolog"]["log_pairs"]:
        if str(message.channel.id) == pair["source"]:
            target_channel = bot.get_channel(int(pair["target"]))
            if not target_channel:
                continue
            
            # Create embed with deleted message info
            embed = discord.Embed(
                title="🗑️ Message Deleted",
                description=message.content,
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            
            embed.set_author(
                name=f"{message.author.name}#{message.author.discriminator}",
                icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
            )
            
            embed.add_field(name="Channel", value=f"<#{message.channel.id}>", inline=True)
            embed.add_field(name="Message ID", value=message.id, inline=True)
            
            # Add attachments if any
            if message.attachments:
                attachment_urls = "\n".join([att.url for att in message.attachments])
                embed.add_field(name="Attachments", value=attachment_urls, inline=False)
            
            try:
                await target_channel.send(embed=embed)
            except Exception:
                pass  # Silently fail if we can't send to the target channel  
                
@bot.command(aliases=['mcserver'])
async def mcserverinfo(ctx, address: str, port: str="25565"):
    await ctx.message.delete()
    
    try:
        port = int(port)
        if not 1 <= port <= 65535:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError:
        await ctx.send("> **[ERROR]**: Invalid port number. Must be between 1-65535", delete_after=5)
        return

    # Show initial loading message
    loading_msg = await ctx.send(f"> Querying Minecraft server `{address}:{port}`...")

    try:
        # Use aiohttp for async HTTP request to Minecraft server
        async with aiohttp.ClientSession() as session:
            # First try with SRV record resolution
            try:
                resolved = await asyncio.get_event_loop().getaddrinfo(
                    address, port, 
                    type=socket.SOCK_STREAM, 
                    proto=socket.IPPROTO_TCP
                )
                ip_addr = resolved[0][4][0]
            except socket.gaierror:
                ip_addr = address

            # Create TCP connection with timeout
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip_addr, port),
                timeout=10
            )

            # Send handshake packet
            handshake = bytearray()
            handshake.extend(b'\x00')  # Packet ID
            handshake.extend(b'\x04')  # Protocol version (varint 4)
            handshake.extend(len(address).to_bytes(1, 'big'))  # Address length
            handshake.extend(address.encode('utf-8'))  # Address
            handshake.extend(port.to_bytes(2, 'big'))  # Port
            handshake.extend(b'\x01')  # Next state (status)

            # Prepend length
            packet = bytearray(len(handshake).to_bytes(1, 'big'))
            packet.extend(handshake)

            writer.write(packet)
            await writer.drain()

            # Send status request
            writer.write(b'\x01\x00')
            await writer.drain()

            # Read response length
            length = await asyncio.wait_for(read_varint(reader), timeout=5)
            
            # Read packet ID
            packet_id = await asyncio.wait_for(read_varint(reader), timeout=5)
            if packet_id != 0x00:
                raise ValueError("Invalid packet ID received")

            # Read JSON response length
            json_length = await asyncio.wait_for(read_varint(reader), timeout=5)
            
            # Read JSON data
            json_data = await asyncio.wait_for(reader.read(json_length), timeout=5)
            server_info = json.loads(json_data.decode('utf-8'))

            # Send ping packet (for latency measurement)
            ping_time = time.time()
            ping_payload = int(ping_time * 1000).to_bytes(8, 'big', signed=True)
            writer.write(b'\x01\x00' + ping_payload)
            await writer.drain()

            # Read pong response
            await asyncio.wait_for(read_varint(reader), timeout=5)  # Length
            await asyncio.wait_for(read_varint(reader), timeout=5)  # Packet ID
            pong_time = await asyncio.wait_for(reader.read(8), timeout=5)
            pong_time = int.from_bytes(pong_time, 'big', signed=True)
            latency_ms = int((time.time() - ping_time) * 1000)

            writer.close()
            await writer.wait_closed()

        # Parse server info
        motd = server_info.get('description', {}).get('text', 'No MOTD')
        if isinstance(server_info.get('description'), str):
            motd = server_info.get('description', 'No MOTD')
        
        version = server_info.get('version', {}).get('name', 'Unknown')
        protocol = server_info.get('version', {}).get('protocol', -1)
        
        players = server_info.get('players', {})
        online = players.get('online', 0)
        max_players = players.get('max', 0)
        player_list = players.get('sample', [])
        
        favicon = server_info.get('favicon', None)
        
        # Create embed
        embed = discord.Embed(
            title=f"🟢 {address}:{port}",
            description=f"**{motd}**",
            color=0x00FF00 if online > 0 else 0xFF0000,
            timestamp=datetime.datetime.utcnow()
        )
        
        # Server info
        embed.add_field(
            name="📊 Server Info",
            value=(
                f"**Version:** {version} (Protocol {protocol})\n"
                f"**Players:** {online}/{max_players}\n"
                f"**Latency:** {latency_ms}ms\n"
                f"**Address:** `{address}:{port}`"
            ),
            inline=True
        )
        
        # Player list (if available)
        if player_list and len(player_list) > 0:
            player_names = [f"• {p['name']}" for p in player_list[:10]]  # Show max 10 players
            if len(player_list) > 10:
                player_names.append(f"... and {len(player_list) - 10} more")
            embed.add_field(
                name=f"👥 Online Players ({len(player_list)})",
                value="\n".join(player_names),
                inline=True
            )
        
        # Server icon (if available)
        if favicon:
            try:
                # Decode base64 favicon (data:image/png;base64,...)
                favicon_data = favicon.split(',')[1]
                favicon_bytes = base64.b64decode(favicon_data)
                
                # Save to temp file
                with open("temp_favicon.png", "wb") as f:
                    f.write(favicon_bytes)
                
                # Attach to embed
                file = discord.File("temp_favicon.png", filename="server_icon.png")
                embed.set_thumbnail(url="attachment://server_icon.png")
                
                await loading_msg.delete()
                await ctx.send(file=file, embed=embed)
                
                # Clean up
                os.remove("temp_favicon.png")
                return
            except Exception as e:
                print(f"Failed to process favicon: {e}")
        
        await loading_msg.delete()
        await ctx.send(embed=embed)
        
    except asyncio.TimeoutError:
        await loading_msg.edit(content=f"> **[ERROR]**: Connection timed out for `{address}:{port}`")
    except ConnectionRefusedError:
        await loading_msg.edit(content=f"> **[ERROR]**: Connection refused by `{address}:{port}`")
    except socket.gaierror:
        await loading_msg.edit(content=f"> **[ERROR]**: Could not resolve hostname `{address}`")
    except Exception as e:
        await loading_msg.edit(content=f"> **[ERROR]**: Failed to query server - `{str(e)}`")

async def read_varint(reader):
    data = 0
    for i in range(5):
        byte = await reader.read(1)
        if not byte:
            raise IOError("Unexpected end of stream")
        byte = byte[0]
        data |= (byte & 0x7F) << 7*i
        if not byte & 0x80:
            return data
    raise IOError("VarInt too big")               
    
@bot.command()
async def restart(ctx):
    await ctx.message.delete()
    
    # Send a message indicating the restart
    msg = await ctx.send("> **Restarting selfbot...**")
    await asyncio.sleep(2)
    
    # Close the bot connection
    await bot.close()
    
    # Restart the script
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(aliases=['anumber'])
async def autonumber(ctx, action: str=None, arg1: str=None, arg2: str=None, arg3: str=None, arg4: str=None):
    await ctx.message.delete()
    
    # Initialize autonumber config if it doesn't exist
    if "autonumber" not in config:
        config["autonumber"] = {
            "enabled": False,
            "targets": []  # Each target will store channel_id, server_id, direction, status
        }
        save_config(config)
    
    # Helper function to find target index
    def find_target(channel_id, server_id=None):
        for i, target in enumerate(config["autonumber"]["targets"]):
            if target["channel_id"] == channel_id and (server_id is None or target.get("server_id") == server_id):
                return i
        return -1
    
    # LIST command
    if action and action.lower() == "list":
        if not config["autonumber"]["targets"]:
            await ctx.send("> No active autonumber targets configured", delete_after=5)
            return
        
        target_list = "> **Active Autonumber Targets**:\n"
        for i, target in enumerate(config["autonumber"]["targets"], 1):
            channel = bot.get_channel(int(target["channel_id"]))
            server = bot.get_guild(int(target["server_id"])) if target.get("server_id") else None
            
            channel_name = f"#{channel.name}" if channel else f"Unknown Channel ({target['channel_id']})"
            server_name = f" in {server.name}" if server else ""
            direction = target.get("direction", "up").capitalize()
            status = "Enabled" if target.get("status", "true").lower() == "true" else "Disabled"
            
            target_list += f"{i}. {channel_name}{server_name} | Direction: {direction} | Status: {status}\n"
        
        await ctx.send(target_list, delete_after=15)
        return
    
    # CONFIG command
    elif action and action.lower() == "config":
        enabled_targets = sum(1 for t in config["autonumber"]["targets"] if t.get("status", "true").lower() == "true")
        disabled_targets = len(config["autonumber"]["targets"]) - enabled_targets
        
        config_msg = f"""**Autonumber Configuration**:
> Global Status: {'Enabled' if config["autonumber"]["enabled"] else 'Disabled'}
> Active Targets: {enabled_targets}
> Inactive Targets: {disabled_targets}
> Total Targets: {len(config["autonumber"]["targets"])}"""
        
        await ctx.send(config_msg, delete_after=10)
        return
    
    # PANIC command
    elif action and action.lower() == "panic":
        if arg1 and arg1.lower() == "confirm":
            config["autonumber"] = {
                "enabled": False,
                "targets": []
            }
            save_config(config)
            await ctx.send("> **PANIC MODE**: All autonumber configurations have been reset!", delete_after=5)
        else:
            await ctx.send("> Please confirm with `.autonumber panic confirm` to reset all settings", delete_after=5)
        return
    
    # HERE command
    elif action and action.lower() == "here":
        if not ctx.guild:
            await ctx.send("> This command can only be used in a server", delete_after=5)
            return
        
        if not arg1 or arg1.lower() not in ["on", "off"]:
            await ctx.send("> Usage: `.autonumber here <on/off> [up/down]`", delete_after=5)
            return
        
        direction = arg2.lower() if arg2 and arg2.lower() in ["up", "down"] else "up"
        status = arg1.lower() == "on"
        
        # Check if target already exists
        target_index = find_target(str(ctx.channel.id), str(ctx.guild.id))
        
        if target_index == -1 and status:
            # Add new target
            config["autonumber"]["targets"].append({
                "channel_id": str(ctx.channel.id),
                "server_id": str(ctx.guild.id),
                "direction": direction,
                "status": str(status).lower()
            })
            config["autonumber"]["enabled"] = True
            save_config(config)
            await ctx.send(f"> Autonumber enabled in this channel (Direction: {direction})", delete_after=5)
        elif target_index != -1:
            # Update existing target
            if status:
                config["autonumber"]["targets"][target_index].update({
                    "direction": direction,
                    "status": str(status).lower()
                })
                await ctx.send(f"> Autonumber updated in this channel (Direction: {direction})", delete_after=5)
            else:
                config["autonumber"]["targets"].pop(target_index)
                await ctx.send("> Autonumber disabled in this channel", delete_after=5)
            save_config(config)
        return
    
    # ADD/REMOVE commands
    elif action and action.lower() in ["add", "remove"]:
        if not arg1 or not arg1.isdigit():
            await ctx.send("> Please provide a valid channel ID", delete_after=5)
            return
        
        channel_id = arg1
        server_id = arg2 if arg2 and arg2.isdigit() else None
        direction = arg3.lower() if arg3 and arg3.lower() in ["up", "down"] else "up"
        
        if action.lower() == "add":
            # Check if target already exists
            if find_target(channel_id, server_id) != -1:
                await ctx.send("> This channel is already configured for autonumber", delete_after=5)
                return
            
            config["autonumber"]["targets"].append({
                "channel_id": channel_id,
                "server_id": server_id,
                "direction": direction,
                "status": "true"
            })
            config["autonumber"]["enabled"] = True
            save_config(config)
            
            channel = bot.get_channel(int(channel_id))
            channel_name = f"#{channel.name}" if channel else f"Channel {channel_id}"
            await ctx.send(f"> Added autonumber to {channel_name} (Direction: {direction})", delete_after=5)
        
        else:  # remove
            target_index = find_target(channel_id, server_id)
            if target_index == -1:
                await ctx.send("> No autonumber configuration found for this channel", delete_after=5)
                return
            
            config["autonumber"]["targets"].pop(target_index)
            if not config["autonumber"]["targets"]:
                config["autonumber"]["enabled"] = False
            save_config(config)
            
            channel = bot.get_channel(int(channel_id))
            channel_name = f"#{channel.name}" if channel else f"Channel {channel_id}"
            await ctx.send(f"> Removed autonumber from {channel_name}", delete_after=5)
        return
    
    # Standard configuration (channel_id, server_id, direction, on/off)
    elif action and action.isdigit():
        channel_id = action
        server_id = arg1 if arg1 and arg1.isdigit() else None
        direction = arg2.lower() if arg2 and arg2.lower() in ["up", "down"] else "up"
        status = arg3.lower() == "on" if arg3 else True
        
        # Check if target already exists
        target_index = find_target(channel_id, server_id)
        
        if target_index == -1:
            # Add new target
            config["autonumber"]["targets"].append({
                "channel_id": channel_id,
                "server_id": server_id,
                "direction": direction,
                "status": str(status).lower()
            })
            config["autonumber"]["enabled"] = True
            save_config(config)
            
            channel = bot.get_channel(int(channel_id))
            channel_name = f"#{channel.name}" if channel else f"Channel {channel_id}"
            await ctx.send(f"> Autonumber {'enabled' if status else 'disabled'} for {channel_name} (Direction: {direction})", delete_after=5)
        else:
            # Update existing target
            config["autonumber"]["targets"][target_index].update({
                "direction": direction,
                "status": str(status).lower()
            })
            save_config(config)
            
            channel = bot.get_channel(int(channel_id))
            channel_name = f"#{channel.name}" if channel else f"Channel {channel_id}"
            await ctx.send(f"> Autonumber updated for {channel_name} (Direction: {direction}, Status: {'enabled' if status else 'disabled'})", delete_after=5)
        return
    
    # Invalid command
    await ctx.send(f"""**Autonumber Command Usage**:
> `.autonumber <channel-id> [server-id] [up/down] [on/off]` - Configure autonumber
> `.autonumber here <on/off> [up/down]` - Configure for current channel
> `.autonumber add <channel-id> [server-id] [up/down]` - Add target
> `.autonumber remove <channel-id> [server-id]` - Remove target
> `.autonumber list` - List all targets
> `.autonumber config` - Show configuration
> `.autonumber panic confirm` - Reset all settings""", delete_after=15)

@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)
    
    # Check if autonumber is enabled and message is not from bot
    if (not config.get("autonumber", {}).get("enabled", False) or 
        message.author == bot.user or 
        not message.content.strip().isdigit()):
        return
    
    # Check if message is in a target channel
    for target in config["autonumber"].get("targets", []):
        if (str(message.channel.id) == target["channel_id"] and 
            target.get("status", "true").lower() == "true" and
            (not target.get("server_id") or str(message.guild.id) == target["server_id"])):
            
            try:
                number = int(message.content.strip())
                direction = target.get("direction", "up")
                
                if direction == "up":
                    response = str(number + 1)
                else:
                    response = str(number - 1)
                
                await message.channel.send(response)
            except Exception as e:
                print(f"Autonumber error: {e}")
            break

@bot.command(name='count')
async def count(ctx, *, args: str = None):
    try:
        await ctx.message.delete()
    except:
        pass
    
    if args is None:
        await ctx.send("> Use `.count 1 to 10`", delete_after=3)
        return
    
    try:
        parts = args.split()
        if len(parts) != 3 or parts[1].lower() != 'to':
            raise ValueError
        
        first = int(parts[0])
        second = int(parts[2])
    except:
        await ctx.send("> Invalid format. Use `.count {first} to {second}`", delete_after=3)
        return

    # Check if counting is already running anywhere
    if hasattr(bot, 'active_count'):
        await ctx.send("> Count already running in another channel (use .stopcount)", delete_after=3)
        return
    
    if first == second:
        await ctx.send("> Numbers can't be equal", delete_after=3)
        return
    
    # Store active count information
    bot.active_count = {
        'task': None,
        'channel': ctx.channel,
        'guild': ctx.guild,
        'running': True
    }
    
    # Create counting task
    async def counting_task():
        current = first
        step = 1 if first < second else -1
        
        try:
            while bot.active_count['running']:
                # Random delay between 1.1-1.5 seconds
                await asyncio.sleep(random.uniform(1.1, 1.5))
                
                # Check completion
                if (step > 0 and current > second) or (step < 0 and current < second):
                    break
                
                try:
                    await ctx.channel.send(str(current))
                except discord.HTTPException as e:
                    if e.status == 429:  # Rate limited
                        await asyncio.sleep(e.retry_after + 1)
                        continue
                    break
                
                current += step
        except:
            pass
        finally:
            if hasattr(bot, 'active_count'):
                del bot.active_count
    
    # Start the task
    bot.active_count['task'] = bot.loop.create_task(counting_task())
    await ctx.send(f"> Counting started: {first} → {second}", delete_after=3)

@bot.command()
async def stopcount(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    if not hasattr(bot, 'active_count'):
        await ctx.send("> No count is currently running", delete_after=3)
        return
    
    # Stop the count from anywhere
    bot.active_count['running'] = False
    bot.active_count['task'].cancel()
    
    # Notify in the original channel if possible
    try:
        original_channel = bot.active_count['channel']
        if original_channel != ctx.channel:
            await original_channel.send("> Count was stopped remotely", delete_after=3)
    except:
        pass
    
    del bot.active_count
    await ctx.send("> Stopped the active count", delete_after=3)

@bot.command(name='count2')
async def count2(ctx, channel_id: str = None, server_id: str = None, direction: str = "up", status: str = "on"):
    try:
        await ctx.message.delete()
    except:
        pass
    
    # Validate inputs
    if not channel_id or not channel_id.isdigit():
        await ctx.send("> Please provide a valid channel ID", delete_after=5)
        return
    
    if not server_id or not server_id.isdigit():
        await ctx.send("> Please provide a valid server ID", delete_after=5)
        return
    
    direction = direction.lower()
    if direction not in ["up", "down"]:
        await ctx.send("> Direction must be 'up' or 'down'", delete_after=5)
        return
    
    status = status.lower()
    if status not in ["on", "off"]:
        await ctx.send("> Status must be 'on' or 'off'", delete_after=5)
        return
    
    # Get the target channel
    target_guild = bot.get_guild(int(server_id))
    if not target_guild:
        await ctx.send("> Server not found or bot is not in that server", delete_after=5)
        return
    
    target_channel = target_guild.get_channel(int(channel_id))
    if not target_channel:
        await ctx.send("> Channel not found in the specified server", delete_after=5)
        return
    
    # Initialize active_counts if it doesn't exist
    if not hasattr(bot, 'active_counts'):
        bot.active_counts = {}
    
    # If status is off, stop counting in this channel
    if status == "off":
        if channel_id in bot.active_counts:
            bot.active_counts[channel_id]['running'] = False
            bot.active_counts[channel_id]['task'].cancel()
            del bot.active_counts[channel_id]
            await ctx.send(f"> Stopped counting in <#{channel_id}>", delete_after=5)
        else:
            await ctx.send("> No counting is running in this channel", delete_after=5)
        return
    
    # Check if counting is already running in this channel
    if channel_id in bot.active_counts:
        await ctx.send("> Counting is already running in this channel", delete_after=5)
        return
    
    # Start counting in the target channel
    current_number = 1 if direction == "up" else 100  # Default starting numbers
    
    # Try to find the last number in the channel
    try:
        async for message in target_channel.history(limit=1):
            if message.content.isdigit():
                current_number = int(message.content)
                if direction == "up":
                    current_number += 1
                else:
                    current_number -= 1
    except:
        pass
    
    # Create counting task with rate limit bypass
    async def counting_task():
        nonlocal current_number
        try:
            while True:
                if not hasattr(bot, 'active_counts') or channel_id not in bot.active_counts:
                    break
                
                if not bot.active_counts[channel_id]['running']:
                    break
                
                # Send the number with error handling
                try:
                    await target_channel.send(str(current_number))
                except discord.HTTPException as e:
                    if e.status == 429:  # Rate limited
                        # Random delay between 5-10 seconds when rate limited
                        delay = random.uniform(5, 10)
                        await asyncio.sleep(delay)
                        continue
                    break
                except:
                    break
                
                # Update number based on direction
                if direction == "up":
                    current_number += 1
                else:
                    current_number -= 1
                
                # Random delay between 1.5-3 seconds to avoid rate limits
                await asyncio.sleep(random.uniform(1.5, 3))
                
        except Exception as e:
            print(f"Count2 error: {e}")
        finally:
            if hasattr(bot, 'active_counts') and channel_id in bot.active_counts:
                del bot.active_counts[channel_id]
    
    # Store the counting task
    bot.active_counts[channel_id] = {
        'task': bot.loop.create_task(counting_task()),
        'running': True,
        'direction': direction,
        'channel': target_channel
    }
    
    await ctx.send(f"> Started counting {'up' if direction == 'up' else 'down'} in <#{channel_id}>", delete_after=5)

@bot.command()
async def stopcount2(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    if not hasattr(bot, 'active_counts') or not bot.active_counts:
        await ctx.send("> No counting is currently running", delete_after=5)
        return
    
    # Stop all counting tasks
    stopped_channels = []
    for channel_id, count_data in list(bot.active_counts.items()):
        count_data['running'] = False
        count_data['task'].cancel()
        stopped_channels.append(channel_id)
    
    # Clear all counts
    bot.active_counts.clear()
    
    if stopped_channels:
        channels_list = ", ".join([f"<#{cid}>" for cid in stopped_channels])
        await ctx.send(f"> Stopped counting in: {channels_list}", delete_after=5)
    else:
        await ctx.send("> No counting was running", delete_after=5) 
bot.run(token)            