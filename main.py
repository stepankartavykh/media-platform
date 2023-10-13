from telegram.ext import ApplicationBuilder, CommandHandler, Application
from dotenv import load_dotenv
import os

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, BotCommand
from telegram.ext import ContextTypes, InlineQueryHandler

from handlers import start, echo, support

load_dotenv()

commands = [
    BotCommand(command='start', description='start description'),
    BotCommand(command='help', description='help description'),
    BotCommand(command='echo', description='echo description'),
]


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        ('start', 'start description'),
        ('help', 'help description'),
        ('echo', 'echo description'),
    ])


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [InlineQueryResultArticle(
        id=query.upper(),
        title='Caps',
        input_message_content=InputTextMessageContent(query.upper())
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


BOT_TOKEN = os.getenv('BOT_TOKEN')
START_URL = 'https://www.nytimes.com/'


app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("help", support))

inline_caps_handler = InlineQueryHandler(inline_caps)

app.add_handler(inline_caps_handler)

app.run_polling()
