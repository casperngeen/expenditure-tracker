TOKEN = "5896294445:AAGtO3PamgqsEIB9OeXZW9Mj8okVaCe7xjg"

import logging
import os
PORT = int(os.environ.get('PORT', '8443'))

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

LOGS = []

NEWLOG, ADDLOG, CATEGORIES, CONFIRM, SUMMARY, CATEGORYSUM = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation."""
    await update.message.reply_text(
        "Welcome! Here is a guide on how to use the bot. \n"
        "/summary - Allows you to get an overview of your spending.\n"
        "/new - To create a new spending log.\n"
        "/add - Allows you to add an expedniture to the spending logs.\n"
    )

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Creates a new spending log."""

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Input the title of your new spending log.\nEnter /cancel if you wish to cancel this request.")
    return NEWLOG

async def readback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Add to the list of spending logs."""
    
    newLog = {"name": update.message.text, "transport": 0, "food": 0, "nutrition": 0, "shopping": 0, "entertainment": 0, "others": 0, "total": 0}
    LOGS.append(newLog)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="The new spending log has been created.\nGo to /summary to view it.")
    return ConversationHandler.END

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Allows user to add to a spending log"""
    if len(LOGS) > 0:
        keyboard = []
        for i in range(len(LOGS)):
            keyboard.append([LOGS[i]["name"]])

        markup = ReplyKeyboardMarkup(keyboard=keyboard, input_field_placeholder="Spending Logs" ,resize_keyboard=True, one_time_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a spending log.\nEnter /cancel if you wish to cancel this request.", reply_markup=markup)
        return ADDLOG
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You have no spending logs.\nPlease go to /new to create a spending log.")
        return ConversationHandler.END

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Allows user to choose from the list of categories to clasify it under."""
    
    context.user_data["log"]=update.message.text
    for i in range(len(LOGS)):
        if LOGS[i]["name"] == context.user_data["log"]:
            reply_keyboard = [["Transport", "Food", "Nutrition"], ["Shopping", "Entertainment", "Others"]]
            markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, input_field_placeholder="Categories" ,resize_keyboard=True, one_time_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a category.\nEnter /cancel if you wish to cancel this request.", reply_markup=markup)
            return CATEGORIES
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ensure you select a valid spending log. Enter /add to try again.")
    return ConversationHandler.END
    

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Allows user to choose from the list of categories to clasify it under."""
    
    context.user_data["category"]=update.message.text.lower()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter the amount of money spent in numbers (eg. $42.45 would be keyed in as 42.45).\nEnter /cancel if you wish to cancel this request.")
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Updates spending logs and sends a confirmation to the user."""
    number = float(update.message.text)
    
    for i in range(len(LOGS)):
        if LOGS[i]["name"] == context.user_data["log"]:
            LOGS[i][context.user_data["category"]] += number
            LOGS[i]["total"] += number
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Your spending has been updated.\nGo to /summary to view it.")
    return ConversationHandler.END

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Gives the user a summary of the spending logs."""
    
    if len(LOGS) > 0:
        keyboard = []
        for i in range(len(LOGS)):
            keyboard.append([LOGS[i]["name"]])

        markup = ReplyKeyboardMarkup(keyboard=keyboard, input_field_placeholder="Spending Logs" ,resize_keyboard=True, one_time_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a spending log.\nEnter /cancel if you wish to cancel this request.", reply_markup=markup)
        return SUMMARY
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You have no spending logs.\nPlease go to /new to create a spending log.")
        return ConversationHandler.END

async def categorysum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Allows user to choose from the list of categories to view spending summary."""
    
    context.user_data["name"]=update.message.text
    for i in range(len(LOGS)):
        if LOGS[i]["name"] == context.user_data["name"]:
            reply_keyboard = [["Transport", "Food", "Nutrition"], ["Shopping", "Entertainment", "Others"], ["Total"]]
            markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, input_field_placeholder="Categories" ,resize_keyboard=True, one_time_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a category of spending to view.\nEnter /cancel if you wish to cancel this request.", reply_markup=markup)
            return CATEGORYSUM

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ensure you select a valid spending log. Enter /summary to try again.")
    return ConversationHandler.END

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Updates the user on the spending amount and ends the conversation."""
    
    month = context.user_data["name"]
    category = update.message.text.lower()
    for i in range(len(LOGS)):
        if LOGS[i]["name"] == month:
            amount = LOGS[i][category]

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You spent ${amount} in {category.upper()} for {month}.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Your request has been cancelled.")
    return ConversationHandler.END

if __name__ == "__main__":
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)

    new_handler = ConversationHandler(
        entry_points=[CommandHandler("new", new)],
        states={
            NEWLOG: [MessageHandler(filters.TEXT & (~ filters.COMMAND), readback)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    add_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={
            ADDLOG: [MessageHandler(filters.TEXT & (~ filters.COMMAND), categories)],
            CATEGORIES: [MessageHandler(filters.Regex("^(Transport|Food|Nutrition|Shopping|Entertainment|Others)$"), amount)],
            CONFIRM: [MessageHandler(filters.Regex("^[0-9]"), confirm)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    summary_handler = ConversationHandler(
        entry_points=[CommandHandler("summary", summary)],
        states={
            SUMMARY: [MessageHandler(filters.TEXT & (~ filters.COMMAND), categorysum)],
            CATEGORYSUM: [MessageHandler(filters.Regex("^(Transport|Food|Nutrition|Shopping|Entertainment|Others|Total)$"), end)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(start_handler)
    application.add_handler(new_handler)
    application.add_handler(add_handler)
    application.add_handler(summary_handler)
    application.run_webhook(
        listen="0.0.0.0", 
        port=PORT, 
        url_path=TOKEN, 
        webhook_url="https://damp-beach-74652.herokuapp.com/" + TOKEN
    )
    