import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Логирование
logging.basicConfig(level=logging.INFO)

# Этапы диалога
CHOOSING, NAME, AREA, ADDRESS, DATETIME = range(5)

# Токен и ID админа (твой)
BOT_TOKEN = "7890639729:AAFDTlwxytuM02fTdoygl6PZ6LrYZ_K9YTM"
ADMIN_ID = 425785910

# Типы уборки
CLEAN_TYPES = ["Генеральная", "Поддерживающая", "После ремонта", "После арендаторов", "Мытьё окон"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [[t] for t in CLEAN_TYPES]
    await update.message.reply_text(
        "Привет! Какой тип уборки вам нужен?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CHOOSING

async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["type"] = update.message.text
    await update.message.reply_text("Введите ваше имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Укажите площадь помещения в м²:")
    return AREA

async def get_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["area"] = update.message.text
    await update.message.reply_text("Введите адрес:")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("Укажите дату и время уборки:")
    return DATETIME

async def get_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["datetime"] = update.message.text
    data = context.user_data

    summary = (
        f"🧹 Новая заявка:\n"
        f"Тип: {data['type']}\n"
        f"Имя: {data['name']}\n"
        f"Площадь: {data['area']} м²\n"
        f"Адрес: {data['address']}\n"
        f"Когда: {data['datetime']}"
    )

    await update.message.reply_text("Спасибо! Ваша заявка принята ✅")
    await context.bot.send_message(chat_id=ADMIN_ID, text=summary)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Окей, заявка отменена.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_area)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            DATETIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_datetime)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
