# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

from prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_DE, TOOL_DEFINITIONS
from tools import dispatch
from safety import check_free_text

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
MODEL = 'claude-opus-4-5'

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

def run_agent_turn():
    lang = st.session_state.lang
    system_prompt = SYSTEM_PROMPT_DE if lang == 'de' else SYSTEM_PROMPT_EN
    while True:
        import json as _json
        st.write("DEBUG conversation:", _json.dumps(st.session_state.conversation, indent=2))
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=st.session_state.conversation,
        )

        # Serialize assistant content to plain dicts
        serialized = []
        for block in response.content:
            if block.type == 'text':
                serialized.append({'type': 'text', 'text': block.text})
                if block.text.strip():
                    st.session_state.messages.append({'role': 'assistant', 'content': block.text.strip()})
            elif block.type == 'tool_use':
                serialized.append({
                    'type': 'tool_use',
                    'id': block.id,
                    'name': block.name,
                    'input': block.input
                })
        st.session_state.conversation.append({'role': 'assistant', 'content': serialized})

        if response.stop_reason == 'end_turn':
            break

        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type != 'tool_use':
                    continue
                result_str = dispatch(block.name, block.input, lang)
                result = json.loads(result_str)
                if block.name == 'score_phq9' and result.get('crisis_flag'):
                    st.session_state.crisis = True
                    return
                tool_results.append({
                    'type': 'tool_result',
                    'tool_use_id': block.id,
                    'content': result_str,
                })
            st.session_state.conversation.append({'role': 'user', 'content': tool_results})

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
