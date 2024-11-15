// from telegram.ext import ApplicationBuilder, CommandHandler, Application
// from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
// from telegram.ext import (ContextTypes, InlineQueryHandler, CallbackQueryHandler, MessageHandler, filters,
//                           ConversationHandler)

// from config import BOT_TOKEN
// from cache_system_plugin import CacheSystemPlugin
// from config_database_plugin import ConfigDatabasePlugin
// from handlers import start, echo, support, add_source, get_source, observe, stop, observe_topics
// from handlers import add_topics, add_topic_to_config, button_coroutine
// from handlers import last_news

// commands = [
//     ('start', 'start description'),
//     ('help', 'help description'),
//     ('echo', 'echo description'),
//     ('add_source', 'add source of information'),
//     ('add_topics', 'add interesting topics'),
//     ('observe', 'start getting information'),
//     ('stop', 'stop sending messages'),
//     ('observe_topics', 'stop sending messages'),
// ]

// async def post_init(application: Application) -> None:
//     await application.bot.set_my_commands(commands)

// async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
//     query = update.inline_query.query
//     if not query:
//         return
//     results = [InlineQueryResultArticle(
//         id=query.upper(),
//         title='Caps',
//         input_message_content=InputTextMessageContent(query.upper())
//     )]
//     await context.bot.answer_inline_query(update.inline_query.id, results)

// conversation_handler_add_source = ConversationHandler(
//     entry_points=[CommandHandler("add_source", add_source)],
//     states={
//         'NEW_SOURCE': [MessageHandler(filters.TEXT, get_source)],
//     },
//     fallbacks=[CommandHandler("echo", echo)],
// )
// conversation_handler_add_topic = ConversationHandler(
//     entry_points=[CommandHandler("add_topics", add_topics)],
//     states={
//         'NEW_TOPIC': [MessageHandler(filters.TEXT, add_topic_to_config)],
//     },
//     fallbacks=[CommandHandler("echo", echo)],
// )
// inline_caps_handler = InlineQueryHandler(inline_caps)

// app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).concurrent_updates(True).build()

// handlers = [
//     CommandHandler("start", start),
//     CommandHandler("echo", echo),
//     CommandHandler("help", support),
//     CommandHandler("observe", observe),
//     CommandHandler("observe_topics", observe_topics),
//     CommandHandler("last", last_news),
//     CommandHandler("stop", stop),
//     conversation_handler_add_source,
//     # CommandHandler("add_topics", add_topics),
//     conversation_handler_add_topic,
//     MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
//     CallbackQueryHandler(button_coroutine),
//     inline_caps_handler,
// ]
// for handler in handlers:
//     app.add_handler(handler)

// config_database = ConfigDatabasePlugin()
// config_database.check_connection()
// cache_system = CacheSystemPlugin()
// cache_system.check_connection()

// print('Bot is running...')
// app.run_polling()

package main

import (
	"fmt"
	"log"
	"os"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	fmt.Println(os.Getenv("BOT_TOKEN"))
	bot, err := tgbotapi.NewBotAPI(os.Getenv("BOT_TOKEN"))
	if err != nil {
		panic(err)
	}

	bot.Debug = true
	updateConfig := tgbotapi.NewUpdate(0)
	updateConfig.Timeout = 30

	updates := bot.GetUpdatesChan(updateConfig)

	for update := range updates {
		if update.Message == nil {
			continue
		}
		msg := tgbotapi.NewMessage(update.Message.Chat.ID, update.Message.Text)
		msg.ReplyToMessageID = update.Message.MessageID

		if _, err := bot.Send(msg); err != nil {
			panic(err)
		}
	}
}
