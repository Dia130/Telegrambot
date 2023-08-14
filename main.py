from requests import * 
from telegram import * 
from telegram.ext import * 


TOKEN = "6393122674:AAF8bRgYTQTEFsx_qylH37iIsEQuaMdH_SE"


def callback_query_handler_for_attached_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "1":
        query.edit_message_text(text="You pressed button 1")
    elif query.data == "2":
        query.edit_message_text(text="You pressed button 2")


def message_handler_for_below_buttons(update: Update, context: CallbackContext):
    # Use the global keyword to modify IMAGE_COUNTER
    global IMAGE_COUNTER
    IMAGE_COUNTER += 1
    if update.message.text == RANDOM_IMAGE:
        image = get(RANDOM_IMG_URL).content
        context.bot.sendMediaGroup(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(image, caption=f"Random {IMAGE_COUNTER}")]
        )
    elif update.message.text == GET_MP3:
        _send_mp3(update, context)


def help(update, context):
    update.message.reply_text("""
/start   - Start the bot
/help    - Help
/buttons_below    - Get Optional buttons
/buttons_attached - Get Attached buttons
"""
                              )


updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler('buttons_below', get_buttons_below_message))
dispatcher.add_handler(CommandHandler('buttons_attached', get_attached_buttons))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler_for_below_buttons))
dispatcher.add_handler(CallbackQueryHandler(callback_query_handler_for_attached_buttons))


updater.start_polling()
updater.idle()