import os
import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# Настройка логов (чтобы видеть ошибки в консоли)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- НАСТРОЙКИ ---
# Токен и ID берутся из переменных окружения (Secrets)
BOT_TOKEN = os.environ.get("8678523265:AAFES4IC_dwhYk5WDabofCEykmx-UIshgfU")
DEST_CHAT_ID = os.environ.get("1003929981277")
# -----------------

if not BOT_TOKEN or not DEST_CHAT_ID:
    logger.error("❌ ОШИБКА: Не найдены BOT_TOKEN или DEST_CHAT_ID в Secrets!")
    logger.info("👉 Зайди во вкладку Secrets и добавь их.")
else:
    logger.info("✅ Токен и ID загружены.")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция пересылки сообщения"""
    if not update.message:
        return
    
    # Если пришло фото, видео или просто текст — пробуем переслать
    try:
        # Пробуем переслать оригинальное сообщение (сохраняет фото, текст, кнопки)
        await update.message.forward(chat_id=DEST_CHAT_ID)
        logger.info(f"📩 Переслано сообщение от {update.message.from_user.username}")
    except Exception as e:
        logger.error(f"❌ Ошибка пересылки: {e}")
        # Фоллбэк: если не переслалось (например, из-за прав), отправляем текст
        if update.message.text:
            await context.bot.send_message(chat_id=DEST_CHAT_ID, text=update.message.text)

def main():
    if not BOT_TOKEN:
        logger.error("Нет токена. Запуск невозможен.")
        return

    logger.info("🚀 Запуск приложения...")
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчик всех сообщений (текст, фото, видео)
    application.add_handler(MessageHandler(filters.ALL, forward_message))
    
    logger.info("🤖 Бот запущен и ждет сообщений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()