import Constants as keys
from telegram.ext import *
from googletrans import Translator

print("Bot starting...")

translator = Translator()

def start_command(update, context):
    update.message.reply_text('Hello! I am a translation bot! Type in a sentence, followed by = then what language you want to translate to.\nEx: Hello = german')

def help_command(update, context):
    update.message.reply_text('Type /help to print the help message.')


def handle_response(text: str) -> str:
    length = len(text)
    new_lang = ''
    for i in range(length, 0, -1):
        if text[i - 1] == ' ':
            break
        new_lang += text[i - 1]
    new_lang = new_lang[::-1]
    
    new_text = ''
    for i in range(0, length, 1):
        if text[i] == '=':
            break
        new_text += text[i]

    shpee = translator.translate(new_text, dest=new_lang)
    return shpee.text


def handle_message(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}"')

    if message_type == 'group':
        if "@SC_Weather_Bot" in text:
            new_text = text.replace('@SC_Weather_Bot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    update.message.reply_text(response)


def error(update, context):
    print(f'Update {update} caused error: {context.error}')


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    #Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    

    #Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    #Errors
    dp.add_error_handler(error)

    #Run Bot
    updater.start_polling(1.0)
    updater.idle()


main()


