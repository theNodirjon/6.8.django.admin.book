import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters
from .home.models.books import Book

import os
from django.core.management import execute_from_command_line

# Django sozlamalarini yuklash (DJANGO_SETTINGS_MODULE o'rnatish)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book.settings")

# Django'ni ishlashini ta'minlash
execute_from_command_line(['book.manage.py', 'check'])

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot komandalarining ishlashini aniqlash
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Salom! Kitob qo\'shish va tahrir qilish uchun /add, /edit, /delete komandalarini ishlating.')

def add_book(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Kitob nomini kiriting:')
    return 'GET_TITLE'

def get_title(update: Update, context: CallbackContext) -> None:
    context.user_data['title'] = update.message.text
    update.message.reply_text('Muallifni kiriting:')
    return 'GET_AUTHOR'

def get_author(update: Update, context: CallbackContext) -> None:
    context.user_data['author'] = update.message.text
    update.message.reply_text('Nashr qilingan sanani kiriting (YYYY-MM-DD):')
    return 'GET_DATE'

def get_date(update: Update, context: CallbackContext) -> None:
    context.user_data['published_date'] = update.message.text
    # Kitobni saqlash
    bookk = Book.objects.create(
        title=context.user_data['title'],
        author=context.user_data['author'],
        published_date=context.user_data['published_date']
    )
    update.message.reply_text(f"Yangi kitob qo'shildi: \nKitob nomi: {bookk.title}\nMuallifi: {bookk.author}")
    return 'END'

def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Operatsiya bekor qilindi.')
    return 'END'

# Botni ishga tushurish va handlerlarni sozlash
def main() -> None:
    """Start the bot."""
    updater = Updater("7367392547:AAHHmUYw2EL5CRJoyss-Uno-NcQvqILl1tc")  # Tokeningizni bu yerga qo'yganingizga ishonch hosil qiling.

    dispatcher = updater.dispatcher

    # "start" komandasi
    dispatcher.add_handler(CommandHandler("start", start))

    # "add" komandasi
    dispatcher.add_handler(CommandHandler("add", add_book))

    # "cancel" komandasi uchun handler
    dispatcher.add_handler(CommandHandler("cancel", cancel))

    # Foydalanuvchi kirita boshlagan matnni olish va keyingi qadamga o'tkazish
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, get_title))

    # Botni ishga tushurish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
