import os
import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- Настройки ---
TOKEN = os.getenv("BOT_TOKEN")      # ваш токен от BotFather
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))  # ваш Telegram ID или Маргариты

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Здравствуйте!\n\n"
        "Напишите нам, что случилось. Мы в течение 5-10 минут решим Вашу проблему.\n"
        "Или позвоните управляющей Маргарите 8-911-201-55-70"
    )

# Все текстовые сообщения – считаем обратной связью
def feedback_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    text = update.message.text

    # Подтверждение для пользователя
    update.message.reply_text("Спасибо! Мы получили ваше сообщение и скоро с вами свяжемся.")

    # Формируем сообщение для администратора
    msg = (
        f"🆕 <b>Новая обратная связь</b>\n"
        f"👤 От: {user.full_name} (id: {user.id})\n"
        f"📱 Username: @{user.username if user.username else '—'}\n"
        f"💬 Сообщение:\n{text}"
    )

    # Шлём админам
    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=msg,
        parse_mode=ParseMode.HTML
    )

def error_handler(update: object, context: CallbackContext):
    logger.error("Ошибка при обработке сообщения: %s", context.error)

def main():
    # создаём updater & dispatcher
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, feedback_handler))
    dp.add_error_handler(error_handler)

    # старт бота
    updater.start_polling()
    logger.info("Бот запущен.")
    updater.idle()

if __name__ == '__main__':
    main()
