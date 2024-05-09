import requests
from telegram import Update
from telegram.ext import ContextTypes

from BotApp.config import CACHE_SYSTEM_HOST, CACHE_SYSTEM_PORT
from BotApp.database.services.source.service import SourceService

request_to_send_message_directly_url = \
    'https://api.telegram.org/bot{api_bot_token}/sendMessage?chat_id={chat_id_int}&text={message_text_to_send}'


async def send_notification(update: Update):
    print(update.message.chat_id)
    url = CACHE_SYSTEM_HOST + ':' + CACHE_SYSTEM_PORT + '/accept-notification'
    params = {
        'user_id': update.message.from_user.id,
        'chat_id': update.message.chat_id,
    }
    try:
        response = requests.get(url, params=params)
    except requests.exceptions.ConnectionError:
        await update.message.reply_text(f"Problem with notification system.")
    else:
        if response.status_code == 200:
            await update.message.reply_text(f"message send to cache system")
        else:
            await update.message.reply_text(f"something wrong with notifying cache system.")


async def notify_cache_system(update: Update):
    """Subscribe to updates."""
    print(f'system is notified. user {update.message.from_user.id} will receive new updates as soon as possible')
    await send_notification(update)


async def observe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO just send notification to cache system.
    print(update.message.chat_id)
    current_sources = SourceService().get_sources_for_user(update.message.from_user.id)
    if not current_sources:
        await update.message.reply_text('There are no sources to monitor.')
    else:
        await update.message.reply_text("Observation just started...You will receive new updates of your interest.")
        # await start_async_processing(current_sources, update)
        await notify_cache_system(update)
