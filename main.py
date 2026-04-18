import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

#from pytube import Search, YouTube

import random  # add this import
from telegram.ext import MessageHandler, filters
import aiohttp
with open("roasts.txt", "r", encoding="utf-8") as f:
    ROAST_LINES = f.read().splitlines()

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://official-joke-api.appspot.com/random_joke") as response:
                if response.status == 200:
                    data = await response.json()
                    setup = data["setup"]
                    punchline = data["punchline"]
                    joke_text = f"{setup}\n{punchline}"
                else:
                    joke_text = "😅 I'm not in the mood."

        if update.message.reply_to_message:
            await update.message.reply_to_message.reply_text(joke_text)
        else:
            await update.message.reply_text(joke_text)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")





# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")

# /start command
# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Yo! Casanova bot is live 😎\n\n"
        "📖 Here’s what I can do:\n"
        "/joke - Get a random joke 😂\n"
        "If you use /joke while replying to someone’s message,\n" 
        "the bot will reply to that message with a joke.\n"
        "/pickup - Get a pickup line \n"
        "/roast - for roast someone \n"
        "/compliment - for compliment to someone \n"
        "Same rule — use /pickup in reply to a message, and the bot will send a pickup line as a reply. 😉\n"
        "/translate <msg> - it will translate any language and also hinglish msg in english lang.\n"
        "/talk <message> - Casanova repeats your message\n"
        "Just chat normally - Auto reply is off for now\n\n"
        "Tip: Reply to a message with /joke or /pickup to send it directly as a reply!"
    )
    await update.message.reply_text(help_text)




async def pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.popcat.xyz/pickuplines") as response:
                if response.status == 200:
                    data = await response.json()
                    line = data["pickupline"]
                else:
                    line = "I'm not in the mood right now 😅"
    except Exception as e:
        line = f"Error fetching pickup line: {e}"

    sender_name = update.message.from_user.first_name

    if update.message.reply_to_message:
        text = f"{sender_name} says: {line}"
        await update.message.reply_to_message.reply_text(text)
    else:
        await update.message.reply_text(f"{sender_name} says: {line}")


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()


    if "hi" in msg or "hello" in msg:
        await update.message.reply_text("Hey buddy, how’s it going?")
    elif "bye" in msg or "byy" in msg:
        await update.message.reply_text("leaving already? That was quick.")
    elif "lol" in msg or "lmao" in msg:
        await update.message.reply_text("Hahaahahah 😂")

    elif "aven" in msg:
        await update.message.reply_text("Aven please reply bruh")

    elif "hey" in msg or "hyy" in msg:
        await update.message.reply_text("hey, wassup buddy")

    elif "casanova" in msg:
        await update.message.reply_text("Go on.. I've got your attention.")
    elif "wassup" in msg or "hru" in msg or "wbu" in msg or "how are you" in msg:
        await update.message.reply_text("I'm cool, wbu?")

    elif "gay" in msg or "you are gay" in msg:
         await update.message.reply_text("I'm lesbian - I like gurls.")

    elif "fine" in msg:
         await update.message.reply_text("Fine is good, but not exciting 😄 tell me something better.")

    elif "love" in msg:
         await update.message.reply_text("No-one loves you except me , Did you get that?")
    
    else:
        # Random human-like reply from file (20% chance)
        if random.randint(1, 10) <= 0:
            try:
                with open("replies.txt", "r", encoding="utf-8") as f:
                    human_replies = f.read().splitlines()
                reply = random.choice(human_replies)
                await update.message.reply_text(reply)
            except Exception:
                await update.message.reply_text("Bro, I’m speechless rn 😅")
        else:
            print(f"Casanova ignored: {msg}")

    

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.replace("/translate", "").strip()

    if not msg:
        await update.message.reply_text("Bro, give me some text to translate 😅")
        return

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.popcat.xyz/translate?to=en&text={msg}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    translated = data["translated"]
                    detected_lang = data.get("lang", "unknown")
                    await update.message.reply_text(
                        f"Detected language: {detected_lang}\nEnglish: {translated}"
                    )
                else:
                    await update.message.reply_text("😅 I'm not in the mood bruh.")
    except Exception as e:
        await update.message.reply_text(f"Error translating: {e}")



async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Try API first
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.popcat.xyz/roast") as response:
                if response.status == 200:
                    data = await response.json()
                    roast_line = data["roast"]
                else:
                    roast_line = random.choice(ROAST_LINES)
    except Exception:
        # If API fails → fallback to file
        roast_line = random.choice(ROAST_LINES)

    if update.message.reply_to_message:
        sender_name = update.message.from_user.first_name
        text = f"{sender_name} says: {roast_line}"
        await update.message.reply_to_message.reply_text(text)
    else:
        await update.message.reply_text(roast_line)


async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fallback_compliments = [
        "You light up the room 🌟",
        "Your smile is contagious 😁",
        "You’re smarter than you think 🧠",
        "You make people feel special 💖",
        "You’re a vibe ✨",
        "You have a great sense of humor 😂",
        "You’re more talented than you realize 🎨",
        "You make everything better just by being there 🌈",
        "You’re someone people can count on 🤝",
        "You’re cooler than the other side of the pillow ❄️"
    ]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.popcat.xyz/compliment") as response:
                if response.status == 200:
                    data = await response.json()
                    compliment_line = data["compliment"]
                else:
                    compliment_line = random.choice(fallback_compliments)
    except Exception:
        compliment_line = random.choice(fallback_compliments)

    if update.message.reply_to_message:
        sender_name = update.message.from_user.first_name
        text = f"{sender_name} says: {compliment_line}"
        await update.message.reply_to_message.reply_text(text)
    else:
        await update.message.reply_text(compliment_line)


    # Agar user ne kisi message pe reply karke /compliment likha hai
   


# /talk command
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.replace("/talk", "").strip()

    if not msg:
        reply = "Bro, Casanova says nothing 😶"
    else:
        reply = f"Bro, Casanova says: {msg}"

    await update.message.reply_text(reply)

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Exception: {context.error}")
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text("I think, therefore I'm")



# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("talk", talk))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("pickup", pickup))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(CommandHandler("roast", roast))
    app.add_handler(CommandHandler("compliment", compliment))

    
    #app.add_handler(CommandHandler("compliment", compliment))
    




    

    print("Casanova bot is running...")
    app.run_polling()
    
    
