import os
import logging
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "787118697"))

if not TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN. Добавьте токен в переменные окружения хостинга.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["text", "photo", "video", "document", "voice"])
def forward_message(message):
    try:
        bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.reply_to(message, "✅ Сообщение передано!")
    except telebot.apihelper.ApiTelegramException:
        logging.exception("Не удалось переслать сообщение админу")
        try:
            bot.reply_to(message, "Не удалось передать сообщение. Попробуйте позже.")
        except telebot.apihelper.ApiTelegramException:
            logging.exception("Не удалось отправить ответ пользователю")

if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
