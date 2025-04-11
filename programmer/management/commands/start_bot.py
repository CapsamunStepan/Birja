import os
import django
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.core.management.base import BaseCommand
from programmer.models import TelegramUser, Portfolio
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Birja.settings")
django.setup()

User = get_user_model()
logging.basicConfig(level=logging.INFO)


def start(update: Update, context: CallbackContext):
    args = context.args
    tg_user = update.effective_user

    if args:
        token = args[0]
        try:
            portfolio = Portfolio.objects.select_related("user").filter(telegram_link_token=token).first()
            if portfolio:
                user = portfolio.user
                TelegramUser.objects.get_or_create(
                    user=user,
                    defaults={"telegram_id": tg_user.id}
                )
                user.telegram_link_token = None
                user.save()
                update.message.reply_text("✅ Telegram успешно привязан!")
            else:
                update.message.reply_text("❌ Пользователь с таким токеном не найден.")
        except Exception as e:
            print(e)
            logging.exception("Ошибка при привязке токена")
            update.message.reply_text("❌ Ошибка при привязке.")
    else:
        update.message.reply_text("👋 Привет! Перейди по ссылке с сайта, чтобы привязать Telegram.")


class Command(BaseCommand):
    help = "Запуск синхронного Telegram бота"

    def handle(self, *args, **options):
        updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start, pass_args=True))
        logging.info("Бот запущен...")
        updater.start_polling()
        updater.idle()
