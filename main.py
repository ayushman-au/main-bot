import os
import random
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load env
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8000))

if not TOKEN:
    raise ValueError("TOKEN is missing")

# -------- SAFE FILE LOAD --------
try:
    with open("roasts.txt", "r", encoding="utf-8") as f:
        ROAST_LINES = f.read().splitlines()
except:
    ROAST_LINES = ["You're not stupid… just creatively wrong 😂"]

try:
    with open("replies.txt", "r", encoding="utf-8") as f:
        HUMAN_REPLIES = f.read().splitlines()
except:
    HUMAN_REPLIES = ["Hmm", "Nice", "Okay", "Bruh 😂"]

# -------- COMMANDS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Casanova Bot is live 😎\n\n"
        "/joke\n/pickup\n/roast\n/compliment\n/translate <text>\n/talk <msg>"
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://official-joke-api.appspot.com/random_joke") as res:
                data = await res.json()
                text = f"{data['setup']}\n{data['punchline']}"
    except:
        text = "No jokes today 😅"

    await update.message.reply_text(text)

async def pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.popcat.xyz/pickuplines") as res:
                data = await res.json()
                line = data["pickupline"]
    except:
        line = "You're already a 10 😉"

    await update.message.reply_text(line)

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    line = random.choice(ROAST_LINES)

    if update.message.reply_to_message:
        name = update.message.reply_to_message.from_user.first_name
        await update.message.reply_text(f"{name}, {line}")
    else:
        await update.message.reply_text(line)

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    compliments = [
        "You’re amazing ✨",
        "You have great vibes 😎",
        "You’re smarter than you think 🧠",
    ]
    await update.message.reply_text(random.choice(compliments))

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.replace("/translate", "").strip()

    if not msg:
        await update.message.reply_text("Give text to translate 😅")
        return

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.popcat.xyz/translate?to=en&text={msg}"
            async with session.get(url) as res:
                data = await res.json()
                await update.message.reply_text(data["translated"])
    except:
        await update.message.reply_text("Translation failed 😅")

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.replace("/talk", "").strip()
    await update.message.reply_text(msg if msg else "Say something 😶")

# -------- AUTO REPLY --------

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    msg = update.message.text.lower()

    if "hi" in msg or "hello" in msg:
        await update.message.reply_text("Hey 👋")

    elif "bye" in msg:
        await update.message.reply_text("Bye 👋")

    elif "lol" in msg:
        await update.message.reply_text("😂😂")

    else:
        if random.randint(1, 10) == 1:
            await update.message.reply_text(random.choice(HUMAN_REPLIES))

# -------- ERROR --------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("Error:", context.error)

# -------- MAIN --------

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("pickup", pickup))
    app.add_handler(CommandHandler("roast", roast))
    app.add_handler(CommandHandler("compliment", compliment))
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(CommandHandler("talk", talk))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    app.add_error_handler(error_handler)

    print("Bot running...")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
