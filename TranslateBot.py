from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator, LANGUAGES

TOKEN = '6807276388:AAEmh0oFSd_M5h9kABBluZxwJWhru3EeTfU'

user_language_settings = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать в Перевод-бота! \nНапишите /setlang (переводимый язык) (язык перевода), чтобы установить ваши настройки перевода, например: /setlang ru en \nЧтобы получить больше информации о возможностях бота введите команду /help')

def bothelp(update: Update, context: CallbackContext):
    update.message.reply_text('/setlang (переводимый язык) (язык перевода) - команда, которая позволяет задать настройки перевода, например: /setlang ru en \n/settings - команда, которая дает узнать ваши настройки перевода. \n/languages - команда, которая выводит список поддерживаемых языков.')

def set_language(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    message_text = update.message.text.split(' ')
    
    if len(message_text) != 3:
        update.message.reply_text('Пожалуйста, используйте формат: /setlang (переводимый язык) (язык перевода), например: /setlang ru en')
    else:
        source_lang, target_lang = message_text[1], message_text[2]
        if source_lang not in LANGUAGES or target_lang not in LANGUAGES:
            update.message.reply_text('Один или оба из указанных языков не поддерживается либо вы не верно использовали команду. \nИспользуйте /languages, чтобы увидеть список поддерживаемых языков или /help, чтобы получить всю необходимую информацию.')
        else:
            user_language_settings[chat_id] = (source_lang, target_lang)
            update.message.reply_text(f'Ваши настройки перевода установлены: {source_lang} -> {target_lang}')

def settings(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in user_language_settings:
        source_lang, target_lang = user_language_settings[chat_id]
        update.message.reply_text(f'Ваши настройки перевода: {source_lang} -> {target_lang}')
    else:
        update.message.reply_text('Настройки перевода не установлены.')

def list_languages(update: Update, context: CallbackContext):
    language_list = "\n".join([f"{code} - {name}" for code, name in LANGUAGES.items()])
    update.message.reply_text(f'Поддерживаемые языки:\n{language_list}')

def translate(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if chat_id in user_language_settings:
        source_lang, target_lang = user_language_settings[chat_id]
        translation = Translator().translate(text, src=source_lang, dest=target_lang)
        translated_text = translation.text
        update.message.reply_text('Перевод:')
        update.message.reply_text(f'{translated_text}')
    else:
        update.message.reply_text('Настройки перевода не установлены.')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", bothelp))
    dispatcher.add_handler(CommandHandler("setlang", set_language))
    dispatcher.add_handler(CommandHandler("settings", settings))
    dispatcher.add_handler(CommandHandler("languages", list_languages))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()