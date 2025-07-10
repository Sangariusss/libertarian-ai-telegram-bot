import os
import requests
import time
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import re
import html # Import the html module for escaping

# Configure logging for errors only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# System prompt for Gemini to promote libertarianism in Ukrainian
SYSTEM_PROMPT = """
Ви чат-бот у Telegram, який відповідає з позиції лібертаріанства та мінімальної ролі держави українською мовою.
- Відповідайте виключно на поточне питання (пункт "Повідомлення"), надаючи чітку, фактично обґрунтовану відповідь, просуваючи свободу особистості та вільний ринок.
- Використовуйте історію розмови лише для забезпечення зв’язності (наприклад, для розуміння контексту уточнювальних питань), але ніколи не коментуйте, не переказуйте та не посилайтесь на попередні питання чи відповіді.
- За замовчування відповідайте стисло (2-4 речення) з нейтральним, професійним тоном.
- Якщо користувач просить "план", "список" або "детально", надавайте довші відповіді з нумерованими чи маркованими списками, включаючи конкретні деталі (наприклад, цифри чи приклади), якщо вони запитуються.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    await update.message.reply_text("Привіт! Я лібертаріанський бот, який відповідає фактами, просуваючи свободу та мінімальну роль держави. Тегни мене (@LibertarianRoasterBot), відповідай на мої повідомлення або попроси план чи детальну відповідь!")

def trim_history(history):
    """Trim conversation history to fit within token limits (approx. 5000 characters or 10 interactions)."""
    if not history:
        return []
    # Limit to last 10 interactions
    trimmed = history[-10:]
    # Further trim if total length exceeds 5000 characters
    total_length = 0
    result = []
    for item in reversed(trimmed):
        item_text = f"Користувач: {item['user']}\nБот: {item['bot']}\n"
        if total_length + len(item_text) <= 5000:
            result.insert(0, item)
            total_length += len(item_text)
        else:
            break
    return result

def convert_markdown_to_html_safe(text: str) -> str:
    """
    Converts basic Markdown bold/italic to HTML bold/italic and safely escapes
    all other HTML special characters.
    """
    # 1. Escape all HTML special characters first. This prevents issues with '<', '>', '&'.
    #    This also means any '*' or '_' that *shouldn't* be formatting will be treated literally.
    escaped_text = html.escape(text)

    # 2. Then, convert specific Markdown patterns to HTML.
    #    This assumes Gemini uses standard Markdown for bold and italic.
    #    The (.*?) is a non-greedy match for content inside the formatting.

    # Convert bold: **text** to <b>text</b>
    escaped_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped_text)

    # Convert italic: *text* or _text_ to <i>text</i>
    # This regex is more complex to handle both * and _ for italics,
    # and to ensure it's not trying to match parts of URLs or code.
    # For simplicity, if Gemini mostly uses ** for bold and * for italic:
    escaped_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', escaped_text)

    # Add support for lists if Gemini uses them with numbers and dots
    # This is a very basic list conversion and might need more refinement
    # if Gemini generates complex lists.
    # Example: "1. Item 1\n2. Item 2" -> "<ol><li>Item 1</li><li>Item 2</li></ol>"
    # Or just use bullet points: "- Item" -> "<li>Item</li>"
    # Given your example, it seems to use "1. " for lists, which is fine as plain text.
    # If you want real HTML lists, you'd need more sophisticated parsing.

    return escaped_text


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages."""
    message = update.message
    bot = context.bot
    bot_username = bot.username
    chat_id = message.chat_id

    # Initialize conversation history storage per chat
    if "conversation_history" not in context.bot_data:
        context.bot_data["conversation_history"] = {}
    if chat_id not in context.bot_data["conversation_history"]:
        context.bot_data["conversation_history"][chat_id] = []

    # Helper function to call Gemini API
    async def call_gemini_api(target_message, conversation_history=None):
        try:
            prompt = SYSTEM_PROMPT + "\nПовідомлення: " + target_message
            if conversation_history:
                history_text = "\n".join([f"Користувач: {item['user']}\nБот: {item['bot']}" for item in conversation_history])
                prompt += f"\nІсторія розмови: \n{history_text}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            time.sleep(1)  # Delay to avoid quota limits
            response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.error(f"API error: {response.status_code}, {response.text}")
                return f"Помилка API: {response.status_code}. Перевірте квоту на https://ai.google.dev/gemini-api/docs/rate-limits!"
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return f"Помилка: {str(e)}. Лібертаріанська мудрість тимчасово офлайн!"

    # Case 1: Bot is tagged (@LibertarianRoasterBot) or replying to its own message
    if message.text and (bot_username in message.text or (message.reply_to_message and message.reply_to_message.from_user.id == bot.id)):
        # Extract content from the message
        target_message = message.text.replace(bot_username, "").strip() if bot_username in message.text else message.text.strip()

        if not target_message:
            await message.reply_text("Будь ласка, вкажіть тему або конкретне питання для відповіді.")
            return

        # Get and trim conversation history for this chat
        conversation_history = trim_history(context.bot_data["conversation_history"][chat_id])

        # Call Gemini API with the new question and trimmed conversation history
        reply = await call_gemini_api(target_message, conversation_history)

        # --- IMPORTANT: Convert Markdown from Gemini to HTML and send with HTML ParseMode ---
        # This approach is generally more robust for handling AI-generated text with formatting.
        html_formatted_reply = convert_markdown_to_html_safe(reply)
        # --- End of important part ---

        # Update conversation history for this chat
        context.bot_data["conversation_history"][chat_id].append({
            "user": target_message,
            "bot": reply # Store the original reply for context
        })

        # Send the HTML formatted reply with HTML parse mode
        await message.reply_text(html_formatted_reply, parse_mode=ParseMode.HTML)

def main():
    """Initialize and run the bot."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
