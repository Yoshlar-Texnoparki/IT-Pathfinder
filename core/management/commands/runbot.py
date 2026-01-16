from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from core.models import UserProfile
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs the Telegram Bot'

    def handle(self, *args, **options):
        application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            args = context.args
            if args:
                token = args[0]
                # Verify token from cache
                cached_data = cache.get(f"auth_token:{token}")
                if cached_data:
                    otp = cached_data.get('otp')
                    # Send OTP to user
                    await update.message.reply_text(f"Sizning tasdiqlash kodingiz: {otp}\n\nBu kodni saytga kiriting.")
                else:
                    await update.message.reply_text("Sessiya vaqti tugagan yoki xato havola. Iltimos, saytdan qaytadan ro'yxatdan o'ting.")
            else:
                await update.message.reply_text("Assalomu alaykum! IT-Pathfinder tizimiga xush kelibsiz.\n\nHisobingizni tasdiqlash uchun saytdagi 'Open Telegram Bot' tugmasini bosing yoki havolani bosing. Shunchaki 'Start' bosish yetarli emas.")

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        self.stdout.write(self.style.SUCCESS('Bot started...'))
        application.run_polling()
