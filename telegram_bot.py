# -*- coding: utf-8 -*-
import json
import os
import sys
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic
import logging
from datetime import datetime, timezone

logging.basicConfig(
    filename='crisis_log.txt',
    level=logging.INFO,
    format='%(message)s'
)

def log_crisis(reason: str):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f'{timestamp} | trigger: {reason}')


from prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_DE, TOOL_DEFINITIONS
from tools import dispatch
from safety import check_free_text

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
MODEL = 'claude-opus-4-5'

user_sessions = {}

CRISIS_MESSAGE_EN = (
    'IMMEDIATE SUPPORT AVAILABLE\n\n'
    'If you are having thoughts of harming yourself, please reach out now:\n\n'
    'Die Dargebotene Hand: 143 (24/7, free, anonymous)\n'
    'Psychologische Beratung UniLU: +41 41 229 54 00\n\n'
    'You do not have to face this alone. The screening has been paused.'
)

CRISIS_MESSAGE_DE = (
    'SOFORTHILFE VERFUEGBAR\n\n'
    'Wenn du Gedanken hegst, dir selbst zu schaden, wende dich bitte jetzt an:\n\n'
    'Die Dargebotene Hand: 143 (24/7, kostenlos, anonym)\n'
    'Psychologische Beratung UniLU: +41 41 229 54 00\n\n'
    'Du musst das nicht alleine tragen. Das Screening wurde pausiert.'
)


DISCLAIMER = (
    "IMPORTANT - Please read before continuing:\n\n"
    "1. This tool screens only. It does not diagnose "
    "any medical or psychiatric condition.\n\n"
    "2. Your responses are not stored or shared with "
    "anyone at the University of Lucerne.\n\n"
    "3. This is not an emergency service. If you are "
    "in crisis, contact:\n"
    "   Die Dargebotene Hand: 143\n\n"
    "4. By continuing, you confirm you are a student "
    "or staff member of the University of Lucerne.\n\n"
    "Do you agree to proceed?"
)

AGREE_KEYBOARD = ReplyKeyboardMarkup(
    [['I Agree', 'I Do Not Agree']],
    resize_keyboard=True, one_time_keyboard=True
)

LANG_KEYBOARD = ReplyKeyboardMarkup(
    [['English', 'Deutsch']],
    resize_keyboard=True, one_time_keyboard=True
)

OLBI_KEYBOARD_EN = ReplyKeyboardMarkup(
    [['1 - Always', '2 - Often'], ['3 - Rarely', '4 - Never']],
    resize_keyboard=True, one_time_keyboard=True
)

OLBI_KEYBOARD_DE = ReplyKeyboardMarkup(
    [['1 - Immer', '2 - Oft'], ['3 - Selten', '4 - Nie']],
    resize_keyboard=True, one_time_keyboard=True
)

FREQ_KEYBOARD_EN = ReplyKeyboardMarkup(
    [['0 - Not at all', '1 - Several days'],
     ['2 - More than half the days', '3 - Nearly every day']],
    resize_keyboard=True, one_time_keyboard=True
)

FREQ_KEYBOARD_DE = ReplyKeyboardMarkup(
    [['0 - Ueberhaupt nicht', '1 - An einzelnen Tagen'],
     ['2 - Mehr als die Haelfte der Tage', '3 - Beinahe jeden Tag']],
    resize_keyboard=True, one_time_keyboard=True
)

REMOVE_KEYBOARD = ReplyKeyboardRemove()

WELCOME_EN = (
    "Welcome to the UniLU Mental Wellbeing Screening Bot.\n\n"
    "This tool screens for burnout, depression, and anxiety\n"
    "using validated instruments (OLBI, PHQ-9, GAD-7).\n\n"
    "- It does NOT diagnose\n"
    "- Your responses are confidential\n"
    "- If you need immediate support at any point,\n"
    "  the bot will provide crisis resources\n\n"
    "Professional support is available at:\n"
    "Psychologische Beratung UniLU\n"
    "+41 41 229 54 00\n\n"
    "Please select your language:"
)

WELCOME_DE = (
    "Willkommen beim Mental Wellbeing-Screening-Bot der UniLU.\n\n"
    "Dieses Tool prueft auf Burnout, Depression und Angst\n"
    "mit validierten Instrumenten (OLBI, PHQ-9, GAD-7).\n\n"
    "- Es stellt KEINE Diagnose\n"
    "- Ihre Antworten sind vertraulich\n"
    "- Bei Bedarf werden sofort Krisenressourcen angezeigt\n\n"
    "Professionelle Unterstuetzung:\n"
    "Psychologische Beratung UniLU\n"
    "+41 41 229 54 00\n\n"
    "Bitte Sprache auswaehlen:"
)

def get_keyboard(text, lang):
    if any(x in text for x in ['1=Always', '1 = Always', 'Immer', '1=Immer']):
        return OLBI_KEYBOARD_DE if lang == 'de' else OLBI_KEYBOARD_EN
    elif any(x in text for x in ['Not at all', 'Nearly every day', 'Ueberhaupt nicht', 'jeden Tag']):
        return FREQ_KEYBOARD_DE if lang == 'de' else FREQ_KEYBOARD_EN
    return REMOVE_KEYBOARD

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {'lang': None, 'agreed': False, 'conversation': []}
    await update.message.reply_text(DISCLAIMER, reply_markup=AGREE_KEYBOARD)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text.strip()

    if user_id not in user_sessions:
        await update.message.reply_text('Please type /start to begin. / Bitte /start eingeben.')
        return

    session = user_sessions[user_id]

    # Agreement check
    if not session.get('agreed'):
        if user_input == 'I Agree':
            session['agreed'] = True
            await update.message.reply_text(WELCOME_EN, reply_markup=LANG_KEYBOARD)
        else:
            await update.message.reply_text(
                'You have not agreed to the terms. Type /start to try again.',
                reply_markup=ReplyKeyboardRemove()
            )
            del user_sessions[user_id]
        return

    # Language selection step
    if session['lang'] is None:
        if user_input == 'Deutsch':
            session['lang'] = 'de'
        else:
            session['lang'] = 'en'
        session['conversation'] = [{'role': 'user', 'content': 'Hello, I would like to start the screening.'}]
        await update.message.reply_text('Starting... / Wird gestartet...')
        response_text, crisis = await run_agent_turn(user_id)
        if crisis:
            msg = CRISIS_MESSAGE_DE if session['lang'] == 'de' else CRISIS_MESSAGE_EN
            await update.message.reply_text(msg, reply_markup=REMOVE_KEYBOARD)
        else:
            keyboard = get_keyboard(response_text, session['lang'])
            await update.message.reply_text(response_text, reply_markup=keyboard)
        return

    # Crisis check
    if check_free_text(user_input):
        log_crisis('free_text')
        msg = CRISIS_MESSAGE_DE if session['lang'] == 'de' else CRISIS_MESSAGE_EN
        await update.message.reply_text(msg, reply_markup=REMOVE_KEYBOARD)
        del user_sessions[user_id]
        return

    session['conversation'].append({'role': 'user', 'content': user_input})
    response_text, crisis = await run_agent_turn(user_id)

    if crisis:
        msg = CRISIS_MESSAGE_DE if session['lang'] == 'de' else CRISIS_MESSAGE_EN
        await update.message.reply_text(msg, reply_markup=REMOVE_KEYBOARD)
        del user_sessions[user_id]
    else:
        keyboard = get_keyboard(response_text, session['lang'])
        await update.message.reply_text(response_text, reply_markup=keyboard)

async def run_agent_turn(user_id):
    session = user_sessions[user_id]
    conversation = session['conversation']
    lang = session['lang']
    system_prompt = SYSTEM_PROMPT_DE if lang == 'de' else SYSTEM_PROMPT_EN
    collected_text = []

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=conversation,
        )

        conversation.append({'role': 'assistant', 'content': response.content})

        for block in response.content:
            if hasattr(block, 'text') and block.text.strip():
                collected_text.append(block.text.strip())

        if response.stop_reason == 'end_turn':
            return '\n'.join(collected_text), False

        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type != 'tool_use':
                    continue
                result_str = dispatch(block.name, block.input)
                result = json.loads(result_str)

                if block.name == 'score_phq9' and result.get('crisis_flag'):
                    log_crisis('phq9_q9')
                    return '', True

                tool_results.append({
                    'type': 'tool_result',
                    'tool_use_id': block.id,
                    'content': result_str,
                })
            conversation.append({'role': 'user', 'content': tool_results})


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
        await update.message.reply_text(
            'Screening stopped. Your responses have been cleared.\n\nType /start to begin a new screening.',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            'No active screening found. Type /start to begin.',
            reply_markup=ReplyKeyboardRemove()
        )

def main():
    print('Bot starting...')
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print('Bot is running. Press Ctrl+C to stop.')
    app.run_polling()

if __name__ == '__main__':
    main()
