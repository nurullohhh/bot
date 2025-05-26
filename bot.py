from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import schedule
import time
import threading
from datetime import datetime

# Foydalanuvchi ma'lumotlari uchun oddiy saqlash (keyin MongoDB yoki Google Sheets qo'shiladi)
user_data = {}

def start(update, context):
    user_id = update.message.from_user.id
    user_data[user_id] = {"tasks": {}, "weekly_report": [], "goals": []}
    update.message.reply_text("MaverickMind botiga xush kelibsiz! 🛠️\n"
                              "/setroutine - Kunlik vazifalarni sozlash\n"
                              "/checkin - Kunlik hisobot\n"
                              "/goals - Haftalik maqsadlarni kiritish\n"
                              "focus, workout, reset, calm deb yozing, playlist beraman!")

def set_routine(update, context):
    user_id = update.message.from_user.id
    user_data[user_id]["tasks"] = {
        "04:00": {"task": "Uyg‘onish vaqti! Hayoting kutmaydi.", "done": False},
        "05:10": {"task": "Yugurishga chiq! Kuch to‘plamaydigan kun — yo‘qotilgan kun.", "done": False}
    }
    update.message.reply_text("Kunlik rejalar sozlandi! Vaqtida eslataman.")

def check_task(update, context):
    user_id = update.message.from_user.id
    text = update.message.text.lower()
    if user_id in user_data and "tasks" in user_data[user_id]:
        for time, task_info in user_data[user_id]["tasks"].items():
            if task_info["task"].lower() in text:
                task_info["done"] = True
                update.message.reply_text(f"{time} vazifa bajarildi! 💪")
                return
    update.message.reply_text("Vazifa topilmadi. To‘g‘ri vazifani yozing.")

def daily_checkin(update, context):
    update.message.reply_text("Bugun o‘zingdan rozimisan?\n"
                             "3 ta foydali ish?\n"
                             "Yaxshilanishi kerak bo‘lgan narsa?")
    context.user_data["awaiting_checkin"] = True

def handle_checkin_response(update, context):
    if context.user_data.get("awaiting_checkin", False):
        user_id = update.message.from_user.id
        user_data[user_id]["checkin"] = update.message.text
        update.message.reply_text("Javobingiz saqlandi. Yaxshi harakat qilding! 🚀")
        context.user_data["awaiting_checkin"] = False

def motivation(update, context):
    text = update.message.text.lower()
    if "chalg‘iyabman" in text or "chalg'iyabman" in text:
        update.message.reply_text("Eslat: Sen kuchli bo‘lish uchun kelding. Endi harakat qil! 💥")

def playlist(update, context):
    text = update.message.text.lower()
    playlists = {
        "focus": "https://open.spotify.com/playlist/focus_playlist_link",
        "workout": "https://open.spotify.com/playlist/workout_playlist_link",
        "reset": "https://open.spotify.com/playlist/reset_playlist_link",
        "calm": "https://open.spotify.com/playlist/calm_playlist_link"
    }
    for key, link in playlists.items():
        if key in text:
            update.message.reply_text(f"{key.title()} playlist: {link}")
            return
    update.message.reply_text("Iltimos, focus, workout, reset yoki calm deb yozing.")

def weekly_report(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text("Hisobot vaqti. Bu hafta necha kun rejaga amal qilding?\n"
                             "Qaysi qoida eng ko‘p buzildi?")
    context.user_data["awaiting_report"] = True

def handle_report_response(update, context):
    if context.user_data.get("awaiting_report", False):
        user_id = update.message.from_user.id
        user_data[user_id]["weekly_report"].append(update.message.text)
        update.message.reply_text("Hisobot saqlandi. Agar ko‘p qoidabuzarlik bo‘lsa: "
                                 "Jazo faollashdi: Bugun telefon faqat 20:00 gacha. 📴")
        context.user_data["awaiting_report"] = False

def set_goals(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text("Bu haftaga qo‘ygan maqsadlaringizni yozing:")
    context.user_data["awaiting_goals"] = True

def handle_goals_response(update, context):
    if context.user_data.get("awaiting_goals", False):
        user_id = update.message.from_user.id
        user_data[user_id]["goals"].append(update.message.text)
        update.message.reply_text("Maqsadlar saqlandi! Hafta oxirida progressni tekshiramiz. 🎯")
        context.user_data["awaiting_goals"] = False

def send_scheduled_messages(context):
    for user_id, data in user_data.items():
        for time, task_info in data.get("tasks", {}).items():
            if task_info["done"] is False:
                context.bot.send_message(chat_id=user_id, text=task_info["task"])

def schedule_tasks(context):
    schedule.every().day.at("04:00").do(send_scheduled_messages, context=context)
    schedule.every().day.at("05:10").do(send_scheduled_messages, context=context)
    schedule.every().day.at("21:30").do(context.bot.send_message,
                                        chat_id=list(user_data.keys())[0] if user_data else None,
                                        text="Bugun o‘zingdan rozimisan?\n3 ta foydali ish?\nYaxshilanishi kerak bo‘lgan narsa?")
    schedule.every().sunday.at("10:00").do(context.bot.send_message,
                                           chat_id=list(user_data.keys())[0] if user_data else None,
                                           text="Hisobot vaqti. Bu hafta necha kun rejaga amal qilding?\nQaysi qoida eng ko‘p buzildi?")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    updater = Updater("7357791893:AAGsOtyt8JHupETmYQuT2cHGs2jIByg_N1k", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setroutine", set_routine))
    dp.add_handler(CommandHandler("checkin", daily_checkin))
    dp.add_handler(CommandHandler("goals", set_goals))
    dp.add_handler(CommandHandler("weeklyreport", weekly_report))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: motivation(update, context) or playlist(update, context) or handle_checkin_response(update, context) or handle_report_response(update, context) or handle_goals_response(update, context)))

    threading.Thread(target=run_scheduler, daemon=True).start()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
