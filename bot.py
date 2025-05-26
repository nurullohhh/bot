from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading
from datetime import datetime

# Foydalanuvchi ma'lumotlari (vaqtinchalik xotira)
user_data = {}

def start(update, context):
    user_id = update.message.from_user.id
    user_data[user_id] = {"tasks": {}}
    update.message.reply_text("MaverickMind botiga xush kelibsiz! 🛠️\n"
                              "Kunlik tartibingiz sozlandi. Vazifalarni vaqtida eslataman.\n"
                              "/setroutine - Rejani qayta sozlash")

def set_routine(update, context):
    user_id = update.message.from_user.id
    # Kundalik tartib (namoz vaqtlari taxminiy, keyin API bilan moslashtiriladi)
    user_data[user_id]["tasks"] = {
        "04:00": {"task": "Uyg‘onish", "done": False},
        "04:05": {"task": "Bomdod namozi", "done": False},  # Namoz vaqti moslashtiriladi
        "04:30": {"task": "Yugurish", "done": False},
        "05:30": {"task": "Deep Learning", "done": False},
        "05:10": {"task": "YouTube video", "done": False},
        "06:10": {"task": "Kitob o‘qish", "done": False},
        "07:00": {"task": "Trading o‘rganish", "done": False},
        "07:30": {"task": "Nonushta", "done": False},
        "08:30": {"task": "YouTube video", "done": False},
        "09:30": {"task": "Kitob o‘qish", "done": False},
        "10:30": {"task": "Matematika o‘rganish", "done": False},
        "12:20": {"task": "Peshin namozi", "done": False},  # Namoz vaqti moslashtiriladi
        "12:40": {"task": "YouTube video", "done": False},
        "13:40": {"task": "Kitob o‘qish", "done": False},
        "14:40": {"task": "Uyqu", "done": False},
        "16:00": {"task": "Ingliz tili o‘rganish", "done": False},
        "17:00": {"task": "Asr namozi", "done": False},  # Taxminiy vaqt, moslashtiriladi
        "19:00": {"task": "Shom namozi", "done": False},  # Taxminiy vaqt, moslashtiriladi
        "21:00": {"task": "Kechki ovqat", "done": False},
        "21:30": {"task": "Xufton namozi", "done": False},  # Namoz vaqti moslashtiriladi
        "21:50": {"task": "Mashq qilish", "done": False},
        "22:20": {"task": "Uyqu", "done": False}
    }
    update.message.reply_text("Kunlik tartib sozlandi! Vazifalarni vaqtida eslataman.")

def send_scheduled_messages(context):
    for user_id, data in user_data.items():
        for time, task_info in data.get("tasks", {}).items():
            if task_info["done"] is False:
                context.bot.send_message(chat_id=user_id, text=f"⏰ {time}: {task_info['task']}")

def schedule_tasks(context):
    # Har bir vazifa uchun eslatma sozlanadi
    schedule.every().day.at("04:00").do(send_scheduled_messages, context=context)
    schedule.every().day.at("04:05").do(send_scheduled_messages, context=context)
    schedule.every().day.at("04:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("05:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("05:10").do(send_scheduled_messages, context=context)
    schedule.every().day.at("06:10").do(send_scheduled_messages, context=context)
    schedule.every().day.at("07:00").do(send_scheduled_messages, context=context)
    schedule.every().day.at("07:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("08:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("09:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("10:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("12:20").do(send_scheduled_messages, context=context)
    schedule.every().day.at("12:40").do(send_scheduled_messages, context=context)
    schedule.every().day.at("13:40").do(send_scheduled_messages, context=context)
    schedule.every().day.at("14:40").do(send_scheduled_messages, context=context)
    schedule.every().day.at("16:00").do(send_scheduled_messages, context=context)
    schedule.every().day.at("17:00").do(send_scheduled_messages, context=context)  # Asr taxminiy
    schedule.every().day.at("19:00").do(send_scheduled_messages, context=context)  # Shom taxminiy
    schedule.every().day.at("21:00").do(send_scheduled_messages, context=context)
    schedule.every().day.at("21:30").do(send_scheduled_messages, context=context)
    schedule.every().day.at("21:50").do(send_scheduled_messages, context=context)
    schedule.every().day.at("22:20").do(send_scheduled_messages, context=context)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    updater = Updater("7357791893:AAGsOtyt8JHupETmYQuT2cHGs2jIByg_N1k", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setroutine", set_routine))

    threading.Thread(target=run_scheduler, daemon=True).start()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
