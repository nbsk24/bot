```python
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен и ID админа из переменных окружения
BOT_TOKEN = os.getenv("7591380644:AAGfXO7Ehkppu_HfGxMt5fGC2GmUUiC2JZc")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "643393091"))  # например ваш личный chat_id

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /start"""
    text = (
        "Здравствуйте!\n\n"
        "Напишите нам, что случилось. Мы в течение 5-10 минут решим Вашу проблему.\n"
        "Или позвоните управляющему Михаилу 8-925-936-07-11"
    )
    await update.message.reply_text(text)

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает любое текстовое сообщение администратору и отвечает клиенту"""
    user = update.effective_user
    msg = update.message.text

    # Формируем заголовок для админа
    header = (
        f"🆕 Новая обратная связь от @{user.username or user.first_name} "
        f"(ID {user.id}):"
    )

    # Пересылаем header + текст администратору
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=header)
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

    # Подтверждение клиенту
    await update.message.reply_text("Спасибо! Ваше сообщение получено, ожидайте ответа.")

def main():
    if not BOT_TOKEN or ADMIN_CHAT_ID == 0:
        logger.error("Не заданы BOT_TOKEN или ADMIN_CHAT_ID в переменных окружения")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback))

    # Запускаем бот
    app.run_polling()

if __name__ == "__main__":
    main()
```
