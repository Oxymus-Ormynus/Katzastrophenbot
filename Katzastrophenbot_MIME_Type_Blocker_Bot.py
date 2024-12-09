import discord
from discord.ext import commands
# Siehe Zeile 7-8 // from dotenv import load_dotenv
import os
import mimetypes
from Keep_the_Katzastrophe_alive import keep_alive

# Lade .env-Datei
# <- Hash entfernen, wenn BOT_TOKEN lokal liegt // load_dotenv(dotenv_path="Katzastrophentoken")

# Token abrufen aus .env-Datei, liegt ebenso bei Replit!!!  
TOKEN = os.getenv("BOT_TOKEN")

# Liste erlaubter MIME-Typen (für Nutzer ohne Sonderrolle)
ERLAUBTE_MIME_TYPS = [
    # Bilder
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp', 'image/tiff', 'image/svg+xml', 'image/heif', 'image/heic',

    # Audioformate
    'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac',

    # Videoformate
    'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/3gpp',

    # Dokumente (PDF, TXT)
    'application/pdf',
    'text/plain',
]

# Diese Rolle darf uneingeschränkt Dateien hochladen
SONDERROLLE = "Mod"  

# Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Filter für unerwünschte Dateien
@bot.event
async def on_message(message):
    if message.author.bot:  # Bots werden ignoriert
        return

    # Prüfe, ob der Nutzer die Sonderrolle hat
    roles = getattr(message.author, "roles", [])
    hat_sonderrolle = any(role.name == SONDERROLLE for role in roles)

    # Überspringe Prüfung, wenn User Sonderrolle hat
    if hat_sonderrolle:
        return

    # Prüfe die Anhänge der Nachricht
    for attachment in message.attachments:
        # MIME-Type Bestimmung
        mime_type, _ = mimetypes.guess_type(attachment.filename)

        # Wenn der MIME-Typ nicht in den erlaubten MIME-Typen ist
        if mime_type not in ERLAUBTE_MIME_TYPS:
            try:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, Achtung - es droht eine Katzastrophe! :Panic: Dieser Dateityp ist leider nicht erlaubt! Miau :Sus:")
            except discord.Forbidden:
                print(f"Achtung, Katzastrophe! :Panic: Anhang nicht ausführen! Berechtigung zum Löschen der Nachricht von {message.author.name} fehlt. :Sus:")
            break

# Starte Flask-Server, dann Bot
if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("Error: BOT_TOKEN nicht gefunden. Überprüfe die Katzastrophentoken-Datei.")
