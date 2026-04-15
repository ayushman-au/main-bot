import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

#from pytube import Search, YouTube

import random  # add this import
from telegram.ext import MessageHandler, filters
import requests

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            data = response.json()
            setup = data["setup"]
            punchline = data["punchline"]
            joke_text = f"{setup}\n{punchline}"

            # Agar user ne kisi message ko reply kiya hai
            if update.message.reply_to_message:
                await update.message.reply_to_message.reply_text(joke_text)
            else:
                # Normal case: direct joke
                await update.message.reply_text(joke_text)
        else:
            await update.message.reply_text("😅 Sorry bro, joke API is down rn.")
    except Exception as e:
        await update.message.reply_text(f"Error fetching joke: {e}")







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
        "Same rule — use /pickup in reply to a message, and the bot will send a pickup line as a reply. 😉\n"
        "/translate <msg> - it will translate any language and also hinglish msg in english lang.\n"
        "/talk <message> - Casanova repeats your message\n"
        "Just chat normally - I may auto-reply like a human\n\n"
        "Tip: Reply to a message with /joke or /pickup to send it directly as a reply!"
    )
    await update.message.reply_text(help_text)



async def pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://api.popcat.xyz/pickuplines")
        if response.status_code == 200:
            data = response.json()
            line = data["pickupline"]

            # Agar user ne kisi message ko reply kiya hai
            if update.message.reply_to_message:
                await update.message.reply_to_message.reply_text(line)
            else:
                # Normal case: direct pickup line
                await update.message.reply_text(line)
        else:
            await update.message.reply_text("😅 Sorry bro, pickup API is down.")
    except Exception as e:
        await update.message.reply_text(f"sorry, i am busy: {e}")


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()

    human_replies = [
    "How are you?❤️",
    "Really?🤔",
    "No way",
    "I’m at clg right now.🏫",
    "You're kinda fun.",
    "Okay bro, noted.📝",
    "Yo, what’s up?",
    "Hmm, interesting.",
    "Alright, catch you later.",
    "Don't worry I'll carry this conversation.",
    "Careful, I notice everything.",
    "I didn’t expect that.",
    "For real?",
    "Not everyone gets my attention. you're lucky.",
    "Interesting.. go on.",
    "You came here for a chat or for me?",
    "I’m chilling rn.",
    "I think you're hiding something",
    "do you love me?",
    "why don't you love me?",
    "That’s wild 😂",
    "I hear you.",
    "I'll pretend I didn't hear that.",
    "Careful I might start liking this conversation",
    "I feel you.",
    "what did you say?",
    "Okay, I’ll remember that.",
    "Careful I'm addictive",
    "you know who i am",
    "Damn bro, cracked me up 🤣",
    "casanova loves you",
    "wth",
    "hey!, lonely person",
    "who is a gay here?.",
    "you know what? I've got four gf.😏",
    "I don't care.",
    "I'm Casanova.",
    "Everyone loves me",
    "we don't talk anymore."

]


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

    elif "Casanova" in msg:
        await update.message.reply_text("Go on.. I've got your attention.")

    elif "wassup" in msg or "hru" in msg or "wbu" in msg or "how are you" in msg:
        await update.message.reply_text("I'm cool, wbu?")

    elif "gay" in  msg or " you are gay" in msg:
        await update.message.reply_text("I'm lesbian - I like gurls.")

    
    
    else:
        # 30% chance reply, 70% ignore
        if random.randint(1, 10) <= 3:
            reply = random.choice(human_replies)
            await update.message.reply_text(reply)
        else:
            print(f"casanova ignored: {msg}")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get user message after /translate
    msg = update.message.text.replace("/translate", "").strip()

    if not msg:
        await update.message.reply_text("Bro, give me some text to translate 😅")
        return

    try:
        # Popcat Translate API (auto-detects language)
        response = requests.get(f"https://api.popcat.xyz/translate?to=en&text={msg}")
        if response.status_code == 200:
            data = response.json()
            translated = data["translated"]
            detected_lang = data.get("lang", "unknown")
            await update.message.reply_text(
                f"Detected language: {detected_lang}\nEnglish: {translated}"
            )
        else:
            await update.message.reply_text("😅 Translation API down hai bro")
    except Exception as e:
        await update.message.reply_text(f"Error translating: {e}")





# /talk command
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.replace("/talk", "").strip()
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

    #app.add_handler(CommandHandler("compliment", compliment))
    




    print("Loaded TOKEN:", TOKEN) 

    print("Casanova bot is running...")
    app.run_polling()
    
    
