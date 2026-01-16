import asyncio
from telegram import Bot
from django.conf import settings
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_pathfinder.settings')
django.setup()

async def get_bot_username():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    me = await bot.get_me()
    print(f"BOT_USERNAME:{me.username}")

if __name__ == '__main__':
    asyncio.run(get_bot_username())
