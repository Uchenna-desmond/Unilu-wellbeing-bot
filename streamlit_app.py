# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

from prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_DE, TOOL_DEFINITIONS
from tools import dispatch
from safety import check_free_text

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

CRISIS_MESSAGE = (
    'IMMEDIATE SUPPORT AVAILABLE\n\n'
    'Die Dargebotene Hand: 143 (24/7, free, anonymous)\n'
    'Psychologische Beratung UniLU: +41 41 229 54 00\n'
    'Email: info@pblu.ch'
)

st.set_page_config(page_title='UniLU Mental Wellbeing Screening', page_icon='U', layout='centered')
st.title('UniLU Mental Wellbeing Screening')
st.caption('Confidential - Not a diagnosis - Powered by PBLU')

if 'lang' not in st.session_state:
    st.session_state.lang = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'crisis' not in st.session_state:
    st.session_state.crisis = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

def build_prompt():
    parts = []
    for msg in st.session_state.conversation:
        role = msg['role']
        content = msg['content']
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'text':
                        parts.append(f"{role}: {block['text']}")
                    elif block.get('type') == 'tool_result':
                        parts.append(f"tool_result: {block['content']}")
        else:
            parts.append(f"{role}: {content}")
    return '\n'.join(parts)

def run_agent_turn():
    lang = st.session_state.lang
    system_prompt = SYSTEM_PROMPT_DE if lang == 'de' else SYSTEM_PROMPT_EN

    tool_desc = '\n'.join([
        f"- {t['name']}: {t['description']}" for t in TOOL_DEFINITIONS
    ])

    full_prompt = f"""{system_prompt}

Available tools:
{tool_desc}

To call a tool, respond with exactly:
TOOL_CALL: tool_name
INPUT: {{"key": "value"}}

Conversation so far:
{build_prompt()}

Continue the conversation. If you need to call a tool, use the format above. Otherwise respond normally."""

    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    while True:
        response = model.generate_content(full_prompt)
        text = response.text.strip()

        if 'TOOL_CALL:' in text:
            lines = text.split('\n')
            tool_name = None
            tool_input = {}
            for line in lines:
                if line.startswith('TOOL_CALL:'):
                    tool_name = line.replace('TOOL_CALL:', '').strip()
                if line.startswith('INPUT:'):
                    try:
                        tool_input = json.loads(line.replace('INPUT:', '').strip())
                    except:
                        tool_input = {}

            if tool_name:
                result_str = dispatch(tool_name, tool_input, lang)
                result = json.loads(result_str)

                if tool_name == 'score_phq9' and result.get('crisis_flag'):
                    st.session_state.crisis = True
                    return

                st.session_state.conversation.append({
                    'role': 'assistant',
                    'content': [{'type': 'text', 'text': text}]
                })
                st.session_state.conversation.append({
                    'role': 'user',
                    'content': [{'type': 'tool_result', 'content': result_str}]
                })

                full_prompt = f"""{system_prompt}

Available tools:
{tool_desc}

To call a tool, respond with exactly:
TOOL_CALL: tool_name
INPUT: {{"key": "value"}}

Conversation so far:
{build_prompt()}

Continue the conversation."""
                continue
        else:
            st.session_state.conversation.append({
                'role': 'assistant',
                'content': [{'type': 'text', 'text': text}]
            })
            if text:
                st.session_state.messages.append({'role': 'assistant', 'content': text})
            break

if st.session_state.lang is None:
    st.markdown('### Welcome / Willkommen')
    st.markdown('Please select your language:')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('English', use_container_width=True):
            st.session_state.lang = 'en'
            st.session_state.messages = []
            st.session_state.conversation = [{'role': 'user', 'content': 'Hello, I would like to start the screening.'}]
            run_agent_turn()
            st.rerun()
    with col2:
        if st.button('Deutsch', use_container_width=True):
            st.session_state.lang = 'de'
            st.session_state.messages = []
            st.session_state.conversation = [{'role': 'user', 'content': 'Hallo, ich moechte mit dem Screening beginnen.'}]
            run_agent_turn()
            st.rerun()
else:
    if st.session_state.crisis:
        st.error(CRISIS_MESSAGE)
        if st.button('Start over'):
            for key in ['lang', 'conversation', 'crisis', 'messages']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
        user_input = st.chat_input('Type your response...')
        if user_input:
            if check_free_text(user_input):
                st.session_state.crisis = True
                st.rerun()
            else:
                st.session_state.messages.append({'role': 'user', 'content': user_input})
                st.session_state.conversation.append({'role': 'user', 'content': user_input})
                run_agent_turn()
                st.rerun()
        if st.button('Start over'):
            for key in ['lang', 'conversation', 'crisis', 'messages']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
