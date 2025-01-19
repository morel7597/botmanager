from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# تنظیمات اولیه
TOKEN = '7793831713:AAE-KWAHsYCVWAM36t_oubTJiGB57aN6V-8'

# راه‌اندازی لاگ برای بررسی خطاها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ذخیره هشدارها برای هر کاربر
user_warnings = {}

# کلمات مورد نظر برای جستجو
blocked_words = ['سکس', 'sex', 'خر']  # اینجا کلمات مدنظر خود را قرار دهید

# فرمان شروع ربات
def start(update: Update, context: CallbackContext):
    update.message.reply_text('start')

# بررسی و حذف پیام‌هایی که کلمه‌ی ممنوع دارند
def check_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    message_text = update.message.text

    # بررسی وجود کلمات ممنوع
    for word in blocked_words:
        if word in message_text:
            update.message.delete()  # حذف پیام
            if user.id not in user_warnings:
                user_warnings[user.id] = 1
            else:
                user_warnings[user.id] += 1

            # ارسال هشدار به کاربر
            update.message.reply_text(f'هشدار! شما از کلمه غیرمجاز "{word}" استفاده کرده‌اید.')

            # بررسی تعداد هشدارها
            if user_warnings[user.id] >= 2:
                # حذف کاربر از گروه بعد از دو هشدار
                context.bot.kick_chat_member(update.message.chat.id, user.id)
                update.message.reply_text(f'کاربر {user.first_name} به دلیل دو هشدار از گروه حذف شد.')
                del user_warnings[user.id]  # پاک کردن هشدارهای قبلی

            break

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # ثبت دستورات
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
