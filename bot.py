import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# загружаем .env
load_dotenv()

BOT_TOKEN    = os.getenv("7591380644:AAGfXO7Ehkppu_HfGxMt5fGC2GmUUiC2JZc")
ADMIN_CHAT   = int(os.getenv("ADMIN_CHAT_ID", "643393091"))
PHONE_NUMBER = os.getenv("MANAGER_PHONE", "8-925-936-07-11")

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте!\n\n"
        "Напишите нам, что случилось. Мы в течение 5-10 минут решим Вашу проблему.\n"
        f"Или позвоните управляющему Михаилу {PHONE_NUMBER}"
    )
    await update.message.reply_text(text)

async def feedback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg  = update.message.text

    header = (
        f"📩 Новая обратная связь от @{user.username or user.first_name} "
        f"(ID {user.id}):"
    )
    # отправляем админу
    await ctx.bot.send_message(chat_id=ADMIN_CHAT, text=header)
    await ctx.bot.send_message(chat_id=ADMIN_CHAT, text=msg)
    # подтверждаем клиенту
    await update.message.reply_text("Спасибо! Ваше сообщение получено, ожидайте ответа.")

def main():
    if not BOT_TOKEN or ADMIN_CHAT == 0:
        logger.error("Не заданы BOT_TOKEN или ADMIN_CHAT_ID")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, feedback))
    app.run_polling()

if __name__ == "__main__":
    main()
