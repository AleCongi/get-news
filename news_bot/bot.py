import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from .email_processor import elabora_dati_email, get_most_recent_email, clean_email_body

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

async def send_email_to_channel(context: CallbackContext):
    path = os.getenv("PATH_TO_INBOX")  # Assicurati che il percorso del file delle email sia nel tuo .env
    emails = elabora_dati_email(path)
    most_recent_email = get_most_recent_email(emails)

    if most_recent_email:
        if most_recent_email['Mittente'] != context.bot_data.get('last_email_sender') and most_recent_email['Data di ricezione'] != context.bot_data.get('last_email_date'):
            cleaned_body = clean_email_body(most_recent_email['Body'])
            print (cleaned_body)
            message = (
                f"Mittente: {most_recent_email['Mittente']}\n"
                f"Subject: {most_recent_email['Subject']}\n"
                f"Data: {most_recent_email['Data di ricezione']}\n"
                f"Body:\n{cleaned_body}"
            )
            await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
            context.bot_data['last_email_sender'] = most_recent_email['Mittente']
            context.bot_data['last_email_date'] = most_recent_email['Data di ricezione']

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot started. Checking emails every minute.")
    # Schedula la funzione per inviare le email al canale ogni 60 secondi
    context.job_queue.run_repeating(send_email_to_channel, interval=5, first=1)

def main():
    print('Bot starting...')
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
