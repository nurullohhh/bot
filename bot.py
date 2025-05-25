from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Salom! Men sizning botingizman.")

def main():
    updater = Updater("7357791893:AAGsOtyt8JHupETmYQuT2cHGs2jIByg_N1k", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()